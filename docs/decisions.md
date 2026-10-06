# Rozhodnutí

Stručný log rozhodnutí. Data jsou popsaná v [data.md](data.md).

## 2026-10-05

1. **Data: jádro tvoří IoT senzory z úlů (BeeObserver, Německo).** Zadání chce OLAP nad časovými řadami z chytrých zařízení. US Bee OLAP (USDA statistiky) odpadá, protože to nejsou IoT data a srovnatelná US senzorová data nejsou veřejně dostupná. Vedoucí souhlasí.
2. **Rozsah dat se nezužuje** (doporučení vedoucího). Ke kontextu patří počasí, fenologie, vegetace, plodiny a makro data, každé jako samostatný fakt. Metodiku slučování (grainy, constellation, neaditivní metriky) přebíráme z US návodu.
3. **Přínos práce: LLM jako orchestrátor analýzy.**
   - Anomálie detekuje deterministický algoritmus.
   - LLM vybírá, co zkoumat, plánuje drill-down, hledá souvislosti v jiných faktech a vysvětluje.
   - Semantic layer zaručuje, že čísla jsou spočítaná správně.
   - Každé tvrzení v odpovědi má provenance (dotaz, který ho podložil).
4. **Proaktivita:** anomálie hlásí systém sám. Hledá kontextově, tedy pod aktuálním řezem a vedle něj, a hlásí nejvýš 1–2 upozornění na odpověď, seřazená podle zajímavosti a relevance k otázce.
5. **Vysvětlení má dvě části:**
   - *kde*: rozpad změny přes dimenze ve stylu DIFF,
   - *proč*: souvislosti v jiných faktech přes sdílené dimenze. Kandidáty vybere semantic layer, hypotézy LLM, ověří je statistika (včetně zpoždění).
   - Formulace „souvisí s“, ne „způsobilo“.
6. **UI stack zatím nerozhodnutý.** Nejdřív vznikne API hranice (FastAPI) kolem agenta. Chainlit nad ní poběží dál a stack se vybere později.
7. **Literární kotvy (vault):**
   - Sarawagi 1998: proaktivní výjimky,
   - Sarawagi 1999: DIFF,
   - Vassiliadis 2019: intentional analytics, subjektivní zajímavost,
   - Francia 2024: operátor explain.

**Otevřené:**
- volba UI stacku,
- MSPB jako ground truth pro evaluaci anomálií,
- nový dataset pack, nebo rozšíření `senger`.
