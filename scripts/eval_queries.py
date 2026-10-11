"""Evaluation of OLAP operation accuracy - human-readable accuracy report.

Runs the shared eval dataset (diplomka.eval) through the agent and prints per-case pass/fail
plus an overall accuracy figure. For each query it checks that the agent recognized the
expected metric/fact+agg/dimension/filters and that the query over DuckDB ran without error.
It does not check the exact wording of `answer` (that's up to the LLM), only the structured
`intent` and execution success.
"""

from diplomka.config import DATASET
from diplomka.eval import MULTI_TURN_CASES, TEST_CASES, run_case, run_multi_turn_case


def _report(label: str, mismatches: list[str]) -> bool:
    print(f"[{'FAIL' if mismatches else 'OK '}] {label}")
    for m in mismatches:
        print(f"        - {m}")
    return not mismatches


def main() -> None:
    print(f"Dataset: {DATASET}\n")
    passed = sum(
        _report(f"{i:2d}. {case['question']}", run_case(case, f"eval-{i}")) for i, case in enumerate(TEST_CASES, 1)
    )
    print(f"\nAccuracy: {passed}/{len(TEST_CASES)} ({100 * passed / len(TEST_CASES):.0f}%)\n")

    passed = sum(
        _report(f"multi-turn {i}. {' -> '.join(case['questions'])}", run_multi_turn_case(case, f"eval-multiturn-{i}"))
        for i, case in enumerate(MULTI_TURN_CASES, 1)
    )
    print(f"Multi-turn accuracy: {passed}/{len(MULTI_TURN_CASES)}")


if __name__ == "__main__":
    main()
