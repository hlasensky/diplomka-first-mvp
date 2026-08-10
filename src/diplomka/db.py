"""Thin DuckDB access helpers, anchored to the configured database path."""

import duckdb

from diplomka.config import DUCKDB_PATH


def connect(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    """Open a connection to the project's DuckDB database."""
    return duckdb.connect(database=str(DUCKDB_PATH), read_only=read_only)
