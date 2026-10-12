"""Contract tests for every dataset pack under datasets/ (not only the active one).

A pack is valid when its semantic layer loads, its example queries pass the semantic
validator (and run, if its database is built) and its eval cases refer only to metrics,
measures and levels that exist in the layer.
"""

from pathlib import Path

import pytest
import yaml

from diplomka.config import DATA_DIR, DATASETS_DIR
from diplomka.schema import SemanticLayer
from diplomka.semantic_validator import validate_semantics

PACKS = sorted(p.name for p in DATASETS_DIR.iterdir() if (p / "semantic_layer.yaml").exists())


def _layer(pack: str) -> SemanticLayer:
    return SemanticLayer.from_yaml(DATASETS_DIR / pack / "semantic_layer.yaml")


def _database(pack: str) -> Path | None:
    db = DATA_DIR / f"{pack}.duckdb"
    return db if db.exists() and db.stat().st_size > 0 else None


@pytest.mark.parametrize("pack", PACKS)
def test_pack_has_required_files(pack):
    for name in ("semantic_layer.yaml", "build.sql", "eval.yaml"):
        assert (DATASETS_DIR / pack / name).exists(), name


@pytest.mark.parametrize("pack", PACKS)
def test_layer_references_are_consistent(pack):
    layer = _layer(pack)
    assert layer.name and layer.measures and layer.levels
    for measure in layer.measures.values():
        assert set(measure.tables) <= set(layer.tables), measure.measure_id
    for dimension in layer.raw["dimensions"].values():
        for path in (dimension.get("hierarchies") or {}).values():
            assert set(path) <= set(layer.levels), path
    for entry in layer.glossary:
        target = entry["maps_to"]
        assert target.get("metric") is None or target["metric"] in layer.metrics, entry["term"]
        assert target.get("measure") is None or target["measure"] in layer.measures, entry["term"]
        assert target.get("level") is None or target["level"] in layer.levels, entry["term"]
    for starter in layer.starters:
        assert starter["label"] and starter["message"]


@pytest.mark.parametrize("pack", PACKS)
def test_eval_cases_use_layer_vocabulary(pack):
    layer = _layer(pack)
    eval_data = yaml.safe_load((DATASETS_DIR / pack / "eval.yaml").read_text())
    cases = [c["expected"] for c in eval_data.get("cases") or []]
    cases += [c["expected_last"] for c in eval_data.get("multi_turn") or []]
    assert cases
    for expected in cases:
        assert set(expected.get("metrics", [])) <= set(layer.metrics), expected
        for m in expected.get("measures", []):
            assert m["agg"] in layer.measures[m["measure"]].allowed_aggs, expected
        assert set(expected.get("group_by", [])) <= set(layer.levels), expected
        assert set(expected.get("filters", {})) <= set(layer.levels), expected


@pytest.mark.parametrize("pack", PACKS)
def test_layer_examples_pass_validation_and_execute(pack):
    layer = _layer(pack)
    db = _database(pack)
    if db is None:
        for example in layer.raw.get("examples") or []:
            assert validate_semantics(example["sql"], layer, {}) == [], example["id"]
        pytest.skip(f"{pack}: database not built - only validated without domains")

    duckdb = pytest.importorskip("duckdb")
    with duckdb.connect(str(db), read_only=True) as con:
        domains = layer.load_domains(con)
        for table in layer.tables:
            con.execute(f"DESCRIBE {table}")
        for example in layer.raw.get("examples") or []:
            assert validate_semantics(example["sql"], layer, domains) == [], example["id"]
            con.execute(example["sql"]).fetchall()


@pytest.mark.parametrize("pack", PACKS)
def test_many_to_one_joins_do_not_fan_out(pack):
    """A many_to_one join must find at most one `to` row per key, otherwise sums get multiplied.

    Range and asof joins pick their row by a condition, not by key uniqueness, so they are skipped.
    """
    layer = _layer(pack)
    db = _database(pack)
    if db is None:
        pytest.skip(f"{pack}: database not built")

    duckdb = pytest.importorskip("duckdb")
    fan_outs = []
    with duckdb.connect(str(db), read_only=True) as con:
        for join in layer.joins.values():
            if join.cardinality != "many_to_one" or join.kind in {"range", "asof"}:
                continue
            keys = ", ".join(join.to.columns)
            duplicates = con.execute(
                f"SELECT count(*) FROM (SELECT {keys} FROM {join.to.table} GROUP BY ALL HAVING count(*) > 1)"
            ).fetchone()[0]
            if duplicates:
                fan_outs.append(f"{join.join_id}: {duplicates} duplicate keys ({keys}) in {join.to.table}")
    assert not fan_outs, "; ".join(fan_outs)

@pytest.mark.parametrize("pack", PACKS)
def test_required_joins_have_no_orphans(pack):
    """Every key of a required (not `optional`) fk/rollup join must find a `to` row.

    An orphan key makes an INNER JOIN drop the row without warning. `condition_sql` covers
    expr keys (event_date, minute_time) as well as plain columns.
    """
    layer = _layer(pack)
    db = _database(pack)
    if db is None:
        pytest.skip(f"{pack}: database not built")

    duckdb = pytest.importorskip("duckdb")
    orphans = []
    with duckdb.connect(str(db), read_only=True) as con:
        for join in layer.joins.values():
            if join.optional or join.kind not in {"fk", "rollup"}:
                continue
            missing = con.execute(
                f"SELECT count(*) FROM {join.from_.table} "
                f"WHERE NOT EXISTS (SELECT 1 FROM {join.to.table} WHERE {join.condition_sql})"
            ).fetchone()[0]
            if missing:
                orphans.append(f"{join.join_id}: {missing} rows of {join.from_.table} have no {join.to.table} row")
    assert not orphans, "; ".join(orphans)



@pytest.mark.parametrize("pack", PACKS)
def test_table_grain_is_unique(pack):
    """The declared `grain` of every table must identify one row, otherwise drill-across and sums double count."""
    layer = _layer(pack)
    db = _database(pack)
    if db is None:
        pytest.skip(f"{pack}: database not built")

    duckdb = pytest.importorskip("duckdb")
    duplicated = []
    with duckdb.connect(str(db), read_only=True) as con:
        for table, spec in layer.tables.items():
            grain = (spec or {}).get("grain")
            if not grain:
                continue
            keys = ", ".join(grain)
            duplicates = con.execute(
                f"SELECT count(*) FROM (SELECT {keys} FROM {table} GROUP BY ALL HAVING count(*) > 1)"
            ).fetchone()[0]
            if duplicates:
                duplicated.append(f"{table}: {duplicates} duplicate grains ({keys})")
    assert not duplicated, "; ".join(duplicated)


@pytest.mark.parametrize("pack", PACKS)
def test_fact_to_fact_keys_cover_target_grain(pack):
    """A many_to_one drill-across or asof join must name the whole grain of its target fact.

    The two facts have different grains (they meet through shared dimensions), so compare the
    join's `to` keys with the target grain, not the two grains with each other. A missing grain
    column (e.g. plant_id in agg_cell_bloom) matches several rows and multiplies sums. An asof
    join adds its `to.time` column; a `time_expr` (e.g. event_ts::DATE) is coarser than the
    column, so it covers nothing and ties at the same time are picked arbitrarily. Columns in
    `requires_filter` are fixed to one value by the query, so they count as keys.
    """
    layer = _layer(pack)
    uncovered = []
    for join in layer.joins.values():
        if join.kind not in {"drill_across", "asof"} or join.cardinality != "many_to_one":
            continue
        grain = set(layer.tables[join.to.table].get("grain") or [])
        keys = set(join.to.columns) | set(join.requires_filter)
        if join.kind == "asof" and join.to.time and not join.to.time_expr:
            keys.add(join.to.time)
        missing = grain - keys
        if missing:
            uncovered.append(f"{join.join_id}: keys miss {sorted(missing)} of {join.to.table} grain")
    assert not uncovered, "; ".join(uncovered)
    

@pytest.mark.parametrize("pack", PACKS)
def test_layer_column_references_exist(pack):
    """Every column the layer names (measures, levels, join keys) must exist in the built database.

    The YAML does not list table columns, so DESCRIBE is the source of truth. A column written
    `table.column` (reached through `via`) is looked up in that table; expressions are evaluated.
    """
    layer = _layer(pack)
    db = _database(pack)
    if db is None:
        pytest.skip(f"{pack}: database not built")

    duckdb = pytest.importorskip("duckdb")
    missing = []
    with duckdb.connect(str(db), read_only=True) as con:
        columns = {t: {row[0] for row in con.execute(f"DESCRIBE {t}").fetchall()} for t in layer.tables}

        def check_column(table: str, column: str, owner: str) -> None:
            table, column = column.split(".", 1) if "." in column else (table, column)
            if column not in columns.get(table, set()):
                missing.append(f"{owner}: {table}.{column}")

        def check_expr(table: str, expr: str, owner: str) -> None:
            try:
                con.execute(f"SELECT {expr} FROM {table} LIMIT 0")
            except duckdb.Error as error:
                missing.append(f"{owner}: {str(error).splitlines()[0]}")

        for measure in layer.measures.values():
            for table in measure.tables:
                for column in measure.columns:
                    check_column(table, column, f"measure {measure.measure_id}")
        for level in layer.levels.values():
            check_expr(level.table, level.sql, f"level {level.name}")
        for join in layer.joins.values():
            owner = f"join {join.join_id}"
            for side in (join.from_, join.to):
                for column in (*side.columns, *filter(None, (side.time, side.start, side.end))):
                    check_column(side.table, column, owner)
                for expr in filter(None, (side.expr, side.time_expr)):
                    check_expr(side.table, expr, owner)
            for column in join.requires_filter:
                check_column(join.to.table, column, owner)
            if join.bridge:
                for column in (*join.bridge.from_columns, *join.bridge.to_columns, *filter(None, [join.bridge.weight])):
                    check_column(join.bridge.table, column, owner)
    assert not missing, "; ".join(missing)