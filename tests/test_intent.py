"""Integration tests for intent recognition accuracy (hit the LLM + DuckDB).

Marked ``slow`` so they can be deselected in fast runs:
    uv run pytest -m "not slow"     # skip these
    uv run pytest -m slow           # run only these
"""

import pytest

from diplomka.eval import MULTI_TURN_CASES, TEST_CASES, run_case, run_multi_turn_case


@pytest.mark.slow
@pytest.mark.parametrize("case", TEST_CASES, ids=lambda c: c["question"][:40])
def test_intent_recognition(case):
    mismatches = run_case(case, f"test-{case['question'][:20]}")
    assert not mismatches, "; ".join(mismatches)


@pytest.mark.slow
@pytest.mark.parametrize("case", MULTI_TURN_CASES, ids=lambda c: c["questions"][-1][:40])
def test_multi_turn(case):
    mismatches = run_multi_turn_case(case, f"test-mt-{case['questions'][-1][:20]}")
    assert not mismatches, "; ".join(mismatches)
