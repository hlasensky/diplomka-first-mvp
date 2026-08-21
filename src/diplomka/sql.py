"""Schema context for LLM-generated SQL: grounds the free-form ``generate_sql`` node in the
real table columns plus the semantic layer (schema/semantic_schema.yaml), so it isn't just
guessing at column names."""

from functools import lru_cache

from diplomka.db import connect
from diplomka.schema import SCHEMA

MAX_ROWS = 500


@lru_cache(maxsize=1)
def _table_columns() -> list[tuple[str, str]]:
    with connect(read_only=True) as conn:
        return [(row[0], row[1]) for row in conn.execute(f"DESCRIBE {SCHEMA['table']}").fetchall()]


@lru_cache(maxsize=1)
def build_schema_context() -> str:
    """System prompt for the SQL-generating LLM: real columns + named metrics/dimensions + rules."""

    columns = "\n".join(f"- {name} ({dtype})" for name, dtype in _table_columns())
    metrics = "\n".join(
        f"- {name}: {m['sql']} ({m.get('note', m.get('unit', 'value'))})" for name, m in SCHEMA["metrics"].items()
    )
    dimensions = "\n".join(
        f"- {name}: column `{d['column']}`" + (f" - {d['note']}" if "note" in d else "")
        for name, d in SCHEMA["dimensions"].items()
    )

    return (
        "You write a single analytical SQL query (DuckDB dialect) against the table "
        f"`{SCHEMA['table']}` (1 row = 1 order item), based on a resolved user intent.\n\n"
        f"== COLUMNS in `{SCHEMA['table']}` ==\n{columns}\n\n"
        f"== NAMED METRICS (prefer these exact SQL expressions when they match the intent) ==\n{metrics}\n\n"
        f"== NAMED DIMENSIONS ==\n{dimensions}\n\n"
        "== RULES ==\n"
        "- Output a single SELECT statement only - no DDL/DML (the connection is read-only anyway).\n"
        "- Inline all literal values directly in the SQL - there are no bind parameters.\n"
        "- Alias EVERY selected expression explicitly with `AS <name>` - including plain columns, "
        "casts and window functions, not just aggregates. `x`/`y` in your structured output must "
        "match those exact aliases, since they're read back against the query's real result columns.\n"
        "- Free to use CTEs, window functions, HAVING, subqueries, CASE WHEN, period-over-period "
        "comparisons etc. when the intent calls for them - you are not limited to a single GROUP BY.\n"
        "- For a time breakdown, use DATE_TRUNC('<granularity>', order_purchase_timestamp) and order "
        "chronologically, not by metric value.\n"
        f"- Limit results to at most {MAX_ROWS} rows (results are truncated to this anyway).\n"
        "- Monetary amounts (payment_value, freight_value, price) are in Brazilian reais (BRL, R$).\n\n"
        "== CHARTING ==\n"
        "If the intent explicitly requested a chart_type, use exactly that. Otherwise choose one only "
        "when the result has a clear x-axis + at least one numeric y (e.g. a dimension breakdown): "
        "time dimension -> line; a single additive metric with few rows -> pie; otherwise -> bar. "
        "Leave chart_type/x/y empty when the query doesn't produce a chartable breakdown "
        "(e.g. a single aggregate row, or a detail/lookup query)."
    )
