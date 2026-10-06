---
type: concept
aliases: [anomaly, anomalies, exception, exceptions, outlier detection, outliers]
---

Identifikace hodnot, které se výrazně odchylují od očekávání daného modelem nebo kontextem.

## Sources
- [[sarawagiDiscoverydrivenExplorationOLAP1998]] — C2, C3: výjimka v OLAP kostce = standardizované reziduum log-lineárního modelu přes všechna group-by nad prahem τ = 2,5.
- [[vassiliadisRollUpsDrillDownsIntentional2019]] — C5: outlier model (z-score > 2σ) je jedna z antagonistických komponent. V příkladu vyhrává jako highlight (skóre 0,85 vs 0,61 pro top-5).
- [[wuScorpionExplainingAway2013]] — C1: neodhaluje anomálie sám, ale vysvětluje uživatelem označené odlehlé agregované hodnoty (např. vadné senzory v datech Intel, C8).
- [[franciaVOOLModularInsightbased2025]] — C4: modul Outliers vrací odlehlé fakty výsledku dotazu, zájem = anomaly score (Isolation Forest).
- [[blazquez-garciaReviewOutlierAnomaly2021]] — C2–C4: taxonomie detekce odlehlých hodnot v časových řadách (vstup, typ odlehlé hodnoty – bod/podsekvence/celá řada, povaha metody); většina metod porovnává pozorování s očekávanou hodnotou a prahem.
- [[liuElephantRoomReliable2024]] — C2–C4: benchmark TSB-AD (1070 řad, 40 algoritmů); doporučuje metriku VUS-PR, point adjustment zvýhodňuje náhodné skóre, statistické metody často vedou.
- [[zhouCanLLMsUnderstand2025]] — C3, C7: LLM detekují jednoduché anomálie zero-shot (lépe z obrázku), CoT nepomáhá; důkaz pro jemné reálné anomálie chybí (C8).

## Související
- [[llm-time-series]]
- [[olap]]
- [[guided-data-exploration]]
