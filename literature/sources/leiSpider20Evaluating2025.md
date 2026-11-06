---
citekey: leiSpider20Evaluating2025
title: "Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows"
authors: "Lei, Fangyu; Chen, Jixuan; Ye, Yuxiao; Cao, Ruisheng; Shin, Dongchan; Su, Hongjin; Suo, Zhaoqing; Gao, Hongcheng; Hu, Wenjing; Yin, Pengcheng; Zhong, Victor; Xiong, Caiming; Sun, Ruoxi; Liu, Qian; Wang, Sida; Yu, Tao"
year: 2025
venue: "The Thirteenth International Conference on Learning Representations (ICLR 2025)"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [text-to-sql, llm-agents, llm-data-agents]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/YMU64NSD)

## TL;DR
Benchmark Spider 2.0 (632 úloh) přenáší [[text-to-sql]] z malých akademických databází do podnikového prostředí: reálné databáze se stovkami až tisíci sloupců, vnořenými schématy, různými SQL dialekty (BigQuery, Snowflake, SQLite, DuckDB…) a projekty v DBT. Nejlepší agent (o1-preview) vyřeší jen 21,3 % úloh a klasické text-to-SQL metody, které mají na Spider 1.0 a BIRD vysokou přesnost, dosahují na Spider 2.0-lite jen jednotek procent. Hlavní příčiny chyb jsou chybná analýza dat (plánování dotazů, funkce dialektu) a špatné schema linking.

## Klíčová tvrzení
- C1: Problém: LLM sice na klasických benchmarcích dosahují vysoké přesnosti, ty ale používají neprůmyslové databáze s málo tabulkami a sloupci, jednoduché SQL a opomíjejí SQL dialekty; reálná podniková data leží v různých databázových systémech s vlastními dialekty, mají schémata s tisíci sloupců a vnořenými strukturami a reálné workflow vyžadují codebase projektu, externí znalosti a víc kroků. (s. 1, s. 2, §1)
- C2: Spider 2.0 obsahuje 632 úloh z podnikových případů užití; databáze pocházejí z průmyslových aplikací (např. Google Analytics, Salesforce), mají v průměru 812 sloupců a data v řádu terabajtů, běží lokálně (SQLite, DuckDB) i v cloudových skladech (BigQuery, Snowflake) a referenční SQL má v průměru 144 tokenů; vedle agentního nastavení (codebase + rozhraní databáze, metrika success rate) nabízí self-contained varianty Spider 2.0-lite a Spider 2.0-snow, kde je výstupem jen SQL hodnocené execution accuracy (EX). (s. 1, s. 2, s. 3, s. 6, Abstract, §1, §2.1, §3.1)
- C3: Konstrukce: osm autorů zběhlých v SQL vybralo databáze s více než 200 sloupci nebo vnořeným schématem (74 BigQuery, 54 Snowflake, 30 SQLite, 40 DuckDB, 10 PostgreSQL, 5 ClickHouse) a z 1 021 SQL z tutoriálů a fór a 157 transformačních projektů ponechalo 547 SQL a 78 DBT projektů; SQL musí mít víc než 50 tokenů (průměr BIRD je 30,9), proti úniku dat byla přepsána (84,2 % povrchově, 42 % sémanticky) a každou anotaci kontrolovali nejméně tři anotátoři (chyby v 45 % příkladů po prvním a 5 % po druhém kole, pak opraveny všechny). (s. 3, s. 4, s. 5, §2.2)
- C4: Výsledky agentů: nejlepší Spider-Agent s o1-preview má na Spider 2.0 success rate 21,36 % (v abstraktu 21,3 %); pro kontext autoři uvádějí, že metody založené na GPT-4 dosahují na Spider 1.0 a BIRD execution accuracy 91,2 % a 73,0 % (jiná metrika i nastavení). Nejvyšší EX je 23,40 % na Spider 2.0-lite (o3-mini) a 23,77 % na Spider 2.0-snow (o1-preview), Claude-3.5-Sonnet má na Spider 2.0 SR 14,87 % a GPT-4o 12,34 %. (s. 1, s. 6, s. 7, Abstract, §1, §3.2, Tab. 4, Tab. 6)
- C5: Klasické text-to-SQL metody: nejlepší DAIL-SQL + GPT-4o dosahuje na Spider 2.0-lite EX jen 5,68 % oproti 86,6 % na Spider 1.0 a 57,4 % na BIRD; fine-tunovaný SFT CodeS-15B má 0,73 % a na Spider 2.0-snow dosáhne i nejlepší metoda jen 2,20 % EX, což autoři přisuzují rozdílům SQL dialektů. (s. 7, §3.2, Tab. 5)
- C6: Na úlohách mimo DBT projekty klesá úspěšnost u databází s vnořenými sloupci (SR 10,34 % vs. 27,38 % bez nich) a u úloh s externími dokumenty (11,54 % vs. 26,64 %); u projektových úloh v DBT je SR 12,82 % vs. 23,22 % bez nich. U dokumentů model podle autorů obvykle volí správnou strategii, ale selže v převodu požadavků z dokumentu do SQL. (s. 8, §4.1, Tab. 7–9)
- C7: Rozbor chyb na 300 náhodně vybraných příkladech: chybná analýza dat 35,5 % (použití funkcí dialektu 10,3 %, pokročilé výpočty 7,5 %, složité plánování dotazu 17,7 %), špatné schema linking 27,6 % (sloupce 16,6 % – Spider 2.0-lite má přes 755 sloupců na databázi oproti zhruba 54 v BIRD –, tabulky 10,1 %) a chyby JOIN 8,3 %, protože databáze v BigQuery často nemají explicitní cizí klíče. (s. 8, s. 9, §4.2)
- C8: Dodání dokumentace k potřebným SQL funkcím (oracle) podle autorů přináší jen mírné zlepšení – v Tab. 10 jen u DAIL-SQL + GPT-4o (5,68 → 5,85 % EX), u DAIL-SQL + o1-preview EX naopak klesne (12,60 → 9,51 %); few-shot prompting s ručně vybranými příklady pomáhá jen okrajově (DAIL-SQL + GPT-4o: 5,68 % při 0-shot, 6,40 % při 1-shot, 6,76 % při 3-shot). Podle autorů je problémem hlavně správně použít funkce tak, aby odrážely záměr uživatele, a LLM potřebují výrazné zlepšení, aby byly použitelné v reálném podnikovém nasazení. (s. 1, s. 9, s. 10, Abstract, §4.3, Tab. 10–11)

## Vztah k mé práci


## Citovat pro


## Pozor
- Srovnání „91,2 % / 73,0 % → 21,3 %“ (abstrakt, seznam.md) míchá metriky i nastavení: 91,2 % a 73,0 % jsou EX metod založených na GPT-4 na Spider 1.0 a BIRD převzaté z literatury, 21,3 % je success rate agentu na Spider 2.0. Srovnatelné EX stejné metody jsou v Tab. 5 (DAIL-SQL + GPT-4o: 86,6 % / 57,4 % / 5,68 %), viz C5.
- Průměrný počet sloupců se v textu liší: s. 2 uvádí 812, Tab. 2 (s. 5) 743,5 pro Spider 2.0 a 812,1 pro Spider 2.0-snow, s. 9 „over 755“ pro Spider 2.0-lite.
- Tab. 10 (s. 9): u DAIL-SQL + o1-preview je EX s oracle funkcemi 9,51 % a bez nich 12,60 %, tj. horší; tvrzení o „mírném zlepšení“ platí jen pro GPT-4o (5,68 → 5,85 %). Tab. 4, 5, 10 a 11 ověřeny proti renderu PDF (s. 7–9).
- Obtížnost úloh je definována jen délkou referenčního SQL (< 80, 80–159, ≥ 160 tokenů); autoři v poznámce uvádějí, že existují i jiné způsoby měření (s. 6). Samostatnou sekci omezení paper nemá.
- Hodnocení je „execution-based focused“: skripty ignorují nepodstatné sloupce výsledku (s. 4, s. 6), takže EX tu není přesná shoda celé výsledkové tabulky.
- Fulltext: s. 18 a 26 (příloha) nahrazeny OCR; s. 19 je PAGE_WARN, obsahuje jen obrázky DAG (Obr. 9–10) a text o DBT úlohách – žádné tvrzení z ní nečerpá. Tvrzení jsou jen z hlavního textu (s. 1–10).
- Modely jsou z let 2024–2025 (o1-preview, o3-mini, GPT-4o, Claude-3.5-Sonnet); čísla stárnou.
