-- build.sql (multi-senger)
-- BeeObserver hive sensors (core) + context facts (weather, phenology, vegetation, crops, national stats).
-- Source of the hive data: Senger et al., Data in Brief 52 (2024) 110015; Zenodo 10.5281/zenodo.10407693
-- Run:    DATASET=multi-senger uv run python scripts/build_db.py
--         Paths are relative to data/raw/multi-senger/ (see MANIFEST.json there).
-- Data checks behind the decisions below: docs/decisions.md, 2026-10-07.

-- ---------------------------------------------------------------------------
-- 1) STAGING: minute sensor data, all years (bob/years/<year>/preprocessed/<year>_m/<key>.csv)
--    One file per colony (`key` = sensor kit) and year. Timestamps are naive UTC.
--    Only sensor columns are kept; events come from inspections.csv (section 2).
--    Some files hold a column that is entirely NA, which makes the union infer VARCHAR,
--    so the sensor columns are typed explicitly.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TEMP TABLE stg_m_raw AS
SELECT
    "key"::INTEGER              AS colony_key,
    "X"::BIGINT                 AS seq,          -- running row number of the source series
    "time"                      AS ts_raw,
    t_i_1, t_i_2, t_i_3, t_i_4, t_i_5, t_o,
    t                           AS t_bme,
    h, p,
    weight_kg,
    weight_delta,
    weight_delta_noOutlier      AS weight_delta_no_outlier,
    weight_kg_noOutlier         AS weight_kg_no_outlier,
    outlier_lim                 AS is_outlier,
    lat, lon
FROM read_csv(
    'bob/years/*/preprocessed/*_m/*.csv',
    union_by_name = true,
    nullstr = 'NA',
    types = {
        'time': 'TIMESTAMP', 'key': 'VARCHAR', 'X': 'BIGINT',
        't_i_1': 'DOUBLE', 't_i_2': 'DOUBLE', 't_i_3': 'DOUBLE', 't_i_4': 'DOUBLE', 't_i_5': 'DOUBLE',
        't_o': 'DOUBLE', 't': 'DOUBLE', 'h': 'DOUBLE', 'p': 'DOUBLE', 'weight_kg': 'DOUBLE',
        'weight_delta': 'DOUBLE', 'weight_delta_noOutlier': 'DOUBLE', 'weight_kg_noOutlier': 'DOUBLE',
        'outlier_lim': 'BOOLEAN', 'lat': 'DOUBLE', 'lon': 'DOUBLE'
    }
);

-- 1a) Spring DST artefact. On the days Germany switches to summer time the source labels the
--     minutes 02:00-02:59 (UTC) as 01:00-01:59 again: hour 01 occurs twice, hour 02 is missing.
--     The running number `seq` (per colony and year file) keeps the true order: within hour 01
--     of those days, a row belongs to the second block when an earlier row (lower seq) already
--     carried the same or a later minute, i.e. the clock jumped back. Matching on duplicates
--     alone would miss second-block minutes whose first-block twin is missing.
CREATE OR REPLACE TEMP TABLE stg_m AS
SELECT
    * EXCLUDE (ts_raw, prev_max_ts),
    CASE WHEN prev_max_ts >= ts_raw THEN ts_raw + INTERVAL 1 HOUR ELSE ts_raw END AS ts,
    coalesce(prev_max_ts >= ts_raw, false) AS ts_shifted_dst
FROM (
    SELECT
        *,
        CASE WHEN ts_raw::DATE IN (DATE '2020-03-29', DATE '2021-03-28', DATE '2022-03-27')
                  AND hour(ts_raw) = 1
             THEN max(ts_raw) OVER (
                      PARTITION BY colony_key, ts_raw::DATE, hour(ts_raw)
                      ORDER BY seq ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)
        END AS prev_max_ts
    FROM stg_m_raw
);

-- 1b) Guard: after the fix every (colony, minute) is unique; otherwise the build fails.
SELECT CASE WHEN count(*) > 0
            THEN error('stg_m: ' || count(*) || ' duplicate (colony_key, ts) rows left after the DST fix')
       END
FROM (SELECT colony_key, ts FROM stg_m GROUP BY ALL HAVING count(*) > 1);

DROP TABLE stg_m_raw;

-- ---------------------------------------------------------------------------
-- 2) HIVE FACTS
--    weight_kg_no_outlier is relative (cumulative sum restarting at 0 in every year file),
--    so only its increments are used, never its level.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE fact_hive_minute AS
SELECT
    colony_key,
    ts,
    t_i_1, t_i_2, t_i_3, t_i_4, t_i_5, t_o, t_bme, h, p,
    weight_kg,
    weight_delta_no_outlier,
    is_outlier,
    ts_shifted_dst
FROM stg_m
ORDER BY colony_key, ts;

-- Hourly means of the corrected minutes (the published hourly files are the same means,
-- but without the DST fix). n_minutes = data completeness of the hour.
CREATE OR REPLACE TABLE fact_hive_hourly AS
WITH h AS (
    SELECT
        colony_key,
        date_trunc('hour', ts)      AS time_key,
        count(*)                    AS n_minutes,
        avg(weight_kg)              AS weight_kg,
        avg(weight_kg_no_outlier)   AS weight_rel_kg,
        avg(t_i_1) AS t_i_1, avg(t_i_2) AS t_i_2, avg(t_i_3) AS t_i_3,
        avg(t_i_4) AS t_i_4, avg(t_i_5) AS t_i_5,
        avg(t_o)   AS t_o, avg(t_bme) AS t_bme, avg(h) AS h, avg(p) AS p
    FROM stg_m
    GROUP BY ALL
)
SELECT
    colony_key,
    time_key,
    n_minutes,
    weight_kg,
    CASE WHEN time_key - lag(time_key) OVER w = INTERVAL 1 HOUR
         THEN weight_rel_kg - lag(weight_rel_kg) OVER w
    END                    AS weight_gain_kg,
    CASE WHEN time_key - lag(time_key) OVER w = INTERVAL 1 HOUR
         THEN weight_kg - lag(weight_kg) OVER w
    END                    AS weight_change_raw_kg,
    t_i_1, t_i_2, t_i_3, t_i_4, t_i_5,
    t_o,
    t_i_3 - t_o            AS t_diff_in_out,
    h,
    t_bme,
    p
FROM h
-- the relative weight restarts in every year file, so increments never cross a year boundary
WINDOW w AS (PARTITION BY colony_key, year(time_key) ORDER BY time_key);

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
-- 3) EVENTS from the beekeepers' inspection records (same mapping as the senger pack):
--    a Boolean inspection category answered "yes" (value = '1') is one event.
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
FROM read_csv('bob/inspections/inspections.csv', nullstr = ['NA', 'NULL'])
WHERE category_id IN (1012, 476, 495, 595, 769, 968, 183)
  AND "value" = '1'
  AND deleted_at IS NULL
  AND "key" IN (SELECT DISTINCT colony_key FROM stg_m);

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
-- 4) WEATHER: Open-Meteo archive (ERA5), hourly, UTC, one file per cell (3 metadata lines).
--    Radiation is the mean of the preceding hour; temperature is instantaneous.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE fact_weather AS
SELECT
    regexp_extract(filename, '([^/]+)\.csv$', 1)   AS cell_id,
    "time"::TIMESTAMP                              AS time_key,
    "temperature_2m (°C)"                          AS air_temp_c,
    "precipitation (mm)"                           AS precip_mm,
    "rain (mm)"                                    AS rain_mm,
    "wind_speed_10m (km/h)"                        AS wind_kmh,
    "shortwave_radiation (W/m²)"                   AS radiation_wm2,
    "relative_humidity_2m (%)"                     AS air_rh_pct
FROM read_csv('weather/*.csv', skip = 3, header = true, filename = true);

CREATE OR REPLACE TABLE agg_weather_daily AS
SELECT
    cell_id,
    time_key::DATE                       AS date,
    avg(air_temp_c)                      AS air_temp_avg_c,
    min(air_temp_c)                      AS air_temp_min_c,
    max(air_temp_c)                      AS air_temp_max_c,
    sum(precip_mm)                       AS precip_mm,
    count(*) FILTER (WHERE precip_mm >= 0.1) AS rain_hours,
    sum(radiation_wm2) / 1000            AS radiation_kwh_m2,
    avg(wind_kmh)                        AS wind_avg_kmh,
    avg(air_rh_pct)                      AS air_rh_avg_pct,
    count(*)                             AS n_hours
FROM fact_weather
GROUP BY ALL;

-- ---------------------------------------------------------------------------
-- 5) TIME: built in section 12, after all facts, so it covers every date they use
-- ---------------------------------------------------------------------------

-- ---------------------------------------------------------------------------
-- 6) GEOGRAPHY: colony -> cell (0.1 degree, rounded) -> district (Kreis) -> state
--    Districts and states: BKG VG250 (31.12.), EPSG:25832, land areas only (GF = 4).
--    A cell centre is rounded to 0.1 degree, so the hive lies anywhere in the box
--    centre +- 0.05 degree; 27 of 34 cells are within 7 km of a district border.
--    bridge_cell_district therefore weights every district by its share of the cell box
--    (German part only, weights sum to 1 per cell).
-- ---------------------------------------------------------------------------
INSTALL spatial;
LOAD spatial;

CREATE OR REPLACE TEMP TABLE stg_krs AS
SELECT AGS AS district_id, GEN AS gen, BEZ AS district_type, geom
FROM st_read('geo/vg250_ebenen_1231/DE_VG250.gpkg', layer = 'vg250_krs')
WHERE GF = 4;

CREATE OR REPLACE TABLE dim_country AS
SELECT * FROM (VALUES ('DE', 'Germany')) AS t(country, country_name);

CREATE OR REPLACE TABLE dim_state AS
SELECT AGS AS state_id, GEN AS state, 'DE' AS country
FROM st_read('geo/vg250_ebenen_1231/DE_VG250.gpkg', layer = 'vg250_lan')
WHERE GF = 4;

-- district names are not unique (e.g. Regensburg city and district): add the type when needed
CREATE OR REPLACE TABLE dim_district AS
SELECT
    k.district_id,
    CASE WHEN count(*) OVER (PARTITION BY k.gen) > 1
         THEN k.gen || ' (' || k.district_type || ')'
         ELSE k.gen
    END                               AS district,
    k.district_type,
    left(k.district_id, 2)            AS state_id,
    s.state,
    round(st_area(k.geom) / 1e6, 1)   AS area_km2
FROM stg_krs AS k
JOIN dim_state AS s ON s.state_id = left(k.district_id, 2);

CREATE OR REPLACE TEMP TABLE stg_cell AS
SELECT DISTINCT
    printf('%.1f_%.1f', lat, lon) AS cell_id,
    lat,
    lon,
    -- EPSG:4326 in DuckDB spatial uses (lat, lon) axis order
    st_transform(st_makeenvelope(lat - 0.05, lon - 0.05, lat + 0.05, lon + 0.05),
                 'EPSG:4326', 'EPSG:25832') AS box
FROM stg_m;

CREATE OR REPLACE TABLE bridge_cell_district AS
WITH o AS (
    SELECT c.cell_id, k.district_id,
           st_area(st_intersection(c.box, k.geom)) / st_area(c.box) AS box_share
    FROM stg_cell AS c
    JOIN stg_krs AS k ON st_intersects(c.box, k.geom)
)
SELECT
    cell_id,
    district_id,
    box_share,
    box_share / sum(box_share) OVER (PARTITION BY cell_id) AS weight
FROM o
WHERE box_share >= 0.005;   -- drop slivers from border-line touches

CREATE OR REPLACE TABLE dim_cell AS
SELECT
    c.cell_id,
    c.lat,
    c.lon,
    m.district_id,
    d.district,
    d.state_id,
    d.state,
    m.weight                                   AS district_weight,
    (SELECT count(*) FROM bridge_cell_district b WHERE b.cell_id = c.cell_id) AS n_districts,
    (SELECT round(sum(box_share), 3) FROM bridge_cell_district b WHERE b.cell_id = c.cell_id) AS share_in_germany
FROM stg_cell AS c
JOIN (SELECT cell_id, arg_max(district_id, weight) AS district_id, max(weight) AS weight
      FROM bridge_cell_district GROUP BY cell_id) AS m USING (cell_id)
JOIN dim_district AS d USING (district_id);

CREATE OR REPLACE TABLE dim_colony AS
SELECT
    s.colony_key,
    s.cell_id,
    c.district,
    c.state,
    'DE'                                   AS country,
    count(*) OVER (PARTITION BY s.cell_id) AS colonies_in_cell,
    s.colony_key IN (SELECT colony_key FROM fact_event WHERE event_type = 'swarming') AS ever_swarmed,
    s.colony_key IN (SELECT colony_key FROM fact_event WHERE event_type = 'died')     AS died
FROM (
    SELECT colony_key, any_value(printf('%.1f_%.1f', lat, lon)) AS cell_id
    FROM stg_m
    GROUP BY colony_key
) AS s
JOIN dim_cell AS c USING (cell_id);

-- ---------------------------------------------------------------------------
-- 7) DAILY AGGREGATE per colony: input for the anomaly detector
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE agg_colony_daily AS
SELECT
    f.colony_key,
    f.time_key::DATE            AS date,
    sum(f.weight_gain_kg)       AS weight_gain_kg,
    min(f.weight_change_raw_kg) AS max_hourly_drop_raw_kg,
    avg(f.t_i_3)                AS t_center_avg,
    stddev_samp(f.t_i_3)        AS t_center_std,
    avg(f.t_diff_in_out)        AS t_diff_avg,
    avg(f.h)                    AS h_avg,
    count(*)                    AS n_hours,
    sum(f.n_minutes)            AS n_minutes
FROM fact_hive_hourly AS f
GROUP BY ALL;

-- ---------------------------------------------------------------------------
-- 8) VEGETATION: MODIS MOD13Q1 NDVI, 250 m, 16-day composites, pixel at the cell centre.
--    `date` is the first day of the composite period.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE fact_vegetation AS
SELECT
    regexp_extract(filename, '([^/]+)\.csv$', 1) AS cell_id,
    "date"::DATE                                 AS date,
    ndvi
FROM read_csv('ndvi/*.csv', filename = true)
WHERE ndvi_raw > -3000;   -- fill value

-- ---------------------------------------------------------------------------
-- 9) PHENOLOGY: DWD annual reporters, phase 5 = beginning of flowering.
--    Quality byte (Eintrittsdatum_QB): 1 no objection, 2 corrected, 3 objection rejected
--    are kept; 5 doubtful and 8 incorrect are dropped.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE dim_plant AS
SELECT * FROM (VALUES
    (205, 'Winterraps',   'winter oilseed rape', 'crop', 'spring', true),
    (120, 'Löwenzahn',    'dandelion',           'herb', 'spring', true),
    (121, 'Robinie',      'black locust',        'tree', 'early summer', true),
    (130, 'Sommer-Linde', 'large-leaved lime',   'tree', 'summer', true)
) AS t(plant_id, plant_de, plant, plant_group, flow_period, is_bee_forage);

CREATE OR REPLACE TABLE dim_station AS
SELECT
    trim(column00)::INTEGER           AS station_id,
    trim(column01)                    AS station_name,
    trim(column02)::DOUBLE            AS lat,
    trim(column03)::DOUBLE            AS lon,
    trim(column04)::INTEGER           AS elevation_m,
    nullif(trim(column09), '')        AS closed_on,
    trim(column10)                    AS state
FROM read_csv('phenology/stations.txt', delim = ';', header = false, skip = 1,
              null_padding = true, quote = '',
              columns = {'column00': 'VARCHAR', 'column01': 'VARCHAR', 'column02': 'VARCHAR',
                         'column03': 'VARCHAR', 'column04': 'VARCHAR', 'column05': 'VARCHAR',
                         'column06': 'VARCHAR', 'column07': 'VARCHAR', 'column08': 'VARCHAR',
                         'column09': 'VARCHAR', 'column10': 'VARCHAR', 'column11': 'VARCHAR',
                         'column12': 'VARCHAR'});

CREATE OR REPLACE TABLE fact_bloom_phenology AS
SELECT
    trim(column0)::INTEGER                          AS station_id,
    trim(column1)::INTEGER                          AS year,
    trim(column3)::INTEGER                          AS plant_id,
    strptime(trim(column5), '%Y%m%d')::DATE         AS bloom_date,
    trim(column7)::INTEGER                          AS bloom_doy,
    trim(column6)::INTEGER                          AS quality_byte
FROM read_csv(['phenology/Winterraps.txt', 'phenology/Loewenzahn.txt',
               'phenology/Robinie.txt', 'phenology/Sommer-Linde.txt'],
              delim = ';', header = false, skip = 1,
              null_padding = true, quote = '',
              columns = {'column0': 'VARCHAR', 'column1': 'VARCHAR', 'column2': 'VARCHAR',
                         'column3': 'VARCHAR', 'column4': 'VARCHAR', 'column5': 'VARCHAR',
                         'column6': 'VARCHAR', 'column7': 'VARCHAR', 'column8': 'VARCHAR',
                         'column9': 'VARCHAR'})
WHERE trim(column4) = '5'
  AND trim(column6) IN ('1', '2', '3')
  AND trim(column1)::INTEGER BETWEEN 2016 AND 2022
  AND trim(column0)::INTEGER IN (SELECT station_id FROM dim_station);

-- Bloom onset per cell: median over the stations within 25 km (great-circle distance).
CREATE OR REPLACE TABLE agg_cell_bloom AS
WITH d AS (
    SELECT c.cell_id, s.station_id,
           2 * 6371 * asin(sqrt(
               pow(sin(radians(s.lat - c.lat) / 2), 2)
               + cos(radians(c.lat)) * cos(radians(s.lat)) * pow(sin(radians(s.lon - c.lon) / 2), 2)
           )) AS dist_km
    FROM dim_cell AS c CROSS JOIN dim_station AS s
)
SELECT
    d.cell_id,
    f.year,
    f.plant_id,
    round(median(f.bloom_doy))::INTEGER                                   AS bloom_doy,
    make_date(f.year, 1, 1) + (round(median(f.bloom_doy))::INTEGER - 1)  AS bloom_date,
    min(f.bloom_doy)                                                      AS bloom_doy_min,
    max(f.bloom_doy)                                                      AS bloom_doy_max,
    count(*)                                                              AS n_stations,
    round(min(d.dist_km), 1)                                              AS nearest_station_km
FROM d
JOIN fact_bloom_phenology AS f USING (station_id)
WHERE d.dist_km <= 25
GROUP BY d.cell_id, f.year, f.plant_id;

-- ---------------------------------------------------------------------------
-- 10) CROPS by district (Regionalstatistik, manual CSV export, latin-1, header/footer lines)
--     41141-02-02-4: arable land by crop (ha), farm structure survey years 2016 and 2020;
--                    areas are counted at the farm's seat (Betriebssitzprinzip).
--     41241-01-03-4: yields (dt/ha) 2016-2025; Berlin, Bremen, Hamburg have no table.
--     Cell symbols: '-' nothing (0), '.' unknown or confidential, '/' not reliable enough,
--     '...' not yet available, 'x' locked -> NULL with value_status.
--     Berlin and Hamburg appear only with their state code (11, 02).
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE dim_crop AS
SELECT * FROM (VALUES
    ('arable_total',  'Ackerland insgesamt',              'arable land total',      NULL,           false),
    ('cereals',       'Getreide',                         'cereals',                'arable_total', false),
    ('wheat',         'Weizen',                           'wheat',                  'cereals',      false),
    ('winter_wheat',  'Winterweizen',                     'winter wheat',           'wheat',        false),
    ('rye',           'Roggen und Wintermenggetreide',    'rye and winter maslin',  'cereals',      false),
    ('triticale',     'Triticale',                        'triticale',              'cereals',      false),
    ('barley',        'Gerste',                           'barley',                 'cereals',      false),
    ('winter_barley', 'Wintergerste',                     'winter barley',          'barley',       false),
    ('spring_barley', 'Sommergerste',                     'spring barley',          'barley',       false),
    ('oats',          'Hafer',                            'oats',                   'cereals',      false),
    ('grain_maize',   'Körnermais/Corn-Cob-Mix',          'grain maize',            'cereals',      false),
    ('other_cereals', 'Sonstiges Getreide',               'other cereals',          'cereals',      false),
    ('green_fodder',  'Pflanzen zur Grünernte',           'plants harvested green', 'arable_total', false),
    ('silage_maize',  'Silomais/Grünmais',                'silage maize',           'green_fodder', false),
    ('sugar_beet',    'Zuckerrüben',                      'sugar beet',             'arable_total', false),
    ('potatoes',      'Kartoffeln',                       'potatoes',               'arable_total', false),
    ('oilseeds',      'Ölfrüchte',                        'oilseeds',               'arable_total', true),
    ('winter_rape',   'Winterraps',                       'winter oilseed rape',    'oilseeds',     true),
    ('pulses',        'Hülsenfrüchte',                    'pulses',                 'arable_total', true)
) AS t(crop, crop_de, crop_label, parent_crop, is_bee_forage);

CREATE OR REPLACE MACRO crop_value(v) AS
    CASE WHEN trim(v) = '-' THEN 0
         WHEN regexp_full_match(trim(v), '[0-9]+(,[0-9]+)?') THEN replace(trim(v), ',', '.')::DOUBLE
    END;
CREATE OR REPLACE MACRO crop_status(v) AS
    CASE WHEN trim(v) = '-' THEN 'zero'
         WHEN regexp_full_match(trim(v), '[0-9]+(,[0-9]+)?') THEN 'value'
         WHEN trim(v) = '.' THEN 'suppressed'
         WHEN trim(v) = '/' THEN 'unreliable'
         WHEN trim(v) = '...' THEN 'not_yet_available'
         ELSE 'locked'
    END;

CREATE OR REPLACE TEMP TABLE stg_crop_lines AS
SELECT filename, string_split(line, ';') AS f
FROM read_csv('crops/*.csv', columns = {'line': 'VARCHAR'}, delim = '|', header = false,
              quote = '', escape = '', auto_detect = false, encoding = 'latin-1',
              filename = true, ignore_errors = true);

CREATE OR REPLACE TABLE fact_crop_area AS
WITH r AS (
    SELECT
        CASE WHEN f[1] IN ('02', '11') THEN f[1] || '000' ELSE f[1] END AS district_id,
        regexp_extract(filename, '_([0-9]{4})\.csv$', 1)::INTEGER     AS year,
        f
    FROM stg_crop_lines
    WHERE filename LIKE '%41141-02-02-4_%'
      AND regexp_full_match(f[1], '[0-9]{5}|02|11')
), u AS (
    SELECT district_id, year, c.crop, f[c.idx] AS v
    FROM r
    CROSS JOIN (VALUES
        ('arable_total', 3), ('cereals', 4), ('wheat', 5), ('winter_wheat', 6), ('rye', 7),
        ('triticale', 8), ('barley', 9), ('oats', 10), ('grain_maize', 11), ('other_cereals', 12),
        ('green_fodder', 13), ('silage_maize', 14), ('sugar_beet', 15), ('potatoes', 16),
        ('oilseeds', 17), ('winter_rape', 18), ('pulses', 19)
    ) AS c(crop, idx)
)
SELECT district_id, year, crop, crop_value(v) AS area_ha, crop_status(v) AS value_status
FROM u
WHERE district_id IN (SELECT district_id FROM dim_district);

CREATE OR REPLACE TABLE fact_crop_yield AS
WITH r AS (
    SELECT
        CASE WHEN f[2] IN ('02', '11') THEN f[2] || '000' ELSE f[2] END AS district_id,
        f[1]::INTEGER AS year,
        f
    FROM stg_crop_lines
    WHERE filename LIKE '%41241-01-03-4_%'
      AND regexp_full_match(f[1], '[0-9]{4}')
      AND regexp_full_match(f[2], '[0-9]{5}|02|11')
), u AS (
    SELECT district_id, year, c.crop, f[c.idx] AS v
    FROM r
    CROSS JOIN (VALUES
        ('winter_wheat', 4), ('rye', 5), ('winter_barley', 6), ('spring_barley', 7), ('oats', 8),
        ('triticale', 9), ('potatoes', 10), ('sugar_beet', 11), ('winter_rape', 12), ('silage_maize', 13)
    ) AS c(crop, idx)
)
SELECT district_id, year, crop, crop_value(v) AS yield_dt_ha, crop_status(v) AS value_status
FROM u
WHERE district_id IN (SELECT district_id FROM dim_district);

-- Crop context per cell, weighted over the districts of the cell box (bridge weights).
-- Districts without a value are left out; *_coverage = weight share that had a value.
CREATE OR REPLACE TABLE agg_cell_crop AS
WITH a AS (
    SELECT b.cell_id, x.year, x.crop,
           100 * sum(b.weight * x.area_ha) / sum(b.weight * t.area_ha) AS crop_share_pct,
           sum(b.weight)                                               AS share_coverage
    FROM bridge_cell_district AS b
    JOIN fact_crop_area AS x USING (district_id)
    JOIN fact_crop_area AS t ON t.district_id = x.district_id AND t.year = x.year AND t.crop = 'arable_total'
    WHERE x.area_ha IS NOT NULL AND t.area_ha > 0 AND x.crop <> 'arable_total'
    GROUP BY ALL
), y AS (
    SELECT b.cell_id, x.year, x.crop,
           sum(b.weight * x.yield_dt_ha) / sum(b.weight) AS yield_w_dt_ha,
           sum(b.weight)                                 AS yield_coverage
    FROM bridge_cell_district AS b
    JOIN fact_crop_yield AS x USING (district_id)
    WHERE x.yield_dt_ha IS NOT NULL AND x.yield_dt_ha > 0
    GROUP BY ALL
)
SELECT
    cell_id, year, crop,
    round(crop_share_pct, 2)  AS crop_share_pct,
    round(share_coverage, 3)  AS share_coverage,
    round(yield_w_dt_ha, 1)   AS yield_w_dt_ha,
    round(yield_coverage, 3)  AS yield_coverage
FROM a FULL JOIN y USING (cell_id, year, crop);

-- ---------------------------------------------------------------------------
-- 11) NATIONAL CONTEXT (Germany)
-- ---------------------------------------------------------------------------
-- FAOSTAT QCL: Bees = number of hives (Stocks), Natural honey = production (t)
CREATE OR REPLACE TABLE fact_country_bees AS
SELECT
    'DE'                                                      AS country,
    "Year"                                                    AS year,
    max("Value") FILTER (WHERE "Item" = 'Bees')::BIGINT       AS hives,
    max("Value") FILTER (WHERE "Item" = 'Natural honey')      AS honey_t
FROM read_csv('faostat/germany_bees.csv')
WHERE "Year" BETWEEN 2016 AND 2023
GROUP BY "Year";

-- Winter colony losses in Germany, transcribed from two literature sources (vault notes,
-- status candidate/unverified at build time). evidence = claim or page the number comes from.
--   DLR Mayen survey (Infobrief2022_10Honigernte, table p. 4):
--     loss_pct_mean   = Verlust1, mean of the individual beekeepers' loss rates
--     loss_pct_pooled = Verlust2, lost / wintered colonies summed per region (COLOSS-like)
--   COLOSS (grayHoneyBeeColony2022, Table 1): pooled total loss rate with 95 % CI.
CREATE OR REPLACE TABLE fact_winter_loss AS
SELECT * FROM (VALUES
    ('DE', '2019/20', 'DLR Mayen', 14969, 181652, 26691, 16.5, 14.7, NULL, NULL,
     'Infobrief2022_10Honigernte', 'C2 (rates); counts p. 4 table, OCR, not in a claim'),
    ('DE', '2020/21', 'DLR Mayen', 13835, 168595, 21699, 14.5, 12.9, NULL, NULL,
     'Infobrief2022_10Honigernte', 'C2 (rates); counts p. 4 table, OCR, not in a claim'),
    ('DE', '2021/22', 'DLR Mayen', 10492, 137145, 28643, 22.4, 20.9, NULL, NULL,
     'Infobrief2022_10Honigernte', 'C2'),
    ('DE', '2019/20', 'COLOSS',    10586, 123368, NULL, NULL, 18.4, 18.0, 18.8,
     'grayHoneyBeeColony2022', 'C2')
) AS t(country, bee_winter, survey, n_reports, colonies_wintered, colonies_lost,
       loss_pct_mean, loss_pct_pooled, ci_low_pct, ci_high_pct, citekey, evidence);

-- ---------------------------------------------------------------------------
-- 12) TIME DIMENSIONS (UTC): hour -> day -> year, day -> overwintering period
--     Every fact references the dimension of its own grain, never a finer one:
--       hourly facts      -> dim_time (one row per hour)
--       daily facts       -> dim_date (one row per day; a join of a daily fact to dim_time
--                            would multiply its rows by 24)
--       year facts        -> dim_year       (crops, phenology, national statistics)
--       winter facts      -> dim_bee_winter (national winter losses)
--     dim_time rolls up to dim_date, dim_date to dim_year and dim_bee_winter
--     (shrunken rollup dimensions with the same attribute values).
--     bee_winter labels the overwintering period Oct-Mar (e.g. '2019/20'), as in loss surveys.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TABLE dim_date AS
WITH r AS (
    SELECT least((SELECT min(ts)::DATE FROM stg_m),
                 (SELECT min(time_key)::DATE FROM fact_weather),
                 (SELECT min(date) FROM fact_vegetation))      AS lo,
           greatest((SELECT max(ts)::DATE FROM stg_m),
                    (SELECT max(time_key)::DATE FROM fact_weather),
                    (SELECT max(date) FROM fact_vegetation))   AS hi
), d AS (
    SELECT unnest(generate_series(lo, hi, INTERVAL 1 DAY))::DATE AS date FROM r
)
SELECT
    date,
    isodow(date)                    AS day_of_week,
    date_trunc('week', date)::DATE  AS week,
    strftime(date, '%Y-%m')         AS month,
    year(date)::INTEGER             AS year,
    dayofyear(date)                 AS day_of_year,
    CASE
        WHEN month(date) IN (12, 1, 2) THEN 'winter'
        WHEN month(date) IN (3, 4, 5)  THEN 'spring'
        WHEN month(date) IN (6, 7, 8)  THEN 'summer'
        ELSE 'autumn'
    END                             AS season,
    month(date) BETWEEN 4 AND 8     AS is_beekeeping_season,
    CASE
        WHEN month(date) >= 10 THEN year(date) || '/' || right((year(date) + 1)::VARCHAR, 2)
        WHEN month(date) <= 3  THEN (year(date) - 1) || '/' || right(year(date)::VARCHAR, 2)
    END                             AS bee_winter
FROM d;

-- hourly rows carry the attributes of their day (denormalised, so hourly queries need one join)
CREATE OR REPLACE TABLE dim_time AS
SELECT
    h.time_key,
    d.date,
    hour(h.time_key)                AS hour,
    d.day_of_week, d.week, d.month, d.year, d.day_of_year,
    d.season, d.is_beekeeping_season, d.bee_winter
FROM (
    SELECT unnest(generate_series(lo, hi, INTERVAL 1 HOUR)) AS time_key
    FROM (
        SELECT least((SELECT date_trunc('hour', min(ts)) FROM stg_m), (SELECT min(time_key) FROM fact_weather)) AS lo,
               greatest((SELECT date_trunc('hour', max(ts)) FROM stg_m), (SELECT max(time_key) FROM fact_weather)) AS hi
    )
) AS h
JOIN dim_date AS d ON d.date = h.time_key::DATE
ORDER BY h.time_key;

CREATE OR REPLACE TABLE dim_year AS
WITH y AS (
    SELECT DISTINCT year FROM dim_date
    UNION SELECT year FROM fact_crop_area
    UNION SELECT year FROM fact_crop_yield
    UNION SELECT year FROM fact_bloom_phenology
    UNION SELECT year FROM fact_country_bees
)
SELECT
    year::INTEGER                                                   AS year,
    year BETWEEN (SELECT min(year(ts)) FROM stg_m) AND (SELECT max(year(ts)) FROM stg_m) AS has_hive_data,
    year IN (SELECT year FROM fact_crop_area)                       AS is_farm_survey_year
FROM y
ORDER BY year;

CREATE OR REPLACE TABLE dim_bee_winter AS
WITH w AS (
    SELECT DISTINCT bee_winter FROM dim_date WHERE bee_winter IS NOT NULL
    UNION SELECT bee_winter FROM fact_winter_loss
)
SELECT
    bee_winter,
    left(bee_winter, 4)::INTEGER                                   AS start_year,
    make_date(left(bee_winter, 4)::INTEGER, 10, 1)                 AS winter_start,
    make_date(left(bee_winter, 4)::INTEGER + 1, 3, 31)             AS winter_end,
    -- hive data cover the whole winter (the data end on 2022-12-31, so 2022/23 is partial)
    make_date(left(bee_winter, 4)::INTEGER, 10, 1) >= (SELECT min(ts)::DATE FROM stg_m)
        AND make_date(left(bee_winter, 4)::INTEGER + 1, 3, 31) <= (SELECT max(ts)::DATE FROM stg_m)
                                                                   AS has_full_hive_data
FROM w
ORDER BY bee_winter;

-- ---------------------------------------------------------------------------
-- 99) CHECKS: the build fails when a grain or a foreign key is violated
-- ---------------------------------------------------------------------------
CREATE OR REPLACE TEMP TABLE build_checks AS
SELECT * FROM (
    SELECT 'fact_hive_hourly grain' AS check_name,
           (SELECT count(*) FROM (SELECT colony_key, time_key FROM fact_hive_hourly GROUP BY ALL HAVING count(*) > 1)) AS bad
    UNION ALL SELECT 'fact_hive_hourly minutes <= 60',
           (SELECT count(*) FROM fact_hive_hourly WHERE n_minutes > 60)
    UNION ALL SELECT 'fact_hive_hourly -> dim_time',
           (SELECT count(*) FROM fact_hive_hourly f ANTI JOIN dim_time t USING (time_key))
    UNION ALL SELECT 'dim_date: one row per day, no gaps',
           (SELECT count(*) - (max(date) - min(date) + 1) + (count(*) - count(DISTINCT date)) FROM dim_date)
    UNION ALL SELECT 'dim_time -> dim_date',
           (SELECT count(*) FROM dim_time t ANTI JOIN dim_date d USING (date))
    UNION ALL SELECT 'daily facts -> dim_date',
           (SELECT count(*) FROM (
                SELECT date FROM agg_colony_daily UNION ALL SELECT date FROM agg_weather_daily
                UNION ALL SELECT date FROM fact_vegetation) x ANTI JOIN dim_date USING (date))
    UNION ALL SELECT 'fact_weather grain',
           (SELECT count(*) FROM (SELECT cell_id, time_key FROM fact_weather GROUP BY ALL HAVING count(*) > 1))
    UNION ALL SELECT 'fact_weather -> dim_cell',
           (SELECT count(*) FROM fact_weather f ANTI JOIN dim_cell c USING (cell_id))
    UNION ALL SELECT 'fact_weather -> dim_time',
           (SELECT count(*) FROM fact_weather f ANTI JOIN dim_time t USING (time_key))
    UNION ALL SELECT 'every cell has weather',
           (SELECT count(*) FROM dim_cell c ANTI JOIN (SELECT DISTINCT cell_id FROM fact_weather) w USING (cell_id))
    UNION ALL SELECT 'every cell has NDVI',
           (SELECT count(*) FROM dim_cell c ANTI JOIN (SELECT DISTINCT cell_id FROM fact_vegetation) v USING (cell_id))
    UNION ALL SELECT 'every colony has a cell and a district',
           (SELECT count(*) FROM dim_colony WHERE cell_id IS NULL OR district IS NULL)
    UNION ALL SELECT 'bridge weights sum to 1',
           (SELECT count(*) FROM (SELECT cell_id FROM bridge_cell_district GROUP BY 1 HAVING abs(sum(weight) - 1) > 1e-9))
    UNION ALL SELECT 'fact_event -> dim_colony',
           (SELECT count(*) FROM fact_event e ANTI JOIN dim_colony c USING (colony_key))
    UNION ALL SELECT 'fact_crop_area grain',
           (SELECT count(*) FROM (SELECT district_id, year, crop FROM fact_crop_area GROUP BY ALL HAVING count(*) > 1))
    UNION ALL SELECT 'fact_crop_yield grain',
           (SELECT count(*) FROM (SELECT district_id, year, crop FROM fact_crop_yield GROUP BY ALL HAVING count(*) > 1))
    UNION ALL SELECT 'crop area: 400 districts x 2 years',
           (SELECT abs(count(DISTINCT (district_id, year)) - 800) FROM fact_crop_area)
    UNION ALL SELECT 'crop yield: 400 districts x 10 years (city states may lack rows)',
           (SELECT CASE WHEN count(DISTINCT (district_id, year)) BETWEEN 3900 AND 4000 THEN 0 ELSE 1 END FROM fact_crop_yield)
    UNION ALL SELECT 'crop codes in dim_crop',
           (SELECT count(*) FROM (SELECT crop FROM fact_crop_area UNION SELECT crop FROM fact_crop_yield) x ANTI JOIN dim_crop USING (crop))
    UNION ALL SELECT 'year columns -> dim_year',
           (SELECT count(*) FROM (
                SELECT year FROM fact_crop_area UNION ALL SELECT year FROM fact_crop_yield
                UNION ALL SELECT year FROM fact_bloom_phenology UNION ALL SELECT year FROM agg_cell_bloom
                UNION ALL SELECT year FROM agg_cell_crop UNION ALL SELECT year FROM fact_country_bees
                UNION ALL SELECT year FROM dim_date) x ANTI JOIN dim_year USING (year))
    UNION ALL SELECT 'bee_winter -> dim_bee_winter',
           (SELECT count(*) FROM (
                SELECT bee_winter FROM fact_winter_loss
                UNION ALL SELECT bee_winter FROM dim_date WHERE bee_winter IS NOT NULL) x
            ANTI JOIN dim_bee_winter USING (bee_winter))
    UNION ALL SELECT 'country -> dim_country',
           (SELECT count(*) FROM (
                SELECT country FROM fact_country_bees UNION ALL SELECT country FROM fact_winter_loss
                UNION ALL SELECT country FROM dim_state UNION ALL SELECT country FROM dim_colony) x
            ANTI JOIN dim_country USING (country))
    UNION ALL SELECT 'winter loss pooled rate = lost / wintered',
           (SELECT count(*) FROM fact_winter_loss
            WHERE colonies_lost IS NOT NULL AND abs(100.0 * colonies_lost / colonies_wintered - loss_pct_pooled) > 0.05)
);

SELECT CASE WHEN count(*) > 0
            THEN error('build checks failed: ' || string_agg(check_name || ' (' || bad || ')', '; '))
       END
FROM build_checks
WHERE bad <> 0;

DROP TABLE stg_m;
DROP TABLE stg_krs;
DROP TABLE stg_cell;
DROP TABLE stg_crop_lines;
DROP TABLE build_checks;
DROP MACRO crop_value;
DROP MACRO crop_status;
