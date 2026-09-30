---
citekey: vassiliadisRollUpsDrillDownsIntentional2019
title: "Beyond Roll-Up's and Drill-Down's: An Intentional Analytics Model to Reinvent OLAP (Long-Version)"
authors: "Vassiliadis, Panos; Marcel, Patrick; Rizzi, Stefano"
year: 2019
venue: "Information Systems 85, pp. 68–91 (PDF: arXiv 1812.07854v2, long version)"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
chapters: []
concepts: [intentional-analytics, olap, interestingness, guided-data-exploration, anomaly-detection]
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/3GSB43VC)

## TL;DR
Vizionářský článek navrhuje nahradit v [[olap]] nízkoúrovňové operace (roll-up, drill-down) pěti „intentional“ operátory: describe, assess, explain, predict a suggest. Uživatel jimi vyjadřuje, *proč* se do dat dívá, a systém záměr přeloží na OLAP dotazy a data-mining modely. Odpovědí není jen tabulka, ale dashboard s daty, modely a automaticky vybranými „highlights“. Highlights se vybírají podle nové subjektivní míry překvapení, která porovnává nový výsledek s tím, co uživatel viděl předtím. Dlouhá verze navíc obsahuje formální definice datového modelu a operátorů (příloha §8–11).

## Klíčová tvrzení
- C1: Autoři navrhují [[intentional-analytics]], tzv. Intentional Analytics Model. Místo operátorů roll-up/drill-down uživatel formuluje analytický cíl operátory describe, assess, explain, predict a suggest. Příklady: místo „drill down to store city“ zadá „explain the drop in the sales of this product family“, místo roll-up zadá „assess whether the sales in a particular region are abnormal“. Motivací je rostoucí podíl BI uživatelů s doménovou znalostí, ale nízkými ICT dovednostmi. (s. 2–3, §1–1.1; s. 8, §1.3 | IS s. 69, 71)
- C2: Odpovědí na intentional dotaz je dashboard, tedy množina „enhanced cubes“. Každou tvoří kostka, její modely (výsledky ML/DM algoritmů nebo uživatelem dané KPI či pravidla) a highlights, tj. podmnožiny dat a modelů, které nejvíc odpovídají záměru uživatele. (s. 3, §1.1; s. 20, §2.4, Def. 5–6 | IS s. 70, 76)
- C3: Heterogenní modely (clustering, rozhodovací stromy, top-k, outliers, časové řady) sjednocuje „data-to-model mapping“. Každá komponenta modelu je atribut, který anotuje každou buňku kostky, a mapování je obousměrné. Model navíc indukuje „antagonistické“ komponenty, které se přetahují o roli highlightu, např. top-k × non-top-k nebo outliers × non-outliers. (s. 15–18, §2.2.3 | IS s. 74–76)
- C4: Highlights se vybírají podle subjektivní míry [[interestingness]] inspirované De Bieho rámcem subjektivní zajímavosti. Předchozí kostka C^O představuje „belief“ uživatele. Surprise buňky nové kostky C^N je rozdíl její significance a significance jejího protějšku v C^O (tzv. proxies, např. předek po drill-downu). Surprise se agreguje na komponenty (A_C) a modely (A_M) a vybere se komponenta s maximem (Algorithm 1). (s. 21–24, §3.1–3.2; s. 48, §6.6 | IS s. 77–78, 89)
- C5: Příklad na datasetu Adult (census 1994), měřítko Hours per Week: significance = z-score, D = rozdíl, A_C = průměr. Komponenta top-5 buněk získá skóre 0,61, komponenta outliers (> 2 směrodatné odchylky, tedy [[anomaly-detection]]) 0,85. Jako highlight se proto zvýrazní dvě extrémní buňky. (s. 10, §2.1, Example 3; s. 25–26, §3.2, Example 7 | IS s. 79, 81)
- C6: Operátor Explain úmyslně nemodeluje kauzalitu: podle autorů je určení příčin příliš složité na automatizaci. „Vysvětlení“ tu znamená automatické odhalení skrytých korelací a informací, které nejsou v dashboardu vidět. Explanation modely jsou t/F-testy mezi úrovněmi granularity, korelace, regrese a rozhodovací strom. Druhá varianta vysvětluje rozdíl proti srovnávací kostce (např. „proč jsou prodeje o 1000 kusů nižší než loni“). (s. 34–35, §4.3 | IS s. 82–83)
- C7: Prototyp Delian Cube Engine (open source, nad relační DBMS) byl testován na PKDD99 datech o půjčkách a na uměle zvětšených verzích s 1M a 10M řádky. Generování modelů trvalo jen pár milisekund, protože modely běží nad výsledkem dotazu, ne nad celou kostkou. Hranici 500 ms pro odpověď tak podle autorů neohrožují, zatímco čas dotazu roste lineárně s velikostí kostky. (s. 43–44, §5 | IS s. 86)
- C8: Omezení: jde o „vision paper“. Vizualizace v prototypu jsou podle autorů naivní, automatická volba grafické reprezentace a generování data stories jsou budoucí práce. Top-down výběr highlights je mimo rozsah článku; funkce significance, surprise, delta a agregace jsou záměrně otevřené. Optimalizátor intentional operátorů (výběr logických operátorů a algoritmů) zůstává otevřeným problémem. (s. 25, §3.2; s. 44, §5; s. 50–51, §7 | IS s. 78, 86, 90)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování stran: claims odkazují na strany PDF dlouhé verze (arXiv 1812.07854v2, prosinec 2020, 74 s.), ne na časopis. Za „IS s.“ jsou tištěné strany v Information Systems 85, převzaté z dřívějšího zpracování časopisecké verze. V LaTeXu cituj IS strany.
- Bib záznam je @article v Information Systems, ale PDF je arXiv long-version. Obsah hlavní části (§1–7) odpovídá časopisu; navíc je příloha s formálními definicemi (§8 data a cube queries, §9 algoritmy, §10 modely, highlights a dashboardy, §11 formální definice operátorů; s. 57–74), která v časopise není.
- Předběžná verze [18] (DOLAP 2018) měla jiné operátory: Describe pokrývá FocusOn a Abstract, Assess pokrývá Compare a Verify, Explain nahrazuje Analyze (s. 31, 34, 35).
- Experiment (C7) je jen ukázka proveditelnosti: jedna session na jednom notebooku (Intel i5-7200U, 8 GB RAM), žádné srovnání ani uživatelská studie. Konkrétní časy jsou jen v obr. 4, který v textovém extraktu chybí.
- Obrázky a část tabulek (např. Table 6, 8 u Example 7) jsou v extraktu rozházené, čísla ověř v PDF.
- Na Sarawagiho odkazují jako [3] Explaining differences in multidimensional aggregates (VLDB 1999), [4] User-adaptive exploration of multidimensional data (VLDB 2000) a [5] Sathe & Sarawagi, Intelligent rollups in multidimensional OLAP data (VLDB 2001). Na [[sarawagiDiscoverydrivenExplorationOLAP1998]] (EDBT'98) přímo neodkazují.
