# diplomka

An LLM analytics agent over the [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) dataset. Ask questions in natural language ("revenue by category", "average freight cost by state") and get a short answer plus a chart. Built with **LangGraph** (agent orchestration), **DuckDB** (query engine), a **YAML semantic layer** (metrics/dimensions/facts), and **Chainlit** (chat UI).

## Architecture

```
Chainlit UI (apps/chainlit_app.py)  ──►  LangGraph agent (diplomka.graph)
                                              │
        ┌─────────────────────────────────────┼───────────────────────────────┐
        ▼                    ▼                 ▼               ▼                ▼
  clarify_intent      embedding_lookup    build_sql      execute_query   generate_response
  (LLM structured)    (fuzzy category)    (semantic      (DuckDB)        (LLM summary +
                                           schema)                        deterministic ChartSpec)
```

The semantic layer lives in [`schema/semantic_schema.yaml`](schema/semantic_schema.yaml) — adding a metric, dimension or fact is a YAML edit, not a code change.

## Project layout

```
src/diplomka/        # the package
  config.py          # paths + environment settings (single source of truth)
  schema.py          # loads the YAML semantic layer
  models.py          # Filters (parsed intent), ChartSpec, AgentState
  sql.py             # deterministic SQL builder
  llm.py             # chat-model factory (Ollama / Anthropic)
  db.py              # DuckDB connection helper
  retrieval.py       # lazy embeddings + vector store for fuzzy category lookup
  nodes.py           # LangGraph node functions + routing
  graph.py           # graph assembly -> get_graph()
  charts.py          # Plotly figure builder
  cli.py             # REPL entry point
  eval.py            # shared evaluation dataset
apps/chainlit_app.py # Chainlit UI entry point
scripts/             # load_data, query smoke test, eval report, render_graph
tests/               # pytest (fast unit + slow integration)
data/  schema/       # DuckDB database + semantic schema
docs/plan.md         # thesis MVP plan
```

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.13.

```bash
uv sync
```

Configuration is via environment variables (a `.env` file is loaded automatically):

| Variable          | Default                        | Purpose                                   |
|-------------------|--------------------------------|-------------------------------------------|
| `LLM_BACKEND`     | `ollama`                       | `ollama` (local) or `anthropic`           |
| `OLLAMA_MODEL`    | `qwen2.5:14b`                  | model when backend is ollama              |
| `ANTHROPIC_MODEL` | `claude-haiku-4-5-20251001`    | model when backend is anthropic           |
| `ANTHROPIC_API_KEY` | —                            | required when backend is anthropic        |

The DuckDB database (`data/olist.duckdb`) is committed. To rebuild it from the raw CSV:

```bash
uv run python scripts/load_data.py
```

## Running

```bash
# Chat UI
uv run chainlit run apps/chainlit_app.py -w

# CLI REPL
uv run diplomka

# Regenerate the graph diagram (graph.png)
uv run python scripts/render_graph.py
```

## Development

```bash
uv run ruff check .            # lint
uv run ruff format .           # format
uv run pytest -m "not slow"    # fast unit tests (no LLM)
uv run pytest -m slow          # intent-accuracy integration tests (LLM + DuckDB)
uv run python scripts/eval_queries.py   # human-readable accuracy report
```
