---
citekey: wuScorpionExplainingAway2013
title: "Scorpion: Explaining Away Outliers in Aggregate Queries"
authors: Wu, Eugene; Madden, Samuel
year: 2013
venue: Proceedings of the VLDB Endowment, 6(8), pp. 553–564
kind: journal
status: candidate
verified: false
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts:
  - query-explanation
  - anomaly-detection
  - olap
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/D3MRVDAN)

## TL;DR
Scorpion vysvětluje odlehlé body ve výsledku group-by agregačního dotazu: uživatel ve vizualizaci označí podezřelé výsledky (a případně „normální“ výsledky jako hold-out) a systém najde predikát nad vstupními řádky, po jehož odstranění odlehlé hodnoty zmizí a normální výsledky se změní co nejméně. Kvalitu predikátu měří „vliv“ odvozený z analýzy citlivosti. Místo exhaustivního prohledávání využívá vlastnosti agregačních funkcí ve dvou rychlejších algoritmech (DT a MC).

## Klíčová tvrzení
- C1: Databáze a vizualizační nástroje neumožňují postupovat zpětně od odlehlého agregovaného bodu ke společným vlastnostem vstupních řádků. Scorpion dostane uživatelem označené odlehlé výsledky (outliers) a hold-out výsledky a hledá booleovský predikát nad vstupními daty, po jehož aplikaci před agregací odlehlé výsledky „vypadají normálně“ a hold-out výsledky se téměř nezmění ([[query-explanation]], [[anomaly-detection]]). (s. 1, Abstract, §1)
- C2: Vliv predikátu vychází z analýzy citlivosti: Δ = agg(g_o) − agg(g_o − p(g_o)) a inf = Δ / |p(g_o)|. Násobí se uživatelským vektorem chyby (výsledek je moc vysoký/nízký), vliv na hold-out je penalizován parametrem λ a přes více výsledků se vliv na outliers průměruje, zatímco na hold-out se bere maximum. Predikát je konjunkce rozsahů nad spojitými a množinových podmínek nad diskrétními atributy. (s. 3, §3.1–3.3)
- C3: Pro libovolnou (black-box) agregaci bez vhodných vlastností je podle autorů obtížné zlepšit se nad exhaustivní algoritmus NAIVE, který vyjmenuje a ohodnotí všechny predikáty: počet klauzulí roste s kardinalitou atributu exponenciálně (diskrétní) resp. kvadraticky (spojité) a počet konjunkcí exponenciálně s počtem atributů, takže je neúnosný i pro malá data. (s. 4, §4.2)
- C4: Rychlejší algoritmy umožňují tři vlastnosti agregací: inkrementální odebíratelnost (splňují COUNT, SUM a z nich odvozené AVG, STDDEV, VARIANCE; nesplňují MAX, MIN, MEDIAN, MODE), nezávislost a antimonotónnost. Inkrementální odebíratelnost autoři vztahují k distributivním a algebraickým funkcím v [[olap]] kostkách a uvádějí, že ne každá distributivní či algebraická funkce je inkrementálně odebíratelná. (s. 5, §5.1–5.3; s. 2, §1)
- C5: DT je top-down dělení podle regresních stromů pro nezávislé agregace (např. AVG, STDDEV), se vzorkováním a samostatným dělením outlier a hold-out skupin. MC je bottom-up algoritmus podle subspace clusteringu (CLIQUE) pro nezávislé antimonotónní agregace (např. COUNT, SUM). Výsledné predikáty slučuje Merger. (s. 5, §5.2; s. 6–7, §6.1, §6.2)
- C6: Parametr c ≥ 0 upravuje vliv na Δo / (Δg_o)^c: při c = 0 Scorpion snižuje výsledek bez ohledu na počet řádků (predikáty vybírají mnoho řádků), vyšší c vede k mnohem selektivnějším predikátům. Výběr atributů pro vysvětlení zatím zadává uživatel, automatický výběr je budoucí práce. (s. 8, §7, §6 Dimensionality Reduction)
- C7: Na syntetických datech (2–4 dimenze, 10 skupin po 2 000 řádcích) dávají DT a MC výsledky srovnatelné s exhaustivním NAIVE a snižují čas až 150×. Výkon závisí na vlastnostech dat a v nejhorším případě škáluje exponenciálně s dimenzionalitou. Cachování DT a Merger pro nízká c snižuje cenu až 25×. (s. 9, §8; s. 11, §8)
- C8: Na datasetu INTEL (2,3 mil. řádků, 61 senzorů) Scorpion v obou dotazech na směrodatnou odchylku teploty identifikoval vadný senzor (sensorid = 15, resp. 18). Na datasetu EXPENSE (116 448 řádků) vrátil predikát popisující výdaje za mediální nákupy (GMMB INC.) s F-score 0,6 kvůli nízké recall. Všechny algoritmy na reálných datech doběhly během několika sekund. (s. 9, §8; s. 11–12, §8)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování stran: tištěná strana = PDF strana + 552 (PDF 1–12 = s. 553–564). V claims jsou PDF strany.
- Litqc: 0 PAGE_WARN. Strana 7 obsahuje v extraktu tisíce řádků bodů z bodových grafů (obr. 5–6, 8); text MC sekce je až za nimi. Grafy a tabulky (obr. 9–16) jsou v extraktu rozházené, čísla z obrázků ověřuj v PDF.
- Čísla podsekcí v kapitole 8 (Datasets, Experimental Setup, Real-World Datasets) nejsou v extraktu čitelná; v claims jsou uváděná podle struktury textu, ověř v PDF. Sekce MC je §6.2 (nadpis na s. 7 čitelný).
- Omezení předpokladů: dotazy jsou group-by nad jedinou tabulkou, joiny se modelují materializací (s. 3); vliv je definován mazáním řádků, perturbace hodnot nebyla zkoumána (s. 3, pozn. 3).
- V related work cituje Sarawagi iDiff [15] = [[sarawagiExplainingDifferencesMultidimensional]] a cube exploration [16] = [[sarawagiDiscoverydrivenExplorationOLAP1998]] (s. 12).
