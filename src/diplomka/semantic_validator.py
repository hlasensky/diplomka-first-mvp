"""Semantic validation of LLM-generated DuckDB SQL against the semantic layer.

Runs in the `validate_sql` node after the syntactic check (DuckDB EXPLAIN).
Violations are sent back to the `generate_sql` node as repair feedback and
logged for evaluation (violations per rule and per model).

The checks are heuristic: aliases are not resolved through CTEs or subqueries,
so e.g. SUM over an alias of AVG(t_i_3) defined in a CTE is not detected.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import sqlglot
from sqlglot import exp

from diplomka.schema import SemanticLayer

# Window navigation functions do not aggregate a measure.
NAVIGATION_FUNCS = frozenset({"lag", "lead", "first_value", "last_value", "nth_value"})
# Counting non-null values and correlating two series are valid for every measure.
ALWAYS_ALLOWED = frozenset({"count", "corr"})
AGG_ALIASES = {"stddev_samp": "stddev", "stddev_pop": "stddev", "arg_max": "last"}
ASOF_PATTERN = re.compile(r"\bASOF\b", re.IGNORECASE)


@dataclass(frozen=True)
class Violation:
    rule: str
    message: str


def _agg_name(node: exp.Expression) -> str:
    name = node.sql_name().lower()
    return AGG_ALIASES.get(name, name)


def _direct_tables(select: exp.Select) -> set[str]:
    """Tables in the FROM and JOIN clauses of this SELECT (not in its subqueries)."""
    sources = []
    from_clause = select.args.get("from") or select.args.get("from_")
    if from_clause is not None:
        sources.append(from_clause.this)
    sources.extend(join.this for join in select.args.get("joins") or [])
    return {source.name for source in sources if isinstance(source, exp.Table)}


def _check_aggregations(tree: exp.Expression, layer: SemanticLayer) -> list[Violation]:
    """R1: every measure is aggregated only with its allowed functions."""
    violations = []
    for agg in tree.find_all(exp.AggFunc):
        name = _agg_name(agg)
        if name in NAVIGATION_FUNCS or name in ALWAYS_ALLOWED:
            continue
        for column in agg.find_all(exp.Column):
            measure = layer.measures_by_column.get(column.name)
            if measure is not None and name not in measure.allowed_aggs:
                violations.append(
                    Violation(
                        "R1",
                        f"{name.upper()}({column.name}) is not allowed for measure "
                        f"'{measure.measure_id}'; allowed: {sorted(measure.allowed_aggs)}.",
                    )
                )
    return violations


def _check_fan_traps(sql: str, tree: exp.Expression, layer: SemanticLayer) -> list[Violation]:
    """R2: fact pairs declared as ASOF-only must not be joined with a plain JOIN."""
    if not layer.asof_only_pairs or ASOF_PATTERN.search(sql):
        return []
    violations = []
    for select in tree.find_all(exp.Select):
        tables = _direct_tables(select)
        for pair in layer.asof_only_pairs:
            if pair <= tables:
                left, right = sorted(pair)
                violations.append(
                    Violation(
                        "R2",
                        f"{left} and {right} are joined with a plain JOIN, which multiplies "
                        f"rows (fan trap); use ASOF JOIN or EXISTS.",
                    )
                )
    return violations


def _check_domains(tree: exp.Expression, domains: dict[str, set[str]]) -> list[Violation]:
    """R3: literals compared with dimension attributes must exist in their domain."""
    violations = []
    for comparison in tree.find_all(exp.EQ, exp.In):
        column = comparison.this
        if not isinstance(column, exp.Column) or column.name not in domains:
            continue
        literals = [comparison.expression] if isinstance(comparison, exp.EQ) else comparison.expressions
        for literal in literals:
            if isinstance(literal, exp.Literal) and literal.is_string and literal.this not in domains[column.name]:
                violations.append(
                    Violation(
                        "R3",
                        f"'{literal.this}' is not a valid value of {column.name}; "
                        f"valid values: {sorted(domains[column.name])}.",
                    )
                )
    return violations


def validate_semantics(sql: str, layer: SemanticLayer, domains: dict[str, set[str]]) -> list[Violation]:
    """Return semantic violations of one DuckDB query; an empty list means valid.

    SQL that sqlglot cannot parse is not checked (DuckDB's EXPLAIN already accepted it).
    """
    try:
        tree = sqlglot.parse_one(sql, read="duckdb")
    except sqlglot.errors.ParseError:
        return []
    violations = _check_aggregations(tree, layer) + _check_fan_traps(sql, tree, layer) + _check_domains(tree, domains)
    # Deduplicate while keeping order (a column can occur several times).
    return list(dict.fromkeys(violations))


def format_feedback(violations: list[Violation]) -> str:
    """Repair feedback for the `generate_sql` node."""
    lines = ["The query violates the semantic layer. Fix these issues:"]
    lines.extend(f"- [{v.rule}] {v.message}" for v in violations)
    return "\n".join(lines)
