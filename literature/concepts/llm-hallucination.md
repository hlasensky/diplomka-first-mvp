---
type: concept
aliases: [hallucination, hallucinations, LLM hallucination, factual errors, faithfulness, unfaithful generation, hallucination mitigation]
---

Tvrzení vygenerované jazykovým modelem, které neodpovídá vstupním datům nebo faktům (chybná hodnota, trend, extrém, vztah), a metody, jak takové chyby odhalit, klasifikovat a omezit.

## Sources
- [[wangChartInsighterApproachMitigating2025]] — C2, C3: taxonomie 10 typů halucinací ve shrnutích grafů časových řad (nejčastější Trend Direction Error a Detail Omission, obě 22,1 %); C4, C5: omezení externími analytickými moduly, majoritním hlasováním a testem sebekonzistence; C7: míra halucinací 0,14 vs. 0,48 u GPT-4.
- [[patilGorillaLargeLanguage2024]] — C3: halucinace volání API = volání, které není podstromem AST žádného API v databázi (vymyšlený nástroj), odlišené od chybného použití existujícího API; C4: zero-shot GPT-4 halucinuje 36,55 / 37,16 / 78,65 % volání (TorchHub / HuggingFace / TensorFlow Hub), dotrénovaná Gorilla 6,98 / 10,95 / 5,40 %.

## Napětí
- [[wangChartInsighterApproachMitigating2025]] C2 vs. [[patilGorillaLargeLanguage2024]] C3: odlišná definice – u Wanga halucinace zahrnuje každou chybu vůči datům (vč. vynechání detailu), u Gorilly jen volání neexistujícího API, zatímco chybné použití existujícího API je samostatná kategorie „error“.

## Související
- [[data-narration]]
- [[llm-time-series]]
- [[llm-agents]]
