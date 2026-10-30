"""Discovery-driven exploration: exceptions in every group-by of a cube [sarawagiDiscoverydrivenExplorationOLAP1998].

- A cell is an exception if its value differs significantly from the value expected by a model that
  combines the trends along all dimensions and group-bys the cell belongs to; the model is fitted
  separately for each group-by (C2).
- Threshold: standardized residual above tau = 2.5 (C3).
- Model: multiplicative, made additive by a logarithm; coefficients estimated robustly by a 75 % trimmed
  mean; variance modelled as a power p of the expected value (C4).
- Per cell: SelfExp (surprise of the cell itself), InExp (max SelfExp of the cells under it - worth
  drilling here), PathExp (max SelfExp reachable by drilling along one dimension - which way) (C5).
- With missing values the residuals of the fast formula can differ; missing values are ignored when
  averaging (C8).

Design note (own, not from the paper): the paper's model has no notion of time order; for daily hive
data the time dimension is better handled by ``series`` and this module used for the other dimensions
at a fixed time window. The log model needs positive values: measures that can be <= 0 (weight gain,
temperatures) need a shift or the additive form - decide and justify in the thesis.
"""

from __future__ import annotations

from dataclasses import dataclass

from diplomka.engine.query import CubeQuery
from diplomka.schema import SemanticLayer

TAU = 2.5


@dataclass(frozen=True)
class CellException:
    coordinates: dict[str, object]  # level -> member
    value: float
    expected: float
    residual: float  # standardized
    self_exp: float
    in_exp: float
    path_exp: dict[str, float]  # dimension -> PathExp


def group_bys(query: CubeQuery, layer: SemanticLayer, dimensions: list[str]) -> list[tuple[str, ...]]:
    """All group-by sets (lattice) over ``dimensions`` at the levels of ``query``; input for
    ``compiler.compile_levels``."""
    raise NotImplementedError


def fit_expected(cube: dict[tuple[str, ...], list[dict]], measure: str) -> dict[tuple[str, ...], list[float]]:
    """Expected value of every cell of every group-by from the log-linear model (C2, C4)."""
    raise NotImplementedError


def standardized_residuals(values: list[float], expected: list[float], p: float) -> list[float]:
    """(y - y_hat) / sigma with sigma^2 proportional to y_hat^p (C4)."""
    raise NotImplementedError


def summarize(cube: dict, residuals: dict, tau: float = TAU) -> list[CellException]:
    """SelfExp, InExp and PathExp for every cell; exceptions are cells with |residual| > tau (C3, C5)."""
    raise NotImplementedError


def find_exceptions(query: CubeQuery, layer: SemanticLayer, measure: str, dimensions: list[str]) -> list[CellException]:
    """Whole pipeline: aggregate all group-bys, fit, summarize; sorted by SelfExp."""
    raise NotImplementedError
