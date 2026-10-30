"""Checks of a cube query against the multidimensional model, before any SQL is generated.

COOL checks parse trees against multidimensional constraints and annotates them either as ambiguities
(e.g. a value that belongs to several attributes, a measure with several valid aggregations, a measure
aggregated with a forbidden function) or as errors that are only reported
[franciaCOOLFrameworkConversational2022 C5, candidate]. Here the same split:

- ``Issue(kind="error")``: the query cannot run (unknown level, forbidden aggregation, rule violation)
- ``Issue(kind="ambiguity")``: the query can run after a choice; the engine fills a default and the
  answer says so, or the agent asks the user

The rules R1-R12 come from ``semantic_layer.yaml`` (``rules``). The engine enforces what it can
structurally; the free-SQL path keeps ``diplomka.semantic_validator`` for the same rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from diplomka.engine.query import CubeQuery
from diplomka.schema import SemanticLayer


@dataclass(frozen=True)
class Issue:
    kind: Literal["error", "ambiguity"]
    rule: str  # rule id (R1...) or a check name (unknown_level, hierarchy_mismatch, ...)
    message: str
    choices: tuple[str, ...] = ()  # options for an ambiguity, best first


def check_query(query: CubeQuery, layer: SemanticLayer, domains: dict[str, set[str]]) -> list[Issue]:
    """All issues of the query; an empty list means the query can be planned.

    Runs the checks below in order: entities, hierarchies, aggregations, domains, grain rules.
    """
    raise NotImplementedError


def check_entities(query: CubeQuery, layer: SemanticLayer) -> list[Issue]:
    """Every measure, metric and level name exists in the semantic layer."""
    raise NotImplementedError


def check_hierarchies(query: CubeQuery, layer: SemanticLayer) -> list[Issue]:
    """At most one level per hierarchy in group-by; a level and its own ancestor together are redundant."""
    raise NotImplementedError


def resolve_aggregations(query: CubeQuery, layer: SemanticLayer) -> tuple[CubeQuery, list[Issue]]:
    """Fill ``MeasureRef.agg`` where it is None and check the given ones (R1).

    Allowed functions = ``layer.allowed_aggs(measure, query.aggregated_over(layer))``. One allowed
    function -> fill it; several -> fill the preferred one and return an ambiguity; none -> error
    (the measure cannot be aggregated over these dimensions, e.g. ``weight_kg`` summed over time).
    """
    raise NotImplementedError


def check_domains(query: CubeQuery, domains: dict[str, set[str]]) -> list[Issue]:
    """Predicate values are members of the level's domain (R3); suggest the closest members otherwise."""
    raise NotImplementedError


def check_grain_rules(query: CubeQuery, layer: SemanticLayer) -> list[Issue]:
    """Rules that depend on the fact and its grain, once the planner has resolved ``query.fact``.

    - R9: crop context needs exactly one crop fixed; crop shares only for 2016 and 2020
    - R12: ``fact_hive_minute`` only for one colony and a short time range
    - R5, R6: data-quality thresholds (``n_hours``, ``colonies_in_cell``) as defaults, not errors
    """
    raise NotImplementedError
