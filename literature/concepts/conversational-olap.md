---
type: concept
aliases: [Conversational OLAP, COOL, conversational BI, conversational business intelligence, natural language OLAP, dialog-based OLAP, conversational analytics, voice-based OLAP, hands-free data exploration]
---

Analýza vícerozměrných dat formou dialogu v přirozeném jazyce (psaném nebo mluveném), kde systém převádí jednotlivé repliky na dotazy a OLAP operace a pamatuje si kontext předchozích dotazů.

## Sources
- [[franciaCOOLFrameworkConversational2022]] — C1, C4, C5: první framework, který překládá dialog na celou OLAP session (úplný GPSJ dotaz + následné OLAP operátory) s disambiguací automaticky, z logu nebo dotazem na uživatele.
- [[franciaVOOLModularInsightbased2025]] — C1: query-to-text část konverzačního OLAP (navazuje na COOL pro text-to-query); hlasový popis výsledků celé OLAP session, ne jen jednotlivých dotazů.
- [[wengDataLabUnifiedPlatform2025]] — C3: LLM-powered BI nad firemními daty; vícekolové dotazy (fráze typu „what about“) se přepisují s kontextem předchozích kol a překládají do DSL s měrami, dimenzemi a podmínkami.
- [[liuLLMassistedConversationalNavigation2026]] — C1, C2: konverzační navigace jako doporučení dalšího pohledu; promluvy uživatele neslouží k překladu na dotaz, ale LLM z nich odhaduje preferenční skóre kandidátních pohledů (drill-down, roll-up, slice, dice) v grafu pohledů.

## Napětí
- [[liuLLMassistedConversationalNavigation2026]] C2 vs. [[franciaCOOLFrameworkConversational2022]] C4: NavLLM se označuje za první formální model konverzační navigace nad kostkami, ale COOL už formalizoval konverzační OLAP session (stavy engage/navigate, gramatika OLAP operátorů nad předchozím dotazem); NavLLM COOL necituje. Liší se i role promluvy: v COOL se deterministicky překládá na OLAP operaci, v NavLLM jen řadí kandidátní pohledy.

## Související
- [[olap]]
- [[text-to-sql]]
- [[intentional-analytics]]
- [[data-narration]]
- [[llm-data-agents]]
