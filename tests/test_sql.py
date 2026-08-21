"""Fast, LLM-free unit tests for intent validation and the SQL-generation schema context."""

from diplomka.models import Filters
from diplomka.sql import MAX_ROWS, build_schema_context


def test_schema_context_lists_table_and_metrics():
    context = build_schema_context()
    assert "orders" in context
    assert "SUM(payment_value)" in context
    assert str(MAX_ROWS) in context


def test_schema_context_lists_real_columns():
    context = build_schema_context()
    assert "order_purchase_timestamp" in context
    assert "customer_state" in context
    assert "product_category_name" in context


def test_invalid_metric_dropped_by_validator():
    assert Filters(metrics=["not_a_metric"]).metrics == []


def test_invalid_fact_agg_pair_cleared():
    # min is not an allowed aggregation for freight_value -> both cleared
    f = Filters(fact="freight_value", agg="min")
    assert f.fact is None and f.agg is None


def test_has_metric():
    assert Filters(metrics=["revenue"]).has_metric()
    assert Filters(fact="price", agg="sum").has_metric()
    assert not Filters().has_metric()
