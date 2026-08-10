"""Fast, LLM-free unit tests for intent validation and SQL construction."""

from diplomka.models import Filters
from diplomka.sql import build_sql


def test_metric_only_query():
    sql, params = build_sql(Filters(metrics=["revenue"]))
    assert "SUM(payment_value) AS revenue" in sql
    assert "GROUP BY" not in sql
    assert params == []


def test_dimension_group_by():
    sql, _ = build_sql(Filters(metrics=["revenue"], dimension="category"))
    assert "GROUP BY product_category_name" in sql
    assert "ORDER BY revenue DESC" in sql


def test_time_dimension_truncates_and_orders_chronologically():
    sql, _ = build_sql(Filters(metrics=["revenue"], dimension="time", granularity="month"))
    assert "DATE_TRUNC('month', order_purchase_timestamp)" in sql
    assert "ORDER BY DATE_TRUNC('month', order_purchase_timestamp)" in sql
    assert "LIMIT 200" in sql


def test_filters_become_parametrized():
    sql, params = build_sql(Filters(metrics=["revenue"], category_filter="beleza_saude", state_filter="SP"))
    assert "product_category_name = ?" in sql
    assert "customer_state = ?" in sql
    assert params == ["beleza_saude", "SP"]


def test_fact_agg_pair():
    sql, _ = build_sql(Filters(fact="freight_value", agg="avg"))
    assert "AVG(freight_value) AS avg_freight_value" in sql


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
