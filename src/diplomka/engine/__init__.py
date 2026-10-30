"""OLAP engine over the semantic layer (skeleton - signatures and docstrings only, no implementation).

Layers, from the cube model to explained insights:

- ``query``     - cube query model (GPSJ query = "where in the cube am I")
- ``operators`` - OLAP operators as pure transformations of a query (roll-up, drill-down, slice, ...)
- ``checks``    - checks of a query against the multidimensional model (additivity, domains, rules)
- ``planner``   - choice of the fact table and of the join path in the join graph
- ``compiler``  - query + plan -> Ibis expression -> SQL
- ``executor``  - runs the SQL, returns rows with provenance
- ``session``   - OLAP session: log of queries, current query as context for the next operator
- ``insight``   - anomaly detection, explanation (where / why) and selection of what to report

The engine reads only ``datasets/<pack>/semantic_layer.yaml`` through ``diplomka.schema.SemanticLayer``.
Ibis (``ibis-framework[duckdb]``) is not a project dependency yet: ``uv add "ibis-framework[duckdb]"``.

Literature references in the docstrings are ``citekey Cn`` (claim n of ``literature/sources/<citekey>.md``).
Status on 2026-10-30 - only the first one may back a \\cite:

- sarawagiDiscoverydrivenExplorationOLAP1998 - confirmed, verified
- sarawagiExplainingDifferencesMultidimensional - candidate (verified: true, precteno: ne; bib entry incomplete)
- franciaCOOLFrameworkConversational2022 - candidate, unverified, precteno: ne
- franciaExplainingCubeMeasures2024 - candidate, unverified, precteno: ne
- vassiliadisRollUpsDrillDownsIntentional2019 - candidate, unverified, precteno: ne
- franciaVOOLModularInsightbased2025 - candidate, unverified, precteno: ne
- wuScorpionExplainingAway2013 - candidate, unverified, precteno: ne
- blazquez-garciaReviewOutlierAnomaly2021 - candidate, unverified, precteno: ne

Tools (not peer-reviewed, see docs/olap-arch.md): Cubes (cell + browser), dbt MetricFlow (join graph,
fan-trap rules), Boring Semantic Layer (YAML -> Ibis -> SQL), Calcite lattices (aggregate navigation).
"""
