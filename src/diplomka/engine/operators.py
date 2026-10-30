"""OLAP operators as pure transformations ``CubeQuery -> CubeQuery``.

The operator set follows COOL [franciaCOOLFrameworkConversational2022 C4, candidate; operator definitions
on PDF p. 6, which has a PAGE_WARN in QC - check in the PDF]:

- drill down: replace a coarser level in group-by with a finer one of the same hierarchy
- roll up: replace a finer level in group-by with a coarser one
- slice and dice: add a selection predicate
- add / drop: add or remove a measure, level or predicate; on a level they act as drill down / roll up,
  on a predicate as slice and dice
- replace: drop + add

Drill-across (combining facts through shared dimensions) is not a COOL operator; it uses the
``drill_across`` joins of the semantic layer and the grain rules R7, R8, R10.

Operators only change the query. They never touch SQL and do not check the result: call
``checks.check_query`` on the returned query. Each operator raises ``OperatorError`` when it cannot be
applied at all (e.g. drill down below the finest level).
"""

from __future__ import annotations

from diplomka.engine.query import CubeQuery, MeasureRef, Predicate
from diplomka.schema import SemanticLayer


class OperatorError(ValueError):
    """The operator cannot be applied to this query (wrong hierarchy, finest/coarsest level, ...)."""


def drill_down(query: CubeQuery, layer: SemanticLayer, from_level: str, to_level: str | None = None) -> CubeQuery:
    """Replace ``from_level`` in group-by with ``to_level`` (default: the next finer level of its hierarchy).

    COOL lists the errors to report here (fulltext §7, not a claim in the note): invalid drill (already
    the finest level), hierarchy mismatch (levels of two hierarchies), hierarchy structure mismatch
    (``to_level`` is not finer). A dimension with several hierarchies (``time``: calendar, weekly) needs
    ``to_level`` or a rule which hierarchy to follow.
    """
    raise NotImplementedError


def roll_up(query: CubeQuery, layer: SemanticLayer, from_level: str, to_level: str | None = None) -> CubeQuery:
    """Replace ``from_level`` in group-by with ``to_level`` (default: the next coarser level).

    Rolling up past the top level drops the level from group-by (aggregation over the whole dimension).
    Changing the grain can change the allowed aggregations (e.g. ``weight_kg`` over time), so the result
    must go through ``checks.check_query`` again.
    """
    raise NotImplementedError


def slice_(query: CubeQuery, layer: SemanticLayer, level: str, value: object) -> CubeQuery:
    """Fix ``level`` to one value and remove it from group-by (one member left, nothing to group by)."""
    raise NotImplementedError


def dice(query: CubeQuery, layer: SemanticLayer, predicates: tuple[Predicate, ...]) -> CubeQuery:
    """Add selection predicates; a predicate on a level that already has one extends its value list."""
    raise NotImplementedError


def add_measure(query: CubeQuery, layer: SemanticLayer, measure: MeasureRef) -> CubeQuery:
    """Add a measure to the measure clause; the measure must be available on the query's fact or on a
    fact reachable by drill-across (resolved by the planner)."""
    raise NotImplementedError


def drop_measure(query: CubeQuery, layer: SemanticLayer, name: str) -> CubeQuery:
    """Remove a measure; dropping the last one is an error (the measure clause is mandatory)."""
    raise NotImplementedError


def replace(query: CubeQuery, layer: SemanticLayer, old: str, new: MeasureRef | Predicate | str) -> CubeQuery:
    """Replace a measure, a level or a predicate with a new one of the same kind (drop + add)."""
    raise NotImplementedError


def drill_across(query: CubeQuery, layer: SemanticLayer, measure: MeasureRef) -> CubeQuery:
    """Add a measure of another fact, combined through the shared (conformed) dimensions.

    The other fact must be at the same grain as the query after aggregation (R8) or is first aggregated
    to it (R10: national facts). Pairs that may only be combined by ASOF or EXISTS (R2) are marked here
    so the compiler emits the right join. Whether the pair is allowed at all is decided by
    ``planner.plan_drill_across``.
    """
    raise NotImplementedError


def compare(query: CubeQuery, layer: SemanticLayer, level: str, a: object, b: object) -> tuple[CubeQuery, CubeQuery]:
    """Two sibling queries that differ only in ``level`` = ``a`` vs. ``b`` (e.g. two years, two cells).

    Input for ``insight.diff.explain_difference`` (DIFF compares two aggregated cells).
    """
    raise NotImplementedError
