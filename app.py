import chainlit as cl
import plotly.graph_objects as go
from graph import graph


def build_figure(cs, rows: list[tuple]) -> go.Figure:
    x = [r[0] for r in rows]
    fig = go.Figure()

    if cs.chart_type == "pie":
        y = [r[1] for r in rows]
        fig.add_trace(go.Pie(labels=x, values=y))
        fig.update_layout(title=cs.title)
        return fig

    # metriky s různou jednotkou (např. R$ vs. počet kusů) jdou na samostatné osy Y,
    # ať se jedna neschová kvůli jinému měřítku (viz screenshot revenue+orders na jedné ose)
    distinct_units = list(dict.fromkeys(cs.y_units))
    use_secondary_axis = len(distinct_units) == 2

    for i, y_col in enumerate(cs.y, start=1):
        y = [r[i] for r in rows]
        on_secondary = use_secondary_axis and cs.y_units[i - 1] == distinct_units[1]
        trace_kwargs = {"name": y_col, "yaxis": "y2" if on_secondary else "y"}
        if cs.chart_type == "line":
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines", **trace_kwargs))
        else:
            fig.add_trace(go.Bar(x=x, y=y, **trace_kwargs))

    layout = {"title": cs.title}
    if cs.chart_type == "bar":
        layout["barmode"] = "group"
    if use_secondary_axis:
        layout["yaxis"] = dict(title=distinct_units[0])
        layout["yaxis2"] = dict(title=distinct_units[1], overlaying="y", side="right")
    fig.update_layout(**layout)
    return fig

STEP_LABELS = {
    "user_input": "Zpracování vstupu",
    "clarify_intent": "Rozpoznávání záměru",
    "basic_query": "Sestavení SQL (basic)",
    "complex_query": "Příprava fuzzy vyhledávání kategorie",
    "embedding_lookup": "Fuzzy vyhledávání kategorie",
    "improve_prompt": "Self-check a sestavení SQL",
    "unclear_query": "Vyhodnocení nejasného dotazu",
    "execute_query": "Spuštění SQL nad DuckDB",
    "generate_response": "Generování odpovědi",
}


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
        fig = build_figure(result["chart_spec"], result["rows"])
        elements.append(cl.Plotly(name="chart", figure=fig))

    await cl.Message(content=result["answer"], elements=elements).send()
