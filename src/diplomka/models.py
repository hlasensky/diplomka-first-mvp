"""Pydantic/TypedDict data models: parsed intent (``Filters``), ``ChartSpec``, graph state.

``metrics``/``dimension``/``granularity``/``fact``/``agg`` are validated dynamically against
schema/semantic_schema.yaml, so adding a new metric/dimension/fact only requires editing the
YAML, not this module.
"""

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field, field_validator, model_validator

from diplomka.schema import SCHEMA

ChartType = Literal["bar", "stacked_bar", "line", "area", "pie", "scatter", "histogram", "box", "heatmap", "table"]


class Filters(BaseModel):
    metrics: list[str] = Field(default_factory=list)
    # generic (unnamed) metric: aggregation function over any fact from SCHEMA["facts"]
    fact: str | None = None
    agg: str | None = None
    dimension: str | None = None
    granularity: str | None = None
    category_filter: str | None = None
    state_filter: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    # explicit user request for chart type (only when mentioned in the question), otherwise computed automatically
    chart_type_request: ChartType | None = None

    @field_validator("metrics")
    @classmethod
    def validate_metrics(cls, v: list[str]) -> list[str]:
        return [m for m in v if m in SCHEMA["metrics"]]

    @field_validator("fact")
    @classmethod
    def validate_fact(cls, v: str | None) -> str | None:
        return v if v in SCHEMA.get("facts", {}) else None

    @field_validator("agg")
    @classmethod
    def validate_agg(cls, v: str | None) -> str | None:
        return v if v in {"sum", "avg", "min", "max"} else None

    @model_validator(mode="after")
    def validate_fact_agg_pair(self) -> "Filters":
        if self.fact is not None and self.agg is not None:
            allowed = SCHEMA.get("facts", {}).get(self.fact, {}).get("agg", [])
            if self.agg not in allowed:
                self.fact = None
                self.agg = None
        return self

    @field_validator("dimension")
    @classmethod
    def validate_dimension(cls, v: str | None) -> str | None:
        return v if v in SCHEMA["dimensions"] else None

    @field_validator("granularity")
    @classmethod
    def validate_granularity(cls, v: str | None) -> str | None:
        valid = SCHEMA["dimensions"].get("time", {}).get("granularities", [])
        return v if v in valid else None

    def has_metric(self) -> bool:
        return bool(self.metrics) or (self.fact is not None and self.agg is not None)


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
    x: str | None = None
    y: list[str] = Field(default_factory=list)
    y_units: list[str] = Field(default_factory=list)
    z: str | None = None
    title: str = ""


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
    category_query_text: str | None
    category_candidates: list[tuple[str, float]] | None
    intent: Filters | None
    sql_generation: SqlGeneration | None
    sql_error: str | None
    sql_attempts: int
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
    category_query_text: str | None
    category_candidates: list[tuple[str, float]] | None
    intent: Filters | None
    sql_generation: SqlGeneration | None
    sql_error: str | None
    sql_attempts: int
    validation_error: str | None
    needs_clarification: bool
    clarification_question: str | None
    columns: list[str]
    rows: list[tuple]
    chart_spec: ChartSpec | None
    chart_validation_error: str | None
    chart_attempts: int
    answer: str
