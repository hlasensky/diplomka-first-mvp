"""Evaluation dataset of the active dataset pack and the intent-checking helper.

Cases live in ``datasets/<name>/eval.yaml``::

    cases:
      - question: "Average center temperature by month"
        expected:
          measures: [{measure: t_center, agg: avg}]
          group_by: [month]
          filters: {event_type: swarming}     # level -> value (or list of values)
      - question: "What was the weather yesterday?"
        expected: {unclear: true}
    multi_turn:
      - questions: ["...", "..."]
        expected_last: {...}

Only the fields present in ``expected`` are checked; lists are compared as sets.

Consumed both by the pytest suite (tests/test_intent.py) and by the human-readable
accuracy report (scripts/eval_queries.py), through ``run_case`` and ``run_multi_turn_case``.
"""

from typing import Any

import yaml
from langchain_core.runnables import RunnableConfig

from diplomka.config import EVAL_PATH
from diplomka.graph import get_graph
from diplomka.models import Filters

_EVAL = yaml.safe_load(EVAL_PATH.read_text()) if EVAL_PATH.exists() else {}
TEST_CASES: list[dict[str, Any]] = _EVAL.get("cases") or []
MULTI_TURN_CASES: list[dict[str, Any]] = _EVAL.get("multi_turn") or []


def _normalize(field: str, value: Any) -> Any:
    """Comparable form of an intent field or of its expected value."""
    if field == "measures":
        return {(m["measure"], m["agg"]) if isinstance(m, dict) else (m.measure, m.agg) for m in value or []}
    if field == "filters":
        pairs = value.items() if isinstance(value, dict) else ((f.level, f.value) for f in value or [])
        normalized: dict[str, set[str]] = {}
        for level, values in pairs:
            normalized.setdefault(level, set()).update(map(str, values if isinstance(values, list) else [values]))
        return normalized
    if isinstance(value, list):
        return set(value)
    return value


def check(intent: Filters | None, expected: dict) -> list[str]:
    """Return a list of mismatch descriptions between the parsed intent and expectations."""
    mismatches = []
    if expected.get("unclear"):
        if intent is not None and intent.has_metric():
            mismatches.append(f"expected 'unclear', but intent has a metric/measure: {intent}")
        return mismatches

    for field, value in expected.items():
        actual = getattr(intent, field, None) if intent is not None else None
        if _normalize(field, actual) != _normalize(field, value):
            mismatches.append(f"{field}: expected '{value}', got '{actual}'")
    return mismatches


def _thread(thread_id: str) -> RunnableConfig:
    return {"configurable": {"thread_id": thread_id}}


def run_case(case: dict, thread_id: str) -> list[str]:
    """Run one question through the agent; mismatches with ``expected`` plus any SQL error."""
    result = get_graph().invoke({"question": case["question"]}, config=_thread(thread_id))
    mismatches = check(result.get("intent"), case["expected"])
    # unclear questions never reach execute_query
    if not case["expected"].get("unclear") and result.get("validation_error") is not None:
        mismatches.append(f"SQL error: {result['validation_error']}")
    return mismatches


def run_multi_turn_case(case: dict, thread_id: str) -> list[str]:
    """Run the questions of one conversation in a single thread; checks the last turn."""
    graph = get_graph()
    results = [graph.invoke({"question": q}, config=_thread(thread_id)) for q in case["questions"]]
    result = results[-1]
    mismatches = check(result.get("intent"), case["expected_last"])
    if result.get("validation_error") is not None:
        mismatches.append(f"SQL error: {result['validation_error']}")
    if result.get("rows") == results[0].get("rows"):
        mismatches.append("rows same as in the first turn - the second query probably didn't run with a new intent")
    return mismatches
