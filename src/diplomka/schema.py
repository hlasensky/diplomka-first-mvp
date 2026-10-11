"""Typed access to the YAML semantic layer of the active dataset pack.

The semantic layer (``datasets/<name>/semantic_layer.yaml``) is the single contract between a
dataset and the agent. Top-level keys:

- ``domain``: ``name``, ``description``, optional ``notes`` (units, currency, data caveats)
- ``glossary``: business terms/synonyms and what they map to (a metric, a measure or a level value)
- ``tables``: every table/view the agent may query, with ``kind``, ``grain``, ``description``
- ``joins``: allowed joins, each with ``id``, ``kind``, ``from`` and ``to``
- ``dimensions``: ``table``, ``key``, ``hierarchies`` and ``levels``; a level may carry ``label``,
  ``note``, ``expr`` (SQL for a computed level) and ``domain: from_data`` (values read from DuckDB)
- ``measures``: ``column``/``columns``, ``tables``, ``unit``, ``additivity`` (dimension or ``all``
  -> allowed aggregation functions)
- ``metrics`` (optional): named SQL expressions, e.g. ratios or COUNT DISTINCT
- ``rules``, ``examples`` (few-shot SQL), ``starters`` (UI example questions)

Level names must be unique across all dimensions: intents, filters and domain checks refer to
a level by its name alone.

Joins are structured so that code (not only the LLM) can read them. ``from`` and ``to`` name a
``table`` and its key ``columns``, paired by position; a column written ``table.column`` belongs
to a table reached through the joins listed in ``via``. A key that is not a plain column is an
``expr`` (one fully qualified SQL expression). Kinds:

- ``fk``: fact -> dimension
- ``rollup``: dimension -> coarser dimension along a hierarchy (hour -> day, cell -> district)
- ``bridge``: many-to-many through a weighted bridge table, ``bridge: {table, from_columns,
  to_columns, weight}``
- ``range``: the ``from`` key BETWEEN the ``start`` and ``end`` columns of ``to``
- ``drill_across``: fact -> fact at the same grain through shared dimensions (``via``)
- ``asof``: fact -> latest matching ``to`` row by ``time`` (or ``time_expr``) and ``direction``;
  such fact pairs must never be joined with a plain JOIN (rule R2)

``optional: true`` marks a key that may be NULL or unmatched (use LEFT JOIN).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from diplomka.config import SCHEMA_PATH


@dataclass(frozen=True)
class Level:
    name: str
    dimension: str
    table: str
    label: str
    note: str | None
    expr: str | None
    has_domain: bool

    @property
    def sql(self) -> str:
        """SQL expression producing the level's values in its dimension table."""
        return self.expr or self.name


@dataclass(frozen=True)
class Measure:
    measure_id: str
    columns: tuple[str, ...]
    tables: tuple[str, ...]
    label: str
    unit: str | None
    allowed_aggs: frozenset[str]
    additivity: dict[str, list[str]]
    description: str | None


JOIN_KINDS = frozenset({"fk", "rollup", "bridge", "range", "drill_across", "asof"})
JOIN_KEYS = frozenset({"id", "kind", "from", "to", "via", "bridge", "cardinality", "optional", "direction", "note"})
SIDE_KEYS = frozenset({"table", "columns", "expr", "time", "time_expr", "start", "end"})
CARDINALITIES = frozenset({"many_to_one", "one_to_many", "many_to_many", "one_to_one"})
ASOF_DIRECTIONS = frozenset({">=", "<=", ">", "<"})


@dataclass(frozen=True)
class JoinSide:
    table: str
    columns: tuple[str, ...] = ()
    expr: str | None = None
    time: str | None = None
    time_expr: str | None = None
    start: str | None = None
    end: str | None = None

    def qualify_columns(self, column: str) -> str:
        return column if "." in column else f"{self.table}.{column}"

    @property
    def keys_sql(self) -> list[str]:
        return [self.expr] if self.expr else [self.qualify_columns(c) for c in self.columns]

    @property
    def time_sql(self) -> str | None:
        return self.time_expr or (self.qualify_columns(self.time) if self.time else None)


@dataclass(frozen=True)
class Bridge:
    table: str
    from_columns: tuple[str, ...]
    to_columns: tuple[str, ...]
    weight: str | None = None


@dataclass(frozen=True)
class Join:
    join_id: str
    kind: str
    from_: JoinSide
    to: JoinSide
    via: tuple[str, ...] = ()
    bridge: Bridge | None = None
    cardinality: str | None = None
    optional: bool = False
    direction: str | None = None
    note: str | None = None

    @property
    def condition_sql(self) -> str:
        if self.kind == "bridge" and self.bridge:
            bridge = self.bridge
            into = [
                f"{self.from_.table}.{c} = {bridge.table}.{bc}"
                for c, bc in zip(self.from_.columns, bridge.from_columns, strict=True)
            ]
            out = [
                f"{bridge.table}.{bc} = {self.to.table}.{c}"
                for bc, c in zip(bridge.to_columns, self.to.columns, strict=True)
            ]
            return " AND ".join(into + out)
        if self.kind == "range" and self.to.start and self.to.end:
            key = self.from_.keys_sql[0]
            return f"{key} BETWEEN {self.to.qualify_columns(self.to.start)} AND {self.to.qualify_columns(self.to.end)}"
        conditions = [f"{f} = {t}" for f, t in zip(self.from_.keys_sql, self.to.keys_sql, strict=True)]
        if self.kind == "asof":
            conditions.append(f"{self.from_.time_sql} {self.direction} {self.to.time_sql}")
        return " AND ".join(conditions)


def _join_side(side: dict, where: str) -> JoinSide:
    unknown = set(side) - SIDE_KEYS
    if unknown:
        raise ValueError(f"{where}: unknown keys {sorted(unknown)}")
    return JoinSide(
        table=side["table"],
        columns=tuple(side.get("columns") or ()),
        expr=side.get("expr"),
        time=side.get("time"),
        time_expr=side.get("time_expr"),
        start=side.get("start"),
        end=side.get("end"),
    )


def _parse_join(spec: dict) -> Join:
    join_id = spec.get("id")
    if "left" in spec or "right" in spec or not join_id:
        raise ValueError(f"Join {spec}: uses the old left/right format or has no id, see the schema module docstring")
    unknown = set(spec) - JOIN_KEYS
    if unknown:
        raise ValueError(f"Join {join_id}: unknown keys {sorted(map(str, unknown))}")
    bridge = spec.get("bridge")
    return Join(
        join_id=join_id,
        kind=spec["kind"],
        from_=_join_side(spec["from"], f"Join {join_id} from"),
        to=_join_side(spec["to"], f"Join {join_id} to"),
        via=tuple(spec.get("via") or ()),
        bridge=Bridge(
            table=bridge["table"],
            from_columns=tuple(bridge["from_columns"]),
            to_columns=tuple(bridge["to_columns"]),
            weight=bridge["weight"],
        )
        if bridge is not None
        else None,
        cardinality=spec.get("cardinality"),
        optional=bool(spec.get("optional")),
        direction=spec.get("direction"),
        note=spec.get("note"),
    )


def _check_join(join: Join, joins: dict[str, Join], tables: set[str]) -> None:
    where = f"Join {join.join_id}"
    if join.kind not in JOIN_KINDS:
        raise ValueError(f"{where}: kind {join.kind} is not in {JOIN_KINDS}")
    if join.cardinality is not None and join.cardinality not in CARDINALITIES:
        raise ValueError(f"{where}: cardinality {join.cardinality} is not in {CARDINALITIES}")
    named = {join.from_.table, join.to.table} | ({join.bridge.table} if join.bridge else set())
    if named - tables:
        raise ValueError(f"{where}: tables {sorted(named - tables)} are not in `tables`")

    for via_id in join.via:
        via = joins.get(via_id)
        if via is None or via.kind not in {"fk", "rollup"} or via.from_.table != join.from_.table:
            raise ValueError(f"{where}: via '{via_id}' is not an fk/rollup join from {join.from_.table}")

    reachable = {join.from_.table, join.to.table} | {joins[v].to.table for v in join.via}
    for side in (join.from_, join.to):
        if side.expr and side.columns:
            raise ValueError(f"{where}: {side.table} has both expr and columns")
        for column in (*side.columns, side.time or ""):
            if "." in column and column.split(".", 1)[0] not in reachable:
                raise ValueError(f"{where}: '{column}' names a table that no `via` join reaches")
    if join.kind == "bridge":
        b = join.bridge
        if b is None or len(join.from_.columns) != len(b.from_columns) or len(join.to.columns) != len(b.to_columns):
            raise ValueError(f"{where}: a bridge join needs `bridge` with columns matching `from` and `to`")
    elif join.kind == "range":
        if len(join.from_.keys_sql) != 1 or not (join.to.start and join.to.end):
            raise ValueError(f"{where}: a range join needs one `from` key and `to.start` / `to.end`")
    elif not join.from_.keys_sql or len(join.from_.keys_sql) != len(join.to.keys_sql):
        raise ValueError(f"{where}: `from` and `to` need the same number of keys")
    if join.kind == "asof" and (
        join.direction not in ASOF_DIRECTIONS or not (join.from_.time_sql and join.to.time_sql)
    ):
        raise ValueError(f"{where}: an asof join needs `time` on both sides and a direction {sorted(ASOF_DIRECTIONS)}")
    if join.kind == "drill_across" and not join.via:
        raise ValueError(f"{where}: a drill_across join needs `via`")


@dataclass(frozen=True)
class SemanticLayer:
    raw: dict[str, Any]
    measures: dict[str, Measure]
    measures_by_column: dict[str, Measure]
    levels: dict[str, Level]
    joins: dict[str, Join]
    asof_only_pairs: tuple[frozenset[str], ...]

    @classmethod
    def from_yaml(cls, path: str | Path) -> SemanticLayer:
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        measures: dict[str, Measure] = {}
        measures_by_column: dict[str, Measure] = {}
        for measure_id, spec in raw["measures"].items():
            measure = Measure(
                measure_id=measure_id,
                columns=tuple(spec.get("columns") or [spec["column"]]),
                tables=tuple(spec.get("tables", [])),
                label=spec.get("label", measure_id),
                unit=spec.get("unit"),
                allowed_aggs=frozenset(agg for aggs in spec["additivity"].values() for agg in aggs),
                additivity=spec["additivity"],
                description=spec.get("description") or spec.get("caveat"),
            )
            measures[measure_id] = measure
            for column in measure.columns:
                measures_by_column[column] = measure

        levels: dict[str, Level] = {}
        for dim_name, dimension in raw["dimensions"].items():
            for level_name, meta in (dimension.get("levels") or {}).items():
                meta = meta or {}
                if level_name in levels:
                    raise ValueError(f"Level '{level_name}' is defined in more than one dimension")
                levels[level_name] = Level(
                    name=level_name,
                    dimension=dim_name,
                    table=dimension["table"],
                    label=meta.get("label", level_name),
                    note=meta.get("note"),
                    expr=meta.get("expr"),
                    has_domain=meta.get("domain") == "from_data",
                )

        joins: dict[str, Join] = {}
        for spec in raw.get("joins") or []:
            join = _parse_join(spec)
            if join.join_id in joins:
                raise ValueError(f"Join id '{join.join_id}' is defined more than once")
            joins[join.join_id] = join
        for join in joins.values():
            _check_join(join, joins, set(raw["tables"] or {}))

        asof_only_pairs = tuple(
            frozenset({join.from_.table, join.to.table}) for join in joins.values() if join.kind == "asof"
        )
        return cls(raw, measures, measures_by_column, levels, joins, asof_only_pairs)

    @property
    def name(self) -> str:
        return self.raw["domain"]["name"]

    @property
    def description(self) -> str:
        return self.raw["domain"].get("description", "").strip()

    @property
    def notes(self) -> list[str]:
        return self.raw["domain"].get("notes") or []

    @property
    def metrics(self) -> dict[str, dict]:
        return self.raw.get("metrics") or {}

    @property
    def tables(self) -> dict[str, dict]:
        return self.raw.get("tables") or {}

    @property
    def glossary(self) -> list[dict]:
        return self.raw.get("glossary") or []

    @property
    def starters(self) -> list[dict]:
        return self.raw.get("starters") or []

    def load_domains(self, con) -> dict[str, set[str]]:
        """Read the allowed values of every level marked `domain: from_data` from DuckDB.

        Levels whose column holds no values yet (e.g. an attribute that is not populated) are
        left out, so they are not checked rather than rejecting every value.
        """
        domains: dict[str, set[str]] = {}
        for level in self.levels.values():
            if not level.has_domain:
                continue
            rows = con.execute(
                f"SELECT DISTINCT {level.sql} FROM {level.table} WHERE {level.sql} IS NOT NULL"
            ).fetchall()
            if rows:
                domains[level.name] = {str(row[0]) for row in rows}
        return domains


LAYER = SemanticLayer.from_yaml(SCHEMA_PATH)


@lru_cache(maxsize=1)
def get_domains() -> dict[str, set[str]]:
    """Domains of the active dataset, read once from its DuckDB database."""
    from diplomka.db import connect

    with connect(read_only=True) as con:
        return LAYER.load_domains(con)
