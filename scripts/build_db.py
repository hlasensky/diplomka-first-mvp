"""Build the DuckDB database of the active dataset pack from its raw files.

Runs ``datasets/<DATASET>/build.sql`` with ``data/raw/<DATASET>/`` as the working directory,
so the paths inside build.sql stay relative and portable. Output: ``data/<DATASET>.duckdb``
(or ``DUCKDB_PATH``).

    DATASET=senger uv run python scripts/build_db.py
"""

import os
import time

import duckdb

from diplomka.config import BUILD_SQL, DATASET, DUCKDB_PATH, RAW_DIR


def main() -> None:
    if not RAW_DIR.exists():
        raise SystemExit(f"Raw data directory {RAW_DIR} not found - put (or symlink) the raw files there.")

    sql = BUILD_SQL.read_text()
    start = time.monotonic()
    con = duckdb.connect(str(DUCKDB_PATH))
    cwd = os.getcwd()
    os.chdir(RAW_DIR)
    try:
        con.execute(sql)
    finally:
        os.chdir(cwd)

    print(f"Built {DUCKDB_PATH} (dataset: {DATASET}) in {time.monotonic() - start:.1f}s")
    for (table,) in con.execute("SELECT table_name FROM information_schema.tables ORDER BY 1").fetchall():
        (count,) = con.execute(f"SELECT count(*) FROM {table}").fetchone() or (0,)
        print(f"  {table}: {count} rows")
    con.close()


if __name__ == "__main__":
    main()
