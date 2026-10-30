---
type: concept
aliases: [discovery-driven exploration, guided exploration, drill-down recommendation, insight recommendation, next-view recommendation, view recommendation]
---

Systém analytika aktivně vede k zajímavým částem dat (např. doporučuje, kam drillovat), místo aby je hledal ručně.

## Sources
- [[sarawagiDiscoverydrivenExplorationOLAP1998]] — C5: předpočítané SelfExp/InExp/PathExp ukazují, které buňky jsou výjimečné, pod kterými se výjimky skrývají a podél které dimenze drillovat.
- [[vassiliadisRollUpsDrillDownsIntentional2019]] — C2, C4: systém k výsledku automaticky vybírá highlights podle subjektivního překvapení; operátor Suggest doporučuje další dotaz.
- [[sarawagiExplainingDifferencesMultidimensional]] — C1, C2: jeden krok místo série drill-downů; systém sám najde řádky vysvětlující změnu mezi dvěma buňkami.
- [[liuLLMassistedConversationalNavigation2026]] — C2, C6: top-k doporučení dalšího pohledu podle součtu datové zajímavosti, LLM preference a diverzity; v simulacích vyšší kumulativní zajímavost než LLM-only i datové heuristiky (SeeDB, Smart Drill-Down, Voyager).

## Související
- [[olap]]
- [[anomaly-detection]]
- [[query-explanation]]
