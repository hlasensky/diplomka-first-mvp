---
type: concept
aliases: [LLM agents, LLM-based agents, language agents, ReAct, reasoning and acting, tool use, tool-augmented LLM, agent loop]
---

Velký jazykový model použitý jako politika agenta, který v cyklu uvažuje, volá akce či nástroje ve vnějším prostředí (vyhledávání, API, databáze) a výsledky pozorování zapracovává do dalšího rozhodování.

## Sources
- [[yaoReActSynergizingReasoning2023a]] — C2: ReAct rozšiřuje prostor akcí o jazykové „myšlenky“ a střídá kroky thought–action–observation; C5, C7: lepší než jen jednání (Act) na HotpotQA, FEVER, ALFWorld a WebShop, kombinace s CoT-SC nejlepší v QA; C6: typická selhání jsou zacyklení a neinformativní vyhledávání.
- [[wangChartInsighterApproachMitigating2025]] — C4, C5: tři agenti (Uni-Insighter, Multi-Insighter, Writer) volají externí analytické moduly a v iteracích (max. 5) skládají shrnutí grafu, které ověří test sebekonzistence.

## Napětí

## Související
- [[llm-data-agents]]
- [[text-to-sql]]
