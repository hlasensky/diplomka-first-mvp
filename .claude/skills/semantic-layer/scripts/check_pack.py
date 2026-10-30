"""Check one dataset pack: load it, run its tests, lint what the tests do not cover.

    uv run python .claude/skills/semantic-layer/scripts/check_pack.py <pack> [--no-tests]

1. Load: datasets/<pack>/semantic_layer.yaml through the user's loader (diplomka.schema).
2. Tests: the pack's parametrized cases of tests/test_datasets.py and the golden test
   (tests/test_golden.py::test_examples_match_golden[<pack>]). Skips mean the DB is not built.
3. Lint (WARN = likely wrong or a question for the user, INFO = worth a look):
   - two measures share a column (the validator finds measures by column name: one is ignored)
   - fact / aggregate / bridge without grain or description; a table no join, measure, metric
     or dimension uses; DB tables the layer does not list (invisible to the agent)
   - a dimension a measure's tables reach (grain/join columns are its key or levels) that its
     additivity does not list: aggregating over it is forbidden - intended?
   - `sum` allowed for a measure whose unit or name suggests an intensive quantity
   - `domain: from_data` level with many values (prompt bloat); glossary value not in its domain
   - R1-R3 missing or not enforced; duplicate rule / example ids
   - measures and metrics no eval case uses; asof / drill_across / bridge / range joins that no
     example shows
Exit code 1 when loading or a test fails.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

INTENSIVE_UNITS = {"°c", "%", "hpa", "ndvi", "dt/ha", "w/m²", "km/h", "m/s", "µg/m³", "ug/m3", "ppm", "ppb", "m³/m³"}
INTENSIVE_WORDS = re.compile(r"temp|humid|press|ndvi|share|pct|rate|ratio|avg|mean|std|concentration", re.I)
DOMAIN_LIMIT = 200


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pack")
    parser.add_argument("--no-tests", action="store_true", help="skip pytest (lint only)")
    args = parser.parse_args()

    # The loader module builds LAYER for the active DATASET at import time, so point it at this pack.
    os.environ["DATASET"] = args.pack
    try:
        from diplomka.config import DATA_DIR, DATASETS_DIR, PROJECT_ROOT
        from diplomka.schema import SemanticLayer
    except Exception as error:  # noqa: BLE001 - any loader error is the finding
        print(f"FAIL load: {type(error).__name__}: {error}")
        sys.exit(1)

    pack_dir = DATASETS_DIR / args.pack
    layer = SemanticLayer.from_yaml(pack_dir / "semantic_layer.yaml")
    print(f"OK   load: {len(layer.tables)} tables, {len(layer.joins)} joins, {len(layer.levels)} levels, "
          f"{len(layer.measures)} measures, {len(layer.metrics)} metrics")

    failed = False if args.no_tests else run_tests(args.pack, PROJECT_ROOT)
    db = DATA_DIR / f"{args.pack}.duckdb"
    lint(layer, pack_dir, db if db.exists() and db.stat().st_size > 0 else None)
    sys.exit(1 if failed else 0)


def run_tests(pack: str, root: Path) -> bool:
    collected = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "tests/test_datasets.py", "tests/test_golden.py"],
        cwd=root, capture_output=True, text=True,
    )
    ids = [line.strip() for line in collected.stdout.splitlines() if line.strip().endswith(f"[{pack}]")]
    if not ids:
        print(f"FAIL tests: no test collected for [{pack}]\n{collected.stdout[-2000:]}{collected.stderr[-2000:]}")
        return True
    run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-rfs", "-p", "no:cacheprovider", *ids],
        cwd=root, capture_output=True, text=True,
    )
    status = "OK  " if run.returncode == 0 else "FAIL"
    print(f"{status} tests ({len(ids)} collected):")
    tail = [line for line in run.stdout.splitlines() if line.strip()][-25:]
    print("\n".join("     " + line for line in tail))
    return run.returncode != 0


def lint(layer, pack_dir: Path, db: Path | None) -> None:
    raw = layer.raw
    warn: list[str] = []
    info: list[str] = []
    dims = raw["dimensions"]

    columns_of: dict[str, set[str]] = {}
    domains: dict[str, set[str]] = {}
    db_tables: set[str] = set()
    if db is not None:
        import duckdb

        with duckdb.connect(str(db), read_only=True) as con:
            db_tables = {r[0] for r in con.execute("SELECT table_name FROM information_schema.tables").fetchall()}
            for table in layer.tables:
                if table in db_tables:
                    columns_of[table] = {r[0] for r in con.execute(f"DESCRIBE {table}").fetchall()}
            domains = layer.load_domains(con)
    else:
        info.append("database not built: column-based checks use grains and join keys only")

    # measures sharing a column
    owners: dict[str, list[str]] = {}
    for measure_id, spec in raw["measures"].items():
        for column in spec.get("columns") or [spec["column"]]:
            owners.setdefault(column, []).append(measure_id)
    for column, ids in owners.items():
        if len(ids) > 1:
            warn.append(f"column {column} belongs to measures {ids}: the validator keeps only {ids[-1]}")

    # tables
    used = {t for j in layer.joins.values() for t in (j.from_.table, j.to.table, j.bridge.table if j.bridge else None)}
    used |= {t for m in layer.measures.values() for t in m.tables}
    used |= {m.get("table") for m in layer.metrics.values()}
    used |= {d["table"] for d in dims.values()}
    for table, spec in layer.tables.items():
        spec = spec or {}
        if spec.get("kind") in {"fact", "factless_fact", "aggregate", "bridge"}:
            if not spec.get("grain"):
                warn.append(f"table {table}: no grain")
            if not spec.get("description"):
                warn.append(f"table {table}: no description")
        if table not in used:
            warn.append(f"table {table}: no join, measure, metric or dimension uses it")
    if db_tables:
        hidden = sorted(db_tables - set(layer.tables))
        if hidden:
            info.append(f"DB tables not in the layer (invisible to the agent): {hidden}")
        missing = sorted(set(layer.tables) - db_tables)
        if missing:
            warn.append(f"layer tables missing in the DB: {missing}")

    # additivity vs. reachable dimensions
    # Only hierarchy levels identify a dimension: flag-like levels (is_bee_forage) share names
    # with columns of unrelated tables.
    level_dim = {
        level: name for name, d in dims.items() for path in (d.get("hierarchies") or {}).values() for level in path
    }
    key_dim = {d.get("key"): name for name, d in dims.items() if d.get("key")}
    table_dim = {d["table"]: name for name, d in dims.items()}

    def table_columns(table: str) -> set[str]:
        if table in columns_of:
            return columns_of[table]
        cols = set((layer.tables.get(table) or {}).get("grain") or [])
        for j in layer.joins.values():
            if j.from_.table == table:
                cols |= {c for c in j.from_.columns if "." not in c}
        return cols

    def reached_dims(table: str) -> set[str]:
        seen, frontier, found = {table}, [table], set()
        while frontier:
            current = frontier.pop()
            if current in table_dim:
                found.add(table_dim[current])
            for column in table_columns(current):
                if column in key_dim:
                    found.add(key_dim[column])
                if column in level_dim:
                    found.add(level_dim[column])
            for j in layer.joins.values():
                if j.kind in {"fk", "rollup"} and j.from_.table == current and j.to.table not in seen:
                    seen.add(j.to.table)
                    frontier.append(j.to.table)
        return found

    for measure in layer.measures.values():
        listed = set(measure.additivity) - {"all"}
        unknown = listed - set(dims)
        if unknown:
            warn.append(f"measure {measure.measure_id}: additivity names unknown dimensions {sorted(unknown)}")
        if "all" in measure.additivity:
            continue
        reached = set().union(*(reached_dims(t) for t in measure.tables)) if measure.tables else set()
        omitted = sorted(reached - listed)
        if omitted:
            info.append(
                f"measure {measure.measure_id}: no aggregation allowed over {omitted} "
                f"(reachable from {list(measure.tables)}) - intended?"
            )
        summed = any("sum" in aggs for aggs in measure.additivity.values())
        unit = (measure.unit or "").lower()
        if summed and (unit in INTENSIVE_UNITS or INTENSIVE_WORDS.search(measure.measure_id)):
            sums_over = sorted(d for d, aggs in measure.additivity.items() if "sum" in aggs)
            warn.append(
                f"measure {measure.measure_id} [{measure.unit}]: sum allowed over {sums_over} "
                f"but unit/name look intensive - check"
            )

    # domains and glossary
    for name, values in domains.items():
        if len(values) > DOMAIN_LIMIT:
            warn.append(f"level {name}: domain has {len(values)} values (> {DOMAIN_LIMIT}), bloats prompts")
    for entry in layer.glossary:
        target = entry.get("maps_to") or {}
        level, value = target.get("level"), target.get("value")
        if level and value is not None and level in domains and str(value) not in domains[level]:
            warn.append(f"glossary '{entry['term']}': value {value!r} is not in the domain of {level}")

    # rules and ids
    rules = raw.get("rules") or []
    rule_ids = [r.get("id") for r in rules]
    for rid in ("R1", "R2", "R3"):
        rule = next((r for r in rules if r.get("id") == rid), None)
        if rule is None or rule.get("enforced") is not True:
            warn.append(f"rule {rid} missing or not enforced: the validator enforces it generically")
    for name, ids in (("rule", rule_ids), ("example", [e.get("id") for e in raw.get("examples") or []])):
        dupes = [i for i, n in Counter(ids).items() if n > 1]
        if dupes:
            warn.append(f"duplicate {name} ids: {dupes}")

    # eval coverage
    eval_path = pack_dir / "eval.yaml"
    if eval_path.exists():
        data = yaml.safe_load(eval_path.read_text()) or {}
        expected = [c.get("expected") or {} for c in data.get("cases") or []]
        expected += [c.get("expected_last") or {} for c in data.get("multi_turn") or []]
        used_measures = {m["measure"] for e in expected for m in e.get("measures", [])}
        used_metrics = {m for e in expected for m in e.get("metrics", [])}
        unclear = sum(1 for e in expected if e.get("unclear"))
        not_covered = sorted(set(layer.measures) - used_measures)
        if not_covered:
            info.append(f"measures without an eval case ({len(not_covered)}/{len(layer.measures)}): {not_covered}")
        if set(layer.metrics) - used_metrics:
            info.append(f"metrics without an eval case: {sorted(set(layer.metrics) - used_metrics)}")
        if unclear < 2:
            info.append(f"only {unclear} 'unclear' eval case(s); add out-of-domain and nonsense questions")
        if not data.get("multi_turn"):
            info.append("no multi_turn eval case")

    # examples per hard join
    sqls = [e.get("sql", "") for e in raw.get("examples") or []]
    for join in layer.joins.values():
        if join.kind not in {"asof", "drill_across", "bridge", "range"}:
            continue
        tables = {join.from_.table, join.to.table} | ({join.bridge.table} if join.bridge else set())
        if not any(all(re.search(rf"\b{t}\b", sql) for t in tables) for sql in sqls):
            info.append(f"join {join.join_id} ({join.kind}): no example uses {sorted(tables)}")

    for line in warn:
        print(f"WARN {line}")
    for line in info:
        print(f"INFO {line}")
    if not warn and not info:
        print("OK   lint: nothing to report")


if __name__ == "__main__":
    main()
