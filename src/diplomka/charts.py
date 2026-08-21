"""Plotly rendering: Chainlit-matched themes and ``build_figure`` from a ``ChartSpec``."""

import plotly.graph_objects as go
import plotly.io as pio

from diplomka.models import ChartSpec


def get_chainlit_theme(is_dark: bool = True) -> go.layout.Template:
    """Returns a Plotly layout template matched to Chainlit's UI."""
    if is_dark:
        text_color = "#F8FAFC"  # Tailwind Slate 50
        grid_color = "#1E293B"  # Tailwind Slate 800
        zero_line = "#334155"  # Tailwind Slate 700
    else:
        text_color = "#0F172A"  # Tailwind Slate 900
        grid_color = "#E2E8F0"  # Tailwind Slate 200
        zero_line = "#CBD5E1"  # Tailwind Slate 300

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


def build_figure(cs: ChartSpec, rows: list[tuple]) -> go.Figure:
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

    fig.update_layout(title=cs.title, template="chainlit_dark")
    if cs.chart_type == "bar":
        fig.update_layout(barmode="group")
    if use_secondary_axis:
        fig.update_layout(
            yaxis=dict(title=distinct_units[0]),
            yaxis2=dict(title=distinct_units[1], overlaying="y", side="right"),
        )
    return fig
