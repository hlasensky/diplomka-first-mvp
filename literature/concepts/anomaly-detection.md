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
- [[sengerWeightTemperatureHumidity2024]] — C7: prahové vyřazení chybných hodnot senzorů (váha mimo −50..150 kg, teplota mimo −40..85 °C, vlhkost mimo 0–100) a vyřazení skoků ve váze nad 0,3 kg/min (zásahy včelaře).
- [[alnegheimishLargeLanguageModels2024]] — C4, C7: detekce z reziduí mezi signálem a předpovědí (vyhlazení EWMA, práh čtyři směrodatné odchylky); na 11 datasetech (NASA, Yahoo S5, NAB) vede AER (F1 0,753), LLM přístup SigLLM dosahuje 0,525.

## Napětí
- [[liuElephantRoomReliable2024]] C4 vs. [[alnegheimishLargeLanguageModels2024]] C7: Liu uvádí, že na jednorozměrném TSB-AD tvoří víc než polovinu 12 nejlepších metod statistické přístupy a jednodušší architektury překonávají transformery; u Alnegheimish vede model hlubokého učení AER a statistické ARIMA a MP jsou až za ním. Liší se benchmark (TSB-AD vs. NASA/Yahoo S5/NAB) i metrika (VUS-PR vs. F1 se započtením částečné detekce).

## Související
- [[llm-time-series]]
- [[olap]]
- [[guided-data-exploration]]
