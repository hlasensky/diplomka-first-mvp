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
        "If the intent explicitly requested a chart_type, use exactly that. Otherwise pick the "
        "chart_type that best fits the query's actual shape - don't default to bar for everything:\n"
        "- line: a metric broken down by time, ordered chronologically.\n"
        "- area: like line, when the cumulative volume under the trend is itself meaningful.\n"
        "- bar: one metric (or a few) broken down by a category/state/seller dimension.\n"
        "- stacked_bar: 2+ metrics or a part-of-whole breakdown across a category dimension, "
        "where the total per category also matters.\n"
        "- pie: a single additive metric, few rows (<=8), where shares of a whole are the point.\n"
        "- scatter: correlation between two numeric columns (e.g. price vs freight_value) - "
        "x and a single y, both numeric, no aggregation/grouping.\n"
        "- histogram: the distribution of a single numeric column across raw (non-aggregated) rows - "
        "set only x (the numeric column), leave y empty.\n"
        "- box: comparing the distribution/spread of a numeric column across a category - "
        "x = category, y = the single numeric column, on non-aggregated rows.\n"
        "- heatmap: one metric broken down by two dimensions at once (e.g. category x state) - "
        "x and y are the two dimension columns, z is the value/color column.\n"
        "- table: a detail/lookup query, or anything with no clear single chartable breakdown - "
        "leave x/y/z empty in this case.\n"
        "Leave chart_type empty only when none of the above fit and a table would be equally useless "
        "(e.g. a single aggregate value)."
    )
