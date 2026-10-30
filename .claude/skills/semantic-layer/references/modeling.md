# Modeling guide: grain, dimensions, additivity, joins, rules

How to decide what goes into the layer. The syntax is in `contract.md`. The principles come from
the existing packs (`senger`: star schema, `multi-senger`: fact constellation with context facts)
and the merging rules in docs/data.md ("Pravidla slučování"). Each section says why, so new cases
can be decided by the same reasoning.

## Contents
1. Grain first
2. Dimensions
3. Measures and additivity
4. Choosing a join kind
5. Rules
6. Examples, glossary, starters
7. Where caveats go
8. Review checklist

## 1. Grain first

Write the grain of every source in words ("one row = colony × hour"), then as columns, then prove
it with a query (`profile.py --grain`). Everything else depends on it: additivity, joins, the
fan-trap tests.

- **One fact per grain.** Never mix grains in one table (no daily totals as extra rows in an
  hourly table, no "total" crop rows next to leaf crops without a hierarchy that marks them).
- **Aggregate finer data up; never allocate coarser data down.** District crop *area* is not split
  into cells. What may go down is an *intensive* context value describing the surroundings
  (share of rapeseed, yield per ha), weighted over the overlapping areas (`agg_cell_crop`).
- **Fact kinds**:
  - `fact`: measurements.
  - `factless_fact`: occurrences (events, inspections); counted with a metric (`COUNT(*)`).
  - `aggregate`: a precomputed coarser grain (`derived_from`), so that the LLM does not have to
    write the aggregation itself; it is also the natural partner of other facts at that grain
    (`agg_colony_daily` ↔ `agg_weather_daily`).
  - `bridge`: many-to-many with a weight that sums to 1 per `from` key (checked in build guards).
- **Completeness columns.** Aggregates carry how much data stands behind a row (`n_hours`,
  `n_minutes`, `n_stations`, `*_coverage`). A rule then says what threshold to use (R5:
  `n_hours >= 20`). Without them an anomaly detector flags days with missing data.
- **Event targets for ASOF.** If several events can share a timestamp, an ASOF join picks one at
  random. Build an aggregate with one row per (entity, day) that lists the event types
  (`agg_event_daily`) and make that the ASOF target.

## 2. Dimensions

- **Conformed dimensions.** Facts that users will compare must share dimension tables and key
  values (`cell_id`, `date`, `year`). A new context source attaches to the existing dimensions; if
  its key is different (weather station vs. hive cell), build a mapping: an aggregate at the
  shared key (median over stations within 25 km, `agg_cell_bloom`) or a bridge with weights.
  Record the mapping method and its error (distance, coverage) in the description and in data.md.
- **One time dimension per grain.** Hourly facts → `dim_time`, daily facts and event dates →
  `dim_date`, yearly facts → `dim_year`, special periods (overwintering, campaigns) → a dimension
  with `start`/`end` and a `range` join. Rollups connect them. A daily fact joined to an hourly
  time dimension multiplies its rows by 24 (that was the original `senger` `daily_time` join).
  Build the time dimensions after all facts and cover the full date range of every fact (events
  can run past sensor data).
- **Time zone.** Store UTC (or the source's zone, verified) and say which in `domain.notes`.
  Hour-of-day levels get a note on local time. Check DST switch days for duplicated or missing
  local hours (BeeObserver had a duplicated hour 01 on spring switch days).
- **Hierarchies** go coarse → fine. Denormalize the levels into the dimension's base table, so one
  join reaches all of them; coarser dimension tables (`dim_cell`, `dim_district`, `dim_year`,
  `dim_country`: shrunken rollup dimensions) exist for facts at that grain.
- **Codes and labels.** Dimensions translate codes into readable values, and keep the original
  code or source-language name for provenance (`crop_de`, `plant_de`, category ids in comments).
- **Flags as levels.** Entity properties derived from facts (`ever_swarmed`, `died`) are levels
  with a note telling the LLM to use them instead of joining the events.
- **Domains.** `domain: from_data` for categorical levels the user filters by. If a level is empty
  until some data is loaded, say so in its note (`state` in `senger`).

## 3. Measures and additivity

For every measure ask: what does a row *mean*, and what does adding two rows mean? Then fill
`additivity` for **every dimension its tables reach** (dimensions whose key is in the grain or
reachable through fk/rollup joins). Omitting a dimension forbids aggregation over it; do that on
purpose (nested categories, a join that fans out), never by accident.

| Kind of quantity | Examples | Over time | Over entities / space | Notes |
|---|---|---|---|---|
| Flow / increment per period | weight gain, precipitation, energy, harvest kg | sum, avg, min, max | sum if entities are disjoint and a total means something (weight gain of a set of colonies); avg if the value describes a place's condition (rain at several cells: average) | ask when unsure: this choice is domain-specific |
| Stock / level / state | hive weight, number of hives, inventory, battery % | avg, min, max, last; **never sum** | sum if extensive and disjoint (hives over regions); avg if levels are not comparable (hive weight includes the box) | semi-additive |
| Intensive / per unit | temperature, humidity, pressure, NDVI, concentration, yield per ha, share % | avg, median, min, max, stddev | avg, median, min, max; weighted avg if weights exist | **never sum** |
| Ratio / rate | loss %, share of total | store numerator and denominator as measures; metric `SUM(num) / SUM(den)` | same | avg of rates only within one survey/source, labelled as such |
| Pre-aggregated statistic | daily max, daily std, largest hourly drop | only what composes: max of max, min of min, avg of avg (approx.), avg of std as "typical variability" | same | never sum |
| Distinct count | number of colonies | metric `COUNT(DISTINCT ...)` | not additive across overlapping groups | metric, not measure |
| Day-of-year, dates as numbers | bloom_doy | avg, median, min, max | avg, median, min, max | never sum |
| Completeness counter | n_hours, n_minutes | sum, avg, min, max | sum, avg, min, max | |

More rules that came from real mistakes:
- **Nested categories** (crop → parent crop): summing over the category dimension double counts.
  Leave that dimension out of `additivity`, add a rule "always filter exactly one crop".
- **NULL is not 0.** Missing → NULL. Suppressed or unreliable values (`.`, `/`, `x`) → NULL plus a
  status column (`value_status`); explicit zero markers (`-`) → 0. Say in the description what NULL
  means for this measure.
- **One column name = one meaning** in the whole pack (the validator looks measures up by column
  name). Same quantity in two tables → one measure with both `tables`.
- Units go into the column name where possible (`weight_kg`, `precip_mm`) and always into `unit`.
- A measure only available in some years or places says so in `description` (crop area: only
  2016 and 2020) and, if it changes how to join, in a rule.

## 4. Choosing a join kind

| Situation | Kind | Watch out for |
|---|---|---|
| fact → its dimension | `fk`, many_to_one | orphans (required join drops rows); expression keys (`date_trunc('hour', ts)`) |
| dimension → coarser dimension | `rollup` | nullable parents → `optional: true` |
| fact ↔ fact, same grain, through shared dimensions | `drill_across` with `via` | keys must cover the target grain, otherwise many_to_many and sums multiply: add the missing grain column to `requires_filter` or to a rule |
| fact → latest row of another fact (events, 16-day composites, inspections) | `asof` | makes the pair ASOF-only (R2 rejects plain JOINs); ties at one timestamp → `requires_filter` or a one-row-per-time aggregate as target |
| "did X happen in a window before/after" | no join: `EXISTS` | say it in the asof note and in an example |
| fact → period (season, winter, campaign) | `range` to a dimension with start/end | periods must not overlap; uncovered dates → `optional: true` |
| many-to-many (spatial overlap, multi-membership) | `bridge` with weights | weights sum to 1 per from key; precompute weighted aggregates so the LLM need not write weighted SQL |
| facts at different grains | none directly | aggregate the finer fact to the coarser grain first (rule), then join through the coarse dimension (R10 in multi-senger) |

For every join, ask "how many `to` rows can one `from` row match?" If it can be more than one for
any key, it is not many_to_one: sums over the `from` fact multiply (fan trap). Two facts joined
through a common dimension without aggregating each first produce a cross product (chasm trap):
aggregate each to the shared grain, then join.

## 5. Rules

- R1-R3 are generic and enforced by the validator (additivity, ASOF-only pairs, domains). Every
  pack has them; R2's text names this pack's ASOF-only pairs and the EXISTS alternative.
- R4 onward: one rule per trap, `enforced: false`. Typical traps: levels that are not comparable
  across entities (R4), completeness thresholds (R5), minimum peer group size (R6), time dimension
  per grain (R7), which facts join at which grain (R8), nested categories (R9), coarse facts
  joined only after aggregation (R10), association-not-causation wording for context data (R11),
  huge tables only with tight filters (R12).
- Write rules as instructions that name tables and columns and give the correct alternative, not
  only the prohibition: "Join daily hive data only with agg_weather_daily, through
  dim_colony.cell_id" beats "Do not mix grains".

## 6. Examples, glossary, starters

- **Examples**: one per hard pattern the LLM must get right in this pack: peer comparison with a
  window, rollup with GROUPING, ASOF event context, EXISTS window, drill-across at the same grain,
  bridge-weighted aggregation, range join to periods, coarse facts after aggregation, a correlation
  with a lag. Use the completeness filters the rules ask for. Every example must run, pass the
  validator and match its golden snapshot.
- **Glossary**: what a domain user types, incl. source-language terms (Kreis, Landkreis), mapped to
  a measure, a metric, a level, or a level value that exists in the domain.
- **Starters**: 3-6 questions that show what the pack can do and that the eval set covers.

## 7. Where caveats go

The LLM sees the layer only through prompts; a caveat helps only where it is shown when it
matters:

| Caveat about | Put it in |
|---|---|
| units, time zone, data coverage, association vs. causation | `domain.notes` |
| what a row means, years covered, size, when to use the table | table `description` |
| NULL meaning, availability, comparability | measure `description` |
| how to use one join correctly | join `note` |
| something that spans tables | a rule |
| a filter value's meaning | level `note` |

Only write facts you verified with a query, and re-verify them in audits.

## 8. Review checklist

Use it in audits and before finishing a new pack or an extension.

- [ ] Every fact, aggregate and bridge has a `grain`, verified unique.
- [ ] Every measure lists additivity for each dimension its tables reach, or omits one on purpose
      (reason in the description or a rule).
- [ ] No intensive measure, stock-over-time or pre-aggregated statistic allows `sum`; rates are
      ratio-of-sums metrics.
- [ ] Column names mean the same thing everywhere they occur.
- [ ] Every fact joins the time dimension of its own grain; time dimensions cover every fact's range.
- [ ] Every fact pair users will combine has a join (drill_across / asof / range) or a rule saying how.
- [ ] many_to_one joins are really many_to_one (test); ASOF targets have one row per key and time,
      or `requires_filter`.
- [ ] NULL vs. 0 handled in build.sql and explained in descriptions.
- [ ] Descriptions, notes and rules are factually true (re-queried).
- [ ] Glossary values exist in their domains; level names are unique; `domain: from_data` only on
      small categorical levels.
- [ ] eval.yaml covers every measure, metric and level users would ask about, plus two `unclear`
      cases and one multi-turn case.
- [ ] Every asof / drill_across / bridge / range join is shown in at least one example.
- [ ] Time zone stated; DST switch days checked.
- [ ] docs/data.md, docs/decisions.md and both diagrams match the pack.
