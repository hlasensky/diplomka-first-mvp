"""Planner: which fact table answers the query and through which joins.

Two decisions that the LLM must not make:

1. Fact choice (aggregate navigation). Several tables carry the same measure at different grains
   (``fact_hive_hourly`` vs. ``agg_colony_daily``, ``fact_weather`` vs. ``agg_weather_daily``). Pick the
   coarsest table whose grain is still at least as fine as the query's group-by and predicates. This is
   the idea of Calcite lattices / "tiles" (docs/olap-arch.md, tool documentation, not peer-reviewed).

2. Join path. The joins of ``semantic_layer.yaml`` form a graph: tables are nodes, joins are edges with a
   kind (fk, rollup, bridge, range, drill_across, asof) and a cardinality. A level is reachable from a
   fact through fk/rollup edges; another fact through a drill_across edge (``via`` shared dimensions).
   Path search on such a graph with fan-out / chasm trap rules is how dbt MetricFlow builds joins
   (docs/olap-arch.md, tool documentation).

Grain rules applied here: R7 (each fact to the time dimension of its grain), R8 (context at the same
grain through ``dim_colony.cell_id``), R10 (national facts after aggregating colony data), R2 (asof /
exists-only pairs). ``requires_filter`` of a join is a predicate the compiler puts into the ON clause.
"""

from __future__ import annotations

from dataclasses import dataclass

from diplomka.engine.query import CubeQuery
from diplomka.schema import Join, SemanticLayer


@dataclass(frozen=True)
class JoinStep:
    join: Join
    how: str  # "inner" | "left" | "asof" | "exists"; "left" when ``join.optional``
    fixed: dict[str, object]  # ``requires_filter`` columns -> value, for the ON clause


@dataclass(frozen=True)
class Plan:
    """How to compute one query: base fact, joins in order, and which measure comes from which fact."""

    fact: str
    steps: tuple[JoinStep, ...]
    measure_sources: dict[str, str]  # measure name -> table
    level_sources: dict[str, str]  # level name -> table that holds its column (or ``expr``)
    notes: tuple[str, ...] = ()  # assumptions to state in the answer (e.g. "crop pattern of 2020 used")


class PlanningError(ValueError):
    """No allowed fact or join path answers the query."""


def join_graph(layer: SemanticLayer) -> dict[str, list[Join]]:
    """Adjacency list table -> outgoing joins, built once from ``layer.joins``."""
    raise NotImplementedError


def candidate_facts(query: CubeQuery, layer: SemanticLayer) -> list[str]:
    """Facts/aggregates that carry all measures of the query, ordered coarsest grain first.

    A fact qualifies only if every level in group-by and predicates is reachable from it and its grain
    is not coarser than any of them (a daily table cannot answer an hourly group-by).
    """
    raise NotImplementedError


def choose_fact(query: CubeQuery, layer: SemanticLayer) -> str:
    """The first of ``candidate_facts``; raise ``PlanningError`` when none qualifies."""
    raise NotImplementedError


def level_path(layer: SemanticLayer, fact: str, level: str) -> tuple[Join, ...]:
    """Shortest fk/rollup path from ``fact`` to the dimension table of ``level``.

    The path must respect R7: a daily fact reaches ``dim_time`` levels only through ``dim_date`` and
    never joins ``dim_time`` itself. A bridge edge (cell -> district) multiplies rows: allowed only
    with a weighted measure or when the bridge weight is applied (``Bridge.weight``).
    """
    raise NotImplementedError


def plan_drill_across(query: CubeQuery, layer: SemanticLayer, base_fact: str, other_fact: str) -> JoinStep:
    """Join step for a measure of ``other_fact``: drill_across at the same grain, asof for R2 pairs,
    or an error when the pair has no allowed edge (e.g. daily hive data with hourly weather, R8)."""
    raise NotImplementedError


def plan(query: CubeQuery, layer: SemanticLayer) -> Plan:
    """Full plan: choose the fact, collect level paths, add drill-across steps, merge shared joins."""
    raise NotImplementedError
