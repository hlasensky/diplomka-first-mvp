"""Plotly rendering: Chainlit-matched themes and ``build_figure`` from a ``ChartSpec``."""

import pandas as pd
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


def build_figure(cs: ChartSpec, columns: list[str], rows: list[tuple]) -> go.Figure:
    """Renders a `ChartSpec` (whose x/y/z name real result columns, looked up by name here -
    not assumed to be in column order) into the matching Plotly figure for its chart_type."""

    fig = go.Figure()

    if cs.chart_type == "table":
        # go.Table doesn't pick up the template's font/background - default cell fill is
        # near-white, which combined with the forced-white theme font is invisible text.
        fig.add_trace(
            go.Table(
                header=dict(values=columns, fill_color="#1E293B", font=dict(color="#F8FAFC")),
                cells=dict(
                    values=list(zip(*rows, strict=False)), fill_color="#0F172A", font=dict(color="#F8FAFC")
                ),
            )
        )
        fig.update_layout(title=cs.title, template="chainlit_dark")
        return fig

    assert cs.x is not None
    x = [r[columns.index(cs.x)] for r in rows]

    if cs.chart_type == "pie":
        y = [r[columns.index(cs.y[0])] for r in rows]
        fig.add_trace(go.Pie(labels=x, values=y))
        fig.update_layout(title=cs.title, template="chainlit_dark")
        return fig

    if cs.chart_type == "histogram":
        fig.add_trace(go.Histogram(x=x))
        fig.update_layout(title=cs.title, template="chainlit_dark")
        return fig

    if cs.chart_type == "scatter":
        y = [r[columns.index(cs.y[0])] for r in rows]
        fig.add_trace(go.Scatter(x=x, y=y, mode="markers"))
        fig.update_layout(title=cs.title, template="chainlit_dark")
        return fig

    if cs.chart_type == "box":
        y = [r[columns.index(cs.y[0])] for r in rows]
        fig.add_trace(go.Box(x=x, y=y))
        fig.update_layout(title=cs.title, template="chainlit_dark")
        return fig

    if cs.chart_type == "heatmap":
        assert cs.z is not None
        df = pd.DataFrame(rows, columns=columns)
        pivot = df.pivot_table(index=cs.y[0], columns=cs.x, values=cs.z, aggfunc="sum")
        fig.add_trace(go.Heatmap(z=pivot.to_numpy(), x=pivot.columns, y=pivot.index, colorbar=dict(title=cs.z)))
        fig.update_layout(title=cs.title, template="chainlit_dark")
        return fig

    # bar / stacked_bar / line / area - one or more y metrics against the same x
    # metrics with different units (e.g. R$ vs. item count) go on separate Y axes,
    # so one isn't hidden due to a different scale (see the revenue+orders on one axis screenshot)
    distinct_units = list(dict.fromkeys(cs.y_units))
    use_secondary_axis = len(distinct_units) == 2

    for i, y_col in enumerate(cs.y):
        y = [r[columns.index(y_col)] for r in rows]
        on_secondary = use_secondary_axis and cs.y_units[i] == distinct_units[1]
        trace_kwargs = {"name": y_col, "yaxis": "y2" if on_secondary else "y"}
        if cs.chart_type == "line":
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines", **trace_kwargs))
        elif cs.chart_type == "area":
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines", fill="tozeroy", **trace_kwargs))
        else:
            fig.add_trace(go.Bar(x=x, y=y, **trace_kwargs))

    fig.update_layout(title=cs.title, template="chainlit_dark")
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
