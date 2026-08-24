"""Integration tests for intent recognition accuracy (hit the LLM + DuckDB).

Marked ``slow`` so they can be deselected in fast runs:
    uv run pytest -m "not slow"     # skip these
    uv run pytest -m slow           # run only these
"""

import pytest

from langchain_core.runnables import RunnableConfig

from diplomka.eval import MULTI_TURN_CASES, TEST_CASES, check
from diplomka.graph import get_graph


@pytest.mark.slow
@pytest.mark.parametrize("case", TEST_CASES, ids=lambda c: c["question"][:40])
def test_intent_recognition(case):
    thread: RunnableConfig = {"configurable": {"thread_id": f"test-{case['question'][:20]}"}}
    result = get_graph().invoke({"question": case["question"]}, config=thread)

    mismatches = check(result.get("intent"), case["expected"])
    assert not mismatches, "; ".join(mismatches)

    if not case["expected"].get("unclear"):
        assert result.get("validation_error") is None, result.get("validation_error")


@pytest.mark.slow
@pytest.mark.parametrize("case", MULTI_TURN_CASES, ids=lambda c: c["questions"][-1][:40])
def test_multi_turn(case):
    thread: RunnableConfig = {"configurable": {"thread_id": f"test-mt-{case['questions'][-1][:20]}"}}
    graph = get_graph()
    results = [graph.invoke({"question": q}, config=thread) for q in case["questions"]]
    result = results[-1]

    mismatches = check(result.get("intent"), case["expected_last"])
    assert not mismatches, "; ".join(mismatches)
    assert result.get("validation_error") is None
    assert result.get("rows") != results[0].get("rows"), "second query did not re-run with a new intent"
