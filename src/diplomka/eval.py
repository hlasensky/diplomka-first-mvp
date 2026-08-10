"""Shared evaluation dataset and intent-checking helper.

Consumed both by the pytest suite (tests/test_intent.py) and by the human-readable
accuracy report (scripts/eval_queries.py).
"""

from diplomka.models import Filters

TEST_CASES = [
    {"question": "What is the total revenue?", "expected": {"metric": "revenue", "dimension": None}},
    {"question": "How many orders were there in 2017?", "expected": {"metric": "orders"}},
    {"question": "What is the average order value?", "expected": {"metric": "avg_order_value"}},
    {"question": "What is the cancellation rate?", "expected": {"metric": "cancellation_rate"}},
    {"question": "How long does delivery take on average?", "expected": {"metric": "delivery_time"}},
    {"question": "Show me revenue by category", "expected": {"metric": "revenue", "dimension": "category"}},
    {"question": "Break down order count by state", "expected": {"metric": "orders", "dimension": "state"}},
    {"question": "What is the revenue by week?", "expected": {"metric": "revenue", "dimension": "time"}},
    {
        "question": "What is the revenue by month?",
        "expected": {"metric": "revenue", "dimension": "time", "granularity": "month"},
    },
    {
        "question": "How much did we earn on beauty and health?",
        "expected": {"metric": "revenue", "category_filter": "beleza_saude"},
    },
    {
        "question": "What was the revenue in the cama_mesa_banho category in the third quarter of 2018?",
        "expected": {"metric": "revenue", "category_filter": "cama_mesa_banho"},
    },
    {"question": "What was the revenue in SP?", "expected": {"metric": "revenue", "state_filter": "SP"}},
    {"question": "What is the average freight cost?", "expected": {"fact": "freight_value", "agg": "avg"}},
    {
        "question": "What is the maximum product price by category?",
        "expected": {"fact": "price", "agg": "max", "dimension": "category"},
    },
    {
        "question": "What is the total sum of product prices by seller?",
        "expected": {"fact": "price", "agg": "sum", "dimension": "seller"},
    },
    {
        "question": "How much do we earn on sports equipment?",
        "expected": {"metric": "revenue", "category_filter": "esporte_lazer"},
    },
    {"question": "What is the revenue by seller?", "expected": {"metric": "revenue", "dimension": "seller"}},
    {
        "question": "What is the average delivery time in RJ?",
        "expected": {"metric": "delivery_time", "state_filter": "RJ"},
    },
    {"question": "What was the weather yesterday in Prague?", "expected": {"unclear": True}},
    {"question": "asdkjaskdj nonsense text xyz", "expected": {"unclear": True}},
]

MULTI_TURN_CASES = [
    {
        "questions": [
            "What is the revenue and order count by category?",
            "show me the trend of orders over time for the category cama_mesa_banho",
        ],
        "expected_last": {"dimension": "time", "category_filter": "cama_mesa_banho"},
    },
]


def check(intent: Filters | None, expected: dict) -> list[str]:
    """Return a list of mismatch descriptions between the parsed intent and expectations."""
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
