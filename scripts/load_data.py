"""Load the flat Olist CSV into a persistent DuckDB database as the `orders` table."""

import duckdb

from diplomka.config import DUCKDB_PATH, RAW_CSV

con = duckdb.connect(str(DUCKDB_PATH))

con.execute(f"""
    CREATE OR REPLACE TABLE orders AS
    SELECT * EXCLUDE (column00)
    FROM read_csv_auto('{RAW_CSV}', header=True, quote='"', sample_size=-1)
""")

row = con.execute("SELECT COUNT(*) FROM orders").fetchone()
n = row[0] if row is not None else 0
print(f"Loaded {n} rows into {DUCKDB_PATH} (table: orders)")
con.close()
