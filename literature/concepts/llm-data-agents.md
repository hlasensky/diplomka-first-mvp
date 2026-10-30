---
type: concept
aliases: [LLM data agents, LLM-based agents for BI, LLM-based data analysis, LLM-powered business intelligence, data agents, multi-agent data analysis, NL2Insight, NL2VIS]
---

Autonomní systémy postavené na velkých jazykových modelech, které z dotazu v přirozeném jazyce plánují a provádějí kroky analýzy dat (SQL, kód, grafy, insighty) ve spustitelném prostředí, často jako spolupráce více specializovaných agentů.

## Sources
- [[wengDataLabUnifiedPlatform2025]] — C1, C3: DataLab spojuje víceagentní framework s proxy agentem a notebook; dotaz se přes znalostní graf a JSON DSL převádí na SQL/Vega-Lite; C4, C5: doménové znalosti a výběr kontextu podle DAG buněk zlepšují přesnost a šetří tokeny.
- [[liuLLMassistedConversationalNavigation2026]] — C3: LLM omezené na odhad preferencí a vysvětlení, všechny výpočty a přístup k datům má deterministický cube engine; LLM vidí jen popisy schématu a předpočítané statistiky.

## Napětí
- [[liuLLMassistedConversationalNavigation2026]] C3 vs. [[wengDataLabUnifiedPlatform2025]] C3: NavLLM záměrně nenechává LLM generovat dotazy (jediný halucinovaný token v text-to-SQL může dát neplatný dotaz) a omezuje ho na skóre a vysvětlení; DataLab nechává LLM překládat dotaz do DSL a z něj na SQL/Vega-Lite a chyby krotí validací proti JSON Schema.

## Související
- [[llm-agents]]
- [[text-to-sql]]
- [[conversational-olap]]
