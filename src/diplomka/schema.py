"""Typed access to the YAML semantic layer of the active dataset pack.

The semantic layer (``datasets/<name>/semantic_layer.yaml``) is the single contract between a
dataset and the agent. Top-level keys:

- ``domain``: ``name``, ``description``, optional ``notes`` (units, currency, data caveats)
- ``glossary``: business terms/synonyms and what they map to (a metric, a measure or a level value)
- ``tables``: every table/view the agent may query, with ``kind``, ``grain``, ``description``
- ``joins``: allowed joins; ``type: asof`` marks fact pairs that must never be joined with a plain JOIN
- ``dimensions``: ``table``, ``key``, ``hierarchies`` and ``levels``; a level may carry ``label``,
  ``note``, ``expr`` (SQL for a computed level) and ``domain: from_data`` (values read from DuckDB)
- ``measures``: ``column``/``columns``, ``tables``, ``unit``, ``additivity`` (dimension or ``all``
  -> allowed aggregation functions)
- ``metrics`` (optional): named SQL expressions, e.g. ratios or COUNT DISTINCT
- ``rules``, ``examples`` (few-shot SQL), ``starters`` (UI example questions)

Level names must be unique across all dimensions: intents, filters and domain checks refer to
a level by its name alone.
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


@dataclass(frozen=True)
class SemanticLayer:
    raw: dict[str, Any]
    measures: dict[str, Measure]
    measures_by_column: dict[str, Measure]
    levels: dict[str, Level]
    asof_only_pairs: tuple[frozenset[str], ...]

    @classmethod
    def from_yaml(cls, path: str | Path) -> SemanticLayer:
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        for join in raw.get("joins") or []:
            # YAML 1.1 reads a bare `on:` key as boolean True
            if True in join:
                join["on"] = join.pop(True)

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

        asof_only_pairs = tuple(
            frozenset((join["left"], join["right"])) for join in raw.get("joins") or [] if join.get("type") == "asof"
        )
        return cls(raw, measures, measures_by_column, levels, asof_only_pairs)

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
