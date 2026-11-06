---
type: concept
aliases: [LLM agents, LLM-based agents, language agents, ReAct, reasoning and acting, tool use, tool-augmented LLM, agent loop]
---

Velký jazykový model použitý jako politika agenta, který v cyklu uvažuje, volá akce či nástroje ve vnějším prostředí (vyhledávání, API, databáze) a výsledky pozorování zapracovává do dalšího rozhodování.

## Sources
- [[yaoReActSynergizingReasoning2023a]] — C2: ReAct rozšiřuje prostor akcí o jazykové „myšlenky“ a střídá kroky thought–action–observation; C5, C7: lepší než jen jednání (Act) na HotpotQA, FEVER, ALFWorld a WebShop, kombinace s CoT-SC nejlepší v QA; C6: typická selhání jsou zacyklení a neinformativní vyhledávání.
- [[wangChartInsighterApproachMitigating2025]] — C4, C5: tři agenti (Uni-Insighter, Multi-Insighter, Writer) volají externí analytické moduly a v iteracích (max. 5) skládají shrnutí grafu, které ověří test sebekonzistence.
- [[gengJSONSchemaBenchRigorousBenchmark2025]] — C1: benchmark omezeného dekódování JSON schémat zahrnuje i signatury funkcí pro volání nástrojů (GlaiveAI function calling V2).
- [[leiSpider20Evaluating2025]] — C2, C4: agentní nastavení Spider 2.0 (codebase + rozhraní databáze); nejlepší Spider-Agent s o1-preview vyřeší jen 21,36 % podnikových text-to-SQL úloh.
- [[patilGorillaLargeLanguage2024]] — C1, C2: generování volání API z přirozeného jazyka; LLaMA-7B dotrénovaný na 16 450 dvojicích instrukce–API, s retriever-aware training na přiložené dokumentaci API; C4: zero-shot přesnost 59,13 / 71,68 / 83,79 % proti 38,70 / 19,80 / 18,20 % u GPT-4; C5: dotrénování lepší než naivní retrieval a než GPT se 3 příklady v kontextu.

## Napětí
- [[yaoReActSynergizingReasoning2023a]] C5 vs. [[patilGorillaLargeLanguage2024]] C5: ReAct staví na few-shot promptování zmrazeného modelu a vnější vyhledávání mu v QA pomáhá; Gorilla pro generování volání API ukazuje, že přiložený retrieval může výkon zhoršit (BM25 −52,27 % proti oracle) a dotrénování překonává promptování (jiná úloha: fakta z Wikipedie vs. syntaxe a výběr API).

## Související
- [[llm-data-agents]]
- [[text-to-sql]]
