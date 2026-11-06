---
citekey: wangChartInsighterApproachMitigating2025
title: "ChartInsighter: An Approach for Mitigating Hallucination in Time-Series Chart Summary Generation With a Benchmark Dataset"
authors: "Wang, Fen; Wang, Bomiao; Shu, Xueli; Liu, Zhen; Shao, Zekai; Liu, Chao; Chen, Siming"
year: 2025
venue: "IEEE Transactions on Visualization and Computer Graphics 31(6)"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [llm-hallucination, data-narration, llm-time-series, llm-agents]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/PQAGWX9H)

## TL;DR
Autoři nejdřív na 80 shrnutích grafů časových řad od čtyř LLM sestaví taxonomii 10 typů halucinací (např. chybný směr trendu, chybné extrémy, vynechané detaily). Pak navrhují ChartInsighter: více LLM agentů, kteří z datové tabulky a Vega-Lite specifikace vytahují insighty přes externí analytické moduly (segmentace řady, statistiky, majoritní hlasování), iterativně je skládají do textu a nakonec ho ověří testem sebekonzistence. Na vlastním benchmarku 75 grafů s halucinacemi anotovanými po větách má nejnižší míru halucinací (0,14 proti 0,48 u GPT-4).

## Klíčová tvrzení
- C1: Dosavadní generování shrnutí grafů pomocí LLM se podle autorů soustředí na základní analýzu a trpí [[llm-hallucination|halucinacemi]] jako chyby ve výpočtu čísel a chybné určení trendu; LLM navíc často chybí hlubší uvažování o vztazích mezi dimenzemi a selhávají v matematických výpočtech potřebných k nalezení vlastností a trendů v časové řadě. (s. 1, §I)
- C2: Taxonomii halucinací autoři odvodili testem čtyř LLM (GPT-4, Claude-3, GPT-4o, LLaMA-3.1-70B) na 20 reálných čárových grafech časových řad se vstupem Vega-Lite specifikace a datové tabulky: 80 shrnutí, 1083 vět, 199 halucinací; čtyři autoři je nezávisle klasifikovali a shodli se na 10 typech, na úrovni L1 se žádná halucinace nevyskytla. (s. 4, §III-C)
- C3: Četnosti typů (z 199 halucinací): L2 – Extremum Error 12,6 %, Numerical Value Error 3,0 % (vzácná ne kvůli dobrým výpočtům, ale protože LLM výpočty do shrnutí málokdy zahrnou); L3 – Trend Direction Error 22,1 %, Multidimensional Trend Error 10,0 %, Range Error 4,0 %, Cyclicality Error 3,5 %, Stability Error 1,5 %; omezení shrnutí – Detail Omission 22,1 %, Junk Description 12,1 %, Proportion Perception Error 9,1 %; nejčastější jsou Detail Omission a Trend Direction Error (shodně 22,1 %). (s. 4, §III-C, obr. 3; s. 5, §III-C)
- C4: ChartInsighter je pipeline Brainstorming – Refining – Self-consistency test se vstupem datové tabulky a vizualizační specifikace (Vega-Lite) a s [[llm-agents|agenty]] Uni-Insighter, Multi-Insighter a Writer; Numerical Pattern Analysis Module dělí řadu podle významných extrémů na úseky (patches), slučuje sousední úseky s rozptylem pod prahem (medián rozptylů + k·směrodatná odchylka, nejlépe k = 0) a pro úseky počítá statistiky (max, min, volatilita) do JSON; Multi-Insighter generuje vícedimenzionální popis třikrát a vybírá majoritním hlasováním. (s. 5, §IV-A; s. 6, §IV-A, obr. 4; s. 7, §IV-A; s. 8, obr. 5)
- C5: Ve fázi Refining Writer píše shrnutí a Multi-Insighter ho opakovaně doplňuje, dokud nenajde žádný nový insight (maximum 5 iterací, většina grafů 2–3); test sebekonzistence pak cílí na Extremum Error a Proportion Perception Error, které vznikají analýzou po úsecích: LLM označí podezřelé věty, znovu je analyzuje a při neshodě nové a původní věty původní větu opraví (v příkladu „maximum 1.48“, skutečné maximum 3.38). (s. 7, §IV-B, §IV-C; s. 11, §VI-C)
- C6: Benchmark obsahuje 75 reálných čárových grafů časových řad (po 25 jednoduchých, středních a složitých), ke každému data, Vega-Lite specifikaci, obrázek, ručně vytvořené zlaté shrnutí a shrnutí od GPT-4, VL2NL a ChartInsighteru; halucinace anotovali po větách podle taxonomie z §III-C (celkem 2693 vět). (s. 2, §I; s. 8, §V; s. 9, §V)
- C7: Na benchmarku má ChartInsighter (základní model GPT-4) míru halucinací (počet halucinací / počet vět, může přesáhnout 1) 0,14 proti 0,48 u GPT-4 a 1,63 u VL2NL, sémantickou bohatost (podíl vět L2 a L3) 0,75 proti 0,74 a 0,33 a nejvyšší lidské hodnocení 3,79 (GPT-4 2,86, VL2NL 1,70; škála 1–5); medián doby generování přes GPT-4 API je 87,23 s (± 36,1 s) na graf, maximum 171 s, minimum 18 s. (s. 9, §VI-A; s. 10, §VI-A, §VI-B, tab. I, §VI-C)
- C8: Omezení podle autorů: zmírněna je jen část halucinací a jiné typy přetrvávají; shrnutí pokrývají jen obsah L1–L3, kontextový obsah L4 vyžaduje doménové znalosti a zůstává výzvou; generování není v reálném čase; vstupem jsou surová data a specifikace, ne obrázek grafu, protože podle citovaného výzkumu dávají podkladová data efektivnější shrnutí než jiné formy vstupu (obrázky zmiňují jako budoucí práci). (s. 11, §VII; s. 12, §VII)

## Vztah k mé práci


## Citovat pro


## Pozor
- Stránky v tvrzeních jsou stránky PDF (1–13); tištěné stránky v časopise jsou 3733–3745, tj. tištěná = PDF + 3732 (např. s. 4 = 3736, s. 10 = 3742).
- QC fulltextu: s. 6 a 9 jsou nahrazeny OCR textem (s. 6 obsahuje obr. 4, v OCR je hodnota k zkomolená na „O“ – v PDF je k = 0, ověřeno z vykreslené strany); s. 4 a 8 jsou PAGE_WARN (sloupce, obrázky). C2, C3 (s. 4) a C4 (s. 6) ověřeny proti vykresleným stranám PDF, C6 (s. 8) je ze souvislého textu, ale před citací ověř v PDF.
- Obr. 3 (s. 4, četnosti typů halucinací) a tab. I (s. 10, výsledky) ve fulltextu chyběly; jsou ručně přepsány z PDF (`[Fig. 3 …]`, `[Table I …]`), kopie v `fulltext/wangChartInsighterApproachMitigating2025.corrected.txt`.
- Procenta v C3 jsou podíly z 199 halucinací ze vstupní studie čtyř LLM, ne z benchmarku 75 grafů.
- Kategorie Detail Omission, Junk Description a Proportion Perception Error autoři v §III-C řadí mezi „Limitations of Chart Summaries Generated“, ale počítají je mezi 10 typů halucinací (obr. 3) – pojem halucinace je tu širší než jen fakticky chybné tvrzení.
- Lidské hodnocení i anotaci halucinací dělalo vždy 6 účastníků; benchmarkové grafy i taxonomii klasifikovali autoři sami. Automatické metriky diverzity (RC, Chamfer, MST…) podle autorů kvalitu plně nezachytí – zlaté shrnutí v nich nemá nejlepší skóre (s. 9).
- Obr. 2 (s. 4) označuje prvek L2 jako „Change Rate“, text jako „Growth Rate“.
- Seznam četby (položka 18) odkazuje i na arXiv preprint 2501.09349; cituj verzi z IEEE TVCG.

## Obrázky
- Obr. 4 (s. 6) – pipeline ChartInsighteru (Brainstorming, Refining, Self-consistency test, externí moduly a šablony promptů) na příkladu akcií Google a Apple ![[figures/wangChartInsighterApproachMitigating2025/fig4.png]]
