"""Explanation "where": which parts of the cube explain a change between two aggregated cells.

DIFF operator [sarawagiExplainingDifferencesMultidimensional, candidate - verified: true, precteno: ne,
bib entry incomplete]:

- the answer is at most N rows (user's choice, about a dozen) mixing detail and aggregated rows; every
  aggregated row carries a ratio r valid for all its children not listed separately (C2)
- the rows are chosen information-theoretically: minimize the bits needed to rebuild the second subcube
  from the first and the answer; Poisson for counts, normal for other measures (C3)
- more compact than the naive "detail-N" (N largest detail changes) (C4)
- dynamic programming in one pass over the data, optimal for correctly estimated ratios (C5)

Alternative for a single outlying aggregate - Scorpion [wuScorpionExplainingAway2013, candidate,
unverified]: a predicate over input rows that, when removed before aggregation, makes the outlier look
normal while hold-out results barely change (C1); the fast algorithms need incrementally removable
aggregates - COUNT, SUM, AVG, STDDEV yes; MIN, MAX, MEDIAN no (C4).
"""

from __future__ import annotations

from dataclasses import dataclass

from diplomka.engine.query import CubeQuery
from diplomka.schema import SemanticLayer


@dataclass(frozen=True)
class DiffRow:
    coordinates: dict[str, object]  # level -> member; fewer levels = aggregated row
    value_a: float
    value_b: float
    ratio: float  # value_b / value_a, applies to the not-listed children of an aggregated row
    share_of_change: float  # part of the total change this row accounts for


def detail_n(a: CubeQuery, b: CubeQuery, layer: SemanticLayer, dimensions: list[str], n: int) -> list[DiffRow]:
    """Baseline: the N largest absolute changes at the detail level (C4). For evaluation against ``diff``."""
    raise NotImplementedError


def diff(a: CubeQuery, b: CubeQuery, layer: SemanticLayer, dimensions: list[str], n: int = 10) -> list[DiffRow]:
    """DIFF answer: at most ``n`` rows over the hierarchies of ``dimensions`` (C2, C3, C5).

    ``a`` and ``b`` come from ``operators.compare``. The measure must be summable over ``dimensions``
    (``allowed_aggs`` contains sum); for averages compare the sum and the count separately.
    """
    raise NotImplementedError


def explain_away(
    outlier: CubeQuery, holdout: list[CubeQuery], layer: SemanticLayer, attributes: list[str]
) -> list[dict]:
    """Scorpion-style predicates over input rows that explain away one outlying aggregate (C1, C2).

    Example: one sensor or one colony that pulls a cell average. Only for incrementally removable
    aggregations (C4); otherwise return [] and let ``diff`` answer.
    """
    raise NotImplementedError
