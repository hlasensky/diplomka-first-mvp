"""LangGraph node functions and conditional routing for the analytics agent."""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from diplomka.db import connect
from diplomka.llm import get_llm
from diplomka.models import AgentState, ChartSpec, Filters
from diplomka.retrieval import lookup_categories
from diplomka.schema import SCHEMA
from diplomka.sql import build_sql


def user_input(state: AgentState) -> AgentState:
    """Entry node: wraps `question` (from the initial state at invoke()) into a HumanMessage in the history."""
    return {"messages": [HumanMessage(content=state["question"])]}


def clarify_intent(state: AgentState) -> AgentState:
    """LLM parses the question into `Filters` (merged with `active_filters` from before).
    Sets `intent=None` + `needs_clarification`/`clarification_question` when the query is ambiguous."""

    structured_llm = get_llm().with_structured_output(Filters)
    intent = structured_llm.invoke([SystemMessage(content=SCHEMA["system_prompt"]), *state["messages"]])

    active_filters = state.get("active_filters", Filters())
    intent.metrics = intent.metrics or active_filters.metrics

    is_unclear = not intent.has_metric()

    return {
        "intent": intent,
        "needs_clarification": is_unclear,
        "clarification_question": "Could you clarify what you mean?" if is_unclear else None,
        "attempts": state.get("attempts", 0) if is_unclear else 0,
    }


def basic_query(state: AgentState) -> AgentState:
    """Simple branch: metric (+dimension) is clear, no fuzzy lookup needed;
    goes straight to execute_query."""

    sql, params = build_sql(state["intent"])

    return {"sql": sql, "params": params, "needs_clarification": False, "clarification_question": None}


def complex_query(state: AgentState) -> AgentState:
    """Branch where an ambiguous reference (e.g. a category written as free text)
    must be resolved before building SQL."""
    return {"category_query_text": state["intent"].category_filter}


def unclear_query(state: AgentState) -> AgentState:
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


def embedding_lookup(state: AgentState) -> AgentState:
    """Fuzzy-matches the user's text (e.g. "beauty products") to `product_category_name`
    (73 PT values) via embeddings, result into `category_candidates`."""

    candidates = lookup_categories(state["category_query_text"], k=3)
    return {"category_candidates": candidates}


def improve_prompt(state: AgentState) -> AgentState:
    """Self-check: verifies the resolved intent/SQL makes sense; on a problem increments
    `attempts` and returns to clarify_intent (up to the limit), otherwise proceeds to execute_query."""

    candidates_have_good_score = any(score > 0.5 for _, score in state["category_candidates"] or [])

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

    intent = state["intent"].model_copy(update={"category_filter": state["category_candidates"][0][0]})

    sql, params = build_sql(intent)

    return {
        "intent": intent,
        "sql": sql,
        "params": params,
        "needs_clarification": False,
        "clarification_question": None,
    }


def execute_query(state: AgentState) -> AgentState:
    """Builds parametrized SQL from `intent`/`active_filters` and schema/semantic_schema.yaml
    and runs it against data/olist.duckdb -> columns/rows."""

    sql = state["sql"]
    params = state["params"]

    columns, rows = [], []
    error = None
    with connect() as conn:
        try:
            result = conn.execute(sql, params).fetchall()
            columns = [desc[0] for desc in conn.description]
            rows = result
        except Exception as e:
            error = str(e)

    return {
        "columns": columns,
        "rows": rows,
        "needs_clarification": False,
        "clarification_question": None,
        "validation_error": error,
        "active_filters": state["intent"],
    }


def _intent_summary(intent: Filters) -> str:
    """Deterministic recap of the resolved Filters for AIMessage - input for clarify_intent in the next turn."""
    metrics = ", ".join(intent.metrics) if intent.metrics else "-"
    fact_agg = f"{intent.agg} {intent.fact}" if intent.fact and intent.agg else "-"
    return (
        "[PREVIOUS TURN CONTEXT - only for resolving references, DO NOT automatically copy into the new question]\n"
        f"metrics: {metrics} | fact/agg: {fact_agg} | dimension: {intent.dimension or '-'}\n"
        f"category_filter: {intent.category_filter or '-'} | state_filter: {intent.state_filter or '-'} | "
        f"period: {intent.date_from or '-'} to {intent.date_to or '-'}"
    )


def generate_response(state: AgentState) -> AgentState:
    """LLM summarizes columns/rows into a short NL answer (`answer`); `ChartSpec` is derived
    deterministically from the intent/columns."""

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

    chart_spec = None
    if intent.dimension is not None and len(columns) >= 2:
        metrics = intent.resolve_metrics()
        y_cols = columns[1:]

        if intent.chart_type_request is not None:
            chart_type = intent.chart_type_request
        elif intent.dimension == "time":
            chart_type = "line"
        elif len(metrics) == 1 and metrics[0]["additive"] and len(rows) <= 8:
            chart_type = "pie"
        else:
            chart_type = "bar"

        title = metrics[0]["label"] if len(metrics) == 1 else ", ".join(m["label"] for m in metrics)
        y_units = [m["unit"] for m in metrics]
        chart_spec = ChartSpec(chart_type=chart_type, x=columns[0], y=y_cols, y_units=y_units, title=title)

    preview = "\n".join(str(dict(zip(columns, row, strict=False))) for row in rows[:20])
    answer = (
        get_llm()
        .invoke(
            f"User question: {state['question']}\n\n"
            f"Query result (columns {columns}):\n{preview}\n\n"
            "Summarize the result briefly in English (1-3 sentences), stick to the numbers "
            "from the data above, don't make anything up. "
            "Monetary amounts are in Brazilian reais (BRL, R$), never in korunas or dollars. "
            "Answer in plain text, no code, no SQL, no ``` blocks."
        )
        .content
    )

    return {
        "answer": answer,
        "chart_spec": chart_spec,
        "messages": [AIMessage(content=f"{_intent_summary(intent)}\n\nAnswer to the user: {answer}")],
    }


# Conditional routing
def route_intent(state: AgentState) -> str:
    if not state["intent"].has_metric():
        return "unclear"
    return "complex" if state["intent"].category_filter is not None else "basic"


def route_clarification(state: AgentState) -> str:
    if state["needs_clarification"]:
        return "user_input"
    return "execute_query"
