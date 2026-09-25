"""Contract tests for every dataset pack under datasets/ (not only the active one).

A pack is valid when its semantic layer loads, its example queries pass the semantic
validator (and run, if its database is built) and its eval cases refer only to metrics,
measures and levels that exist in the layer.
"""

from pathlib import Path

import pytest
import yaml

from diplomka.config import DATA_DIR, DATASETS_DIR
from diplomka.schema import SemanticLayer
from diplomka.semantic_validator import validate_semantics

PACKS = sorted(p.name for p in DATASETS_DIR.iterdir() if (p / "semantic_layer.yaml").exists())


def _layer(pack: str) -> SemanticLayer:
    return SemanticLayer.from_yaml(DATASETS_DIR / pack / "semantic_layer.yaml")


def _database(pack: str) -> Path | None:
    db = DATA_DIR / f"{pack}.duckdb"
    return db if db.exists() and db.stat().st_size > 0 else None


@pytest.mark.parametrize("pack", PACKS)
def test_pack_has_required_files(pack):
    for name in ("semantic_layer.yaml", "build.sql", "eval.yaml"):
        assert (DATASETS_DIR / pack / name).exists(), name


@pytest.mark.parametrize("pack", PACKS)
def test_layer_references_are_consistent(pack):
    layer = _layer(pack)
    assert layer.name and layer.measures and layer.levels
    for measure in layer.measures.values():
        assert set(measure.tables) <= set(layer.tables), measure.measure_id
    for dimension in layer.raw["dimensions"].values():
        for path in (dimension.get("hierarchies") or {}).values():
            assert set(path) <= set(layer.levels), path
    for entry in layer.glossary:
        target = entry["maps_to"]
        assert target.get("metric") is None or target["metric"] in layer.metrics, entry["term"]
        assert target.get("measure") is None or target["measure"] in layer.measures, entry["term"]
        assert target.get("level") is None or target["level"] in layer.levels, entry["term"]
    for starter in layer.starters:
        assert starter["label"] and starter["message"]


@pytest.mark.parametrize("pack", PACKS)
def test_eval_cases_use_layer_vocabulary(pack):
    layer = _layer(pack)
    eval_data = yaml.safe_load((DATASETS_DIR / pack / "eval.yaml").read_text())
    cases = [c["expected"] for c in eval_data.get("cases") or []]
    cases += [c["expected_last"] for c in eval_data.get("multi_turn") or []]
    assert cases
    for expected in cases:
        assert set(expected.get("metrics", [])) <= set(layer.metrics), expected
        for m in expected.get("measures", []):
            assert m["agg"] in layer.measures[m["measure"]].allowed_aggs, expected
        assert set(expected.get("group_by", [])) <= set(layer.levels), expected
        assert set(expected.get("filters", {})) <= set(layer.levels), expected


@pytest.mark.parametrize("pack", PACKS)
def test_layer_examples_pass_validation_and_execute(pack):
    layer = _layer(pack)
    db = _database(pack)
    if db is None:
        for example in layer.raw.get("examples") or []:
            assert validate_semantics(example["sql"], layer, {}) == [], example["id"]
        pytest.skip(f"{pack}: database not built - only validated without domains")

    duckdb = pytest.importorskip("duckdb")
    with duckdb.connect(str(db), read_only=True) as con:
        domains = layer.load_domains(con)
        for table in layer.tables:
            con.execute(f"DESCRIBE {table}")
        for example in layer.raw.get("examples") or []:
            assert validate_semantics(example["sql"], layer, domains) == [], example["id"]
            con.execute(example["sql"]).fetchall()
