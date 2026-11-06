---
citekey: jensenTimeSeriesManagement2017
title: "Time Series Management Systems: A Survey"
authors: "Jensen, Soren Kejser; Pedersen, Torben Bach; Thomsen, Christian"
year: 2017
venue: "IEEE Transactions on Knowledge and Data Engineering 29(11), 2581–2600"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [time-series-database, internet-of-things, olap]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/EN54E83N)

## TL;DR
Přehledový článek o systémech pro správu časových řad (TSMS, jinak též time series databáze) z akademického a průmyslového výzkumu publikovaných v 2010s. Systémy třídí podle toho, jak je propojeno úložiště a zpracování dotazů (interní úložiště, externí DBMS/DFS, rozšíření RDBMS), a u každého sleduje mj. distribuovanost, vyspělost, aproximaci (AQP) a stream processing. Končí shrnutím výzkumných směrů a vizí distribuovaného „model-based sensor warehouse“ s datovou kostkou jako rozhraním pro analýzu.

## Klíčová tvrzení
- C1: Rostoucí nasazení senzorů (od IoT zařízení v domácnosti po rozsáhlé kyberfyzikální systémy) produkuje velké objemy časových řad, např. senzory Boeingu 787 vytvoří přes půl terabajtu dat za let ([[internet-of-things]]); obecné DBMS, zejména RDBMS, jsou podle autorů pro rychlost a objem těchto dat nevhodné, analýza často vyžaduje export do R nebo SPSS, a starší generace TSMS (SEQ, AQuery, SQL-TS) má omezenou paralelizaci a žádnou podporu distribuovaného zpracování. (s. 1, §Abstract, §1; s. 2, §1)
- C2: TSMS autoři definují jako jakýkoli systém vyvinutý nebo rozšířený pro ukládání a dotazování dat ve formě časových řad ([[time-series-database]]; jiný běžný název je Time Series Database); časová řada je konečná nebo neomezená posloupnost datových bodů seřazená podle rostoucího času. (s. 1, §1, pozn. 1)
- C3: Rozsah a metoda: přehled pokrývá systémy z akademického či průmyslového výzkumu dokumentované publikacemi z aktuální dekády, primárně systémy perzistentně ukládající mnoho časových řad pro agregační analýzu, se zaměřením na škálovatelnost; systémy pro senzorové uzly (Antelope, HybridStore, LittleD, StreamOp) vynechává; jako populární open-source/proprietární TSMS jmenuje OpenTSDB, KairosDB, Druid, InfluxDB a IBM Informix a pro výběr TSMS pro daný workload odkazuje na jiné práce (Druid sám rozebírá v §4.2); literaturu hledali nestrukturovaně přes Google Scholar a pak iterativně (reference, citující práce, ročníky konferencí a časopisů jako ACM SIGMOD, IEEE Big Data, PVLDB, USENIX, publikace autorů). (s. 1, §Abstract; s. 2, §1; s. 11, §4.2)
- C4: Systémy dělí do tří kategorií podle propojení úložiště a zpracování (interní úložiště, externí DBMS nebo distribuovaný souborový systém, rozšíření RDBMS) a dále podle kritérií Year, Purpose (IoT, monitoring průmyslových instalací, datová analytika, evaluace výzkumu), Motivational Use Case, Distributed, Maturity (třístupňově: proof-of-concept, demonstration, mature), Scale Shown, Processing Engine, API, Approximation (jednoduché agregáty bez záruk chyby vs. AQP s modely nebo vzorkováním), Stream Processing, Storage Engine a Storage Layout (Tab. 1); podporované dotazy shrnuje Tab. 2 (select, insert, append, update, delete, aggregates, join, over, analytics). (s. 2, §2; s. 5–6, §2)
- C5: Kompromisy architektur: interní úložiště umožňuje hlubokou integraci a optimalizaci layoutu a jednoduché nasazení, ale nevyužije existující distribuovanou infrastrukturu; externí úložiště znovu využije existující DBMS/DFS a znalost jejich konfigurace a zkrátí vývoj, ale datový model DBMS omezuje zpracování a nasazení více systémů je složitější; rozšíření RDBMS (např. PostgreSQL) dává ukládání i analýzu v jednom systému bez exportu do R/SPSS, ale návrh RDBMS omezuje možné změny a transakce přidávají zbytečnou režii, pokud je časová řada neměnná. (s. 6, §3.1; s. 9, §4.1; s. 14, §5.1)
- C6: Zjištění k architektuře: TSMS s interním úložištěm jsou převážně centralizované (distribuovaný je jen WearDrive) a slouží hlavně pro embedded zařízení nebo jako proof-of-concept, za obecné a dostatečně úplné považují jen tsdb, Plato a PhilDB; systémy s externím úložištěm jsou z větší části distribuované, často vyvíjené s firmou a žádný neimplementuje zcela nové úložiště (znovu využívají např. MySQL, HDFS, Couchbase); rozšíření RDBMS je málo (v přehledu TimeTravel, F2DB a systém Bakkalian et al.), všechna přidávají AQP pomocí matematických modelů a žádné není distribuované. (s. 9, §3.3; s. 14, §4.3; s. 14–15, §5.2; s. 18, §7)
- C7: Zjištění k doplňkové funkcionalitě: stream processing při ingestu podporuje jen omezený počet systémů (žádný ze tří obecných TSMS s interním úložištěm ani žádné rozšíření RDBMS); aproximaci časových řad pro zrychlení dotazů, úsporu místa nebo analytiku implementuje víc systémů, ale rozhraní, kterým by doménoví experti doplnili vlastní modely, je vzácné. (s. 9, §3.3; s. 16, §5.3; s. 18, §7)
- C8: Výzkumné směry a vize: podle shrnutých prací je třeba úložiště a dotazovací procesor navržený od základu pro časové řady místo převzatých komponent RDBMS, in-memory/paralelní/distribuované zpracování pro interaktivní analýzu a vizualizaci a AQP (Shafer et al. navíc uvádějí, že RDBMS nesou pro časové řady zbytečnou funkcionalitu jako mazání a úpravy libovolných hodnot, a existující systémy fungují v podstatě jako sloupcová úložiště; Cuzzocrea označuje za naléhavé analytické metody odolné vůči nepřesným hodnotám a odlehlým hodnotám); autoři navrhují distribuovaný TSMS ukládající časové řady jako matematické modely s datovou kostkou jako rozhraním pro analýzu vícerozměrných časových řad ([[olap]]), se stream processingem pro transformaci a čištění dat při ingestu a s uživatelsky definovanými modely. (s. 16–17, §6.1; s. 17–18, §6.2; s. 18, §7)

## Vztah k mé práci


## Citovat pro


## Pozor
- Čísla stran v tvrzeních jsou strany PDF (1–20). Tištěné stránkování časopisu je 2581–2600, tedy tištěná strana = PDF strana + 2580 (s. 1 = 2581). Při citaci se stranou v práci přepočítat.
- Strany 3 a 4 jsou ve fulltextu nahrazené OCR textem (pdftotext byl horší). Obsahují jen Tab. 1 (souhrn systémů podle klasifikačních kritérií), která je v PDF otočená na šířku; v textu je i po OCR nečitelná. Tvrzení na Tab. 1 nestojí, kritéria jsou popsaná v textu na s. 2 a 5–6. Hodnoty pro jednotlivé systémy (Year, Maturity, Scale Shown, …) ověřovat jen v PDF.
- Tab. 2 (s. 5, podporované dotazy): v textovém extraktu zůstaly jen názvy systémů a sloupec Analytics, značky podpory (černé kroužky) se ztratily.
- Přehled je z roku 2017 a zahrnuje jen systémy z publikací v 2010s. InfluxDB, OpenTSDB, KairosDB a IBM Informix jen jmenuje (s. 2), Druid analyzuje (s. 11); TimescaleDB ani DuckDB v textu nejsou. Pro srovnání DuckDB vs. InfluxDB/TimescaleDB dává jen obecné kompromisy architektur (C5), ne přímé srovnání těchto systémů.
- Výzkumné směry v C8 jsou zčásti převyprávěné názory jiných autorů (Cuzzocrea et al., Shafer et al., Sharma et al., Palpanas), ne zjištění tohoto přehledu. Pokud je chceš citovat, zvaž primární zdroj.
- Obrázky v článku jsou překreslené z původních publikací jednotlivých systémů, taxonomický obrázek článek nemá.
