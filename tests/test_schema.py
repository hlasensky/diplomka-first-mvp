"""Tests for the typed semantic layer, on the multi-senger pack."""

import pytest

from diplomka.config import DATASETS_DIR
from diplomka.schema import SemanticLayer

MULTI = SemanticLayer.from_yaml(DATASETS_DIR / "multi-senger" / "semantic_layer.yaml")


@pytest.mark.parametrize(
    "measure, aggregated_over, expected",
    [
        # precip_mm: time [sum, avg, max], geography [avg, min, max]
        ("precip_mm", {"time"}, {"sum", "avg", "max"}),
        ("precip_mm", {"geography"}, {"avg", "min", "max"}),
        ("precip_mm", {"time", "geography"}, {"avg", "max"}),
        ("precip_mm", set(), {"sum", "avg", "min", "max"}),
        # a dimension the measure does not list allows nothing (fan-out after a join)
        ("precip_mm", {"plant"}, set()),
        # area_ha: crops nest (parent_crop), so summing over them is never allowed
        ("area_ha", {"crop"}, set()),
        ("area_ha", {"geography"}, {"sum", "avg", "min", "max"}),
        ("area_ha", {"time"}, {"avg", "min", "max"}),
    ],
)
def test_allowed_aggs_intersects_the_aggregated_dimensions(measure, aggregated_over, expected):
    assert MULTI.allowed_aggs(measure, aggregated_over) == expected


def test_allowed_aggs_rejects_unknown_dimension():
    with pytest.raises(ValueError, match="Unknown dimensions"):
        MULTI.allowed_aggs("precip_mm", {"geo"})
