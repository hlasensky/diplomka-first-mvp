# diplomka

An LLM analytics agent over OLAP-style data in DuckDB. Ask questions in natural language ("average brood nest temperature by month", "revenue by category") and get a short answer plus a chart. Built with **LangGraph** (agent orchestration), **DuckDB** (query engine), a **YAML semantic layer** (measures, metrics, dimensions, rules) and **Chainlit** (chat UI).

The code is dataset-agnostic: everything specific to one dataset lives in a *dataset pack* under [`datasets/`](datasets/), selected with the `DATASET` environment variable. Two packs are included:

| Pack     | Data                                                                 | Model                        |
|----------|----------------------------------------------------------------------|------------------------------|
| `senger` (default) | BeeObserver hive sensors, 78 colonies, 2019-2022 ([Senger et al. 2024](https://doi.org/10.5281/zenodo.10407693)) | star schema, 9 tables/views |
| `olist`  | [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) orders | one flat table               |

## Architecture

```
Chainlit UI (apps/chainlit_app.py)  ──►  LangGraph agent (diplomka.graph)
                                              │
     ┌──────────────────┬─────────────────────┼──────────────────┬──────────────────┐
     ▼                  ▼                     ▼                  ▼                  ▼
clarify_intent    embedding_lookup       generate_sql       validate_sql     generate_response
(LLM -> Filters)  (fuzzy filter values)  (LLM, prompt from  (EXPLAIN +       (LLM summary +
                                          semantic layer)    semantic rules)  ChartSpec)
```

Prompts, intent validation, fuzzy matching and SQL validation are all generated from the active semantic layer, so no module names a table, column or business term.

## Project layout

```
datasets/<name>/         # dataset pack (versioned)
  semantic_layer.yaml    #   the contract: domain, glossary, tables, joins, dimensions, measures,
                         #   metrics, rules, examples, UI starters (documented in schema.py)
  build.sql              #   builds the DuckDB database from the raw files
  eval.yaml              #   evaluation questions with expected intents
data/                    # artifacts: <name>.duckdb + raw/<name>/ input files
src/diplomka/
  config.py              # paths + environment settings; DATASET selects the pack
  schema.py              # typed semantic layer (LAYER) + level domains from DuckDB
  prompts.py             # intent / SQL / answer prompts rendered from the layer
  semantic_validator.py  # R1 aggregations, R2 fan traps, R3 filter values
  models.py              # Filters (parsed intent), ChartSpec, AgentState
  retrieval.py           # embeddings for fuzzy matching of level values
  nodes.py, graph.py     # LangGraph nodes + graph assembly
  llm.py, db.py, charts.py, cli.py, eval.py
apps/chainlit_app.py     # Chainlit UI entry point
scripts/                 # build_db, eval report, render_graph
tests/                   # pytest (fast unit + contract tests for every pack + slow LLM tests)
```

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.13.

```bash
uv sync
```

Configuration is via environment variables (a `.env` file is loaded automatically):

| Variable          | Default                        | Purpose                                   |
|-------------------|--------------------------------|-------------------------------------------|
| `DATASET`         | `senger`                       | dataset pack under `datasets/`            |
| `DUCKDB_PATH`     | `data/<DATASET>.duckdb`        | override the database location            |
| `LLM_BACKEND`     | `ollama`                       | `ollama` (local), `anthropic`, or `openrouter` |
| `OLLAMA_MODEL`    | `qwen2.5:14b`                  | model when backend is ollama              |
| `ANTHROPIC_MODEL` | `claude-haiku-4-5-20251001`    | model when backend is anthropic           |
| `ANTHROPIC_API_KEY` | —                            | required when backend is anthropic        |
| `OPENROUTER_MODEL` | `openai/gpt-4o-mini`         | model when backend is openrouter          |
| `OPENROUTER_API_KEY` | —                           | required when backend is openrouter       |

Build the database of a pack from its raw files in `data/raw/<DATASET>/`:

```bash
# senger: unzip bob_publication_data.zip from Zenodo and put (or symlink) it at data/raw/senger
DATASET=senger uv run python scripts/build_db.py
# olist: data/raw/olist/olist.csv is committed, and so is data/olist.duckdb
DATASET=olist uv run python scripts/build_db.py
```

## Running

```bash
uv run chainlit run apps/chainlit_app.py -w          # chat UI
DATASET=olist uv run chainlit run apps/chainlit_app.py -w
uv run diplomka                                       # CLI REPL
uv run python scripts/render_graph.py                 # regenerate graph.png
```

## Adding a dataset

1. Create `datasets/<name>/` with `semantic_layer.yaml`, `build.sql` and `eval.yaml` (copy a pack as a template; the YAML contract is documented at the top of `src/diplomka/schema.py`).
2. Put the raw files in `data/raw/<name>/` (paths in `build.sql` are relative to it) and run `DATASET=<name> uv run python scripts/build_db.py`.
3. Run `uv run pytest -m "not slow"`. `tests/test_datasets.py` checks every pack: references between sections, eval vocabulary, and example queries (validated, and executed when the database is built).
4. Run `DATASET=<name> uv run python scripts/eval_queries.py` to measure intent accuracy.

## Development

```bash
uv run ruff check .            # lint
uv run ruff format .           # format
uv run pytest -m "not slow"    # fast unit + dataset-pack contract tests (no LLM)
uv run pytest -m slow          # intent-accuracy integration tests (LLM + DuckDB)
uv run python scripts/eval_queries.py   # human-readable accuracy report
```
