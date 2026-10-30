"""Proactive scan: after every answer the system itself looks for anomalies around the current query.

"Around" (docs/decisions.md 2026-10-05, point 4): under the current slice (drill-down children) and next
to it (siblings on the same level, the same period last year). Discovery-driven exploration motivates
this: anomalies may not show at higher aggregation levels because exceptions cancel out or are hidden
by the volume of aggregated data [sarawagiDiscoverydrivenExplorationOLAP1998 C1], and InExp / PathExp
say where and in which direction to drill [C5].

Runs deterministically and within a time budget; the LLM only words the selected insights.
"""

from __future__ import annotations

from diplomka.engine.insight.ranking import Insight
from diplomka.engine.query import CubeQuery
from diplomka.engine.session import Session
from diplomka.schema import SemanticLayer


def neighbourhood(query: CubeQuery, layer: SemanticLayer) -> list[CubeQuery]:
    """Queries to scan: drill-down children of the current slice and its siblings / previous period."""
    raise NotImplementedError


def scan(session: Session, layer: SemanticLayer, time_budget_s: float = 5.0) -> list[Insight]:
    """Run ``exceptions``, ``series`` and ``diff`` on the neighbourhood of ``session.current``; return
    candidates for ``ranking.select``. Stops when the time budget runs out."""
    raise NotImplementedError
