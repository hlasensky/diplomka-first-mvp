"""Result tests for the example queries of every dataset pack.

- Snapshots (``tests/golden/<pack>/<example id>.parquet``) catch regressions: a rebuild must not
  change what an example returns. After a reviewed, intended change, rewrite them with
  ``UPDATE_GOLDEN=1 uv run pytest tests/test_golden.py`` and check the diff.
- Verified numbers were checked against external sources; a failure there is a bug, never a
  reason to update anything.
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from tests.test_datasets import PACKS, _database, _layer

GOLDEN = Path(__file__).parent / "golden"


def _sorted(df: pd.DataFrame) -> pd.DataFrame:
    """Rows in a fixed order: examples without ORDER BY have none. Lists become tuples to be sortable."""
    df = df.map(lambda v: tuple(v) if isinstance(v, (list, np.ndarray)) else v)
    return df.sort_values(list(df.columns)).reset_index(drop=True)


@pytest.mark.parametrize("pack", PACKS)
def test_examples_match_golden(pack):
    """Example results must not change between builds. UPDATE_GOLDEN=1 rewrites the snapshots."""
    layer, db = _layer(pack), _database(pack)
    if db is None:
        pytest.skip(f"{pack}: database not built")
    duckdb = pytest.importorskip("duckdb")
    folder = GOLDEN / pack
    update = bool(os.getenv("UPDATE_GOLDEN"))
    if update:
        folder.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(db), read_only=True) as con:
        for example in layer.raw.get("examples") or []:
            path = folder / f"{example['id']}.parquet"
            if update:
                con.execute(f"COPY ({example['sql']}) TO '{path}' (FORMAT parquet)")
                continue
            if not path.exists():
                pytest.fail(f"{pack} {example['id']}: no snapshot, run with UPDATE_GOLDEN=1")
            got = _sorted(con.execute(example["sql"]).df())
            # Read through DuckDB: pandas would need pyarrow, which the project does not depend on.
            want = _sorted(con.execute("SELECT * FROM read_parquet(?)", [str(path)]).df())
            pd.testing.assert_frame_equal(got, want, rtol=1e-6, check_dtype=False, obj=f"{pack} {example['id']}")
    if update:
        pytest.skip(f"{pack}: snapshots rewritten")


def test_verified_numbers():
    """Values checked against external sources; a failure is a bug, never a snapshot update."""
    db = _database("multi-senger")
    if db is None:
        pytest.skip("multi-senger: database not built")
    duckdb = pytest.importorskip("duckdb")
    ex = {e["id"]: e["sql"] for e in _layer("multi-senger").raw["examples"]}
    with duckdb.connect(str(db), read_only=True) as con:
        # Colonies that died in the dataset per bee winter (EX8 repeats them per survey).
        died = {w: n for w, _, s, *_, n in con.execute(ex["EX8"]).fetchall() if s in (None, "DLR Mayen")}
        assert died == {"2018/19": 0, "2019/20": 5, "2020/21": 2, "2021/22": 1, "2022/23": 0}
        # Daily weight gain 14 days before vs. after oilseed rape bloom onset.
        # EX6 has no ORDER BY, so pick the rows by period, not by position.
        gain = {period: g for period, g, *_ in con.execute(ex["EX6"]).fetchall()}
        assert gain["before bloom"] == pytest.approx(-0.0157, abs=1e-3)
        assert gain["after bloom"] == pytest.approx(0.359, abs=1e-3)
        # FAOSTAT honey production in Germany, tonnes.
        honey = {y: h for y, _, _, _, h, _ in con.execute(ex["EX10"]).fetchall()}
        assert honey == {2019: 24100, 2020: 29200, 2021: 19600, 2022: 34100}
