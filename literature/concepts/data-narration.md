---
type: concept
aliases: [vocalization, data vocalization, query result vocalization, data-to-text, natural language description of query results, result verbalization, insight narration]
---

Automatické vytvoření textového nebo mluveného popisu výsledku dotazu nad daty, typicky výběrem a seřazením nejzajímavějších zjištění (insightů) a jejich převodem do přirozeného jazyka.

## Sources
- [[franciaVOOLModularInsightbased2025]] — C1–C3: místo celé tabulky vokalizuje vybrané insighty (šablonové věty modulů) seřazené podle pokrytí, s rozpočtem na počet slov řešeným jako multiple-choice knapsack.
- [[wangChartInsighterApproachMitigating2025]] — C4, C5: LLM agenti generují shrnutí grafu časové řady z datové tabulky a Vega-Lite specifikace přes insighty z externích modulů, iterativní zpřesňování a test sebekonzistence; C7: méně halucinací než GPT-4 a VL2NL.

## Související
- [[conversational-olap]]
- [[interestingness]]
- [[llm-hallucination]]
