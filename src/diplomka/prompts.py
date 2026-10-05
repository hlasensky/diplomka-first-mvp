"""LLM prompts, rendered from the active dataset's semantic layer.

Nothing here names a table, column or business term directly: every dataset-specific fact
comes from ``LAYER`` (the YAML) or from DuckDB itself (real columns, level domains), so the
same prompts serve any dataset pack.
"""

from functools import lru_cache

from diplomka.config import MAX_ROWS
from diplomka.db import connect
from diplomka.schema import LAYER, get_domains

# Levels with at most this many values list them all in the prompts; larger domains show a sample.
MAX_LISTED_VALUES = 30


def _domain_hint(level_name: str) -> str:
    values = sorted(get_domains().get(level_name, set()))
    if not values:
        return ""
    if len(values) <= MAX_LISTED_VALUES:
        return f" values: {', '.join(values)}"
    return f" {len(values)} values, e.g. {', '.join(values[:8])}"


def _dataset_header() -> str:
    lines = [f"Dataset '{LAYER.name}': {LAYER.description}"]
    lines.extend(f"- {note}" for note in LAYER.notes)
    return "\n".join(lines)


def _metrics_section() -> str:
    if not LAYER.metrics:
        return "(none - use `measures`)"
    return "\n".join(
        f"- {name}: {m.get('label', name)}" + (f" [{m['unit']}]" if m.get("unit") else "")
        for name, m in LAYER.metrics.items()
    )


def _measures_section() -> str:
    return "\n".join(
        f"- {m.measure_id}: {m.label}{f' [{m.unit}]' if m.unit else ''}; agg: {', '.join(sorted(m.allowed_aggs))}"
        for m in LAYER.measures.values()
    )


def _levels_section() -> str:
    lines = []
    for dim_name, dimension in LAYER.raw["dimensions"].items():
        lines.append(f"{dim_name}:")
        for level_name in dimension.get("levels") or {}:
            level = LAYER.levels[level_name]
            note = f" ({level.note})" if level.note else ""
            lines.append(f"  - {level.name}: {level.label}{note}{_domain_hint(level.name)}")
    return "\n".join(lines)


def _glossary_section() -> str:
    lines = []
    for entry in LAYER.glossary:
        synonyms = f" (also: {', '.join(entry.get('synonyms', []))})" if entry.get("synonyms") else ""
        target = ", ".join(f"{k}={v}" for k, v in entry["maps_to"].items())
        lines.append(f"- {entry['term']}{synonyms} -> {target}")
    return "\n".join(lines) or "(none)"


@lru_cache(maxsize=1)
def intent_prompt() -> str:
    """System prompt for `clarify_intent`: resolve the question into a `Filters` intent."""
    return (
        "You are an analytics assistant. From the user's question in English, resolve which "
        "metrics or measures they ask about, how to break the result down and which filters apply.\n\n"
        f"{_dataset_header()}\n\n"
        "IMPORTANT - the conversation has multiple turns: you receive the full message history. "
        "`HumanMessage` = user questions, `AIMessage` = a structured recap of what was resolved in the "
        'previous turn (marked "[PREVIOUS TURN CONTEXT]") plus the given answer.\n'
        "ALWAYS base your answer on the LAST `HumanMessage` - that is the current question. Use older "
        "messages only to resolve explicit references/follow-ups ('and over time', 'same, but for X') - "
        "never copy them as a template. If the last question does not mention a breakdown, filter or "
        "period that was resolved before, leave that field empty - even if it was set earlier. The only "
        "exception: if the last question names no metric or measure, you may leave both empty and the "
        "previous turn's metrics are reused automatically.\n\n"
        "== NAMED METRICS (`metrics`, list of names; prefer these when one matches) ==\n"
        f"{_metrics_section()}\n\n"
        "== MEASURES (`measures`, list of {measure, agg}; agg must be one of the listed ones) ==\n"
        f"{_measures_section()}\n\n"
        "== DIMENSION LEVELS (use level names in `group_by` and in `filters[].level`) ==\n"
        f"{_levels_section()}\n\n"
        "== GLOSSARY (map the user's words to the semantic layer) ==\n"
        f"{_glossary_section()}\n\n"
        "Fields:\n"
        "- `group_by`: level names to break the result down by, e.g. 'by month' -> a month level. "
        "Leave it empty when the user wants a single total.\n"
        "- `filters`: equality filters {level, value}. Use the exact value from the listed values when "
        "one matches; otherwise write the user's wording and it will be matched fuzzily.\n"
        "- `date_from` / `date_to`: YYYY-MM-DD, from the mentioned period "
        "(e.g. 'Q3 2021' -> 2021-07-01 / 2021-09-30).\n"
        "- `chart_type_request`: only when the user explicitly asks for a chart type (pie, bar, line, ...).\n\n"
        "If the question makes no sense for this dataset, or is too vague to pick a metric or measure, "
        "leave `metrics` and `measures` empty."
    )


@lru_cache(maxsize=1)
def _table_columns() -> dict[str, list[tuple[str, str]]]:
    with connect(read_only=True) as conn:
        return {
            table: [(row[0], row[1]) for row in conn.execute(f"DESCRIBE {table}").fetchall()] for table in LAYER.tables
        }


def _tables_section() -> str:
    blocks = []
    for table, columns in _table_columns().items():
        meta = LAYER.tables[table] or {}
        header = f"{table} ({meta.get('kind', 'table')}"
        header += f", grain: {', '.join(meta['grain'])})" if meta.get("grain") else ")"
        if meta.get("description"):
            header += f" - {meta['description']}"
        blocks.append(header + "\n" + "\n".join(f"  - {name} ({dtype})" for name, dtype in columns))
    return "\n".join(blocks)


def _joins_section() -> str:
    lines = []
    for join in LAYER.raw.get("joins") or []:
        if join.get("type") == "asof":
            # Rendered as literal SQL: a prose form ("ASOF JOIN a with b ON ...") made models emit
            # "ASOF JOIN ON ..." without the right-hand table, a DuckDB parser error.
            line = f"- FROM {join['left']} ASOF [LEFT] JOIN {join['right']} ON {join['on']}"
        else:
            line = f"- {join['left']} = {join['right']} ({join.get('cardinality', '')})"
        if join.get("note"):
            line += f" - {join['note']}"
        lines.append(line)
    return "\n".join(lines) or "(single table, no joins)"


def _sql_metrics_section() -> str:
    lines = []
    for name, m in LAYER.metrics.items():
        table = f" on {m['table']}" if m.get("table") else ""
        note = f" - {m['note']}" if m.get("note") else ""
        lines.append(f"- {name}: {m['sql']}{table}{note}")
    return "\n".join(lines) or "(none)"


def _sql_measures_section() -> str:
    lines = []
    for m in LAYER.measures.values():
        additivity = "; ".join(f"{dim}: {', '.join(aggs)}" for dim, aggs in m.additivity.items())
        line = f"- {m.measure_id} = column {', '.join(m.columns)} in {', '.join(m.tables)}"
        line += f" [{m.unit}]" if m.unit else ""
        line += f"; allowed aggregations by dimension: {additivity}"
        if m.description:
            line += f" - {m.description.strip()}"
        lines.append(line)
    return "\n".join(lines)


def _sql_levels_section() -> str:
    lines = []
    for dim_name, dimension in LAYER.raw["dimensions"].items():
        hierarchies = "; ".join(f"{h}: {' > '.join(path)}" for h, path in (dimension.get("hierarchies") or {}).items())
        lines.append(f"{dim_name} (table {dimension['table']}, key {dimension.get('key', '-')}) {hierarchies}")
        for level_name in dimension.get("levels") or {}:
            level = LAYER.levels[level_name]
            expr = f" = {level.expr}" if level.expr else ""
            note = f" ({level.note})" if level.note else ""
            lines.append(f"  - {level.name}{expr}: {level.label}{note}{_domain_hint(level.name)}")
    return "\n".join(lines)


def _rules_section() -> str:
    return "\n".join(f"- [{r['id']}] {r['text']}" for r in LAYER.raw.get("rules") or []) or "(none)"


def _examples_section() -> str:
    return (
        "\n\n".join(f"-- {ex['question']}\n{ex['sql'].strip()}" for ex in LAYER.raw.get("examples") or []) or "(none)"
    )


@lru_cache(maxsize=1)
def sql_prompt() -> str:
    """System prompt for `generate_sql`: real columns + semantic layer + SQL and charting rules."""
    return (
        "You write a single analytical SQL query (DuckDB dialect) over the tables below, based on a "
        "resolved user intent.\n\n"
        f"== DATASET ==\n{_dataset_header()}\n\n"
        f"== TABLES AND COLUMNS ==\n{_tables_section()}\n\n"
        f"== JOINS ==\n{_joins_section()}\n\n"
        f"== NAMED METRICS (use these exact SQL expressions when they match the intent) ==\n"
        f"{_sql_metrics_section()}\n\n"
        f"== MEASURES ==\n{_sql_measures_section()}\n\n"
        f"== DIMENSIONS AND LEVELS ==\n{_sql_levels_section()}\n\n"
        f"== SEMANTIC RULES ==\n{_rules_section()}\n\n"
        f"== EXAMPLE QUERIES ==\n{_examples_section()}\n\n"
        "== SQL RULES ==\n"
        "- Output a single SELECT statement only - no DDL/DML (the connection is read-only anyway).\n"
        "- Inline all literal values directly in the SQL - there are no bind parameters.\n"
        "- Alias EVERY selected expression explicitly with `AS <name>` - including plain columns, "
        "casts and window functions, not just aggregates. `x`/`y` in your structured output must "
        "match those exact aliases, since they're read back against the query's real result columns.\n"
        "- Free to use CTEs, window functions, HAVING, subqueries, CASE WHEN, period-over-period "
        "comparisons etc. when the intent calls for them - you are not limited to a single GROUP BY.\n"
        "- Use only the join paths listed above. For a time breakdown use the time dimension's levels "
        "and order chronologically, not by metric value.\n"
        "- If the resolved intent has no group_by, write a single aggregate row - no GROUP BY, no "
        "breakdown of any kind - even if the underlying data spans a wide time range.\n"
        f"- Limit results to at most {MAX_ROWS} rows (results are truncated to this anyway).\n\n"
        "== CHARTING ==\n"
        "If the intent explicitly requested a chart_type, use exactly that. Otherwise pick the "
        "chart_type that best fits the query's actual shape - don't default to bar for everything:\n"
        "- line: a metric broken down by time, ordered chronologically.\n"
        "- area: like line, when the cumulative volume under the trend is itself meaningful.\n"
        "- bar: one metric, or a few metrics with DIFFERENT units, broken down by a categorical "
        "dimension - differing-unit metrics are automatically placed on separate y-axes, so this is "
        "the right choice for them.\n"
        "- stacked_bar: 2+ metrics that share the SAME unit, where the stacked total per category is "
        "itself meaningful. Never stack metrics with different units/scales - use bar instead.\n"
        "- pie: a single additive metric, few rows (<=8), where shares of a whole are the point - "
        "x = the category/dimension column (the slice labels), y = the single metric column.\n"
        "- scatter: correlation between two numeric columns - x and a single y, both numeric, no "
        "aggregation/grouping.\n"
        "- histogram: the distribution of a single numeric column across raw (non-aggregated) rows - "
        "set only x (the numeric column), leave y empty.\n"
        "- box: comparing the distribution/spread of a numeric column across a category - "
        "x = category, y = the single numeric column, on non-aggregated rows.\n"
        "- heatmap: one metric broken down by two dimensions at once - x and y are the two dimension "
        "columns, z is the value/color column.\n"
        "- table: a detail/lookup query, or anything with no clear single chartable breakdown - "
        "leave x/y/z empty in this case.\n"
        "Set y_units from the units of the measures/metrics above.\n"
        "Leave chart_type empty only when none of the above fit and a table would be equally useless "
        "(e.g. a single aggregate value)."
    )


def response_instructions() -> str:
    """Dataset-specific guidance appended to the answer-summarizing prompt."""
    units = sorted({f"{m.label}: {m.unit}" for m in LAYER.measures.values() if m.unit})
    units += sorted(f"{m.get('label', name)}: {m['unit']}" for name, m in LAYER.metrics.items() if m.get("unit"))
    lines = [f"Dataset: {LAYER.name}."]
    lines.extend(LAYER.notes)
    if units:
        lines.append("Units: " + "; ".join(units) + ".")
    return " ".join(lines)


# Separates the answer from its derivation in `generate_response` output; only the part before
# it goes into the conversation history.
DERIVATION_HEADING = "How this was derived:"


def response_prompt(question: str, columns: list[str], preview: str, derivation: str) -> str:
    """Prompt for `generate_response`: a short answer plus the steps that led to the data,
    so the user can see where the conclusion comes from."""
    return (
        f"User question: {question}\n\n"
        f"Query result (columns {columns}):\n{preview}\n\n"
        f"Facts about how the result was obtained:\n{derivation}\n\n"
        f"{response_instructions()}\n\n"
        "Write the reply in English. Start directly with the answer - no heading, label or numbering - "
        "in 1-3 sentences, sticking to the numbers from the query result above; don't make anything up.\n"
        f"Then an empty line, the line '{DERIVATION_HEADING}' and a numbered list of 3-6 "
        "short steps that explain, for a non-technical user, how the answer was reached: how the "
        "question was interpreted (which measure/metric, aggregation, breakdown, filters and period), "
        "any free-text value that was matched to a value in the data, which data it comes from (describe "
        "the tables in plain words, e.g. 'hourly sensor readings of each hive'), how it was computed "
        "(joins, aggregation, grouping, ordering, row limits), any correction of the query, and a "
        "caveat from the dataset notes only if it limits this conclusion - never use a note to claim "
        "the result is reliable. Use only the facts given above.\n"
        "Plain text only: no SQL, no code, no ``` blocks."
    )
