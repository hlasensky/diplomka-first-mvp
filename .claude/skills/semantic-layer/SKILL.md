---
name: semantic-layer
description: Build, extend or audit a dataset pack for the diplomka agent and OLAP engine - datasets/PACK/build.sql (raw files to a DuckDB star schema or fact constellation), semantic_layer.yaml (tables, grains, joins, dimensions, measures with additivity, metrics, rules, examples, glossary, starters) and eval.yaml, plus build guard checks, docs/data.md + decisions.md entries and PlantUML diagrams. Use whenever the user wants a new dataset or data source modelled, raw CSV/Parquet/JSON/API data turned into facts and dimensions, a measure, dimension, level, context fact, join, rule or example added to a semantic layer, grain or additivity decided, a fan trap fixed, or a semantic_layer.yaml checked against its database - even when they only say "add the soil data to multi-senger", "new pack", "cube model", "star schema" or "is the layer still right".
---

# Semantic layer (dataset packs)

A dataset pack is everything dataset-specific in this project. The agent, the SQL validator and
the user's OLAP engine (Python + Ibis) are dataset-agnostic and read only the pack:

```
datasets/<pack>/build.sql            raw files in data/raw/<pack>/ -> data/<pack>.duckdb
datasets/<pack>/semantic_layer.yaml  the contract: what the tables mean and how they may be combined
datasets/<pack>/eval.yaml            questions with the expected intent (vocabulary check + accuracy eval)
```

Wrong semantics produce numbers that look fine: a fan-out join silently multiplies sums, a summed
temperature is a valid SQL query. The Cube spike (docs/spike_cube.md, N3) found that both of its
failures were silent. That is why this skill profiles before it models, asks before it guesses,
and checks results against independent queries before calling anything done.

## Boundaries

Write only these:
- `datasets/<pack>/*`, `data/raw/<pack>/` (downloaded raw files + `MANIFEST.json`), `data/<pack>.duckdb` (via the build script)
- `docs/data.md`, `docs/decisions.md`, `docs/<pack>_schema.puml`, `docs/<pack>_joins.puml` and their renders
- `tests/golden/<pack>/*.parquet` only through the test runner, as described under Validation

Never edit `src/`, `tests/*.py`, `scripts/*.py` or `apps/`. The loader (`schema.py`), prompt
renderer, validator and the OLAP engine are the user's own code and they write it themselves.
If the layer needs something the contract cannot express (the loader rejects unknown join keys,
for example), stop and describe the contract change and which consumers it would break. Do not
add the key and do not adapt the Python. Raw files stay untouched; every fix happens in build.sql.
No git commands unless the user asks.

## The contract

The authoritative contract is the module docstring of `src/diplomka/schema.py` plus the checks in
`tests/test_datasets.py`. Read both at the start of every run, because they evolve.
`references/contract.md` is a cheat sheet with examples; where it disagrees with schema.py,
schema.py wins and the reference is out of date (say so in the report).

## Modes

Pick the mode from the request; if it is unclear, ask.

| Mode | Input | Output |
|---|---|---|
| **new** | raw files or a source URL, a pack name | a complete pack + docs + diagrams |
| **extend** | an existing pack + what to add (a context fact, measure, dimension, rule, example...) | the pack changed in place, nothing else in it broken |
| **audit** | an existing pack | a findings report; fixes only after the user picks them |

## Asking the user

The user decides semantic questions themselves. A pause costs a minute; a wrong additivity or
grain costs a wrong chapter. So:

1. **First settle with data whatever data can settle**: grain uniqueness, NULL markers, value
   domains, key coverage between tables, timestamp resolution, time-zone evidence (e.g. the daily
   temperature minimum near sunrise in UTC), duplicates. Record each as verified, with the number
   that proves it. Do not ask the user something a query can answer.
2. **Ask about what remains**: meaning of a code or column, additivity of a measure that is not
   clearly a flow or an intensive quantity, whether data should be excluded, which grain a context
   fact should join at, how a nested category should aggregate, how to name business terms,
   anything where two readings of the data are plausible.
3. **Batch the questions per checkpoint**, not one per turn. Use AskUserQuestion (max 4 questions
   per call; make more calls if needed). Each question stands on its own: what you found (with
   numbers), the options, your recommendation first.
4. **Checkpoints**:
   - C1, after profiling and before writing build.sql: scope, grains, keys, NULL and time handling,
     how new data attaches to existing dimensions.
   - C2, after drafting the layer and before validation: additivity table, rules, glossary
     mappings, anything you marked uncertain while writing.
   - C3 (audit): which findings to fix.
5. If you cannot ask (a non-interactive run), write the questions with your recommended answers to
   `questions.md` next to your other outputs (or in the final report), continue with the
   recommendation, and mark every place that depends on it as `ASSUMPTION` in the report.

## Workflow: new pack

1. **Sources.** Find the data paper / documentation, licence and citation for every source. Put raw
   files in `data/raw/<pack>/` (gitignored). For downloads, write `MANIFEST.json` there: per file
   the URL, access date and SHA-256 (as `data/raw/multi-senger/MANIFEST.json` does).
2. **Profile.** `uv run python .claude/skills/semantic-layer/scripts/profile.py --files '<glob>'`
   (or `--db data/<pack>.duckdb --table <t>`; `--grain col1,col2` tests uniqueness;
   `--csv-option key=value` passes read_csv options for odd files). Read the output for: the real
   grain, NULL markers (`NA`, `-200`, `-999`, `.`, empty strings), decimal commas, encodings,
   header/footer lines, timestamp resolution and gaps, duplicate timestamps (DST!), units in
   headers, categorical domains, totals or nested categories mixed with leaf rows. Then query
   further with `uv run python -c "import duckdb; ..."` where the profile raises a question.
3. **Model** with `references/modeling.md`: facts and their grains, conformed dimensions with
   hierarchies, one time dimension per grain, aggregates for common grains and ASOF targets,
   bridges for many-to-many.
4. **Checkpoint C1.**
5. **build.sql** following `references/build-sql.md` (numbered sections, explicit types, NULL
   handling, staging dropped at the end, section `99) CHECKS` that fails the build).
   Build: `DATASET=<pack> uv run python scripts/build_db.py`. Iterate until it builds and every
   guard passes.
6. **semantic_layer.yaml** with `references/contract.md` (syntax) and `references/modeling.md`
   (semantics: additivity, join kinds, rules, examples).
7. **eval.yaml**: cases that cover every measure, metric and level the user is likely to ask
   about, two `unclear` cases (out of domain, nonsense) and one multi-turn case. Format in
   `references/contract.md`.
8. **Checkpoint C2.**
9. **Validation** (below).
10. **Docs and diagrams** with `references/docs.md`: `docs/data.md` section, dated
    `docs/decisions.md` entry (both in Czech, like the existing ones), `docs/<pack>_schema.puml`
    and `docs/<pack>_joins.puml`, rendered to SVG and PNG.
11. **Report** (below).

## Workflow: extend

Same steps, limited to the new part, with these additions:

- Read the whole pack first: layer, build.sql section headers and the sections you touch, the
  pack's part of docs/data.md and its decisions. Reuse existing dimensions, keys and naming: a new
  context fact attaches through the dimensions that are already there (e.g. `cell_id` + `date`),
  so it can be drilled across with the existing facts.
- New build.sql sections go before the section that derives shared dimensions from all facts (in
  multi-senger, section 12 builds `dim_date` from the date range of every fact). Add the new fact to
  that range and to the cross-table guards in section 99 (e.g. "daily facts -> dim_date").
- Rebuilding replaces `data/<pack>.duckdb`. Build into a scratch path first
  (`DUCKDB_PATH=<scratchpad>/<pack>.duckdb`) until it passes, then rebuild in place.
- Existing example results must not change. Run the golden test for the pack before creating
  snapshots for new examples (see Validation).
- Update what the change makes stale: table descriptions, domain notes, rules that list facts
  (e.g. R7's list of daily facts, R8's join partners), glossary, starters, eval cases.

## Workflow: audit

1. Run `check_pack.py` (below) and read every failure and warning.
2. Go through the review checklist at the end of `references/modeling.md`: additivity per measure
   and dimension, declared grains, join kinds and cardinalities, fan-trap pairs covered by ASOF
   joins and R2, time dimension per grain, NULL meaning in descriptions, glossary values in their
   domains, eval coverage, examples for every hard join.
3. Verify text against data. Descriptions, notes and rules make factual claims (year coverage, row
   meaning, "only 2016 and 2020", "NULL until ..."). The LLM trusts them, so a stale claim is a
   bug. Check each with a query.
4. Write the report: a table `severity | where (file:line) | problem | evidence | proposed fix`.
   Severity order: wrong numbers (fan-out, wrong additivity, wrong grain) > failing contract test >
   misleading or stale text > completeness (eval coverage, missing examples) > style.
5. **Checkpoint C3**, then apply the chosen fixes with the extend workflow.

## Validation

Run all of it in every mode, and quote the results in the report.

1. `uv run python .claude/skills/semantic-layer/scripts/check_pack.py <pack>` loads the layer with
   the user's loader, runs the pack's contract tests from `tests/test_datasets.py` and its golden
   test, and lints things the tests do not check (see the script docstring). Fix every failure.
   Treat each warning as a question: fix it, or say in the report why it is intended.
2. **Independent results.** The tests prove that SQL runs and keys are unique, not that numbers
   are right. For every new measure, metric and example, compute one number two ways (e.g. the
   example vs. a query on the staging data or without the join; a daily sum vs. the sum of hourly
   values) and compare. Put the pairs and the results in the report.
3. **Golden snapshots.** New examples go at the end of `examples`. Run
   `uv run pytest "tests/test_golden.py::test_examples_match_golden[<pack>]"`. If the only failure
   is a missing snapshot for the first new example, every earlier example still matches; then
   create the snapshots with `UPDATE_GOLDEN=1` on the same node id. If an existing example's result
   changed, stop and ask: it is either a regression or an intended change the user must approve.
4. Intent accuracy needs an LLM backend: `DATASET=<pack> uv run python scripts/eval_queries.py`.
   Ask before running it (it calls the configured model and may cost money).

## Report

End with a short report (in the language the user writes in):
- what changed: tables with grain and row count, layer sections, files
- questions asked and the answers (or assumptions, if you could not ask)
- validation: check_pack summary, the independent-result pairs, golden status
- known issues and caveats (they also go into docs/data.md, "Známé problémy")
- what the user's Python code may need, if anything in the contract area changed
