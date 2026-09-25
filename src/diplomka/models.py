"""Pydantic/TypedDict data models: parsed intent (``Filters``), ``ChartSpec``, graph state.

``metrics``/``measures``/``group_by``/``filters`` are validated dynamically against the active
dataset's semantic layer (``diplomka.schema.LAYER``), so switching datasets or adding a
metric/measure/level only requires editing the YAML, not this module.
"""

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.json_schema import SkipJsonSchema

from diplomka.schema import LAYER, get_domains

# Replacement for an aggregation the semantic layer does not allow for a measure (e.g. SUM of
# a temperature): the first of these that the measure allows.
FALLBACK_AGGS = ("avg", "sum", "max", "min")

ChartType = Literal["bar", "stacked_bar", "line", "area", "pie", "scatter", "histogram", "box", "heatmap", "table"]


def _level_of_value(value: str) -> str | None:
    """The only level whose domain contains ``value`` - repairs filters where the LLM named the
    dimension ("event") or a synonym instead of the level ("event_type"). None if ambiguous."""
    try:
        domains = get_domains()
    except Exception:  # database not built yet - nothing to repair against
        return None
    matches = [level for level, values in domains.items() if value in values]
    return matches[0] if len(matches) == 1 else None


class MeasureAgg(BaseModel):
    """A generic (unnamed) metric: one aggregation function over one measure of the semantic layer."""

    measure: str = Field(description="Measure id from the semantic layer.")
    agg: str = Field(description="Aggregation function; must be one of the measure's allowed aggregations.")

    @field_validator("agg")
    @classmethod
    def normalize_agg(cls, v: str) -> str:
        return v.strip().lower()


class LevelFilter(BaseModel):
    """Equality filter on a dimension level, e.g. level=event_type, value=swarming."""

    level: str = Field(description="Dimension level name from the semantic layer.")
    value: str = Field(description="Value of that level, as written in the data if known.")


class Filters(BaseModel):
    metrics: list[str] = Field(default_factory=list, description="Named metrics from the semantic layer.")
    measures: list[MeasureAgg] = Field(
        default_factory=list, description="Measure + aggregation pairs, used when no named metric fits."
    )
    group_by: list[str] = Field(
        default_factory=list, description="Dimension level names to break the result down by; empty = one total."
    )
    filters: list[LevelFilter] = Field(default_factory=list)
    date_from: str | None = Field(default=None, description="YYYY-MM-DD")
    date_to: str | None = Field(default=None, description="YYYY-MM-DD")
    # explicit user request for chart type (only when mentioned in the question), otherwise computed automatically
    chart_type_request: ChartType | None = None

    # What validation changed or ignored in the LLM's output, in plain words. Hidden from the
    # LLM's tool schema; used to explain the answer and to make clarification questions specific.
    adjustments: SkipJsonSchema[list[str]] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_against_layer(self) -> "Filters":
        """Keep the intent within the semantic layer: repair what can be repaired (a column name
        used as a measure, a disallowed aggregation), drop only unknown names - and note both."""
        notes = []

        metrics = [m for m in self.metrics if m in LAYER.metrics]
        notes += [f"'{m}' is not a known metric" for m in self.metrics if m not in LAYER.metrics]

        measures = []
        for m in self.measures:
            measure = LAYER.measures.get(m.measure) or LAYER.measures_by_column.get(m.measure)
            if measure is None:
                notes.append(f"'{m.measure}' is not a known measure")
                continue
            agg = m.agg
            if agg not in measure.allowed_aggs:
                agg = next((a for a in FALLBACK_AGGS if a in measure.allowed_aggs), sorted(measure.allowed_aggs)[0])
                notes.append(
                    f"{m.agg.upper()} is not meaningful for {measure.label}; used {agg.upper()} instead "
                    f"(allowed: {', '.join(sorted(measure.allowed_aggs))})"
                )
            if all((x.measure, x.agg) != (measure.measure_id, agg) for x in measures):
                measures.append(MeasureAgg(measure=measure.measure_id, agg=agg))

        group_by = [level for level in self.group_by if level in LAYER.levels]
        notes += [f"'{level}' is not a known breakdown" for level in self.group_by if level not in LAYER.levels]
        filters = []
        for f in self.filters:
            level = f.level if f.level in LAYER.levels else _level_of_value(f.value)
            if level is None:
                notes.append(f"'{f.level}' is not a known filter")
            elif level != f.level:
                notes.append(f"filter '{f.level} = {f.value}' read as {LAYER.levels[level].label} = {f.value}")
                filters.append(LevelFilter(level=level, value=f.value))
            else:
                filters.append(f)

        # assign via __dict__ - plain attribute assignment would re-run this validator
        self.__dict__.update(metrics=metrics, measures=measures, group_by=group_by, filters=filters)
        self.__dict__["adjustments"] = list(dict.fromkeys([*self.adjustments, *notes]))
        return self

    def has_metric(self) -> bool:
        return bool(self.metrics) or bool(self.measures)


class ChartSpec(BaseModel):
    """x/y/z meaning depends on chart_type:
    - bar/stacked_bar/line/area: x = category or time; y = 1+ metric columns
    - pie/histogram/box/scatter: x = labels/numeric/category/numeric; y = 0 or 1 value column
      (histogram needs none, the rest need exactly one)
    - heatmap: x, y = the two dimension columns; z = the value/color column
    - table: none of x/y/z used - render the raw result as-is
    """

    chart_type: ChartType
    x: str | None = None
    y: list[str] = Field(default_factory=list)
    y_units: list[str] = Field(default_factory=list)
    z: str | None = None
    title: str = ""


class SqlGeneration(BaseModel):
    """LLM-generated SQL plus its own read on how to chart the result (same reasoning, one call)."""

    sql: str
    chart_type: ChartType | None = None
    x: str | None = Field(
        default=None,
        description="X-axis/category column alias. Required whenever chart_type is set (including "
        "pie, where it's the slice-label column) except histogram/table.",
    )
    y: list[str] = Field(
        default_factory=list,
        description="Y-axis metric column alias(es). Required whenever chart_type is set "
        "(including pie, where it's the single slice-value column) except histogram/table.",
    )
    y_units: list[str] = Field(default_factory=list)
    z: str | None = None
    title: str = ""

    @field_validator("y", "y_units", mode="before")
    @classmethod
    def _coerce_scalar_to_list(cls, v: object) -> object:
        """Weaker models occasionally emit a bare string instead of a single-item list here."""
        return [v] if isinstance(v, str) else v


class ChartCritique(BaseModel):
    """LLM's second opinion on a chosen `ChartSpec`, used by `validate_chart_spec`."""

    ok: bool
    issue: str = ""


class AgentState(TypedDict):
    # persistent - survives across turns (thanks to the checkpointer)
    messages: Annotated[list[BaseMessage], add_messages]
    active_filters: Filters
    attempts: int

    # per-turn scratch
    question: str
    unresolved_filters: list[LevelFilter]
    filter_candidates: list[list[tuple[str, float]]]
    intent: Filters | None
    sql_generation: SqlGeneration | None
    sql_error: str | None
    sql_attempts: int
    semantic_violations: list[str]
    validation_error: str | None
    needs_clarification: bool
    clarification_question: str | None
    columns: list[str]
    rows: list[tuple]

    # output
    chart_spec: ChartSpec | None
    chart_validation_error: str | None
    chart_attempts: int
    answer: str


class GraphInput(TypedDict):
    """What a caller must supply to `graph.invoke()` - everything else in `AgentState` is
    per-turn scratch or defaulted by the nodes themselves."""

    question: str


class PartialAgentState(TypedDict, total=False):
    """Same fields as `AgentState`, all optional - what a LangGraph node actually returns (a partial update)."""

    messages: Annotated[list[BaseMessage], add_messages]
    active_filters: Filters
    attempts: int
    question: str
    unresolved_filters: list[LevelFilter]
    filter_candidates: list[list[tuple[str, float]]]
    intent: Filters | None
    sql_generation: SqlGeneration | None
    sql_error: str | None
    sql_attempts: int
    semantic_violations: list[str]
    validation_error: str | None
    needs_clarification: bool
    clarification_question: str | None
    columns: list[str]
    rows: list[tuple]
    chart_spec: ChartSpec | None
    chart_validation_error: str | None
    chart_attempts: int
    answer: str
