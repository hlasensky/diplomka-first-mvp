"""OLAP session: a sequence of related queries, not isolated ones.

COOL has two dialogue states [franciaCOOLFrameworkConversational2022 C4, candidate]: engage (a full query
is expected) and navigate (OLAP operators modify the last query from the log until a reset). The log
also serves defaults for ambiguities - the most frequent past choice [C5].

The previous result is also the user's "belief": subjective interestingness compares a new cube with its
counterpart in the previous one [vassiliadisRollUpsDrillDownsIntentional2019 C4, candidate], so the
session keeps results, not only queries (input for ``insight.ranking``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from diplomka.engine.executor import Result
from diplomka.engine.query import CubeQuery


@dataclass
class SessionStep:
    operator: str  # "query" for a full query, otherwise the operator name (drill_down, slice_, ...)
    query: CubeQuery
    result: Result | None


@dataclass
class Session:
    state: Literal["engage", "navigate"] = "engage"
    steps: list[SessionStep] = field(default_factory=list)
    reported: set[str] = field(default_factory=set)  # ids of insights already shown (no repeats)

    @property
    def current(self) -> CubeQuery | None:
        """The query the next operator applies to (None in state engage)."""
        raise NotImplementedError

    @property
    def previous_result(self) -> Result | None:
        """Result of the step before the current one - the "belief" for interestingness."""
        raise NotImplementedError

    def push(self, operator: str, query: CubeQuery, result: Result | None) -> None:
        """Append a step and switch to navigate."""
        raise NotImplementedError

    def reset(self) -> None:
        """Back to engage; keep the log for defaults."""
        raise NotImplementedError

    def preferred_choice(self, issue_rule: str, choices: tuple[str, ...]) -> str | None:
        """Most frequent past choice for this kind of ambiguity, if it is frequent enough."""
        raise NotImplementedError
