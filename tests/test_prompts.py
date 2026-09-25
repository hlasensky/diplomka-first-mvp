"""Fast, LLM-free unit tests for intent validation and the prompts of the active dataset.

Written against the semantic layer (``LAYER``) rather than concrete names, so they hold
for whichever dataset pack ``DATASET`` selects.
"""

import pytest

from diplomka.config import DUCKDB_PATH, MAX_ROWS
from diplomka.models import Filters, LevelFilter, MeasureAgg
from diplomka.schema import LAYER

needs_db = pytest.mark.skipif(
    not DUCKDB_PATH.exists() or DUCKDB_PATH.stat().st_size == 0,
    reason=f"{DUCKDB_PATH} not built - run scripts/build_db.py",
)

MEASURE = next(iter(LAYER.measures.values()))
LEVEL = next(iter(LAYER.levels))


@needs_db
def test_sql_prompt_lists_tables_columns_and_measures():
    from diplomka.prompts import sql_prompt

    prompt = sql_prompt()
    assert str(MAX_ROWS) in prompt
    for table in LAYER.tables:
        assert table in prompt
    for measure in LAYER.measures.values():
        assert measure.columns[0] in prompt
    for metric in LAYER.metrics.values():
        assert metric["sql"] in prompt


@needs_db
def test_intent_prompt_lists_vocabulary():
    from diplomka.prompts import intent_prompt

    prompt = intent_prompt()
    assert LAYER.description in prompt
    for name in [*LAYER.metrics, *LAYER.measures, *LAYER.levels]:
        assert name in prompt


def test_invalid_metric_dropped_by_validator():
    assert Filters(metrics=["not_a_metric"]).metrics == []


def test_unknown_measure_dropped_with_note():
    f = Filters(measures=[MeasureAgg(measure="not_a_measure", agg="avg")])
    assert f.measures == []
    assert any("not_a_measure" in note for note in f.adjustments)


def test_disallowed_agg_repaired_not_dropped():
    # e.g. SUM of a temperature: keep the measure, swap in an allowed aggregation, say so
    f = Filters(measures=[MeasureAgg(measure=MEASURE.measure_id, agg="not_an_agg")])
    assert [m.measure for m in f.measures] == [MEASURE.measure_id]
    assert f.measures[0].agg in MEASURE.allowed_aggs
    assert f.has_metric()
    assert f.adjustments


def test_column_name_accepted_as_measure():
    agg = sorted(MEASURE.allowed_aggs)[0]
    f = Filters(measures=[MeasureAgg(measure=MEASURE.columns[0], agg=agg)])
    assert [(m.measure, m.agg) for m in f.measures] == [(MEASURE.measure_id, agg)]


def test_adjustments_hidden_from_llm_schema():
    from langchain_core.utils.function_calling import convert_to_openai_tool

    assert "adjustments" not in str(convert_to_openai_tool(Filters))


def test_valid_measure_agg_pair_kept_and_normalized():
    agg = sorted(MEASURE.allowed_aggs)[0]
    measures = Filters(measures=[MeasureAgg(measure=MEASURE.measure_id, agg=agg.upper())]).measures
    assert [(m.measure, m.agg) for m in measures] == [(MEASURE.measure_id, agg)]


def test_unknown_levels_dropped():
    f = Filters(group_by=[LEVEL, "not_a_level"], filters=[LevelFilter(level="not_a_level", value="x")])
    assert f.group_by == [LEVEL]
    assert f.filters == []


def test_has_metric():
    assert Filters(measures=[MeasureAgg(measure=MEASURE.measure_id, agg=sorted(MEASURE.allowed_aggs)[0])]).has_metric()
    assert not Filters().has_metric()


def test_follow_up_without_metric_keeps_previous_measures(monkeypatch):
    from diplomka import nodes

    previous = Filters(measures=[MeasureAgg(measure=MEASURE.measure_id, agg=sorted(MEASURE.allowed_aggs)[0])])
    follow_up = Filters(group_by=[LEVEL])  # e.g. "and now by <level>"

    class FakeLLM:
        def invoke(self, _messages):
            return follow_up

    monkeypatch.setattr(nodes, "get_structured_llm", lambda *_args: FakeLLM())
    monkeypatch.setattr(nodes, "intent_prompt", lambda: "")
    result = nodes.clarify_intent({"messages": [], "active_filters": previous}, {})
    assert result["intent"].measures == previous.measures
    assert result["intent"].group_by == [LEVEL]
    assert not result["needs_clarification"]
