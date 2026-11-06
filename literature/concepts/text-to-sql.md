---
type: concept
aliases: [text-to-SQL, NL2SQL, NLIDB, natural language interface to databases, natural language querying]
---

Překlad otázky v přirozeném jazyce na spustitelný SQL dotaz nad databází, ať už pomocí pravidel a gramatik, nebo pomocí (velkých) jazykových modelů.

## Sources
- [[franciaCOOLFrameworkConversational2022]] — C3, C8: text-to-SQL řízený gramatikou (n-gramy + Levenshteinova podobnost + LL(1) gramatika + generování SQL z metadat DW); related work srovnává NaLIR, SQLizer, SODA, ATHENA, Analyza.
- [[wengDataLabUnifiedPlatform2025]] — C3, C4: LLM nejdřív překládá dotaz do JSON DSL (measures, dimensions, podmínky) validovaného JSON Schema a z něj pravidly SQL; automaticky generované znalosti o tabulkách a sloupcích zvedly na firemních datech Recall@5 schema linkingu o 38,47 % a přesnost NL2DSL o 58,58 %.
- [[liCanLLMAlready2023a]] — C2, C4, C5: benchmark BIRD (12 751 otázek, 95 reálných databází, 33,4 GB) s metrikami EX a VES; GPT-4 na testu 54,89 % EX vs. lidé 92,96 %; C7: nejčastější chyby LLM jsou schema linking a nepochopení obsahu databáze.
- [[leiSpider20Evaluating2025]] — C2, C4, C5: benchmark Spider 2.0 (632 podnikových úloh, průměrně 812 sloupců, různé SQL dialekty); agent s o1-preview SR 21,36 %, DAIL-SQL + GPT-4o na Spider 2.0-lite EX 5,68 % vs. 86,6 % na Spider 1.0 a 57,4 % na BIRD; C7: chyby hlavně v analýze dat (35,5 %) a schema linkingu (27,6 %).

## Napětí
- [[leiSpider20Evaluating2025]] C7 vs. [[liCanLLMAlready2023a]] C7: v BIRD je nejčastější chybou schema linking (41,6 %, ChatGPT), ve Spider 2.0 je to chybná analýza dat (35,5 %) před schema linkingem (27,6 %); různé modely, vzorky i kategorizace chyb.
- [[leiSpider20Evaluating2025]] C4, C5 vs. [[liCanLLMAlready2023a]] C5: BIRD paper uvádí pro GPT-4 na testu 54,89 % EX, Spider 2.0 uvádí pro BIRD 73,0 % (metody s GPT-4, z literatury) a 57,4 % pro DAIL-SQL + GPT-4o; jiné metody, období a sady (test vs. převzaté výsledky).

## Související
- [[conversational-olap]]
- [[olap]]
- [[llm-data-agents]]
