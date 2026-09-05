"""Central configuration: project-root anchor, filesystem paths, environment settings.

Every path in the codebase is derived from ``PROJECT_ROOT`` here, so modules and
scripts work regardless of the current working directory.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# src/diplomka/config.py -> parents[2] == repo root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
DUCKDB_PATH = DATA_DIR / "olist.duckdb"
RAW_CSV = DATA_DIR / "raw" / "olist.csv"

SCHEMA_PATH = PROJECT_ROOT / "schema" / "semantic_schema.yaml"
GRAPH_PNG = PROJECT_ROOT / "graph.png"

# LLM backend selection. "ollama" (default, local), "anthropic", or "openrouter".
LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
