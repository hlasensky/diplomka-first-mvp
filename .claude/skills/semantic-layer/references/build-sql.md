# build.sql conventions

`scripts/build_db.py` runs `datasets/<pack>/build.sql` against `data/<pack>.duckdb` (or
`DUCKDB_PATH`) with `data/raw/<pack>/` as the working directory, so every path in build.sql is
relative to the raw folder. The script is the user's; do not change it.

```bash
DATASET=<pack> uv run python scripts/build_db.py                               # in place
DATASET=<pack> DUCKDB_PATH=<scratchpad>/<pack>.duckdb uv run python scripts/build_db.py   # trial build
```

## File layout

```sql
-- build.sql (<pack>)
-- <one line: what the pack contains>
-- Source: <citation, DOI / URL, licence>
-- Run:    DATASET=<pack> uv run python scripts/build_db.py
--         Paths are relative to data/raw/<pack>/ (see MANIFEST.json there).
-- Data checks behind the decisions below: docs/decisions.md, <date>.

-- ---------------------------------------------------------------------------
-- 1) STAGING: <source> (<path pattern>)
--    <what one row is, time zone, NULL markers, anything surprising about the files>
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TEMP TABLE stg_<x> AS ...;

-- 1a) <a fix of a data artefact, with the evidence for it>
-- 1b) Guard: <invariant after the fix>; otherwise the build fails.

-- 2) <FACT> ... one numbered section per source or fact
-- N) TIME DIMENSIONS, built after all facts so they cover every date
-- 99) CHECKS: the build fails when a grain or a foreign key is violated
-- cleanup: DROP staging tables and macros
```

Section comments explain *why*: the source's quirks, the evidence for a fix, the code mapping
(e.g. `-- 1012 'Bau von Weiselzellen' -> queencell`). The user reads build.sql as documentation of
the data preparation for the thesis.

## Reading raw files

- `read_csv(..., union_by_name = true)` for many files with drifting columns.
- Type columns explicitly (`types = {...}` or casts) when a file can hold an all-NA column; type
  inference then picks VARCHAR for that file and the union breaks.
- NULL markers: `nullstr = ['NA', 'NULL', '']`; numeric sentinels (`-200`, `-999`, `9999`) with
  `nullif(col, -200)`. Confirm sentinels in the profile (a spike at one impossible value).
- Decimal commas: `decimal_separator = ','` or `replace(v, ',', '.')::DOUBLE`.
- Encodings: `encoding = 'latin-1'` for German statistical exports; header/footer lines with `skip`
  plus a filter on a key pattern (`regexp_full_match(code, '[0-9]{5}')`).
- Wide → long with `UNPIVOT` when one concept sits in several columns and users break it down by
  that column (`fact_temperature` from `t_i_1..t_i_5`).
- Status codes in cells (statistical tables): a macro for the value (`'-'` → 0, number → value,
  otherwise NULL) and one for the status (`'zero' | 'value' | 'suppressed' | 'unreliable'`).
- JSON: `read_json_auto`; API dumps are fetched into `data/raw/<pack>/` first (with MANIFEST.json),
  never from build.sql at build time, so the build is reproducible offline.

## Time

- Convert to UTC (or keep the verified source zone) in staging: `timezone('UTC', ts AT TIME ZONE 'Europe/Berlin')`
  for local timestamps. Keep timestamps naive afterwards and document the zone.
- Check DST switch days: duplicate local hours in autumn, missing or relabelled hours in spring.
  Fix with evidence (a running number column, the order of rows), and add a guard.
- Hourly from minutes = mean of minutes plus `n_minutes`; daily from hourly = per-measure
  aggregation following the additivity (sum flows, mean intensives) plus `n_hours`.
- Time dimension tables: `generate_series(lo, hi, INTERVAL 1 DAY)` over the min/max of *every*
  fact that joins them; calendar attributes (`year`, `month` as 'YYYY-MM', `week` as the Monday,
  `season`, domain periods) computed once there.

## Guards: section 99

Every invariant the layer relies on becomes a row in one checks table; the build fails with all
violated names at once. Cover at least:
- grain uniqueness of every fact, aggregate and bridge
- every fk/rollup key finds its dimension row (ANTI JOIN), unless the join is `optional`
- time dimensions: one row per period, no gaps, every fact date inside
- bridge weights sum to 1 per from key
- aggregates keep everything (`sum(n_events) = count(*)` of the source)
- coverage expectations stated in the docs (e.g. "every cell has weather", "400 districts × 2 years")
- derived values recomputed (pooled rate = lost / wintered)

```sql
-- ---------------------------------------------------------------------------
-- 99) CHECKS: the build fails when a grain or a foreign key is violated
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TEMP TABLE build_checks AS
SELECT * FROM (
    SELECT 'fact_x grain' AS check_name,
           (SELECT count(*) FROM (SELECT k1, k2 FROM fact_x GROUP BY ALL HAVING count(*) > 1)) AS bad
    UNION ALL SELECT 'fact_x -> dim_y',
           (SELECT count(*) FROM fact_x f ANTI JOIN dim_y d USING (k1))
    UNION ALL SELECT 'dim_date: one row per day, no gaps',
           (SELECT count(*) - (max(date) - min(date) + 1) + (count(*) - count(DISTINCT date)) FROM dim_date)
    UNION ALL SELECT 'bridge weights sum to 1',
           (SELECT count(*) FROM (SELECT k FROM bridge_x GROUP BY 1 HAVING abs(sum(weight) - 1) > 1e-9))
);

SELECT CASE WHEN count(*) > 0
            THEN error('build checks failed: ' || string_agg(check_name || ' (' || bad || ')', '; '))
       END
FROM build_checks
WHERE bad <> 0;

DROP TABLE build_checks;
```

When extending a pack, add the new tables to the existing cross-table checks (e.g. the union of
daily facts in "daily facts -> dim_date") instead of only appending new rows.

## Size

Keep big raw series as DuckDB tables, not views over Parquet with relative paths: a view's
relative path resolves against the directory the app runs from, which differs between build and
app (decision 6 of 2026-10-07). Drop staging tables at the end so the database holds only what the
layer lists.
