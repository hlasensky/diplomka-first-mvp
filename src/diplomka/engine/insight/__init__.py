"""Anomalies and their explanation on top of the engine (skeleton).

Split from docs/decisions.md (2026-10-05): anomalies are detected deterministically; the LLM only picks
what to examine, plans the next operators and words the explanation. Every claim has provenance.

- ``exceptions`` - exceptions in the cube (discovery-driven exploration), where to drill
- ``series``     - anomalies in a single time series (one colony, one measure)
- ``diff``       - "where": which rows explain a change between two aggregated cells
- ``relate``     - "why": associations with measures of other facts, with time lag
- ``ranking``    - interestingness and the choice of at most 1-2 insights per answer
- ``scan``       - proactive search under and next to the current slice
- ``claims``     - claims with provenance, the only thing the LLM may put into an answer
"""
