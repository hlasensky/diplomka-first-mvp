---
type: concept
aliases: [text-to-SQL, NL2SQL, NLIDB, natural language interface to databases, natural language querying]
---

Překlad otázky v přirozeném jazyce na spustitelný SQL dotaz nad databází, ať už pomocí pravidel a gramatik, nebo pomocí (velkých) jazykových modelů.

## Sources
- [[franciaCOOLFrameworkConversational2022]] — C3, C8: text-to-SQL řízený gramatikou (n-gramy + Levenshteinova podobnost + LL(1) gramatika + generování SQL z metadat DW); related work srovnává NaLIR, SQLizer, SODA, ATHENA, Analyza.
- [[wengDataLabUnifiedPlatform2025]] — C3, C4: LLM nejdřív překládá dotaz do JSON DSL (measures, dimensions, podmínky) validovaného JSON Schema a z něj pravidly SQL; automaticky generované znalosti o tabulkách a sloupcích zvedly na firemních datech Recall@5 schema linkingu o 38,47 % a přesnost NL2DSL o 58,58 %.
- [[liCanLLMAlready2023a]] — C2, C4, C5: benchmark BIRD (12 751 otázek, 95 reálných databází, 33,4 GB) s metrikami EX a VES; GPT-4 na testu 54,89 % EX vs. lidé 92,96 %; C7: nejčastější chyby LLM jsou schema linking a nepochopení obsahu databáze.

## Související
- [[conversational-olap]]
- [[olap]]
- [[llm-data-agents]]
