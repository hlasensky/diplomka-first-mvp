"""Central configuration: project-root anchor, filesystem paths, environment settings.

Every path in the codebase is derived from ``PROJECT_ROOT`` here, so modules and
scripts work regardless of the current working directory.

Everything dataset-specific lives in a *dataset pack* under ``datasets/<DATASET>/``
(semantic layer, build SQL, eval cases); the code itself is dataset-agnostic.
Switch datasets with the ``DATASET`` environment variable.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# src/diplomka/config.py -> parents[2] == repo root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET = os.getenv("DATASET", "senger")

# Dataset pack: definitions, versioned in git.
DATASETS_DIR = PROJECT_ROOT / "datasets"
DATASET_DIR = DATASETS_DIR / DATASET
SCHEMA_PATH = DATASET_DIR / "semantic_layer.yaml"
BUILD_SQL = DATASET_DIR / "build.sql"
EVAL_PATH = DATASET_DIR / "eval.yaml"

# Dataset artifacts: the built DuckDB database and the raw input files.
DATA_DIR = PROJECT_ROOT / "data"
DUCKDB_PATH = Path(os.getenv("DUCKDB_PATH", DATA_DIR / f"{DATASET}.duckdb"))
RAW_DIR = DATA_DIR / "raw" / DATASET  # build.sql paths are relative to this directory

GRAPH_PNG = PROJECT_ROOT / "graph.png"

# Query results are truncated to this many rows.
MAX_ROWS = 500

# LLM backend selection. "ollama" (default, local), "anthropic", or "openrouter".
LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
