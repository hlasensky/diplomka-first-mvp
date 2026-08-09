"""Evaluation of OLAP operation accuracy (week 6 of the plan) - 20 test queries.

For each query it checks that the agent recognized the expected metric/fact+agg/dimension/filters
and that the query over DuckDB ran without error. It does not check the exact wording of `answer` (that's up to the LLM),
only the structured `intent` and execution success.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from graph import graph  # noqa: E402

TEST_CASES = [
    {"question": "What is the total revenue?", "expected": {"metric": "revenue", "dimension": None}},
    {"question": "How many orders were there in 2017?", "expected": {"metric": "orders"}},
    {"question": "What is the average order value?", "expected": {"metric": "avg_order_value"}},
    {"question": "What is the cancellation rate?", "expected": {"metric": "cancellation_rate"}},
    {"question": "How long does delivery take on average?", "expected": {"metric": "delivery_time"}},
    {"question": "Show me revenue by category", "expected": {"metric": "revenue", "dimension": "category"}},
    {"question": "Break down order count by state", "expected": {"metric": "orders", "dimension": "state"}},
    {"question": "What is the revenue by week?", "expected": {"metric": "revenue", "dimension": "time"}},
    {"question": "What is the revenue by month?", "expected": {"metric": "revenue", "dimension": "time", "granularity": "month"}},
    {"question": "How much did we earn on beauty and health?", "expected": {"metric": "revenue", "category_filter": "beleza_saude"}},
    {"question": "What was the revenue in the cama_mesa_banho category in the third quarter of 2018?", "expected": {"metric": "revenue", "category_filter": "cama_mesa_banho"}},
    {"question": "What was the revenue in SP?", "expected": {"metric": "revenue", "state_filter": "SP"}},
    {"question": "What is the average freight cost?", "expected": {"fact": "freight_value", "agg": "avg"}},
    {"question": "What is the maximum product price by category?", "expected": {"fact": "price", "agg": "max", "dimension": "category"}},
    {"question": "What is the total sum of product prices by seller?", "expected": {"fact": "price", "agg": "sum", "dimension": "seller"}},
    {"question": "How much do we earn on sports equipment?", "expected": {"metric": "revenue", "category_filter": "esporte_lazer"}},
    {"question": "What is the revenue by seller?", "expected": {"metric": "revenue", "dimension": "seller"}},
    {"question": "What is the average delivery time in RJ?", "expected": {"metric": "delivery_time", "state_filter": "RJ"}},
    {"question": "What was the weather yesterday in Prague?", "expected": {"unclear": True}},
    {"question": "asdkjaskdj nonsense text xyz", "expected": {"unclear": True}},
]


def check(intent, expected: dict) -> list[str]:
    mismatches = []
    if expected.get("unclear"):
        if intent is not None and intent.has_metric():
            mismatches.append(f"expected 'unclear', but intent has metric/fact+agg: {intent}")
        return mismatches

    for field, value in expected.items():
        actual = getattr(intent, field, None) if intent is not None else None
        if actual != value:
            mismatches.append(f"{field}: expected '{value}', got '{actual}'")
    return mismatches


MULTI_TURN_CASES = [
    {
        "questions": [
            "What is the revenue and order count by category?",
            "show me the trend of orders over time for the category cama_mesa_banho",
        ],
        "expected_last": {"dimension": "time", "category_filter": "cama_mesa_banho"},
    },
]


def run_multi_turn():
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


def main():
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
