"""Evaluation of OLAP operation accuracy - human-readable accuracy report.

Runs the shared eval dataset (diplomka.eval) through the agent and prints per-case pass/fail
plus an overall accuracy figure. For each query it checks that the agent recognized the
expected metric/fact+agg/dimension/filters and that the query over DuckDB ran without error.
It does not check the exact wording of `answer` (that's up to the LLM), only the structured
`intent` and execution success.
"""

from diplomka.eval import MULTI_TURN_CASES, TEST_CASES, check
from diplomka.graph import get_graph

graph = get_graph()


def run_multi_turn() -> bool:
    passed = 0
    for i, case in enumerate(MULTI_TURN_CASES, 1):
        thread = {"configurable": {"thread_id": f"eval-multiturn-{i}"}}
        results = [graph.invoke({"question": q}, config=thread) for q in case["questions"]]
        result = results[-1]

        intent = result.get("intent")
        mismatches = check(intent, case["expected_last"])
        if result.get("validation_error"):
            mismatches.append(f"SQL error: {result['validation_error']}")
        if result.get("rows") == results[0].get("rows"):
            mismatches.append("rows same as in the first turn - the second query probably didn't run with a new intent")

        ok = not mismatches
        passed += ok
        status = "OK " if ok else "FAIL"
        print(f"[{status}] multi-turn {i}. {' -> '.join(case['questions'])}")
        for m in mismatches:
            print(f"        - {m}")

    print(f"Multi-turn accuracy: {passed}/{len(MULTI_TURN_CASES)}")
    return passed == len(MULTI_TURN_CASES)


def main() -> None:
    passed = 0
    for i, case in enumerate(TEST_CASES, 1):
        thread = {"configurable": {"thread_id": f"eval-{i}"}}
        result = graph.invoke({"question": case["question"]}, config=thread)

        intent = result.get("intent")
        mismatches = check(intent, case["expected"])

        exec_ok = not case["expected"].get("unclear") and result.get("validation_error") is None
        if case["expected"].get("unclear"):
            exec_ok = True  # unclear queries never reach execute_query at all

        ok = not mismatches and exec_ok
        passed += ok

        status = "OK " if ok else "FAIL"
        print(f"[{status}] {i:2d}. {case['question']}")
        if mismatches:
            for m in mismatches:
                print(f"        - {m}")
        if not case["expected"].get("unclear") and result.get("validation_error"):
            print(f"        - SQL error: {result['validation_error']}")

    print(f"\nAccuracy: {passed}/{len(TEST_CASES)} ({100 * passed / len(TEST_CASES):.0f}%)")

    print()
    run_multi_turn()


if __name__ == "__main__":
    main()
