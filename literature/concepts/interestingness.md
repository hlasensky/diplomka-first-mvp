---
type: concept
aliases: [interestingness measure, subjective interestingness, surprise, highlight selection, insight ranking]
---

Míra, jak zajímavý (překvapivý, nový, relevantní) je nález pro uživatele. Používá se k řazení a výběru, co uživateli ukázat.

## Sources
- [[vassiliadisRollUpsDrillDownsIntentional2019]] — C4: subjektivní surprise jako rozdíl significance buňky v nové a předchozí kostce; vybere se komponenta modelu s maximem.
- [[franciaExplainingCubeMeasures2024]] — C4: zájem komponenty = R² (regrese) nebo |ρ| (křížová korelace) v [0, 1]; highlight = maximum, pravidla dominance odstraňují duplicity.
- [[franciaVOOLModularInsightbased2025]] — C2, C4: každý modul definuje vlastní zájem komponent; u Top-k se u navazujícího dotazu váží peculiaritou faktu vůči předchozímu výsledku (prior belief); zájem řídí výběr insightů.

## Související
- [[guided-data-exploration]]
- [[anomaly-detection]]
- [[intentional-analytics]]
