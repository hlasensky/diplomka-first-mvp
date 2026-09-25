-- build.sql (senger)
-- Builds a ROLAP star schema for the BeeObserver dataset in DuckDB.
-- Source: Senger et al., Data in Brief 52 (2024) 110015; Zenodo 10.5281/zenodo.10407693
-- Run:    DATASET=senger uv run python scripts/build_db.py
--         Paths are relative to data/raw/senger/ = the unzipped bob_publication_data folder.
--
-- Optional: provide states.geojson (German federal states) and enable section 4b.

-- ---------------------------------------------------------------------------
-- 1) STAGING: hourly preprocessed data, all years
--    `key` identifies the sensor kit = colony; one file per colony and year.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE stg_h AS
SELECT
    "key"::INTEGER AS colony_key,
    * EXCLUDE ("key") RENAME ("time" AS ts)
FROM read_csv(
    'years/*/preprocessed/*_h/*.csv',
    union_by_name = true,
    nullstr = 'NA'
);

-- ---------------------------------------------------------------------------
-- 2) EVENTS: from the beekeepers' inspection records.
--    The precomputed *.last / *.next timestamp columns of the sensor files are empty
--    in the hourly aggregates, so events are taken from inspections.csv directly:
--    a Boolean inspection category answered "yes" (value = '1') is one event.
--    Category -> event type mapping (inspections/categories.csv, German translation):
--      1012 'Bau von Weiselzellen' -> queencell    476 'Fütterung'   -> feeding
--       495 'Honig'                -> honey         595 'Behandlung' -> treatment
--       769 'Volk eingegangen'     -> died
--       968 'Schwarm abgegangen', 183 'geschwärmt'  -> swarming
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE fact_event AS
SELECT DISTINCT
    "key"::INTEGER AS colony_key,
    CASE category_id
        WHEN 1012 THEN 'queencell'
        WHEN 476  THEN 'feeding'
        WHEN 495  THEN 'honey'
        WHEN 595  THEN 'treatment'
        WHEN 769  THEN 'died'
        ELSE 'swarming'
    END            AS event_type,
    created_at     AS event_ts
FROM read_csv('inspections/inspections.csv', nullstr = ['NA', 'NULL'])
WHERE category_id IN (1012, 476, 495, 595, 769, 968, 183)
  AND "value" = '1'
  AND deleted_at IS NULL
  AND "key" IN (SELECT colony_key FROM stg_h);

CREATE OR REPLACE TABLE dim_event_type AS
SELECT * FROM (VALUES
    ('queencell', 'colony',    'queen cell found'),
    ('swarming',  'colony',    'swarming'),
    ('died',      'colony',    'colony death'),
    ('feeding',   'beekeeper', 'supplementary feeding'),
    ('honey',     'beekeeper', 'honey harvest'),
    ('treatment', 'beekeeper', 'treatment')
) AS t(event_type, cause_class, label);

-- ---------------------------------------------------------------------------
-- 3) TIME
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE dim_time AS
SELECT
    ts                            AS time_key,
    ts::DATE                      AS date,
    hour(ts)                      AS hour,
    isodow(ts)                    AS day_of_week,
    date_trunc('week', ts)::DATE  AS week,
    strftime(ts, '%Y-%m')         AS month,
    year(ts)                      AS year,
    CASE
        WHEN month(ts) IN (12, 1, 2) THEN 'winter'
        WHEN month(ts) IN (3, 4, 5)  THEN 'spring'
        WHEN month(ts) IN (6, 7, 8)  THEN 'summer'
        ELSE 'autumn'
    END                           AS season,
    month(ts) BETWEEN 4 AND 8     AS is_beekeeping_season
FROM (
    SELECT unnest(generate_series(lo, hi, INTERVAL 1 HOUR)) AS ts
    FROM (
        SELECT date_trunc('hour', min(ts)) AS lo,
               date_trunc('hour', max(ts)) AS hi
        FROM stg_h
    )
);

-- ---------------------------------------------------------------------------
-- 4) GEOGRAPHY: state -> cell (0.1 degree, ~5-7 km) -> colony
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE dim_cell AS
SELECT DISTINCT
    printf('%.1f_%.1f', lat, lon) AS cell_id,
    lat,
    lon,
    NULL::VARCHAR                 AS state
FROM stg_h
WHERE lat IS NOT NULL AND lon IS NOT NULL;

-- 4b) OPTIONAL: assign the federal state by point-in-polygon.
--     Check NULLs afterwards (rounded points may fall outside a polygon) and fix manually.
-- INSTALL spatial; LOAD spatial;
-- UPDATE dim_cell
-- SET state = s.name                      -- TODO: column name depends on the GeoJSON
-- FROM ST_Read('states.geojson') AS s
-- WHERE ST_Contains(s.geom, ST_Point(dim_cell.lon, dim_cell.lat));

CREATE OR REPLACE TABLE dim_colony AS
SELECT
    s.colony_key,
    s.cell_id,
    c.state,
    count(*) OVER (PARTITION BY s.cell_id) AS colonies_in_cell,
    s.colony_key IN (SELECT colony_key FROM fact_event WHERE event_type = 'swarming') AS ever_swarmed,
    s.colony_key IN (SELECT colony_key FROM fact_event WHERE event_type = 'died')     AS died
FROM (
    SELECT colony_key, any_value(printf('%.1f_%.1f', lat, lon)) AS cell_id
    FROM stg_h
    WHERE lat IS NOT NULL AND lon IS NOT NULL
    GROUP BY colony_key
) AS s
JOIN dim_cell AS c USING (cell_id);

-- ---------------------------------------------------------------------------
-- 5) MAIN FACT: one row = one colony x one hour
--    weight_kg_noOutlier is relative (cumulative sum starting at 0 per file),
--    so only increments are stored, never compared as levels.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE fact_hive_hourly AS
SELECT
    colony_key,
    date_trunc('hour', ts) AS time_key,
    weight_kg,
    CASE WHEN ts - lag(ts) OVER w = INTERVAL 1 HOUR
         THEN weight_kg_noOutlier - lag(weight_kg_noOutlier) OVER w
    END                    AS weight_gain_kg,
    CASE WHEN ts - lag(ts) OVER w = INTERVAL 1 HOUR
         THEN weight_kg - lag(weight_kg) OVER w
    END                    AS weight_change_raw_kg,
    t_i_1, t_i_2, t_i_3, t_i_4, t_i_5,
    t_o,
    t_i_3 - t_o            AS t_diff_in_out,
    h,
    t                      AS t_bme,
    p
FROM stg_h
WINDOW w AS (PARTITION BY colony_key, year(ts) ORDER BY ts);

-- ---------------------------------------------------------------------------
-- 6) SENSOR POSITION: drill-down from colony to individual sensors
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE dim_sensor_position AS
SELECT * FROM (VALUES
    ('t_i_1', 'edge',    1),
    ('t_i_2', 'between', 2),
    ('t_i_3', 'center',  3),
    ('t_i_4', 'between', 4),
    ('t_i_5', 'edge',    5),
    ('t_o',   'outside', NULL)
) AS t(sensor_pos, zone, slot);

CREATE OR REPLACE VIEW fact_temperature AS
UNPIVOT (
    SELECT colony_key, time_key, t_i_1, t_i_2, t_i_3, t_i_4, t_i_5, t_o
    FROM fact_hive_hourly
)
ON t_i_1, t_i_2, t_i_3, t_i_4, t_i_5, t_o
INTO NAME sensor_pos VALUE temp_c;

-- ---------------------------------------------------------------------------
-- 7) DAILY AGGREGATE: input for the anomaly detector
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE agg_colony_daily AS
SELECT
    f.colony_key,
    t.date,
    sum(f.weight_gain_kg)       AS weight_gain_kg,
    min(f.weight_change_raw_kg) AS max_hourly_drop_raw_kg,
    avg(f.t_i_3)                AS t_center_avg,
    stddev_samp(f.t_i_3)        AS t_center_std,
    avg(f.t_diff_in_out)        AS t_diff_avg,
    avg(f.h)                    AS h_avg,
    count(*)                    AS n_hours
FROM fact_hive_hourly AS f
JOIN dim_time AS t USING (time_key)
GROUP BY f.colony_key, t.date;

-- Staging is no longer needed by the agent.
DROP TABLE stg_h;
