"""Loads the YAML semantic layer (metrics, dimensions, facts, system prompt)."""

import yaml

from diplomka.config import SCHEMA_PATH

SCHEMA = yaml.safe_load(SCHEMA_PATH.read_text())
