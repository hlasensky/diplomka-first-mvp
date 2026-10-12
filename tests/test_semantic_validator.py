"""Tests for the semantic validator, on the senger (BeeObserver) semantic layer with fixed domains."""

import pytest

from diplomka.config import DATASETS_DIR
from diplomka.schema import SemanticLayer
from diplomka.semantic_validator import validate_semantics

LAYER = SemanticLayer.from_yaml(DATASETS_DIR / "senger" / "semantic_layer.yaml")
DOMAINS = {
    "state": {"Bremen", "Nordrhein-Westfalen"},
    "event_type": {"queencell", "swarming", "died", "feeding", "honey", "treatment"},
}


def rules(sql: str) -> list[str]:
    return [v.rule for v in validate_semantics(sql, LAYER, DOMAINS)]


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT colony_key, avg(t_i_3) FROM fact_hive_hourly GROUP BY colony_key",
        "SELECT colony_key, stddev_samp(t_i_3), count(t_i_3) FROM fact_hive_hourly GROUP BY 1",
        "SELECT colony_key, sum(weight_gain_kg) FROM fact_hive_hourly GROUP BY 1",
        "SELECT colony_key, weight_kg - lag(weight_kg) OVER (PARTITION BY colony_key ORDER BY time_key) "
        "FROM fact_hive_hourly",
        "SELECT f.colony_key, e.event_type FROM fact_hive_hourly f "
        "ASOF LEFT JOIN fact_event e ON f.colony_key = e.colony_key AND f.time_key >= e.event_ts",
        "SELECT d.colony_key FROM agg_colony_daily d WHERE EXISTS "
        "(SELECT 1 FROM fact_event e WHERE e.colony_key = d.colony_key AND e.event_type = 'swarming')",
        "SELECT * FROM dim_colony WHERE state IN ('Bremen', 'Nordrhein-Westfalen')",
    ],
)
def test_valid_queries(sql):
    assert rules(sql) == []


@pytest.mark.parametrize(
    "sql, expected",
    [
        ("SELECT colony_key, sum(t_i_3) FROM fact_hive_hourly GROUP BY 1", ["R1"]),
        ("SELECT colony_key, sum(t_i_3 - t_o) FROM fact_hive_hourly GROUP BY 1", ["R1", "R1"]),
        ("SELECT colony_key, sum(weight_kg) FROM fact_hive_hourly GROUP BY 1", ["R1"]),
        (
            "SELECT f.colony_key, sum(f.weight_gain_kg) FROM fact_hive_hourly f "
            "JOIN fact_event e ON f.colony_key = e.colony_key GROUP BY 1",
            ["R2"],
        ),
        ("SELECT * FROM dim_colony WHERE state = 'Bremenn'", ["R3"]),
        ("SELECT * FROM fact_event WHERE event_type IN ('swarm', 'honey')", ["R3"]),
    ],
)
def test_invalid_queries(sql, expected):
    assert rules(sql) == expected


def test_unparseable_sql_is_not_checked():
    assert rules("SELECT FROM WHERE (((") == []


MULTI = SemanticLayer.from_yaml(DATASETS_DIR / "multi-senger" / "semantic_layer.yaml")
TODO = pytest.mark.xfail(strict=True, reason="validator lacks this check")

@pytest.mark.parametrize("sql, expected", [
    ("SELECT h.colony_key, sum(h.weight_gain_kg) FROM fact_hive_hourly h "
     "JOIN fact_event e ON h.colony_key = e.colony_key GROUP BY 1", ["R2"]),
    pytest.param("SELECT date, sum(precip_mm) FROM agg_weather_daily GROUP BY date", ["R1"], marks=TODO),
    pytest.param("SELECT district_id, sum(area_ha) FROM fact_crop_area GROUP BY district_id", ["R1"], marks=TODO),
    pytest.param("SELECT t.hour, avg(d.t_center_avg) FROM agg_colony_daily d "
                 "JOIN dim_time t ON d.date = t.date GROUP BY 1", ["R7"], marks=TODO),
])
def test_multi_senger_invalid(sql, expected):
    assert [v.rule for v in validate_semantics(sql, MULTI, {})] == expected
    
@pytest.mark.parametrize("sql", [
    # sum over time within one cell: allowed (precip_mm time: sum)
    "SELECT cell_id, sum(precip_mm) FROM agg_weather_daily GROUP BY cell_id",
    # sum over districts of one crop in each year: allowed (area_ha geography: sum)
    "SELECT year, sum(area_ha) FROM fact_crop_area WHERE crop = 'winter_rape' GROUP BY year",
])
def test_multi_senger_valid(sql):
    assert validate_semantics(sql, MULTI, {}) == []