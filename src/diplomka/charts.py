"""Plotly rendering: a Chainlit-matched dark theme and ``build_figure`` from a ``ChartSpec``."""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

from diplomka.models import ChartSpec

TEXT_COLOR = "#F8FAFC"  # Tailwind Slate 50
GRID_COLOR = "#1E293B"  # Tailwind Slate 800
ZERO_LINE = "#334155"  # Tailwind Slate 700

pio.templates["chainlit_dark"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_COLOR, family="Inter, system-ui, sans-serif"),
        colorway=["#F97316", "#3B82F6", "#10B981", "#8B5CF6", "#EC4899"],
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=ZERO_LINE, tickcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=ZERO_LINE, tickcolor=GRID_COLOR),
        hoverlabel=dict(bgcolor=GRID_COLOR, font=dict(color=TEXT_COLOR)),
        margin=dict(l=40, r=40, t=40, b=40),
        modebar=dict(
            bgcolor="rgba(0,0,0,0)",
            color=TEXT_COLOR,
            activecolor=ZERO_LINE,
            remove=["select2d", "lasso2d", "autoScale2d", "hoverCompareCartesian", "toggleSpikelines"],
        ),
    )
)


def build_figure(cs: ChartSpec, columns: list[str], rows: list[tuple]) -> go.Figure:
    """Renders a `ChartSpec` (whose x/y/z name real result columns, looked up by name here -
    not assumed to be in column order) into the matching Plotly figure for its chart_type."""

    def col(name: str) -> list:
        return [r[columns.index(name)] for r in rows]

    fig = go.Figure()
    fig.update_layout(title=cs.title, template="chainlit_dark")

    if cs.chart_type == "table":
        # go.Table doesn't pick up the template's font/background - default cell fill is
        # near-white, which combined with the forced-white theme font is invisible text.
        fig.add_trace(
            go.Table(
                header=dict(values=columns, fill_color=GRID_COLOR, font=dict(color=TEXT_COLOR)),
                cells=dict(values=list(zip(*rows, strict=False)), fill_color="#0F172A", font=dict(color=TEXT_COLOR)),
            )
        )
        return fig

    assert cs.x is not None
    x = col(cs.x)

    if cs.chart_type == "pie":
        return fig.add_trace(go.Pie(labels=x, values=col(cs.y[0])))
    if cs.chart_type == "histogram":
        return fig.add_trace(go.Histogram(x=x))
    if cs.chart_type == "scatter":
        return fig.add_trace(go.Scatter(x=x, y=col(cs.y[0]), mode="markers"))
    if cs.chart_type == "box":
        return fig.add_trace(go.Box(x=x, y=col(cs.y[0])))
    if cs.chart_type == "heatmap":
        assert cs.z is not None
        pivot = pd.DataFrame(rows, columns=columns).pivot_table(index=cs.y[0], columns=cs.x, values=cs.z, aggfunc="sum")
        return fig.add_trace(go.Heatmap(z=pivot.to_numpy(), x=pivot.columns, y=pivot.index, colorbar=dict(title=cs.z)))

    # bar / stacked_bar / line / area - one or more y metrics against the same x.
    # Metrics with two different units go on separate y axes, so the smaller scale stays visible.
    distinct_units = list(dict.fromkeys(cs.y_units))
    use_secondary_axis = len(distinct_units) == 2

    for i, y_col in enumerate(cs.y):
        on_secondary = use_secondary_axis and cs.y_units[i] == distinct_units[1]
        trace_kwargs = {"x": x, "y": col(y_col), "name": y_col, "yaxis": "y2" if on_secondary else "y"}
        if cs.chart_type == "line":
            fig.add_trace(go.Scatter(mode="lines", **trace_kwargs))
        elif cs.chart_type == "area":
            fig.add_trace(go.Scatter(mode="lines", fill="tozeroy", **trace_kwargs))
        else:
            fig.add_trace(go.Bar(**trace_kwargs))

    if cs.chart_type == "bar":
        fig.update_layout(barmode="group")
    elif cs.chart_type == "stacked_bar":
        fig.update_layout(barmode="stack")
    if use_secondary_axis:
        fig.update_layout(
            yaxis=dict(title=distinct_units[0]),
            yaxis2=dict(title=distinct_units[1], overlaying="y", side="right"),
        )
    return fig
