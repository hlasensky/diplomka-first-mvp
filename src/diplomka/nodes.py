"""LangGraph node functions and conditional routing for the analytics agent."""

import sqlglot
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from sqlglot import exp

from diplomka.config import MAX_ROWS
from diplomka.db import connect
from diplomka.llm import get_llm, get_structured_llm
from diplomka.models import (
    AgentState,
    ChartCritique,
    ChartSpec,
    Filters,
    LevelFilter,
    PartialAgentState,
    SqlGeneration,
)
from diplomka.prompts import DERIVATION_HEADING, intent_prompt, response_prompt, sql_prompt
from diplomka.retrieval import lookup_values
from diplomka.schema import LAYER, get_domains
from diplomka.semantic_validator import format_feedback, validate_semantics

# one more than the chart retries: the semantic validator can also send a query back
MAX_SQL_ATTEMPTS = 3
MAX_CHART_ATTEMPTS = 2
# Minimum embedding similarity for a fuzzy filter-value match to be accepted.
MIN_MATCH_SCORE = 0.5


def _selected_model(config: RunnableConfig) -> str | None:
    """Runtime model override (e.g. from a UI picker), passed as config={"configurable": {"model": ...}}."""
    return config.get("configurable", {}).get("model")


def user_input(state: AgentState) -> PartialAgentState:
    """Entry node: wraps `question` (from the initial state at invoke()) into a HumanMessage in the history."""
    return {"messages": [HumanMessage(content=state["question"])]}


def _clarification_question(intent: Filters) -> str:
    """Specific clarification: what was not recognized and what the dataset can answer."""
    parts = ["I couldn't tell which value to compute for this question."]
    if intent.adjustments:
        parts.append(f"Not recognized: {'; '.join(intent.adjustments)}.")
    labels = [m.get("label", name) for name, m in LAYER.metrics.items()]
    labels += [m.label for m in LAYER.measures.values()]
    parts.append(f"I can compute e.g. {', '.join(labels[:8])} - could you rephrase with one of these?")
    return " ".join(parts)


def clarify_intent(state: AgentState, config: RunnableConfig) -> PartialAgentState:
    """LLM parses the question into `Filters` (merged with `active_filters` from before).
    Sets `intent=None` + `needs_clarification`/`clarification_question` when the query is ambiguous."""

    structured_llm = get_structured_llm(Filters, _selected_model(config))
    intent = structured_llm.invoke([SystemMessage(content=intent_prompt()), *state["messages"]])
    assert isinstance(intent, Filters)

    # a follow-up that names no metric/measure ("and only for colonies that died") keeps the previous ones
    active_filters = state.get("active_filters", Filters())
    if not intent.has_metric():
        intent = intent.model_copy(update={"metrics": active_filters.metrics, "measures": active_filters.measures})

    is_unclear = not intent.has_metric()

    return {
        "intent": intent,
        "needs_clarification": is_unclear,
        "clarification_question": _clarification_question(intent) if is_unclear else None,
        "attempts": state.get("attempts", 0) if is_unclear else 0,
        "sql_attempts": 0,
        "sql_error": None,
        "semantic_violations": [],
        "unresolved_filters": [],
        "filter_candidates": [],
        "chart_attempts": 0,
        "chart_validation_error": None,
    }


def _unresolved_filters(intent: Filters) -> list[LevelFilter]:
    """Filters whose value is not in the known domain of its level (e.g. free text like "beauty
    products" instead of a real category value). Levels without a domain are taken as-is."""
    domains = get_domains()
    return [f for f in intent.filters if f.level in domains and f.value not in domains[f.level]]


def complex_query(state: AgentState) -> PartialAgentState:
    """Branch where filter values written as free text must be resolved to real
    dimension-level values before generating SQL."""
    intent = state["intent"]
    assert intent is not None
    return {"unresolved_filters": _unresolved_filters(intent)}


def unclear_query(state: AgentState) -> PartialAgentState:
    """Intent could not be recognized even after clarify_intent - ends the turn
    and returns `clarification_question` to the user."""

    if state["attempts"] >= 3:
        message = "Sorry, I still don't understand your question."
        return {
            "needs_clarification": False,
            "clarification_question": message,
            "messages": [AIMessage(content=message)],
        }
    return {
        "attempts": state["attempts"] + 1,
        "needs_clarification": True,
        "clarification_question": state["clarification_question"],
        "messages": [AIMessage(content=state["clarification_question"])],
    }


def embedding_lookup(state: AgentState) -> PartialAgentState:
    """Fuzzy-matches each unresolved filter value to the values of its level via embeddings
    (domain values + glossary synonyms), result into `filter_candidates`."""

    candidates = [lookup_values(f.level, f.value, k=3) for f in state["unresolved_filters"]]
    return {"filter_candidates": candidates}


def improve_prompt(state: AgentState) -> PartialAgentState:
    """Self-check: verifies every unresolved filter value has a good fuzzy match; on a problem
    increments `attempts` and returns to clarify_intent (up to the limit), otherwise replaces
    the free-text values with the matched ones and proceeds to generate_sql."""

    resolved: dict[tuple[str, str], str] = {}
    for f, candidates in zip(state["unresolved_filters"], state["filter_candidates"], strict=True):
        if not candidates or candidates[0][1] <= MIN_MATCH_SCORE:
            if state["attempts"] >= 3:
                return {
                    "needs_clarification": False,
                    "clarification_question": "Sorry, I still don't understand your question.",
                }
            label = LAYER.levels[f.level].label
            return {
                "attempts": state["attempts"] + 1,
                "needs_clarification": True,
                "clarification_question": f"Could you clarify what you mean by '{f.value}' ({label})?",
            }
        resolved[(f.level, f.value)] = candidates[0][0]

    intent = state["intent"]
    assert intent is not None
    filters = [f.model_copy(update={"value": resolved.get((f.level, f.value), f.value)}) for f in intent.filters]
    intent = intent.model_copy(update={"filters": filters})

    return {
        "intent": intent,
        "needs_clarification": False,
        "clarification_question": None,
    }


def _intent_summary(intent: Filters) -> str:
    """Deterministic recap of the resolved Filters - used both as input for `generate_sql` and
    for the AIMessage that `clarify_intent` reads back in the next turn."""
    metrics = ", ".join(intent.metrics) or "-"
    measures = ", ".join(f"{m.agg}({m.measure})" for m in intent.measures) or "-"
    group_by = ", ".join(intent.group_by) or "-"
    filters = ", ".join(f"{f.level}={f.value}" for f in intent.filters) or "-"
    return (
        "[PREVIOUS TURN CONTEXT - only for resolving references, DO NOT automatically copy into the new question]\n"
        f"metrics: {metrics} | measures: {measures} | group_by: {group_by}\n"
        f"filters: {filters} | period: {intent.date_from or '-'} to {intent.date_to or '-'} | "
        f"chart_type_request: {intent.chart_type_request or '-'}"
        + (f"\nadjustments: {'; '.join(intent.adjustments)}" if intent.adjustments else "")
    )


def _measure_columns(intent: Filters) -> str:
    """Measure ids in the intent are not column names (t_center = t_i_3) - spell out the mapping."""
    lines = [
        f"- {m.measure} = column {', '.join(LAYER.measures[m.measure].columns)} "
        f"in {', '.join(LAYER.measures[m.measure].tables)}"
        for m in intent.measures
    ]
    return "Measure columns (use these column names in SQL):\n" + "\n".join(lines) + "\n\n" if lines else ""


def generate_sql(state: AgentState, config: RunnableConfig) -> PartialAgentState:
    """LLM writes free SQL (DuckDB dialect) grounded in the semantic schema, from the resolved
    intent; also emits its own chart hint (chart_type/x/y/y_units/title) for that same query.
    On a retry, the previous DuckDB error (`sql_error`) or chart critique (`chart_validation_error`)
    is fed back for a fix."""

    intent = state["intent"]
    assert intent is not None

    human = (
        f"User question: {state['question']}\n\n"
        f"Resolved intent:\n{_intent_summary(intent)}\n\n"
        f"{_measure_columns(intent)}"
        "Write the SQL query. The resolved intent gives you the metric/dimension/filters, but "
        "re-read the user question literally for anything the intent doesn't capture - row limits "
        "('top 10', 'bottom 5'), sort direction, thresholds ('at least 50'), exclusions, etc."
    )
    if state["sql_error"]:
        human += f"\n\nThe previous attempt was rejected - fix it:\n{state['sql_error']}"
    if state["chart_validation_error"]:
        human += (
            "\n\nThe previous chart choice had this problem - keep the same SQL logic but fix "
            f"chart_type/x/y/y_units/title:\n{state['chart_validation_error']}"
        )

    structured_llm = get_structured_llm(SqlGeneration, _selected_model(config))
    generation = structured_llm.invoke([SystemMessage(content=sql_prompt()), HumanMessage(content=human)])
    assert isinstance(generation, SqlGeneration)

    return {"sql_generation": generation, "sql_error": None, "chart_validation_error": None}


def validate_sql(state: AgentState) -> PartialAgentState:
    """Checks the LLM-generated SQL before ever executing it for real: syntactically valid DuckDB
    (via EXPLAIN, on a read-only connection), then semantically valid against the semantic layer
    (allowed aggregations, fan-trap joins, filter values). On failure, records the error for a
    retry in generate_sql; semantic violations are also kept in `semantic_violations` for eval."""

    generation = state["sql_generation"]
    assert generation is not None

    try:
        with connect(read_only=True) as conn:
            conn.execute(f"EXPLAIN {generation.sql}")
    except Exception as e:
        return {"sql_error": str(e), "sql_attempts": state["sql_attempts"] + 1}

    violations = validate_semantics(generation.sql, LAYER, get_domains())
    if violations:
        return {
            "sql_error": format_feedback(violations),
            "sql_attempts": state["sql_attempts"] + 1,
            # accumulated over the turn's retries - kept for eval and for explaining the answer
            "semantic_violations": state["semantic_violations"] + [f"[{v.rule}] {v.message}" for v in violations],
        }
    return {"sql_error": None}


def execute_query(state: AgentState) -> PartialAgentState:
    """Runs the LLM-generated SQL (read-only connection) against the dataset's DuckDB -> columns/rows.
    Also reached after exhausting sql retries - a still-broken query fails here the normal way,
    surfacing as `validation_error` in generate_response."""

    generation = state["sql_generation"]
    intent = state["intent"]
    assert generation is not None
    assert intent is not None

    columns, rows = [], []
    error = None
    with connect(read_only=True) as conn:
        try:
            result = conn.execute(generation.sql).fetchall()
            columns = [desc[0] for desc in conn.description]
            rows = result[:MAX_ROWS]
        except Exception as e:
            error = str(e)

    return {
        "columns": columns,
        "rows": rows,
        "needs_clarification": False,
        "clarification_question": None,
        "validation_error": error,
        "active_filters": intent,
    }


def _valid_chart_generation(generation: SqlGeneration, columns: list[str]) -> bool:
    """Checks generation's chart hint actually matches the query's real result columns, with
    arity rules that depend on chart_type (e.g. histogram needs no y, heatmap needs a z)."""

    if generation.chart_type is None:
        print("No chart_type in generation")
        return False
    if generation.chart_type == "table":
        return True
    if generation.x is None or generation.x not in columns:
        return False
    if generation.chart_type == "histogram":
        return True
    if not generation.y or not all(y in columns for y in generation.y):
        return False
    if generation.chart_type in ("pie", "scatter", "box") and len(generation.y) != 1:
        return False
    if generation.chart_type == "heatmap" and (generation.z is None or generation.z not in columns):
        return False
    print(f"Valid chart generation: {generation.chart_type} x={generation.x} y={generation.y} z={generation.z}")
    return True


def _source_tables(sql: str) -> list[str]:
    """Semantic-layer tables the query reads from (CTE names and unknown tables left out)."""
    try:
        tree = sqlglot.parse_one(sql, read="duckdb")
    except sqlglot.errors.ParseError:
        return []
    return sorted({t.name for t in tree.find_all(exp.Table) if t.name in LAYER.tables})


def _derivation_facts(state: AgentState) -> str:
    """Deterministic record of how the answer was obtained - the LLM turns it into the
    'How this was derived' steps, so they rest on what actually happened, not on its guess."""
    intent = state["intent"]
    generation = state["sql_generation"]
    assert intent is not None
    assert generation is not None

    def level_label(name: str) -> str:
        return LAYER.levels[name].label

    facts = []
    for name in intent.metrics:
        metric = LAYER.metrics[name]
        facts.append(f"- Metric: {metric.get('label', name)} = {metric['sql']}")
    for m in intent.measures:
        measure = LAYER.measures[m.measure]
        unit = f" [{measure.unit}]" if measure.unit else ""
        facts.append(f"- Measure: {m.agg} of {measure.label}{unit}")
    if intent.group_by:
        facts.append(f"- Broken down by: {', '.join(level_label(level) for level in intent.group_by)}")
    else:
        facts.append("- No breakdown: a single total")
    for f in intent.filters:
        facts.append(f"- Filter: {level_label(f.level)} = {f.value}")
    if intent.date_from or intent.date_to:
        facts.append(f"- Period: {intent.date_from or 'start'} to {intent.date_to or 'end'}")

    facts += [f"- Interpretation adjusted: {note}" for note in intent.adjustments]
    for f, candidates in zip(state["unresolved_filters"], state["filter_candidates"], strict=False):
        if candidates:
            value, score = candidates[0]
            facts.append(
                f"- The user's wording '{f.value}' was matched to {level_label(f.level)} '{value}' "
                f"(similarity {score:.2f})"
            )

    for table in _source_tables(generation.sql):
        meta = LAYER.tables[table] or {}
        facts.append(f"- Source table {table}: {meta.get('description', meta.get('kind', ''))}".rstrip(": "))
    facts.append(f"- SQL that ran (explain it in plain words, do not quote it):\n{generation.sql.strip()}")

    if state["sql_attempts"]:
        facts.append(f"- The first draft of the query was rejected {state['sql_attempts']}x and rewritten")
    for violation in state["semantic_violations"]:
        facts.append(f"- Rejected because: {violation}")

    rows = len(state["rows"])
    truncated = f" (truncated to the first {MAX_ROWS})" if rows >= MAX_ROWS else ""
    facts.append(f"- Result: {rows} row(s){truncated}; the summary sees at most the first 20")
    return "\n".join(facts)


def generate_response(state: AgentState, config: RunnableConfig) -> PartialAgentState:
    """LLM summarizes columns/rows into a short NL answer followed by the steps that led to the
    data (`answer`), built from `_derivation_facts`; `ChartSpec` is taken from generate_sql's
    chart hint, validated against the query's real result columns."""

    has_error = state["validation_error"] is not None
    if has_error:
        return {
            "answer": f"An error occurred while executing the query: {state['validation_error']}",
            "chart_spec": None,
            "messages": [AIMessage(content="[The previous query failed with a database error - ignore this context]")],
        }

    columns = state["columns"]
    rows = state["rows"]
    intent = state["intent"]
    generation = state["sql_generation"]
    assert intent is not None
    assert generation is not None

    chart_spec = None
    if _valid_chart_generation(generation, columns):
        assert generation.chart_type is not None
        chart_spec = ChartSpec(
            chart_type=generation.chart_type,
            x=generation.x,
            y=generation.y,
            y_units=generation.y_units or ["value"] * len(generation.y),
            z=generation.z,
            title=generation.title or (", ".join(generation.y) if generation.y else generation.x or ""),
        )

    preview = "\n".join(str(dict(zip(columns, row, strict=False))) for row in rows[:20])
    prompt = response_prompt(state["question"], columns, preview, _derivation_facts(state))
    content = get_llm(_selected_model(config)).invoke(prompt).content
    answer = content if isinstance(content, str) else str(content)
    # the derivation steps stay out of the history - clarify_intent only needs the answer itself
    short_answer = answer.split(DERIVATION_HEADING)[0].strip()

    return {
        "answer": answer,
        "chart_spec": chart_spec,
        "messages": [AIMessage(content=f"{_intent_summary(intent)}\n\nAnswer to the user: {short_answer}")],
    }


def validate_chart_spec(state: AgentState, config: RunnableConfig) -> PartialAgentState:
    """LLM second-opinion on the chosen `ChartSpec` (chart_type fits the data shape, axes not
    swapped, title not empty, etc). `chart_spec=None` (no chartable breakdown) always proceeds -
    nothing to critique. On a real problem, feeds it back to generate_sql for a redo, up to
    MAX_CHART_ATTEMPTS; if still unresolved, drops the chart rather than show a bad one."""

    chart_spec = state["chart_spec"]
    if chart_spec is None or chart_spec.chart_type == "table":
        return {"chart_validation_error": None}

    preview = "\n".join(str(dict(zip(state["columns"], row, strict=False))) for row in state["rows"][:10])
    structured_llm = get_structured_llm(ChartCritique, _selected_model(config))
    critique = structured_llm.invoke(
        [
            SystemMessage(
                content=(
                    "You review a chart choice for a data question, for correctness and basic design "
                    "quality. Flag it (ok=False) only for real problems: wrong chart_type for the data "
                    "shape - a pie/box/scatter with more than one y column, a pie with a time x-axis or "
                    "more than 8 slices, a line/area chart with a non-time categorical x-axis, a scatter "
                    "or histogram computed over already-aggregated/grouped rows instead of raw ones, a "
                    "heatmap missing its z (color) column, x/y swapped, an empty or unhelpful title, or a "
                    "y_units length that doesn't match y. Do not flag mere stylistic preference - a "
                    "reasonable, correctly-shaped chart is always fine even if a different type could "
                    "also have worked.\n"
                    "One specific check: read the chart_type value literally, character for character, "
                    "before judging it - do not assume or recall a different chart_type than the one "
                    "actually given. Only flag mixed-unit y columns (e.g. currency + count) when "
                    "chart_type is literally 'stacked_bar' (name 'bar' as the fix). A plain 'bar' with "
                    "mixed-unit y columns is exactly correct as-is - do NOT flag it, and do NOT describe "
                    "it as 'stacked' in your issue text."
                )
            ),
            HumanMessage(
                content=(
                    f"User question: {state['question']}\n"
                    f"Chart: chart_type={chart_spec.chart_type}, x={chart_spec.x}, y={chart_spec.y}, "
                    f"y_units={chart_spec.y_units}, z={chart_spec.z}, title={chart_spec.title!r}\n"
                    f"Sample rows:\n{preview}"
                )
            ),
        ]
    )
    assert isinstance(critique, ChartCritique)

    if critique.ok:
        return {"chart_validation_error": None}
    if state["chart_attempts"] >= MAX_CHART_ATTEMPTS:
        # give up - show the result without a chart rather than a bad one
        return {"chart_validation_error": None, "chart_spec": None}
    return {"chart_validation_error": critique.issue, "chart_attempts": state["chart_attempts"] + 1}


# Conditional routing
def route_intent(state: AgentState) -> str:
    intent = state["intent"]
    assert intent is not None
    if not intent.has_metric():
        return "unclear"
    return "complex" if _unresolved_filters(intent) else "basic"


def route_clarification(state: AgentState) -> str:
    if state["needs_clarification"]:
        return "user_input"
    return "proceed"


def route_sql_validation(state: AgentState) -> str:
    if state["sql_error"] is None or state["sql_attempts"] >= MAX_SQL_ATTEMPTS:
        return "proceed"
    return "retry"


def route_validate_chart_spec(state: AgentState) -> str:
    return "retry" if state["chart_validation_error"] is not None else "proceed"
