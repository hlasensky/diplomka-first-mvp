# Contract cheat sheet: semantic_layer.yaml and eval.yaml

Authoritative source: the docstring of `src/diplomka/schema.py` and `tests/test_datasets.py`.
This file adds examples and the constraints that only show up in the code. If schema.py says
otherwise, schema.py wins.

## Contents
1. Top level
2. domain, glossary
3. tables
4. joins (the strict part)
5. dimensions and levels
6. measures and additivity
7. metrics, rules, examples, starters
8. eval.yaml
9. How consumers read the layer (why some constraints exist)

## 1. Top level

```yaml
version: 1
domain: {...}
glossary: [...]
tables: {...}
joins: [...]
dimensions: {...}
measures: {...}
metrics: {...}      # optional
rules: [...]
examples: [...]
starters: [...]
```

Indentation: `senger` uses 2 spaces with flow mappings, `multi-senger` uses 4 spaces (formatted by
an editor). When extending a pack, keep its existing style.

## 2. domain, glossary

```yaml
domain:
  name: beeobserver                 # short id, shown in prompts
  description: >                    # what the data is, scope, coverage, the biggest caveat
    Sensor data from 78 honey bee colonies in Germany (2019-2022): ...
  notes:                            # units, time zone, data caveats; every prompt shows them
    - "All timestamps are UTC ..."
    - "Temperatures in °C, weights in kg, ..."
  source: "Senger et al., Data in Brief 52 (2024) 110015; Zenodo 10.5281/zenodo.10407693"

glossary:
  - term: swarming                  # business term the user may type
    synonyms: [swarm, swarm event]
    maps_to: {dimension: event, level: event_type, value: swarming}   # a level value (must be in the domain)
  - term: nectar flow
    synonyms: [honey flow]
    maps_to: {measure: weight_gain_kg, note: "positive daily weight gain"}
  - term: district
    maps_to: {dimension: geography, level: district}                  # a level
```

`maps_to` targets are checked by the tests: `metric` in metrics, `measure` in measures, `level`
in levels. A `value` should be in the level's domain (check_pack.py checks it against the DB).

## 3. tables

Every table or view the agent may query. Anything not listed is invisible to the agent.

```yaml
tables:
  fact_hive_hourly:
    kind: fact                      # fact | factless_fact | aggregate | bridge | dimension
    grain: [colony_key, time_key]   # columns that identify one row; tested for uniqueness
    description: Hourly means of the minute readings; n_minutes is the completeness of the hour.
  agg_colony_daily:
    kind: aggregate
    grain: [colony_key, date]
    derived_from: fact_hive_hourly
    description: Daily aggregates per colony; input for anomaly detection.
  dim_colony: {kind: dimension}     # dimensions may omit grain/description; add a description when
                                    # the table has a trap (row per hour, NULL ranges, only some years)
```

`grain` is checked by `test_table_grain_is_unique`; the drill-across/asof grain-coverage test
reads the target table's `grain` too. Give every fact, aggregate and bridge a grain.

## 4. joins

Allowed keys, enforced by the loader (an unknown key raises):
- join: `id, kind, from, to, via, bridge, cardinality, optional, requires_filter, direction, note`
- side (`from`/`to`): `table, columns, expr, time, time_expr, start, end`

| kind | meaning | required parts |
|---|---|---|
| `fk` | fact -> dimension | same number of keys on both sides |
| `rollup` | dimension -> coarser dimension (hour -> day, cell -> district) | same |
| `bridge` | many-to-many through a weighted bridge | `bridge: {table, from_columns, to_columns, weight}` with column counts matching `from`/`to` |
| `range` | `from` key BETWEEN `to.start` AND `to.end` | exactly one `from` key; `to.start`, `to.end` |
| `drill_across` | fact -> fact at the same grain through shared dimensions | `via` (non-empty) |
| `asof` | fact -> latest matching `to` row by time | `time` (or `time_expr`) on both sides; `direction` in `>=, <=, >, <` |

Other constraints:
- every table named (incl. bridge table) must be in `tables`
- `via` lists ids of `fk`/`rollup` joins whose `from` table is this join's `from` table
- a column written `table.column` must belong to a table reached through `via`
- a side has `expr` or `columns`, never both; `expr` is one fully qualified SQL expression
- `requires_filter` lists plain column names of the `to` table that the query must fix to one value
  (in the ON clause, not in WHERE after the join); the grain-coverage test counts them as keys
- `cardinality`: `many_to_one | one_to_many | one_to_one | many_to_many`
  (`many_to_one` is tested: no duplicate `to` keys, and drill-across/asof keys must cover the target grain)
- `optional: true`: the key may be NULL or unmatched (LEFT JOIN); without it the orphan test
  requires every `fk`/`rollup` key to find a row
- every `asof` join makes its table pair "ASOF-only": the validator (rule R2) rejects a plain JOIN
  between them

Examples (from multi-senger):

```yaml
- {id: hourly_colony, kind: fk, from: {table: fact_hive_hourly, columns: [colony_key]},
   to: {table: dim_colony, columns: [colony_key]}, cardinality: many_to_one}

- id: minute_time                       # key that is an expression
  kind: fk
  from: {table: fact_hive_minute, expr: "date_trunc('hour', fact_hive_minute.ts)"}
  to: {table: dim_time, columns: [time_key]}
  cardinality: many_to_one

- id: date_winter                       # nullable rollup
  kind: rollup
  from: {table: dim_date, columns: [bee_winter]}
  to: {table: dim_bee_winter, columns: [bee_winter]}
  cardinality: many_to_one
  optional: true
  note: "roll-up: day -> winter; NULL in April-September"

- id: cell_district_weighted
  kind: bridge
  from: {table: dim_cell, columns: [cell_id]}
  to: {table: dim_district, columns: [district_id]}
  bridge: {table: bridge_cell_district, from_columns: [cell_id], to_columns: [district_id], weight: weight}
  cardinality: many_to_many

- id: daily_winter
  kind: range
  from: {table: agg_colony_daily, columns: [date]}
  to: {table: dim_bee_winter, start: winter_start, end: winter_end}
  cardinality: many_to_one
  optional: true

- id: daily_weather                     # fact -> fact through a shared dimension
  kind: drill_across
  from: {table: agg_colony_daily, columns: [dim_colony.cell_id, date]}
  to: {table: agg_weather_daily, columns: [cell_id, date]}
  via: [daily_colony]
  cardinality: many_to_one

- id: hourly_event_asof
  kind: asof
  from: {table: fact_hive_hourly, columns: [colony_key], time: time_key}
  to: {table: fact_event, columns: [colony_key], time: event_ts}
  requires_filter: [event_type]         # event_type is part of fact_event's grain
  direction: ">="
  cardinality: many_to_one
  note: "Latest event of ONE type; for 'was there an event in the window' use EXISTS."
```

## 5. dimensions and levels

```yaml
dimensions:
  geography:                        # dimension name: used as an additivity key
    table: dim_colony               # base table; every level must be a column (or expr) of it
    key: colony_key
    hierarchies:
      geo: [country, state, district, cell_id, colony_key]   # coarse -> fine; names from `levels`
    levels:
      state: {label: federal state, domain: from_data, note: "states with colonies only"}
      cell_id: {label: location, note: "0.1 degree cell, precision 5-7 km"}
      colony_key: {label: colony}
      ever_swarmed: {label: colony swarmed at least once, note: "filter value true/false"}
  time:
    table: dim_time
    key: time_key
    hierarchies: {calendar: [year, month, date, hour], weekly: [year, week, date]}
    levels:
      month: {label: month, format: "YYYY-MM"}
      season: {label: season, domain: from_data}
```

- Level names are unique across all dimensions (the loader raises otherwise): intents, filters
  and domain checks refer to a level by its name alone.
- Hierarchy levels are denormalized into the dimension's base table, so one join reaches all of
  them. Coarser dimension tables (dim_cell, dim_district, dim_year) still exist for facts at that
  grain and are reached by `rollup` joins.
- `expr`: SQL over the dimension table for a computed level; the test runs
  `SELECT <expr> FROM <table>`.
- `domain: from_data`: the app reads `SELECT DISTINCT` of the level at startup, lists the values in
  prompts and rejects other filter values (R3). Use it for categorical levels with a small domain
  (tens of values, at most a few hundred). Not for numeric, date or high-cardinality levels.
- Extra keys (`format`, `note`) are passed through; the loader ignores unknown level keys.
- A dimension whose levels live in a fact (degenerate dimension) may use the fact as `table`
  (multi-senger `survey: {table: fact_winter_loss, key: survey}`).

## 6. measures and additivity

```yaml
measures:
  precip_mm:                        # measure id (used in intents and eval)
    column: precip_mm               # or `columns: [t_i_1, t_i_2, ...]` for one concept in several columns
    tables: [fact_weather, agg_weather_daily]    # every table that has this column with this meaning
    label: precipitation
    unit: mm
    additivity: {time: [sum, avg, max], geography: [avg, min, max]}
    description: Sum over time; never sum over locations (average them).
```

- `additivity` keys are dimension names from `dimensions`, or `all`. Values come from this
  vocabulary: `sum, avg, min, max, median, stddev, last`. `count` and `corr` are always allowed by
  the validator, so do not list them. `last` = value at the latest time (semi-additive stocks).
- `SemanticLayer.allowed_aggs(measure, aggregated_over)` intersects the lists of the dimensions a
  query collapses (plus `all`). **A dimension that is not listed allows nothing**: that is how
  "never aggregate over crops" (nested categories) or "a join to plants fans out" is expressed.
  Leave a dimension out on purpose, never by accident.
- `description` (or `caveat`) is shown in the SQL prompt: put the trap there (NULL meaning,
  years covered, "includes the hive structure").
- The validator finds measures by **column name**, across all tables. One column name must mean
  one thing in the whole pack: the same quantity in several tables = one measure with several
  `tables`; a different quantity = a different column name (rename in build.sql).

## 7. metrics, rules, examples, starters

```yaml
metrics:                            # named SQL expressions: counts, ratios of sums, distinct counts
  winter_loss_rate:
    label: pooled winter loss rate over several survey rows
    sql: "100.0 * SUM(colonies_lost) / SUM(colonies_wintered)"
    table: fact_winter_loss         # optional
    unit: "%"
    note: "ratio of sums, never the average of rates; filter one survey"

rules:
  - {id: R1, enforced: true,  text: "Aggregate every measure only with the functions listed in its additivity; ..."}
  - {id: R2, enforced: true,  text: "Join <fact A> with <fact B> only via ASOF JOIN or EXISTS; ..."}
  - {id: R3, enforced: true,  text: "Filter dimension attributes only with values from their domain."}
  - {id: R4, enforced: false, text: "<dataset-specific guidance>"}

examples:                           # few-shot SQL for the hard patterns
  - id: EX1
    question: "Was the drop in weight gain on a given day shared by the whole location?"
    pattern: peer_residual          # short snake_case name of the pattern
    sql: |
      SELECT ...

starters:                           # example questions in the chat UI
  - {label: "Brood nest temperature by month", message: "What is the average center temperature by month?"}
```

- R1-R3 are enforced generically by `semantic_validator.py` (additivity, ASOF-only pairs, domains);
  keep them in every pack with `enforced: true` and dataset-specific wording. R4+ are guidance for
  the LLM and the engine (`enforced: false`). Keep ids unique and in order.
- Every example must pass `validate_semantics` and execute (tested), and gets a golden snapshot.

## 8. eval.yaml

```yaml
cases:
  - question: "What is the average center temperature by month?"
    expected: {measures: [{measure: t_center, agg: avg}], group_by: [month]}
  - question: "How many swarming events were recorded per year?"
    expected: {metrics: [event_count], group_by: [year], filters: {event_type: swarming}}
  - question: "What will the honey price be next year?"
    expected: {unclear: true}
multi_turn:
  - questions:
      - "How much did it rain per month?"
      - "and the average air temperature by season"
    expected_last: {measures: [{measure: air_temp_c, agg: avg}], group_by: [season]}
```

Tested: metrics exist, every `agg` is in the measure's allowed aggregations, `group_by` and
`filters` keys are level names. Filter values should be domain values.

## 9. How consumers read the layer

- `prompts.py` renders domain, notes, glossary, measures (with additivity), levels (with domain
  values), tables (with DESCRIBE columns, grain, description), joins (condition + note), rules and
  examples into the LLM prompts. Text you write is what the model sees: be concrete, name tables
  and columns, say what NULL means.
- `semantic_validator.py`: R1 by column name, R2 for asof pairs, R3 for `domain: from_data` levels.
- The user's OLAP engine (Python + Ibis) reads the same YAML: `allowed_aggs` per dimension, join
  path choice from `joins`, grain rules. Ibis has no ROLLUP/GROUPING SETS and DuckDB `corr` only
  as population correlation; this matters for engine-side features, not for the layer.
