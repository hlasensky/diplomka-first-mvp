import chainlit as cl
import plotly.graph_objects as go
import plotly.io as pio
from graph import graph


def get_chainlit_theme(is_dark=True):
    """Returns a Plotly layout template matched to Chainlit's UI."""
    if is_dark:
        text_color = "#F8FAFC"  # Tailwind Slate 50
        grid_color = "#1E293B"  # Tailwind Slate 800
        zero_line = "#334155"   # Tailwind Slate 700
    else:
        text_color = "#0F172A"  # Tailwind Slate 900
        grid_color = "#E2E8F0"  # Tailwind Slate 200
        zero_line = "#CBD5E1"   # Tailwind Slate 300

    return go.layout.Template(
        layout=go.Layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text_color, family="Inter, system-ui, sans-serif"),
            colorway=["#F97316", "#3B82F6", "#10B981", "#8B5CF6", "#EC4899"],
            xaxis=dict(gridcolor=grid_color, zerolinecolor=zero_line, tickcolor=grid_color),
            yaxis=dict(gridcolor=grid_color, zerolinecolor=zero_line, tickcolor=grid_color),
            hoverlabel=dict(bgcolor=grid_color, font=dict(color=text_color)),
            margin=dict(l=40, r=40, t=40, b=40),
            modebar=dict(
                bgcolor="rgba(0,0,0,0)",
                color=text_color,
                activecolor=zero_line,
                remove=["select2d", "lasso2d", "autoScale2d", "hoverCompareCartesian", "toggleSpikelines"],
            ),
        )
    )


pio.templates["chainlit_dark"] = get_chainlit_theme(is_dark=True)
pio.templates["chainlit_light"] = get_chainlit_theme(is_dark=False)


def build_figure(cs, rows: list[tuple]) -> go.Figure:
    x = [r[0] for r in rows]
    fig = go.Figure()

    if cs.chart_type == "pie":
        y = [r[1] for r in rows]
        fig.add_trace(go.Pie(labels=x, values=y))
        fig.update_layout(title=cs.title, template="chainlit_dark")
        return fig

    # metrics with different units (e.g. R$ vs. item count) go on separate Y axes,
    # so one isn't hidden due to a different scale (see the revenue+orders on one axis screenshot)
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

    layout = {"title": cs.title, "template": "chainlit_dark"}
    if cs.chart_type == "bar":
        layout["barmode"] = "group"
    if use_secondary_axis:
        layout["yaxis"] = dict(title=distinct_units[0])
        layout["yaxis2"] = dict(title=distinct_units[1], overlaying="y", side="right")
    fig.update_layout(**layout)
    return fig

STEP_LABELS = {
    "user_input": "Processing input",
    "clarify_intent": "Recognizing intent",
    "basic_query": "Building SQL (basic)",
    "complex_query": "Preparing fuzzy category search",
    "embedding_lookup": "Fuzzy category search",
    "improve_prompt": "Self-check and SQL build",
    "unclear_query": "Evaluating unclear query",
    "execute_query": "Running SQL over DuckDB",
    "generate_response": "Generating response",
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
        fig = build_figure(result["chart_spec"], result["rows"])
        elements.append(cl.Plotly(name="chart", figure=fig))

    await cl.Message(content=result["answer"], elements=elements).send()
