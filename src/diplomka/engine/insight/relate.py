"""Explanation "why": associations of the anomalous measure with measures of other facts.

Explain operator [franciaExplainingCubeMeasures2024, candidate, unverified]:

- models that explain a measure by other measures: polynomial regression, multivariate linear regression,
  cross-correlation (the shift with maximal |Pearson|, only along one interval-type level such as date) (C2)
- other facts are combined through a shared hierarchy, analogous to drill-across (C3)
- interest of a component in [0, 1]: R^2 for regressions (negative R^2 -> 0), |rho| for cross-correlation;
  the highlight is the component with maximal interest (C4)
- it explains only by other measures, not by dimension members; "relationship", not "correlation" (C8)

Explain deliberately does not model causality; "explanation" means revealing hidden correlations
[vassiliadisRollUpsDrillDownsIntentional2019 C6, candidate]. Rule R11: say "coincided with" /
"was associated with" and report how many days, colonies or locations support the statement.

Candidates come from the semantic layer, not from the LLM: measures of facts that share the cell and the
date with the anomaly (weather, vegetation, bloom phenology, crop context, events). The LLM may propose
hypotheses; the statistics here accept or reject them.
"""

from __future__ import annotations

from dataclasses import dataclass

from diplomka.engine.query import CubeQuery
from diplomka.schema import SemanticLayer


@dataclass(frozen=True)
class Relationship:
    target: str  # anomalous measure
    candidate: str  # measure of another fact
    model: str  # "cross_correlation" | "polyfit" | "linear"
    lag_days: int  # shift of the candidate, 0 for regressions
    interest: float  # |rho| or R^2, in [0, 1]
    support: int  # number of aligned points (days x colonies)
    query: CubeQuery  # drill-across query that produced the aligned series (provenance)


def candidate_measures(layer: SemanticLayer, anomaly_fact: str) -> list[str]:
    """Measures reachable from the anomaly's fact by an allowed drill-across or asof edge at the same grain."""
    raise NotImplementedError


def aligned_series(target: CubeQuery, candidate: str, layer: SemanticLayer) -> CubeQuery:
    """Drill-across query returning target and candidate side by side per date (and cell)."""
    raise NotImplementedError


def cross_correlation(x: list[float], y: list[float], max_lag: int) -> tuple[int, float]:
    """Lag with maximal |Pearson| and its rho (C2); needs a minimum number of points per lag."""
    raise NotImplementedError


def regression_interest(x: list[list[float]], y: list[float]) -> float:
    """R^2 on a held-out part, mapped to [0, 1] (C2, C4)."""
    raise NotImplementedError


def explain_by_context(
    anomaly_query: CubeQuery, measure: str, layer: SemanticLayer, max_lag: int = 14
) -> list[Relationship]:
    """All candidate relationships for one anomaly, sorted by interest; weak ones filtered out."""
    raise NotImplementedError
