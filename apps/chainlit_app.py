"""Chainlit UI entry point. Run with: uv run chainlit run apps/chainlit_app.py -w"""

import time

import chainlit as cl
from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain_core.runnables import RunnableConfig

from diplomka.charts import build_figure
from diplomka.graph import get_graph

graph = get_graph()

STEP_LABELS = {
    "user_input": "Processing input",
    "clarify_intent": "Recognizing intent",
    "complex_query": "Preparing fuzzy category search",
    "embedding_lookup": "Fuzzy category search",
    "improve_prompt": "Resolving category match",
    "generate_sql": "Generating SQL",
    "validate_sql": "Validating SQL",
    "unclear_query": "Evaluating unclear query",
    "execute_query": "Running SQL over DuckDB",
    "generate_response": "Generating response",
    "validate_chart_spec": "Reviewing chart choice",
}

def get_starters() -> list[cl.Starter]:
    return [
        cl.Starter(
            label="Revenue by category",
            message="What is the total revenue by category?",
        ),
        cl.Starter(
            label="Fuzzy category search",
            message="How much did we earn on beauty and health by month?",
        ),
        cl.Starter(
            label="Multiple metrics at once",
            message="Show me revenue and order count by category",
        ),
        cl.Starter(
            label="Generic fact+agg metric",
            message="What is the average freight cost by state?",
        ),
    ]

@cl.set_starters
async def set_starters(get_starters) -> list[cl.Starter]:
    return get_starters()


async def _send_usage_step(usage_cb: UsageMetadataCallbackHandler, elapsed: float, sql: str | None) -> None:
    """Native Chainlit Step (collapsible, consistent with the pipeline trace steps above it) -
    elapsed time, per-model token usage, the SQL that ran."""

    total_tokens = sum(u["total_tokens"] for u in usage_cb.usage_metadata.values())
    lines = [f"{elapsed:.1f}s" + (f" - {total_tokens} tokens" if total_tokens else "")]
    for model, u in usage_cb.usage_metadata.items():
        lines.append(f"- `{model}`: {u['input_tokens']} in / {u['output_tokens']} out ({u['total_tokens']} total)")
    if sql:
        lines.append(f"\n```sql\n{sql.strip()}\n```")

    async with cl.Step(name="Usage & SQL", type="tool") as step:
        step.output = "\n".join(lines)


@cl.on_message
async def on_message(message: cl.Message):
    thread: RunnableConfig = {"configurable": {"thread_id": cl.context.session.id}}
    usage_cb = UsageMetadataCallbackHandler()
    config: RunnableConfig = {**thread, "callbacks": [usage_cb]}
    start = time.monotonic()

    async for update in graph.astream({"question": message.content}, config=config, stream_mode="updates"):
        for node_name, node_output in update.items():
            async with cl.Step(name=STEP_LABELS.get(node_name, node_name), type="tool") as step:
                step.output = "\n".join(f"{k}: {v}" for k, v in node_output.items())

    elapsed = time.monotonic() - start
    result = (await graph.aget_state(thread)).values

    if result.get("needs_clarification"):
        await cl.Message(content=result["clarification_question"]).send()
        return

    elements = []
    if result.get("chart_spec"):
        fig = build_figure(result["chart_spec"], result["columns"], result["rows"])
        elements.append(cl.Plotly(name="chart", figure=fig))

    sql_generation = result.get("sql_generation")
    await _send_usage_step(usage_cb, elapsed, sql_generation.sql if sql_generation else None)

    await cl.Message(content=result["answer"], elements=elements).send()
