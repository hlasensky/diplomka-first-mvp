-- build.sql (olist)
-- Loads the flat Olist CSV into DuckDB as the `orders` table.
-- Run: uv run python scripts/build_db.py   (with DATASET=olist; paths are relative to data/raw/olist/)

CREATE OR REPLACE TABLE orders AS
SELECT *
FROM read_csv_auto('olist.csv', header = true, quote = '"', sample_size = -1);
