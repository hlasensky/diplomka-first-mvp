"""Minimal proof that the YAML semantic schema maps to valid SQL over DuckDB."""
import duckdb
import yaml

with open("schema/semantic_schema.yaml") as f:
    SCHEMA = yaml.safe_load(f)

con = duckdb.connect("data/olist.duckdb", read_only=True)


def build_query(metric: str, dimension: str | None = None, filters: str | None = None, limit: int = 10) -> str:
    metric_sql = SCHEMA["metrics"][metric]["sql"]
    table = SCHEMA["table"]
    select = [f"{metric_sql} AS {metric}"]
    group_by = ""
    if dimension:
        dim_col = SCHEMA["dimensions"][dimension]["column"]
        select.insert(0, dim_col)
        group_by = f"GROUP BY {dim_col} ORDER BY {metric} DESC"
    where = f"WHERE {filters}" if filters else ""
    return f"SELECT {', '.join(select)} FROM {table} {where} {group_by} LIMIT {limit}"


if __name__ == "__main__":
    print("--- tržby podle kategorie (top 5) ---")
    q = build_query("revenue", dimension="category", limit=5)
    print(q)
    print(con.execute(q).fetchdf().to_string())

    print("\n--- drill-down: cama_mesa_banho podle státu (top 5) ---")
    q = build_query("revenue", dimension="state", filters="product_category_name = 'cama_mesa_banho'", limit=5)
    print(q)
    print(con.execute(q).fetchdf().to_string())

    print("\n--- slice: tržby za Q3 2018 podle kategorie (top 5) ---")
    q = build_query(
        "revenue",
        dimension="category",
        filters="order_purchase_timestamp BETWEEN '2018-07-01' AND '2018-09-30'",
        limit=5,
    )
    print(q)
    print(con.execute(q).fetchdf().to_string())

    print("\n--- avg_order_value a delivery_time celkem ---")
    print(con.execute(build_query("avg_order_value", limit=1)).fetchdf().to_string())
    print(con.execute(build_query("delivery_time", limit=1)).fetchdf().to_string())
