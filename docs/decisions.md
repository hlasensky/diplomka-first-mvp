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

## 2026-10-07 – ověření dat před packem `multi-senger`

1. **Časy BeeObserveru jsou v UTC** (naivní timestamp, bez letního času).
   - Denní minimum `t_o` v červnu je v 03:30, ERA5 `t2m` (UTC) v 03:00, kolem východu slunce.
   - Zpoždění mezi `t_o` a ERA5 je v létě i v zimě stejné (±0,35 h), takže posun o hodinu kvůli letnímu času tam není.
   - Počasí z Open-Meteo (UTC) se dá spojit přímo.
2. **Chyba v den jarní změny času** (29. 3. 2020, 28. 3. 2021, 27. 3. 2022):
   - Minuty 02:00–02:59 mají v datech časovou značku 01:xx, takže vzniklo 3 440 duplicitních dvojic (klíč, čas).
   - Druhý blok podle pořadového sloupce `X` je ve skutečnosti 02:xx.
   - Hodinová data `senger` tu chybu přebírají: hodina 01 je průměr ze 120 minut a hodina 02 chybí.
   - **Opraveno** v `datasets/multi-senger/build.sql`, sekce 1a. Raw CSV zůstávají beze změny.
     - Řádek z hodiny 01 v den změny se posune o +1 h, pokud mu podle `X` předchází řádek se stejnou nebo pozdější minutou (čas se vrátil zpět).
     - Posunuto je 3 490 řádků: 3 440 duplicit a 50 minut, jejichž protějšek v prvním bloku chybí. Hlídací dotaz 1b shodí build, kdyby nějaká duplicita zbyla.
   - Hodinová data se proto počítají z opravených minut.
3. **Hodinová data = průměr minut**, i pro `weight_delta`, tedy průměr na minutu, ne změna za hodinu.
   - Agregace minut na hodiny dává totéž co `senger` (638 412 hodin, rozdíl < 1e-5).
   - 15,6 % hodin má méně než 60 minut a 4,2 % méně než 30. Do faktu přidat `n_minutes`.
   - Některé sloupce jsou v jednom CSV celé `NA`, proto je třeba explicitní převod na `DOUBLE`.
4. **Lokace jsou zaokrouhlené na 0,1°** (asi 5–7 km).
   - Každý klíč má jedinou lokaci, shodnou s `locations.csv`. Je 34 buněk.
   - 27 z 34 buněk leží do 7 km od hranice okresu.
   - U 7 buněk spadne bod do jiného okresu, než který pokrývá většinu čtverce zaokrouhlení (např. 48.9_8.3: bod je v okrese Karlsruhe, ale 62 % plochy připadá na Rastatt).
   - Buňka 49.2_6.9 leží bodem ve Francii a 35 % jejího čtverce připadá na Regionalverband Saarbrücken.
   - **Rozhodnutí:** místo jednoho okresu na buňku použít bridge tabulku buňka × okres s váhou podle podílu plochy (čtverec ±0,05°, předpoklad zaokrouhlení na nejbližší hodnotu, ve VG250 v EPSG:25832).
   - Spolková země: u 5 buněk čtverec zasahuje do dvou zemí (Hamburg, Bremen, Berlin).
5. **VG250 a Regionalstatistik:**
   - VG250 má 400 okresů (`vg250_krs`, `GF=4`).
   - CSV mají 472 pětimístných kódů:
     - 73 z nich jsou zaniklé okresy s prázdnými řádky,
     - Eisenach (16056) má data, ale od roku 2021 je součástí 16063,
     - Berlin a Hamburg mají jen dvoumístný kód (`11`, `02`), který je třeba mapovat na `11000` a `02000`.
   - Značky: `-` = nic (0), `.` = neznámé nebo utajené, `/` = nespolehlivé. Poslední dvě převést na NULL a zachovat příznak.
   - Plochy jsou podle sídla podniku (Betriebssitzprinzip). Výnosy v Porýní-Falci mají krajská města započtená do okolních okresů. Pro Berlin, Bremen a Hamburg výnosy nejsou.
   - Pokrytí řepky v okolí úlů (podle váhy plochy):
     - plocha 2020: úplné u 17 z 34 buněk, žádné u 5,
     - výnos 2020: úplné u 14 z 34, žádné u 9.

## 2026-10-07 – pack `multi-senger` postavený

6. **Minutová data jsou tabulka přímo v DuckDB** (`fact_hive_minute`), ne Parquet s view.
   - Relativní cesta ve view se vyhodnocuje vůči složce, ze které se program spouští, a ta se u buildu a aplikace liší.
   - Databáze má 0,94 GB. Kdyby to vadilo, minuty se přesunou do Parquetu a cestu nastaví aplikace při startu.
7. **Přiřazení buňky k okresům přes bridge tabulku s váhami** (`bridge_cell_district`).
   - `dim_cell` a `dim_colony` nesou hlavní okres a spolkovou zemi podle největšího podílu.
   - Kontext plodin pro lokalitu je předpočítaný a vážený v `agg_cell_crop`, takže LLM nemusí psát vážené dotazy.
8. **Fenologie:** pozorování s QB 1, 2 a 3 (bez námitky, opraveno, námitka zamítnuta). Hodnotu pro buňku dává medián přes stanice do 25 km.
   - Pokrytí v letech 2019–2022: pampeliška, akát a lípa u všech 34 buněk, řepka u 30–31.
9. **Eurostat `ef_lsk_bees` se nepoužívá:** z období dat má jen rok 2020 a FAOSTAT pokrývá totéž ročně.
10. **Zimní ztráty** jsou v buildu zapsané ručně (`fact_winter_loss`). U každého čísla je `citekey` a `evidence` (claim nebo strana). Primární míra je `loss_pct_pooled` (ztracená / zazimovaná včelstva, jako u COLOSS).
11. **Změny v kódu aplikace:**
    - Validátor povoluje `corr` u všech měr, stejně jako `count`: korelace dvou řad nic neagreguje nesprávně.
    - Prompt vypisuje spojení faktů přes sdílenou dimenzi i s podmínkou `ON`.
12. **Národní data jsou napojená přes zmenšené dimenze** `dim_country`, `dim_year` a `dim_bee_winter` (shrunken rollup dimension).
    - `dim_time` má jeden řádek na hodinu, takže fakty na grainu rok nebo zima se na něj nesmí napojit přímo. `dim_time` se na nové dimenze jen roluje nahoru (`year`, `bee_winter`).
    - Plodiny, fenologie a národní fakty mají `year` → `dim_year` a `bee_winter` → `dim_bee_winter`.
    - Schéma je v `docs/multi-senger_schema.puml`, povolená spojení faktů v `docs/multi-senger_joins.puml` (obojí vykreslené jako `.svg` a `.png`).
13. **`dim_date` pro denní grain.** Každý fakt se teď napojuje na časovou dimenzi svého grainu (pravidlo R7):

    | Fakty | Časová dimenze |
    |---|---|
    | hodinové | `dim_time` |
    | denní (`agg_colony_daily`, `agg_weather_daily`, `fact_vegetation`) a data událostí | `dim_date` |
    | roční | `dim_year` |
    | zimní | `dim_bee_winter` |

    - Hierarchie: `dim_time` → `dim_date` → `dim_year` a `dim_bee_winter`.
    - Odpadla vazba 1:N mezi denními fakty a hodinovým `dim_time`, kde hrozil fan trap.
