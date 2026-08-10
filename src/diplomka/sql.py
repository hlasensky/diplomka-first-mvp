"""Deterministic SQL builder: turns a validated ``Filters`` intent into parametrized SQL."""

from diplomka.models import Filters
from diplomka.schema import SCHEMA


def build_sql(intent: Filters) -> tuple[str, list]:
    metrics = intent.resolve_metrics()
    select = [f"{m['sql']} AS {m['alias']}" for m in metrics]
    group_by = ""
    order_by = f"ORDER BY {metrics[0]['alias']} DESC"
    limit = 20

    if intent.dimension is not None:
        dim_col = SCHEMA["dimensions"][intent.dimension]["column"]
        if intent.dimension == "time":
            # the time dimension is aggregated by week (default) and sorted chronologically, not by metric value
            granularity = intent.granularity or "week"
            dim_expr = f"DATE_TRUNC('{granularity}', {dim_col})"
            select.insert(0, f"{dim_expr} AS {dim_col}")
            group_by = f"GROUP BY {dim_expr}"
            order_by = f"ORDER BY {dim_expr}"
            limit = 200
        else:
            select.insert(0, dim_col)
            group_by = f"GROUP BY {dim_col}"

    where_clauses, params = [], []
    if intent.category_filter:
        where_clauses.append("product_category_name = ?")
        params.append(intent.category_filter)
    if intent.state_filter:
        where_clauses.append("customer_state = ?")
        params.append(intent.state_filter)
    if intent.date_from:
        where_clauses.append("order_purchase_timestamp >= ?")
        params.append(intent.date_from)
    if intent.date_to:
        where_clauses.append("order_purchase_timestamp <= ?")
        params.append(intent.date_to)
    where = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

    sql = f"SELECT {', '.join(select)} FROM {SCHEMA['table']} {where} {group_by} {order_by} LIMIT {limit}"
    return sql, params
