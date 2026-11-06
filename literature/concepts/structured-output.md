---
type: concept
aliases: [structured output, structured generation, constrained decoding, guided generation, grammar-constrained decoding, JSON schema output, strukturovaný výstup, omezené dekódování]
---

Generování výstupu jazykového modelu tak, aby odpovídal zadané struktuře (regulární výraz, gramatika, JSON schéma), typicky omezením povolených tokenů při dekódování.

## Sources
- [[willardEfficientGuidedGeneration2023]] — C2, C3: regex jako konečný automat a předem postavený index stav → povolené tokeny, maska v průměru O(1) místo O(N) přes slovník (knihovna Outlines); C4: rozšíření na CFG/LALR(1) přes zásobníkové automaty (JSON, Python, SQL), index pro gramatiku Pythonu ~50 MB; C5: srovnání s Guidance jen jedním grafem.
- [[gengJSONSchemaBenchRigorousBenchmark2025]] — C1: JSONSchemaBench, 10K reálných JSON schémat + JSON Schema Test Suite, šest frameworků (Guidance, Outlines, Llamacpp, XGrammar, OpenAI, Gemini) v osách efektivita/pokrytí/kvalita; C3: uzavřená API mají nízké pokrytí, ale míru souladu 0,92–1,00; C4: přeomezení vs. podomezení (XGrammar 38 kategorií podomezení); C5: omezené dekódování přesnost úloh zvyšuje (Guidance 54,0/55,9/83,8 % vs. LM 50,7/52,6/80,1 %).

## Napětí
- [[willardEfficientGuidedGeneration2023]] C3, C5 vs. [[gengJSONSchemaBenchRigorousBenchmark2025]] C2, C3: Willard & Louf (2023) označují běhovou cenu indexu Outlines za prakticky nepodstatnou a Guidance (verze 2023) v jejich jediném grafu škáluje s počtem tokenů hůře; v JSONSchemaBench (2025, novější verze knihoven, JSON schémata) má Outlines nejvyšší dobu kompilace (3,48–8,05 s), TPOT nad samotným LM a timeouty, zatímco Guidance je nejrychlejší.

## Související
- [[llm-agents]]
- [[text-to-sql]]
