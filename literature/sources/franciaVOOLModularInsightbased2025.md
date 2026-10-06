---
citekey: franciaVOOLModularInsightbased2025
title: "VOOL: A Modular Insight-Based Framework for Vocalizing OLAP Sessions"
authors: "Francia, Matteo; Gallinucci, Enrico; Golfarelli, Matteo; Rizzi, Stefano"
year: 2025
venue: "Information Systems 129, 102496"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [data-narration, conversational-olap, olap, interestingness, intentional-analytics, anomaly-detection]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/PTD5C8KR)

## TL;DR
VOOL hlasově popisuje výsledky OLAP session. Nečte celou tabulku, ale vybírá několik insightů, které nad výsledkem dotazu (a nad jeho porovnáním s předchozím dotazem) spočítají zásuvné moduly, např. top-k, clustering, outliers nebo assess. Každý insight má šablonový text, zájem, pokrytí a cenu v počtu slov. Výběr řeší jako multiple-choice knapsack s rozpočtem na délku promluvy. Evaluace zahrnuje uživatelský test s 25 lidmi, měření efektivity, volbu rozpočtu a kvalitativní srovnání s GPT4o a dvěma ChatGPT aplikacemi pro analýzu dat, které podle autorů halucinují a dělají kvantitativní chyby.

## Klíčová tvrzení
- C1: Problém: překlad přirozeného jazyka na OLAP dotazy je dobře prozkoumaný, ale vokalizace výsledků OLAP session jen částečně; hrozí zahlcení uživatele dlouhým popisem, proto se vokalizují jen vybrané insighty ([[data-narration]], [[conversational-olap]]). Šest požadavků: automation, session-awareness, intention-awareness, extensibility, timeliness, conciseness. (s. 1, §1, §1.1; s. 2, §1.1)
- C2: Insight je množina komponent (každá popisuje fakt nebo skupinu faktů výsledku [[olap]] dotazu) s textem NL(s) z předdefinované gramatiky daného modulu, zájmem int(s) = součet int(v) komponent, pokrytím cov(s) ∈ (0, 1] a cenou cost(s) = počet slov NL(s). Insighty jsou samostatné věty a v rámci modulu inkrementální (Top-3 rozšiřuje Top-2). (s. 4, §3.1, Def. 6–7; s. 5, §3.4)
- C3: Výběr insightů je multiple-choice knapsack problém (z každého modulu nejvýš jeden insight), řešený greedy algoritmem, který článek nazývá „Dyemer-Zemel“ (s odkazem na Kellerer et al. [8]). Rozpočet t_voc se zadává v sekundách a převádí na slova (180 slov/min). Na výběr se čeká jen pevnou dobu t_gen a pozdější insighty jsou dostupné přes „Tell me more“ / „Tell me more about F“. Promluva = preambule s popisem dotazu, pak texty insightů seřazené sestupně podle pokrytí. (s. 4, §3.2; s. 5, §3.3–3.4, Alg. 1, Př. 5; s. 14, ref. [8])
- C4: Je implementováno 11 modulů (Top-k, Bottom-k, Outliers, Skyline, Aggregation variance, Assess, Clustering, Correlation, Statistics, Domain variance, Slicing variance), dělených na operator-agnostic/operator-specific a fine-/coarse-grained a vybraných podle operátorů [[intentional-analytics]] (describe, assess, explain). U modulu Top-k se u navazujícího dotazu [[interestingness]] komponent váží peculiaritou faktu vůči odpovídajícím faktům předchozího výsledku (princip prior belief); ostatní moduly mají vlastní definice zájmu. Outliers modul bere jako zájem anomaly score podle ref. [20] (Isolation Forest) ([[anomaly-detection]]). (s. 5, §4; s. 6, Tab. 2–3, §4.1; s. 7–8, §4.2–4.11; s. 14, ref. [20])
- C5: Uživatelská evaluace: 25 uživatelů (hlavně magisterští studenti data science; 58 % expertů, 42 % neexpertů) prošlo tři OLAP session s analytickým cílem a hodnotilo otázky Q1–Q5 (znalost angličtiny, přesnost popisu, zajímavost insightů, zvýraznění důležitých aspektů, celkový zážitek) na škále 1–5 plus otevřenou zpětnou vazbu. Q5: experti 4,07 ± 0,62, neexperti 4,30 ± 0,48. Moduly v Q3: nejlépe Correlation 4,62 ± 0,65, nejhůř Statistics 3,15 ± 1,20 a Clustering 3,11 ± 1,21 (příliš zjednodušující, resp. opakující se). (s. 8, §5.1, Tab. 4; s. 9, Tab. 5)
- C6: Úspora práce: pět doktorandů informatiky mělo 90 min na ruční implementaci modulů outliers a clustering v Pythonu; oba moduly stihli jen dva z nich (ostatní jen jeden), trvalo jim to 25–90 min a napsali 940–3480 znaků kódu. Volba rozpočtu: na 10 OLAP session po 3 operacích roste celkový normalizovaný zájem s rozpočtem (v počtu slov); details-on-demand se vyplatí pod 75 slov a metoda Elbow doporučuje t_voc = 100. (s. 9, §5.1, Tab. 6, §5.2, Obr. 5)
- C7: Efektivita (Foodmart kostka, i7-6700, 8 GB RAM, průměr 10 běhů): všechny moduly kromě Clusteringu zpracují výsledek s 10^4 fakty za méně než 1 s; Clustering v průměru 7 s. Téměř 90 % modulů skončí do několika sekund a všechny do 10 s. Preambule má v průměru 15 slov (≈ 5 s), proto t_gen = 5 s. Prototyp je v Pythonu a Javě, používá scikit-learn a Google text-to-speech. (s. 8, §5; s. 9, §5.3; s. 10, §5.3)
- C8: Srovnání s LLM: 2 OLAP session (úvodní dotaz + 2 zjemnění) zadávané postupně GPT4o, Data Scientist a Data Analyst. Prompt podle guidelines OpenAI s rolí a limitem 100 slov, varianty data v promptu vs. CSV, s příklady vs. bez nich, známá vs. zamaskovaná doména. Při datech v promptu jsou insighty často kvantitativně chybné a halucinované (všechny tři tvrdí, že Produce kupují víc ženy, i když víc kupují muži). S CSV generují Python kód; čísla jsou správná, pokud vycházejí z výstupu kódu, ale halucinace a chyby zůstávají (sémanticky chybný kód, např. Data Analyst zpracoval jen prvních 5 řádků, nebo volná interpretace). S příklady jen napodobují VOOL. U dlouhých promptů zapomínají na limit slov; obecně ignorují sémantiku OLAP operátoru mezi dotazy. (s. 10, §5.4, Př. 7; s. 11, §5.4, Tab. 8)

## Vztah k mé práci


## Citovat pro


## Pozor
- litqc: 0 ERROR, 0 WARN, žádné PAGE_WARN stránky.
- Stránkování: článek má číslo 102496, strany PDF 1–14 odpovídají číslům stran v časopise (1–14).
- Tab. 4 (s. 8) je v extraktu rozházená; přiřazení hodnot Q1–Q5 k expertům/neexpertům (C5) verifikátor potvrdil v OCR stránky 8.
- Text uvádí „Dyemer-Zemel greedy algorithm [8]“ (s. 4) s odkazem na Kellerer et al.; C3 název přebírá doslova. Pravděpodobně jde o Dyer–Zemel, ale tak to článek nepíše.
- Testováno jen na jedné kostce (Foodmart); autoři to zdůvodňují tím, že moduly jsou dataset-agnostic (s. 8, pozn. 2). Srovnání s LLM je kvalitativní, jen na 2 session, bez metrik.
- Budoucí práce (s. 13, §7): nevokalizovat opakovaně stejné insighty během session, ladit výběr podle použití (např. nad Tableau/PowerBI) a zahrnout do zájmu překryv s už vybranými insighty.
- s. 13, §6.3: VOOL záměrně nedává doménovou interpretaci výsledku. Jako příklad uvádějí precision agriculture: nízké teploty mohou být špatné pro produkci, ale dobré pro ochranu proti škůdcům. Může se hodit pro IoT doménu.
- Předběžná verze je [4] (ADBIS 2022). Query-to-text navazuje na COOL [3] (text-to-query). Cituje [[vassiliadisRollUpsDrillDownsIntentional2019]] ([9]), [[franciaExplainingCubeMeasures2024]] ([32]) a [[sarawagiExplainingDifferencesMultidimensional]] ([33]).
- Kód: https://github.com/big-unibo/conversational-olap (s. 8; v extraktu rozdělené jako „conversationalolap“).
