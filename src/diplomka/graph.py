"""LangGraph assembly: wires the nodes into the compiled agent graph."""

from functools import lru_cache

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from diplomka.models import AgentState, GraphInput
from diplomka.nodes import (
    clarify_intent,
    complex_query,
    embedding_lookup,
    execute_query,
    generate_response,
    generate_sql,
    improve_prompt,
    route_clarification,
    route_intent,
    route_sql_validation,
    route_validate_chart_spec,
    unclear_query,
    user_input,
    validate_chart_spec,
    validate_sql,
)


def _build_workflow() -> StateGraph[AgentState, None, GraphInput, AgentState]:
    workflow = StateGraph(AgentState, input_schema=GraphInput)
    workflow.add_node("user_input", user_input)
    workflow.add_node("clarify_intent", clarify_intent)
    workflow.add_node("complex_query", complex_query)
    workflow.add_node("unclear_query", unclear_query)
    workflow.add_node("embedding_lookup", embedding_lookup)
    workflow.add_node("improve_prompt", improve_prompt)
    workflow.add_node("generate_sql", generate_sql)
    workflow.add_node("validate_sql", validate_sql)
    workflow.add_node("execute_query", execute_query)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("validate_chart_spec", validate_chart_spec)

    workflow.add_edge(START, "user_input")
    workflow.add_edge("user_input", "clarify_intent")
    workflow.add_conditional_edges(
        "clarify_intent",
        route_intent,
        {
            "basic": "generate_sql",
            "complex": "complex_query",
            "unclear": "unclear_query",
        },
    )

    workflow.add_edge("complex_query", "embedding_lookup")
    workflow.add_edge("embedding_lookup", "improve_prompt")
    workflow.add_conditional_edges(
        "improve_prompt",
        route_clarification,
        {
            "user_input": "clarify_intent",  # user_input would only re-add an identical HumanMessage, changes nothing
            "proceed": "generate_sql",
        },
    )

    workflow.add_edge("unclear_query", END)

    workflow.add_edge("generate_sql", "validate_sql")
    workflow.add_conditional_edges(
        "validate_sql",
        route_sql_validation,
        {
            "proceed": "execute_query",
            "retry": "generate_sql",  # DuckDB EXPLAIN error is fed back into the next generate_sql call
        },
    )

    workflow.add_edge("execute_query", "generate_response")
    workflow.add_edge("generate_response", "validate_chart_spec")
    workflow.add_conditional_edges(
        "validate_chart_spec",
        route_validate_chart_spec,
        {
            "proceed": END,
            "retry": "generate_sql",  # chart critique is fed back into the next generate_sql call
        },
    )
    return workflow


@lru_cache(maxsize=1)
def get_graph() -> CompiledStateGraph[AgentState, None, GraphInput, AgentState]:
    """Compile (once) and return the agent graph with an in-memory checkpointer."""
    checkpointer = InMemorySaver(
        serde=JsonPlusSerializer(
            allowed_msgpack_modules=[
                ("diplomka.models", "Filters"),
                ("diplomka.models", "MeasureAgg"),
                ("diplomka.models", "LevelFilter"),
                ("diplomka.models", "ChartSpec"),
                ("diplomka.models", "SqlGeneration"),
            ]
        )
    )
    return _build_workflow().compile(checkpointer=checkpointer)
