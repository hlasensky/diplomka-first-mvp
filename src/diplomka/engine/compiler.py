"""Compiler: ``CubeQuery`` + ``Plan`` -> Ibis expression -> DuckDB SQL.

Ibis only builds the expression (filter, join, asof_join, group_by, aggregate); the rules live in the
planner and in ``checks``. ``ibis.to_sql(expr, dialect="duckdb")`` gives the SQL for provenance and for
the sqlglot validator. Reference design: Boring Semantic Layer (YAML -> Ibis -> SQL, docs/olap-arch.md).

Known Ibis gotchas (verified 2026-10-10 on data/multi-senger.duckdb):

- after ``filter``/``join`` refer to columns through ``from ibis import _``, otherwise IntegrityError
- same-named columns of a join get a silent ``_right`` suffix: select columns explicitly
- on DuckDB only ``corr(..., how="pop")`` works
- no ROLLUP / GROUPING SETS / CUBE: one expression per level, combined with ``union`` if needed
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from diplomka.engine.planner import JoinStep, Plan
from diplomka.engine.query import CubeQuery, Predicate
from diplomka.schema import SemanticLayer

if TYPE_CHECKING:
    import ibis.expr.types as ir


def table(con: object, name: str) -> ir.Table:
    """Ibis table for a semantic-layer table name (``con`` is an ``ibis.duckdb`` connection)."""
    raise NotImplementedError


def apply_join(left: ir.Table, step: JoinStep, con: object) -> ir.Table:
    """One join step: inner/left join on ``Join.from_``/``Join.to`` keys plus ``step.fixed`` in the ON
    clause; ``asof_join`` for asof edges (``Join.direction``); a semi join for exists-only pairs (R2);
    bridge edges go through the bridge table and keep its weight column."""
    raise NotImplementedError


def level_column(t: ir.Table, layer: SemanticLayer, level: str) -> ir.Value:
    """Column (or ``Level.expr``, e.g. ``season``) producing the level's values."""
    raise NotImplementedError


def predicate(t: ir.Table, layer: SemanticLayer, p: Predicate) -> ir.BooleanValue:
    """Ibis boolean expression for one selection predicate."""
    raise NotImplementedError


def aggregation(t: ir.Table, layer: SemanticLayer, name: str, agg: str | None) -> ir.Scalar:
    """Ibis aggregate for a measure (``agg``) or a metric (its ``sql`` - ``ibis.literal``/SQL escape).

    Weighted measures over a bridge use the bridge weight (weighted average, not a plain average).
    """
    raise NotImplementedError


def compile_query(query: CubeQuery, plan: Plan, layer: SemanticLayer, con: object) -> ir.Table:
    """Base fact -> joins -> filters -> group_by(levels) -> aggregate(measures) -> order/limit."""
    raise NotImplementedError


def compile_levels(
    query: CubeQuery, plan: Plan, layer: SemanticLayer, con: object, levels: list[tuple[str, ...]]
) -> list[ir.Table]:
    """The same query at several group-by sets (replacement for ROLLUP), one expression per set.

    Needed by ``insight.exceptions`` (all group-bys of a cube) and by ``insight.diff`` (detail and
    aggregated rows of one answer).
    """
    raise NotImplementedError


def to_sql(expr: ir.Table) -> str:
    """DuckDB SQL of the expression (``ibis.to_sql(expr, dialect="duckdb")``)."""
    raise NotImplementedError
