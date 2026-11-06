---
citekey: johnApplicationTimeSeries2023
title: "Application of Time Series Database for IoT Smart City Platform"
authors: "John, Petr; Hynek, Jiří; Hruška, Tomáš; Valný, Michal"
year: 2023
venue: "2023 Smart City Symposium Prague (SCSP), IEEE, 1–6"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [time-series-database, internet-of-things]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/MVHQ28BA)

## TL;DR
Článek skupiny z FIT VUT a firmy Logimic porovnává PostgreSQL, DynamoDB, MongoDB a InfluxDB pro ukládání a dotazování dat z [[internet-of-things|IoT]] zařízení v platformě pro smart city (vkládání, výběr úseku, agregace, poslední hodnota, velikost na disku). Na reálné platformě Logimic pak nahradili DynamoDB [[time-series-database|databází časových řad]] InfluxDB, což snížilo náklady a zabranou plochu.

## Klíčová tvrzení
- C1: Data ze smart city jsou časové řady; uživatel v mnoha případech potřebuje agregovaná data, protože načítání surových dat při zobrazení dlouhého úseku zpomaluje UI, a vhodná agregační funkce sníží počet bodů bez ztráty nebo s přijatelnou ztrátou přesnosti; optimalizace pro časové řady jsou častěji v NoSQL než v relačních databázích. (s. 1, §I; s. 2, §I)
- C2: Metoda: třífázový test (vložení hodnoty, výběr časového úseku bez agregace, s agregací a dotaz na poslední prvek) – nejdřív malý soubor asi 30 MB (každý test 20×, zprůměrováno), pak soubor přes 500 tisíc záznamů o velikosti asi 350 MB a nakonec reálná data ze senzorů RHF1S001 za rok od Logimicu (163 MB, asi 670 tisíc položek). (s. 3, §III)
- C3: Výsledky: po první fázi zůstaly jako použitelné jen MongoDB a InfluxDB (DynamoDB a PostgreSQL výrazně pomalejší); MongoDB bez režimu časových řad byl často rychlejší než InfluxDB (5minutový průměr 2699 ms, s režimem časových řad 4338 ms, InfluxDB 4165 ms) a rozdíly byly často v desítkách ms; 350MB datová sada zabrala v PostgreSQL 787 MB, v nekomprimovaném MongoDB verze 5: 265 MB a v InfluxDB 69 MB. (s. 3, §IV; s. 4, §IV)
- C4: Případová studie Logimic: InfluxDB nahradil DynamoDB pro časové řady (DynamoDB zůstal pro konfiguraci a metadata, metadata senzorů jsou v PostgreSQL); náklady InfluxDB a DynamoDB dohromady klesly asi na 40 % nákladů DynamoDB k 1. 1. 2022. (s. 4, §V)
- C5: Omezení InfluxDB: v jednom poli nelze míchat čísla a řetězce, neumí vnořené dokumenty a nemá optimalizaci pro přístup k poslednímu prvku; v architektuře Logimicu může uložení metadat senzorů v relační databázi zpomalit UI, protože se před dotazem na časové řady musí dotázat relační databáze, a kombinace AWS Lambda a REST API může mít horší výkon kvůli studeným startům, hlavně při nízkém provozu. (s. 4, §VI; s. 5, §VI)

## Vztah k mé práci


## Citovat pro


## Pozor
- Článek z workshopové konference (SCSP), 6 stran; autoři jsou skupina vedoucího (John, Hruška).
- Nekonzistence v číslech úspor: na s. 2 (§I) „40% savings in running costs“, na s. 4 (§V) „reduced to around 40% of the cost“ – to jsou různé věci (úspora 40 % vs. 60 %). Citovat jen znění z §V, nebo se vyhnout číslu.
- Výsledky výkonu jsou hlavně v grafech (obr. 1–3), v textu jsou jen vybraná čísla; testy na jednom notebooku (i5 7500HQ, 16 GB RAM).
- DuckDB ani TimescaleDB článek netestuje.
