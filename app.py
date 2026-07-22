import chainlit as cl
import plotly.graph_objects as go
from graph import graph

@cl.on_message
async def on_message(message: cl.Message):
    thread = {"configurable": {"thread_id": cl.context.session.id}}
    result = await graph.ainvoke({"question": message.content}, config=thread)

    if result.get("needs_clarification"):
        await cl.Message(content=result["clarification_question"]).send()
        return

    elements = []
    if result.get("chart_spec"):
        cs = result["chart_spec"]
        x = [r[0] for r in result["rows"]]
        y = [r[1] for r in result["rows"]]
        fig = go.Figure(go.Bar(x=x, y=y) if cs.chart_type == "bar" else go.Scatter(x=x, y=y))
        fig.update_layout(title=cs.title)
        elements.append(cl.Plotly(name="chart", figure=fig))

    await cl.Message(content=result["answer"], elements=elements).send()
