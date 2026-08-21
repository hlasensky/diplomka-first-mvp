"""LangGraph node functions and conditional routing for the analytics agent."""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from diplomka.db import connect
from diplomka.llm import get_llm
from diplomka.models import AgentState, ChartSpec, Filters, PartialAgentState, SqlGeneration
from diplomka.retrieval import lookup_categories
from diplomka.schema import SCHEMA
from diplomka.sql import MAX_ROWS, build_schema_context

MAX_SQL_ATTEMPTS = 2


def user_input(state: AgentState) -> PartialAgentState:
    """Entry node: wraps `question` (from the initial state at invoke()) into a HumanMessage in the history."""
    return {"messages": [HumanMessage(content=state["question"])]}


def clarify_intent(state: AgentState) -> PartialAgentState:
    """LLM parses the question into `Filters` (merged with `active_filters` from before).
    Sets `intent=None` + `needs_clarification`/`clarification_question` when the query is ambiguous."""

    structured_llm = get_llm().with_structured_output(Filters)
    intent = structured_llm.invoke([SystemMessage(content=SCHEMA["system_prompt"]), *state["messages"]])
    assert isinstance(intent, Filters)

    active_filters = state.get("active_filters", Filters())
    intent.metrics = intent.metrics or active_filters.metrics

    is_unclear = not intent.has_metric()

    return {
        "intent": intent,
        "needs_clarification": is_unclear,
        "clarification_question": "Could you clarify what you mean?" if is_unclear else None,
        "attempts": state.get("attempts", 0) if is_unclear else 0,
        "sql_attempts": 0,
        "sql_error": None,
    }


def complex_query(state: AgentState) -> PartialAgentState:
    """Branch where an ambiguous reference (e.g. a category written as free text)
    must be resolved before generating SQL."""
    intent = state["intent"]
    assert intent is not None
    return {"category_query_text": intent.category_filter}


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
    """Fuzzy-matches the user's text (e.g. "beauty products") to `product_category_name`
    (73 PT values) via embeddings, result into `category_candidates`."""

    query_text = state["category_query_text"]
    assert query_text is not None
    candidates = lookup_categories(query_text, k=3)
    return {"category_candidates": candidates}


def improve_prompt(state: AgentState) -> PartialAgentState:
    """Self-check: verifies the resolved category makes sense; on a problem increments
    `attempts` and returns to clarify_intent (up to the limit), otherwise proceeds to generate_sql."""

    candidates = state["category_candidates"] or []
    candidates_have_good_score = any(score > 0.5 for _, score in candidates)

    if not candidates_have_good_score:
        if state["attempts"] >= 3:
            return {
                "needs_clarification": False,
                "clarification_question": "Sorry, I still don't understand your question.",
            }
        return {
            "attempts": state["attempts"] + 1,
            "needs_clarification": True,
            "clarification_question": "Could you clarify what you mean?",
        }

    intent = state["intent"]
    assert intent is not None
    intent = intent.model_copy(update={"category_filter": candidates[0][0]})

    return {
        "intent": intent,
        "needs_clarification": False,
        "clarification_question": None,
    }


def _intent_summary(intent: Filters) -> str:
    """Deterministic recap of the resolved Filters - used both as input for `generate_sql` and
    for the AIMessage that `clarify_intent` reads back in the next turn."""
    metrics = ", ".join(intent.metrics) if intent.metrics else "-"
    fact_agg = f"{intent.agg} {intent.fact}" if intent.fact and intent.agg else "-"
    return (
        "[PREVIOUS TURN CONTEXT - only for resolving references, DO NOT automatically copy into the new question]\n"
        f"metrics: {metrics} | fact/agg: {fact_agg} | dimension: {intent.dimension or '-'} | "
        f"granularity: {intent.granularity or 'week (default)'}\n"
        f"category_filter: {intent.category_filter or '-'} | state_filter: {intent.state_filter or '-'} | "
        f"period: {intent.date_from or '-'} to {intent.date_to or '-'} | "
        f"chart_type_request: {intent.chart_type_request or '-'}"
    )


def generate_sql(state: AgentState) -> PartialAgentState:
    """LLM writes free SQL (DuckDB dialect) grounded in the semantic schema, from the resolved
    intent; also emits its own chart hint (chart_type/x/y/y_units/title) for that same query.
    On a retry (`sql_error` set), the previous DuckDB error is fed back for a fix."""

    intent = state["intent"]
    assert intent is not None

    human = f"Resolved intent:\n{_intent_summary(intent)}\n\nWrite the SQL query."
    if state["sql_error"]:
        human += f"\n\nThe previous attempt failed with this DuckDB error - fix it:\n{state['sql_error']}"

    structured_llm = get_llm().with_structured_output(SqlGeneration)
    generation = structured_llm.invoke([SystemMessage(content=build_schema_context()), HumanMessage(content=human)])
    assert isinstance(generation, SqlGeneration)

    return {"sql_generation": generation, "sql_error": None}


def validate_sql(state: AgentState) -> PartialAgentState:
    """Checks the LLM-generated SQL is valid DuckDB (via EXPLAIN, on a read-only connection)
    before ever executing it for real. On failure, records the error for a retry in generate_sql."""

    generation = state["sql_generation"]
    assert generation is not None

    try:
        with connect(read_only=True) as conn:
            conn.execute(f"EXPLAIN {generation.sql}")
        return {"sql_error": None}
    except Exception as e:
        return {"sql_error": str(e), "sql_attempts": state["sql_attempts"] + 1}


def execute_query(state: AgentState) -> PartialAgentState:
    """Runs the LLM-generated SQL (read-only connection) against data/olist.duckdb -> columns/rows.
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


def generate_response(state: AgentState) -> PartialAgentState:
    """LLM summarizes columns/rows into a short NL answer (`answer`); `ChartSpec` is taken from
    generate_sql's chart hint, validated against the query's real result columns."""

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
    if (
        generation.chart_type is not None
        and generation.x in columns
        and generation.y
        and all(y in columns for y in generation.y)
    ):
        chart_spec = ChartSpec(
            chart_type=generation.chart_type,
            x=generation.x,
            y=generation.y,
            y_units=generation.y_units or ["value"] * len(generation.y),
            title=generation.title or ", ".join(generation.y),
        )

    preview = "\n".join(str(dict(zip(columns, row, strict=False))) for row in rows[:20])
    content = get_llm().invoke(
        f"User question: {state['question']}\n\n"
        f"Query result (columns {columns}):\n{preview}\n\n"
        "Summarize the result briefly in English (1-3 sentences), stick to the numbers "
        "from the data above, don't make anything up. "
        "Monetary amounts are in Brazilian reais (BRL, R$), never in korunas or dollars. "
        "Answer in plain text, no code, no SQL, no ``` blocks."
    ).content
    answer = content if isinstance(content, str) else str(content)

    return {
        "answer": answer,
        "chart_spec": chart_spec,
        "messages": [AIMessage(content=f"{_intent_summary(intent)}\n\nAnswer to the user: {answer}")],
    }



# Conditional routing
def route_intent(state: AgentState) -> str:
    intent = state["intent"]
    assert intent is not None
    if not intent.has_metric():
        return "unclear"
    return "complex" if intent.category_filter is not None else "basic"


def route_clarification(state: AgentState) -> str:
    if state["needs_clarification"]:
        return "user_input"
    return "proceed"


def route_sql_validation(state: AgentState) -> str:
    if state["sql_error"] is None or state["sql_attempts"] >= MAX_SQL_ATTEMPTS:
        return "proceed"
    return "retry"
