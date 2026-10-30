"""Executor: check -> plan -> compile -> run, with provenance of every result.

Provenance is what makes a number in the answer verifiable: the cube query, the generated SQL, the
tables read and the assumptions the planner made. Every claim the LLM makes must point to one
``Result`` (see ``insight.claims``). The DuckDB connection is read-only with external access disabled,
as in ``diplomka.nodes``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from diplomka.engine.checks import Issue
from diplomka.engine.planner import Plan
from diplomka.engine.query import CubeQuery
from diplomka.schema import SemanticLayer


@dataclass(frozen=True)
class Provenance:
    query: CubeQuery
    sql: str
    tables: tuple[str, ...]
    notes: tuple[str, ...]  # planner assumptions + resolved ambiguities, to be said in the answer
    executed_at: datetime


@dataclass(frozen=True)
class Result:
    columns: tuple[str, ...]
    rows: tuple[tuple[object, ...], ...]
    provenance: Provenance
    truncated: bool = False  # more rows than ``MAX_ROWS``
    issues: tuple[Issue, ...] = field(default=())  # ambiguities resolved by default


class QueryError(Exception):
    """The query has errors (``issues``) and was not run."""

    def __init__(self, issues: list[Issue]) -> None:
        super().__init__("; ".join(i.message for i in issues))
        self.issues = issues


def prepare(
    query: CubeQuery, layer: SemanticLayer, domains: dict[str, set[str]]
) -> tuple[CubeQuery, Plan, str, list[Issue]]:
    """Checks, aggregation defaults, plan and SQL without running anything (dry run, EXPLAIN, tests)."""
    raise NotImplementedError


def run(query: CubeQuery, layer: SemanticLayer, domains: dict[str, set[str]], max_rows: int) -> Result:
    """Prepare and execute; raise ``QueryError`` when ``check_query`` returns errors."""
    raise NotImplementedError
