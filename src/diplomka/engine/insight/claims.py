"""Claims with provenance: the only facts the LLM may state in an answer.

Each claim is backed by one ``Result`` (query + SQL). The LLM receives claims, not raw rows, and words
them; a number in the answer that does not come from a claim is a hallucination by definition (testable
in evaluation). When LLMs get the data in the prompt, their insights are often quantitatively wrong or
hallucinated; numbers are right when they come from executed code [franciaVOOLModularInsightbased2025 C8,
candidate].

Wording follows R11: associations, not causes, with the support (days, colonies, locations).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from diplomka.engine.executor import Result
from diplomka.engine.insight.ranking import Insight


@dataclass(frozen=True)
class Claim:
    claim_id: str
    kind: Literal["value", "anomaly", "where", "why"]
    text: str  # template text with the numbers filled in by code, not by the LLM
    numbers: dict[str, float]
    support: int  # days / colonies / locations behind the statement (R11)
    evidence: Result


def claims_for_result(result: Result) -> list[Claim]:
    """Value claims for the main answer (the numbers the user asked for)."""
    raise NotImplementedError


def claims_for_insight(insight: Insight) -> list[Claim]:
    """Anomaly + where + why claims for one selected insight."""
    raise NotImplementedError


def check_answer(answer: str, claims: list[Claim]) -> list[str]:
    """Numbers in the LLM's answer that match no claim (for repair and for evaluation)."""
    raise NotImplementedError
