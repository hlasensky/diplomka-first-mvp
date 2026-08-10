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
    chart_type_request: Literal["bar", "line", "pie"] | None = None

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

    def resolve_metrics(self) -> list[dict]:
        """Return a list of {sql, alias, label, additive, unit} for all chosen metrics (named as well as fact+agg)."""
        resolved = [
            {
                "sql": SCHEMA["metrics"][m]["sql"],
                "alias": m,
                "label": SCHEMA["metrics"][m]["label"],
                "additive": SCHEMA["metrics"][m].get("additive", False),
                "unit": SCHEMA["metrics"][m].get("unit", "value"),
            }
            for m in self.metrics
        ]
        if self.fact is not None and self.agg is not None:
            alias = f"{self.agg}_{self.fact}"
            resolved.append(
                {
                    "sql": f"{self.agg.upper()}({self.fact})",
                    "alias": alias,
                    "label": f"{self.agg.upper()} {self.fact}",
                    "additive": self.agg == "sum",
                    "unit": SCHEMA.get("facts", {}).get(self.fact, {}).get("unit", "value"),
                }
            )
        if not resolved:
            raise ValueError("Filters has no metric nor a valid `fact`+`agg` pair")
        return resolved


class ChartSpec(BaseModel):
    chart_type: Literal["bar", "line", "pie"]
    x: str
    y: list[str]
    y_units: list[str]
    title: str


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
    sql: str | None
    params: list | None
    validation_error: str | None
    needs_clarification: bool
    clarification_question: str | None
    columns: list[str]
    rows: list[tuple]

    # output
    chart_spec: ChartSpec | None
    answer: str
