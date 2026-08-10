"""Minimal proof that the YAML semantic schema maps to valid SQL over DuckDB."""

from diplomka.db import connect
from diplomka.schema import SCHEMA

con = connect(read_only=True)


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
    print("--- revenue by category (top 5) ---")
    q = build_query("revenue", dimension="category", limit=5)
    print(q)
    print(con.execute(q).fetchdf().to_string())

    print("\n--- drill-down: cama_mesa_banho by state (top 5) ---")
    q = build_query("revenue", dimension="state", filters="product_category_name = 'cama_mesa_banho'", limit=5)
    print(q)
    print(con.execute(q).fetchdf().to_string())

    print("\n--- slice: revenue for Q3 2018 by category (top 5) ---")
    q = build_query(
        "revenue",
        dimension="category",
        filters="order_purchase_timestamp BETWEEN '2018-07-01' AND '2018-09-30'",
        limit=5,
    )
    print(q)
    print(con.execute(q).fetchdf().to_string())

    print("\n--- avg_order_value and delivery_time overall ---")
    print(con.execute(build_query("avg_order_value", limit=1)).fetchdf().to_string())
    print(con.execute(build_query("delivery_time", limit=1)).fetchdf().to_string())
