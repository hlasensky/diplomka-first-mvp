"""Chainlit UI entry point. Run with: uv run chainlit run apps/chainlit_app.py -w"""

import chainlit as cl

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


@cl.set_starters
async def set_starters():
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


@cl.on_message
async def on_message(message: cl.Message):
    thread = {"configurable": {"thread_id": cl.context.session.id}}

    async for update in graph.astream({"question": message.content}, config=thread, stream_mode="updates"):
        for node_name, node_output in update.items():
            async with cl.Step(name=STEP_LABELS.get(node_name, node_name), type="tool") as step:
                step.output = "\n".join(f"{k}: {v}" for k, v in node_output.items())

    result = (await graph.aget_state(thread)).values

    if result.get("needs_clarification"):
        await cl.Message(content=result["clarification_question"]).send()
        return

    elements = []
    if result.get("chart_spec"):
        fig = build_figure(result["chart_spec"], result["columns"], result["rows"])
        elements.append(cl.Plotly(name="chart", figure=fig))

    await cl.Message(content=result["answer"], elements=elements).send()
