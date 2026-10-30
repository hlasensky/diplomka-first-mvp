"""Cube query model: the state "where in the cube am I" that OLAP operators transform.

A query is a GPSJ query (generalized projection, selection, join): a measure clause, a group-by clause
and a selection clause; only the measure clause is mandatory [franciaCOOLFrameworkConversational2022 C3,
candidate]. It names semantic-layer entities only (measure ids, level names, level values), never tables
or SQL: the planner and the compiler resolve those. The same idea is the "cell" of Cubes (docs/olap-arch.md).

Level names are unique across dimensions (see ``diplomka.schema``), so a level identifies its dimension.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from diplomka.schema import SemanticLayer

PredicateOp = Literal["=", "!=", "in", "between", "<", "<=", ">", ">="]


@dataclass(frozen=True)
class MeasureRef:
    """One item of the measure clause.

    ``name`` is a key of ``SemanticLayer.measures`` or of ``SemanticLayer.metrics`` (a metric already
    carries its aggregation in SQL, so ``agg`` stays None). ``agg`` None on a measure means: the
    engine picks the default from ``SemanticLayer.allowed_aggs`` (see ``checks.resolve_aggregations``).
    """

    name: str
    agg: str | None = None
    alias: str | None = None


@dataclass(frozen=True)
class Predicate:
    """One selection predicate on a level, e.g. ``season = 'summer'`` or ``date between (a, b)``."""

    level: str
    op: PredicateOp
    values: tuple[object, ...]


@dataclass(frozen=True)
class CubeQuery:
    """GPSJ query over the cube.

    - ``measures``: measure clause (at least one item)
    - ``group_by``: level names, at most one level per hierarchy
    - ``where``: selection clause, conjunction of predicates
    - ``fact``: fact/aggregate table, filled by the planner (None = not resolved yet)
    """

    measures: tuple[MeasureRef, ...]
    group_by: tuple[str, ...] = ()
    where: tuple[Predicate, ...] = ()
    order_by: tuple[str, ...] = ()
    limit: int | None = None
    fact: str | None = field(default=None, compare=False)

    def dimensions(self, layer: SemanticLayer) -> dict[str, str]:
        """Dimension -> level for every level in ``group_by``."""
        raise NotImplementedError

    def aggregated_over(self, layer: SemanticLayer) -> set[str]:
        """Dimensions the query collapses: dimensions of the fact grain that are not in ``group_by``.

        This is the input for ``SemanticLayer.allowed_aggs``. A dimension fixed to one value by a
        predicate is still collapsed (one member, but the aggregation runs over its finer rows).
        """
        raise NotImplementedError

    def fixed_levels(self) -> dict[str, object]:
        """Levels fixed to exactly one value by an ``=`` predicate (the current slice)."""
        raise NotImplementedError

    def describe(self, layer: SemanticLayer) -> str:
        """Short natural-language description of the query, using labels from the semantic layer.

        Used as the preamble of an answer and in the LLM context (what the user is looking at).
        """
        raise NotImplementedError
