"""Interestingness and the choice of what to report (at most 1-2 insights per answer, docs/decisions.md).

- Subjective interestingness: the previous cube stands for the user's belief; the surprise of a cell is
  the difference between its significance and the significance of its counterpart in the previous cube;
  surprise is aggregated per component and per model, and the component with the maximum becomes the
  highlight [vassiliadisRollUpsDrillDownsIntentional2019 C4, candidate].
- Selection under a budget: every insight has interest, coverage and cost (number of words); choosing
  at most one insight per module is a multiple-choice knapsack solved greedily; later insights are
  available on demand ("tell me more") [franciaVOOLModularInsightbased2025 C2, C3, candidate].
- Relevance to the question: an insight under or next to the current slice ranks above one far away.
"""

from __future__ import annotations

from dataclasses import dataclass

from diplomka.engine.executor import Result
from diplomka.engine.query import CubeQuery


@dataclass(frozen=True)
class Insight:
    insight_id: str  # stable id, so the session does not repeat it
    module: str  # "exception" | "series" | "diff" | "relate"
    query: CubeQuery  # where in the cube it lives
    interest: float  # objective score from the module, normalized to [0, 1]
    payload: object  # CellException | SeriesAnomaly | list[DiffRow] | Relationship


def surprise(insight: Insight, previous: Result | None) -> float:
    """Subjective surprise against the previous result (0 contribution when there is none) (C4)."""
    raise NotImplementedError


def relevance(insight: Insight, current: CubeQuery) -> float:
    """Distance of the insight from the current slice: same slice > child slice > sibling > elsewhere."""
    raise NotImplementedError


def score(insight: Insight, current: CubeQuery, previous: Result | None) -> float:
    """Combined score = f(interest, surprise, relevance); the weights are a thesis decision."""
    raise NotImplementedError


def select(
    insights: list[Insight], current: CubeQuery, previous: Result | None, reported: set[str], budget: int = 2
) -> tuple[list[Insight], list[Insight]]:
    """(shown now, kept for "tell me more"): at most ``budget`` insights, at most one per module,
    none already in ``reported``."""
    raise NotImplementedError
