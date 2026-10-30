"""Profile raw files or DuckDB tables before modelling them (markdown to stdout).

Per relation: row count, then per column: type, NULL %, approximate distinct count, min, max,
and flags for things that change the model (sentinel values, all-NULL columns, constant
columns, numbers stored as text, decimal commas). Low-cardinality columns list their values.
Optional checks: grain uniqueness (--grain) and time-series regularity (--time with --series).

    uv run python .claude/skills/semantic-layer/scripts/profile.py --files 'data/raw/x/*.csv'
    uv run python .claude/skills/semantic-layer/scripts/profile.py --files 'a/*.csv' \
        --csv-option "nullstr='NA'" --csv-option "delim=';'" --grain station,ts --time ts --series station
    uv run python .claude/skills/semantic-layer/scripts/profile.py --db data/senger.duckdb --table fact_event
    uv run python .claude/skills/semantic-layer/scripts/profile.py --db data/x.duckdb --sql "SELECT ..."
    uv run python .claude/skills/semantic-layer/scripts/profile.py --files 'a/*.csv' --head 8   # raw first lines
"""

from __future__ import annotations

import argparse
import glob
import sys
from pathlib import Path

import duckdb

LIST_VALUES_UP_TO = 30
SENTINEL_SHARE = 0.005  # an isolated min/max holding >= 0.5 % of rows looks like a missing-value code
KNOWN_CODES = {-9999.0, -999.0, -99.0, -200.0, 999.0, 9999.0, 99999.0}


def reader_sql(pattern: str, csv_options: list[str]) -> str:
    suffix = Path(pattern.split(",")[0]).suffix.lower()
    if suffix == ".parquet":
        return f"read_parquet('{pattern}', union_by_name = true, filename = true)"
    if suffix in {".json", ".ndjson", ".jsonl"}:
        return f"read_json_auto('{pattern}', filename = true)"
    options = ", ".join(["union_by_name = true", "filename = true", *csv_options])
    return f"read_csv('{pattern}', {options})"


def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def sentinel_flags(con: duckdb.DuckDBPyConnection, name: str, summary: dict, n_rows: int) -> list[str]:
    """Flag a min or max that looks like a missing-value code: a known code, or a value that holds
    many rows and sits further from the next value than the interquartile range (-200 next to 0.1).
    A natural floor such as 0 mm rain is next to its neighbours and is not flagged."""
    flags = []
    try:
        iqr = float(summary["q75"]) - float(summary["q25"])
    except (TypeError, ValueError):
        iqr = 0.0
    for value, nearest in ((summary["min"], "min"), (summary["max"], "max")):
        if value is None:
            continue
        value = float(value)
        (cnt, neighbour) = con.execute(
            f"SELECT count(*) FILTER (WHERE {q(name)} = ?), "
            f"{'min' if nearest == 'min' else 'max'}({q(name)}) FILTER (WHERE {q(name)} {'>' if nearest == 'min' else '<'} ?) "
            f"FROM _p",
            [value, value],
        ).fetchone()
        share = cnt / n_rows
        isolated = neighbour is not None and iqr > 0 and abs(float(neighbour) - value) > iqr
        if (share >= SENTINEL_SHARE and isolated) or (value in KNOWN_CODES and share >= 0.001):
            flags.append(f"sentinel? {value:g} in {share:.1%} of rows (next value {neighbour})")
    return flags


def profile_relation(con: duckdb.DuckDBPyConnection, title: str, rel_sql: str, args: argparse.Namespace) -> None:
    con.execute(f"CREATE OR REPLACE TEMP VIEW _p AS SELECT * FROM {rel_sql}")
    (n_rows,) = con.execute("SELECT count(*) FROM _p").fetchone()
    print(f"## {title}\n\nrows: {n_rows:,}\n")
    if n_rows == 0:
        return

    summary = con.execute("SUMMARIZE _p").fetchall()
    cols = [d[0] for d in con.description]
    rows = [dict(zip(cols, r)) for r in summary]

    print("| column | type | null % | ~distinct | min | max | flags |")
    print("|---|---|---|---|---|---|---|")
    listed: list[tuple[str, list[tuple]]] = []
    for r in rows:
        name, ctype = r["column_name"], r["column_type"]
        if name == "filename" and args.files:
            continue
        flags = []
        null_pct = float(r["null_percentage"] or 0)
        distinct = int(r["approx_unique"] or 0)
        if null_pct >= 99.99:
            flags.append("ALL NULL")
        elif distinct == 1:
            flags.append("constant")
        numeric = any(t in ctype for t in ("INT", "DOUBLE", "FLOAT", "DECIMAL", "REAL"))
        if numeric and n_rows > 100 and distinct > 20:
            flags.extend(sentinel_flags(con, name, r, n_rows))
        if ctype == "VARCHAR":
            (as_number, comma) = con.execute(
                f"SELECT avg((try_cast({q(name)} AS DOUBLE) IS NOT NULL)::INT), "
                f"avg(regexp_full_match({q(name)}, '-?[0-9]+,[0-9]+')::INT) FROM _p WHERE {q(name)} IS NOT NULL"
            ).fetchone()
            if as_number and as_number > 0.5:
                flags.append(f"{as_number:.0%} numeric text")
            if comma and comma > 0.1:
                flags.append("decimal comma")
        if 0 < distinct <= LIST_VALUES_UP_TO:
            values = con.execute(
                f"SELECT {q(name)}, count(*) FROM _p GROUP BY 1 ORDER BY 2 DESC LIMIT {LIST_VALUES_UP_TO + 5}"
            ).fetchall()
            listed.append((name, values))
        print(f"| {name} | {ctype} | {null_pct:.1f} | {distinct:,} | {r['min']} | {r['max']} | {'; '.join(flags)} |")

    if listed:
        print("\nvalues of low-cardinality columns:")
        for name, values in listed:
            shown = ", ".join(f"{v!r} ({c:,})" for v, c in values)
            print(f"- {name}: {shown}")

    if args.files:
        files = con.execute("SELECT filename, count(*) FROM _p GROUP BY 1 ORDER BY 1").fetchall()
        print(f"\nfiles: {len(files)}; rows per file min {min(c for _, c in files):,}, max {max(c for _, c in files):,}")

    present = {r["column_name"] for r in rows}
    if args.grain and not {c.strip() for c in args.grain.split(",")} <= present:
        print(f"\ngrain ({args.grain}): skipped, not all columns are in this relation")
    elif args.grain:
        keys = ", ".join(q(c.strip()) for c in args.grain.split(","))
        (dupes, extra) = con.execute(
            f"SELECT count(*), coalesce(sum(n) - count(*), 0) FROM "
            f"(SELECT {keys}, count(*) AS n FROM _p GROUP BY ALL HAVING count(*) > 1)"
        ).fetchone()
        (null_keys,) = con.execute(
            f"SELECT count(*) FROM _p WHERE {' OR '.join(f'{q(c.strip())} IS NULL' for c in args.grain.split(','))}"
        ).fetchone()
        verdict = "UNIQUE" if dupes == 0 else f"NOT unique: {dupes:,} keys occur more than once ({extra:,} extra rows)"
        print(f"\ngrain ({args.grain}): {verdict}; rows with a NULL key column: {null_keys:,}")
        if dupes:
            sample = con.execute(
                f"SELECT {keys}, count(*) AS n FROM _p GROUP BY ALL HAVING count(*) > 1 ORDER BY n DESC LIMIT 5"
            ).fetchall()
            print("  examples: " + "; ".join(str(s) for s in sample))

    if args.time and args.time not in present:
        print(f"\ntime ({args.time}): skipped, column not in this relation")
    elif args.time:
        t = q(args.time)
        part = f"PARTITION BY {', '.join(q(c.strip()) for c in args.series.split(','))}" if args.series else ""
        con.execute(
            f"CREATE OR REPLACE TEMP VIEW _steps AS SELECT {t} AS ts, "
            f"{t} - lag({t}) OVER ({part} ORDER BY {t}) AS step FROM _p WHERE {t} IS NOT NULL"
        )
        (mode_step,) = con.execute("SELECT mode(step) FROM _steps WHERE step > INTERVAL 0 SECOND").fetchone()
        (zero, gaps, gap_max) = con.execute(
            "SELECT count(*) FILTER (WHERE step = INTERVAL 0 SECOND), "
            "count(*) FILTER (WHERE step > ?), max(step) FROM _steps",
            [mode_step],
        ).fetchone()
        print(
            f"\ntime ({args.time}{', per ' + args.series if args.series else ''}): typical step {mode_step}; "
            f"repeated timestamps {zero:,}; gaps (step > typical) {gaps:,}; largest gap {gap_max}"
        )
        hours = con.execute(
            "SELECT hour(ts) AS h, count(*) FROM _steps GROUP BY 1 ORDER BY 1"
        ).fetchall()
        if len(hours) == 24:
            counts = [c for _, c in hours]
            lo, hi = min(counts), max(counts)
            if hi > 0 and (hi - lo) / hi > 0.02:
                print(f"  rows per hour of day uneven (min {lo:,}, max {hi:,}): check time zone / DST handling")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--files", action="append", help="glob of CSV/Parquet/JSON files (repeatable)")
    parser.add_argument("--csv-option", action="append", default=[], help="raw read_csv option, e.g. \"delim=';'\"")
    parser.add_argument("--db", help="DuckDB database file (opened read-only)")
    parser.add_argument("--table", action="append", help="table in --db (repeatable; default: all)")
    parser.add_argument("--sql", help="profile the result of this query instead")
    parser.add_argument("--grain", help="comma-separated columns that should identify one row")
    parser.add_argument("--time", help="timestamp column for the regularity check")
    parser.add_argument("--series", help="comma-separated columns that identify one series (for --time)")
    parser.add_argument("--head", type=int, help="print the first N raw lines of the first file and stop")
    args = parser.parse_args()

    if args.head and args.files:
        first = sorted(glob.glob(args.files[0]))
        if not first:
            sys.exit(f"no file matches {args.files[0]}")
        print(f"## first {args.head} lines of {first[0]}\n```")
        with open(first[0], encoding="utf-8", errors="replace") as f:
            for _, line in zip(range(args.head), f):
                print(line.rstrip("\n"))
        print("```")
        return

    con = duckdb.connect(args.db or ":memory:", read_only=bool(args.db))
    if args.sql:
        profile_relation(con, "query", f"({args.sql})", args)
    elif args.files:
        for pattern in args.files:
            matched = glob.glob(pattern)
            if not matched:
                sys.exit(f"no file matches {pattern}")
            profile_relation(con, f"{pattern} ({len(matched)} files)", reader_sql(pattern, args.csv_option), args)
    elif args.db:
        tables = args.table or [
            r[0] for r in con.execute("SELECT table_name FROM information_schema.tables ORDER BY 1").fetchall()
        ]
        for table in tables:
            profile_relation(con, table, q(table), args)
    else:
        parser.error("give --files, --db or --sql")


if __name__ == "__main__":
    main()
