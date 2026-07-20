"""Load the flat Olist CSV into a persistent DuckDB database as the `orders` table."""
import duckdb

con = duckdb.connect("data/olist.duckdb")

con.execute("""
    CREATE OR REPLACE TABLE orders AS
    SELECT * EXCLUDE (column00)
    FROM read_csv_auto('data/raw/olist.csv', header=True, quote='"', sample_size=-1)
""")

n = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
print(f"Loaded {n} rows into data/olist.duckdb (table: orders)")
con.close()
