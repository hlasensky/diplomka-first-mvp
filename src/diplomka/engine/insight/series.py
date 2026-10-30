"""Anomalies in one time series (e.g. daily weight gain of one colony).

Taxonomy [blazquez-garciaReviewOutlierAnomaly2021, candidate, unverified]:

- point outlier: global (differs from all values) or local (differs from its neighbours); every global
  outlier is also local (C3)
- subsequence outlier: a contiguous stretch whose joint behaviour is unusual (C3)
- model-based detection: a point is an outlier when |x_t - x_hat_t| > tau; estimation models use past and
  future points, prediction models only past ones and therefore work on streams (C4)
- results depend strongly on the threshold, which few methods choose automatically (C5)

Hive data specifics (docs/decisions.md, semantic_layer.yaml): days with ``n_hours < 20`` are excluded
(R5); peer comparison within a cell needs ``colonies_in_cell >= 3``, otherwise weather separates colony
and environment causes (R6); weight levels are not compared between colonies, gains are (R4).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal


@dataclass(frozen=True)
class SeriesAnomaly:
    colony_key: str
    measure: str
    start: date
    end: date  # == start for a point outlier
    kind: Literal["point", "subsequence"]
    value: float
    expected: float
    score: float  # standardized deviation, comparable across colonies and measures
    method: str


def expected_values(values: list[float | None], method: str, window: int) -> list[float | None]:
    """x_hat_t for every point: rolling median / seasonal baseline (estimation) or a model fitted only
    on the past (prediction, C4). Missing days stay None."""
    raise NotImplementedError


def point_outliers(
    dates: list[date], values: list[float | None], expected: list[float | None], tau: float
) -> list[SeriesAnomaly]:
    """Points with |x - x_hat| / robust scale > tau (C4)."""
    raise NotImplementedError


def subsequence_outliers(dates: list[date], values: list[float | None], min_length: int) -> list[SeriesAnomaly]:
    """Runs of days that are unusual together, e.g. a weight loss over several days (C3)."""
    raise NotImplementedError


def peer_outliers(by_colony: dict[str, list[float | None]], dates: list[date], tau: float) -> list[SeriesAnomaly]:
    """Colonies that differ from the other colonies of the same cell on the same day (R6: >= 3 colonies).

    Same idea as the context model of discovery-driven exploration, which flags a cell that differs from
    the other members at the same time [sarawagiDiscoverydrivenExplorationOLAP1998 C6].
    """
    raise NotImplementedError


def detect(colony_key: str, measure: str, start: date, end: date) -> list[SeriesAnomaly]:
    """Load the daily series through the engine (``agg_colony_daily``, R5 filter) and run the detectors."""
    raise NotImplementedError
