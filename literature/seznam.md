---
type: reading-list
---

> Aktuální znění seznamu literatury. Při nové revizi nahraď celý obsah pod touto poznámkou.
> `python3 literature/tools/litqc.py plan` ho spáruje se Zoterem a poznámkami (podle DOI / názvu, ne podle čísla položky) → `qc/_plan.md`.
> Parser čte jen nadpisy „ÚROVEŇ N“ / „NÁSTROJE A DATA“ a položky ve tvaru `N. …`. Ostatní text ignoruje.

Seznam literatury s odkazy — seřazeno podle důležitosti
Diplomová práce: Konverzační OLAP systém s LLM integrací nad časovými řadami z chytrých zařízení FIT VUT | verze 25. 9. 2026 (rev. 3 — sladěno s oficiálním zadáním, doplněna automatizovaná explorace)
Značka ⚠ = odkaz jsem v této rešerši neověřil, před odevzdáním zkontroluj v DBLP nebo Crossref. Značka [NOVÉ] = doplněno v revizi 2 kvůli pokrytí zadání. [NOVÉ, rev. 3] = doplněno v revizi 3. Kde existuje volně dostupné PDF, uvádím ho vedle oficiálního odkazu.

MAPOVÁNÍ NA BODY ZADÁNÍ
Bod 1 — IoT, chytrá zařízení, časové řady: 8, 9, 10, 22, 23, 64, 65 Bod 2a — vizualizace a nástroje pro analýzu časových řad: 24, 49, 50, 68, 69, 79 
Bod 2b — LLM nad daty: 7, 12, 13, 17–20, 31, 32, 34–46, 54, 70 
Bod 3 — OLAP nad časovými řadami, požadavky na LLM augmentaci: 1–5, 11–14, 25–32, 60–63 
Bod 4 — návrh platformy, lokální vs. cloudové modely: 17, 47, 48, 74, 79 Bod 6a — uživatelské testování, scénáře, Likertova škála: 21, 58, 59, 72 
Bod 6b — srovnání modelů (výkonnost, kvalita analýzy): 6, 33, 55, 56, 57, 75
ÚROVEŇ 1 — POVINNÉ (číst celé)
Bez těchto zdrojů nelze obhájit přínos práce ani splnit zadání. Řazeno podle naléhavosti čtení.
1. Sarawagi, S., Agrawal, R., Megiddo, N. — Discovery-Driven Exploration of OLAP Data Cubes EDBT 1998, LNCS 1377, s. 168–182 DOI: https://doi.org/10.1007/BFb0100984 Zavádí anotaci buněk kostky mírou překvapení (SelfExp, InExp, PathExp) a navádění uživatele k anomáliím. Přesně tvůj pilíř 2+3 bez LLM. Číst jako první.
2. Vassiliadis, P., Marcel, P., Rizzi, S. — Beyond Roll-Up's and Drill-Down's: An Intentional Analytics Model to Reinvent OLAP Information Systems, sv. 85, s. 68–91, 2019 DOI: https://doi.org/10.1016/j.is.2019.03.011 Volný preprint: https://www.cs.uoi.gr/~pvassil/publications/2019_IS_IntentionalModel/IS2019_VassiliadisMarcelRizzi_CR_PreprintUoI.pdf Rozšířená verze (arXiv): https://arxiv.org/abs/1812.07854 Definuje pět intenčních operátorů: describe, assess, explain, predict, suggest. Od stejné skupiny jako COOL a VOOL. Nelze se vymezovat vůči boloňské škole a neznat jejich vlastní explain operátor.
3. Sarawagi, S. — Explaining Differences in Multidimensional Aggregates VLDB 1999, s. 42–53 Záznam: https://netman.aiops.org/~peidan/ANM2023/8.AnomalyLocalization/ReadingLists/Explaining%20differences%20in%20multidimensional%20aggregates.pdf Operátor DIFF — hledá vysvětlení rozdílu dvou agregátů pomocí drill-downu. Doslova „OLAP-aware explanation".
4. Francia, M., Rizzi, S., Marcel, P. — Explaining Cube Measures Through Intentional Analytics [NOVÉ, rev. 3] Information Systems 121:102338, 2024 (open access) DBLP: https://dblp.uni-trier.de/pid/149/9199.html ⚠ DOI dohledat v Crossref Implementace operátoru explain z Intentional Analytics Model (položka 2) — vysvětluje míru kostky pomocí jiných měr a modelů nad nimi. Bez znalosti tohoto článku se nelze vymezit vůči boloňské skupině. Vymezení (ověř po přečtení): jejich explain pracuje se vztahy mezi měrami, tvůj agent s lokalizací v hierarchii dimenzí a kontrafaktuálním ověřením. Tatáž skupina má i operátor predict: Francia, Rizzi, Golfarelli, Marcel — Predicting Multidimensional Cubes Through Intentional Analytics, Information Systems 136:102628, 2026. Citovat jednou větou.
5. Wu, E., Madden, S. — Scorpion: Explaining Away Outliers in Aggregate Queries PVLDB 6(8):553–564, 2013 DOI: https://doi.org/10.14778/2536354.2536356 Volné PDF (MIT): https://dspace.mit.edu/bitstream/1721.1/89076/1/scorpion-vldb13.pdf Kanonická práce o vysvětlování outlierů v agregacích. Najde predikát, který po aplikaci na vstupní data outlier odstraní. Tvůj agent dělá LLM-řízenou variantu.
6. Liu, Q., Paparrizos, J. — The Elephant in the Room: Towards A Reliable Time-Series Anomaly Detection Benchmark (TSB-AD) NeurIPS 2024, Datasets and Benchmarks Track Volné PDF: https://proceedings.neurips.cc/paper_files/paper/2024/file/c3f3c690b7a99fba16d0efd35cb83b2c-Paper-Datasets_and_Benchmarks_Track.pdf Stránka konference: https://neurips.cc/virtual/2024/poster/97690 Kód a data: https://pypi.org/project/TSB-AD/ 1070 časových řad ze 40 datasetů. Určí ti evaluační metriku (VUS-PR, nikoli F1 s point-adjustem) a doloží, že statistický detektor pro MVP stačí. Číst před návrhem detektoru.
7. Zhou, Z., Yu, R. — Can LLMs Understand Time Series Anomalies? ICLR 2025 arXiv: https://arxiv.org/abs/2410.05440 Stránka konference: https://iclr.cc/virtual/2025/poster/30008 LLM rozumí časovým řadám lépe jako obrázkům než jako textu; explicitní reasoning prompt výkon nezlepší, spíš zhorší. Číst před návrhem architektury agenta.
8. Al-Fuqaha, A. et al. — Internet of Things: A Survey on Enabling Technologies, Protocols, and Applications [NOVÉ] IEEE Communications Surveys & Tutorials 17(4):2347–2376, 2015 ⚠ https://doi.org/10.1109/COMST.2015.2444095 — ověřit Hlavní zdroj pro kapitolu o IoT (bod 1 zadání). Architektura IoT, protokoly (MQTT, CoAP), aplikační domény včetně chytrých budov a energetiky.
9. Hyndman, R. J., Athanasopoulos, G. — Forecasting: Principles and Practice, 3. vydání [NOVÉ] OTexts, 2021 Volně online: https://otexts.com/fpp3/ Teoretický základ kapitoly o časových řadách: složky (trend, sezónnost, cykly), dekompozice, stacionarita, autokorelace. Čti kapitoly 2–3 a 5; zbytek referenčně.
10. Blázquez-García, A. et al. — A Review on Outlier/Anomaly Detection in Time Series Data [POVÝŠENO z úrovně 2] ACM Computing Surveys 54(3), 2021 Volný preprint: https://arxiv.org/abs/2002.04236 Taxonomie anomálií (bodové, subsekvenční, celé řady; uni- vs. multivariátní). Páteř teoretické části o anomáliích v časových řadách.
11. Francia, M., Gallinucci, E., Golfarelli, M. — COOL: framework pro konverzační OLAP Information Systems, 2022 https://www.sciencedirect.com/science/article/pii/S0306437921000211 Nejbližší prior work. Musíš přesně vědět, co dělá a co nedělá.
12. VOOL — přirozenojazyková vokalizace výsledků OLAP sessions Information Systems, 2025 https://dl.acm.org/doi/10.1016/j.is.2024.102496 Přímý předchůdce pilíře 3. Převezmi jejich evaluační protokol.
13. Text-to-MDX — generování MDX dotazů z přirozeného jazyka pomocí GPT-4o ER 2025 https://link.springer.com/chapter/10.1007/978-3-032-08623-5_9
14. NavLLM — interaktivní LLM navigace nad multidimenzionálními daty EDBT 2026 Volné PDF: https://backend.orbit.dtu.dk/ws/portalfiles/portal/437649807/paper-316.pdf Záznam: https://orbit.dtu.dk/en/publications/navllm-interactive-llm-assisted-navigation-over-multidimensional-/
15. AXIS — vysvětlitelná detekce anomálií v časových řadách pomocí LLM arXiv 2025 https://arxiv.org/abs/2509.24378 Jediný zdroj pokrývající průnik pilířů 2 a 3.
16. ChartInsighter — redukce halucinací při shrnutí grafů časových řad IEEE TVCG, 2025 https://ieeexplore.ieee.org/document/11113164 Preprint: https://arxiv.org/abs/2501.09349 Metodika proti halucinacím při popisu časových řad = přímo pilíř 3.
17. Yao, S. et al. — ReAct: Synergizing Reasoning and Acting in Language Models ICLR 2023 arXiv: https://arxiv.org/abs/2210.03629 Projekt: https://react-lm.github.io/ Tvůj drill-down agent je v podstatě ReAct smyčka. Primární zdroj pro návrhové rozhodnutí.
18. BIRD — benchmark pro Text-to-SQL nad rozsáhlými reálnými databázemi NeurIPS 2023 https://arxiv.org/abs/2305.03111
19. Lei, F. et al. — Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows ICLR 2025 (Oral) arXiv: https://arxiv.org/abs/2411.07763 Na realistických schématech padá execution accuracy z ~91 % (Spider 1.0) a ~73 % (BIRD) na ~21 %. Musíš explicitně vymezit podmínky, za nichž platí tvoje očekávaná přesnost.
20. Schulhoff, S. et al. — The Prompt Report: A Systematic Survey of Prompt Engineering Techniques arXiv 2024 https://arxiv.org/abs/2406.06608 Terminologický a taxonomický rámec pro kapitolu o promptingu.
21. Lewis, J. R. — The System Usability Scale: Past, Present, and Future [NOVÉ] International Journal of Human–Computer Interaction 34(7):577–590, 2018 ⚠ https://doi.org/10.1080/10447318.2018.1455307 — ověřit Uživatelské testování je podle zadání primární evaluace. Tento zdroj ti dá standardizovaný dotazník (SUS), normy pro interpretaci skóre a argumentaci pro jeho použití vedle vlastních Likertových položek.

ÚROVEŇ 2 — DŮLEŽITÉ (číst metodu a related work)
IoT a správa časových řad [NOVÉ]
22. Atzori, L., Iera, A., Morabito, G. — The Internet of Things: A Survey Computer Networks 54(15):2787–2805, 2010 ⚠ https://doi.org/10.1016/j.comnet.2010.05.010 — ověřit Historicky nejcitovanější survey IoT. Pro vymezení pojmu a vizí; technické detaily ber z položky 8.
23. Jensen, S. K., Pedersen, T. B., Thomsen, C. — Time Series Management Systems: A Survey IEEE TKDE 29(11):2581–2600, 2017 ⚠ https://doi.org/10.1109/TKDE.2017.2740932 — ověřit Přehled TSDB a systémů pro správu senzorových dat. Podklad pro zdůvodnění volby DuckDB oproti InfluxDB/TimescaleDB a pro analýzu požadavků (bod 3).
Vizualizace časových řad [NOVÉ]
24. Aigner, W., Miksch, S., Schumann, H., Tominski, C. — Visualization of Time-Oriented Data Springer, 2011 (2. vydání 2023 ⚠ ověřit) ⚠ https://doi.org/10.1007/978-0-85729-079-3 — ověřit Standardní monografie k bodu 2 zadání. Taxonomie vizualizací časových dat; z přehledu technik (TimeViz Browser) si vyber ty relevantní pro senzorová data. Online katalog technik: https://browser.timeviz.net/
Vysvětlování anomálií v multidimenzionálních datech
25. Bhagwan, R. et al. — Adtributor: Revenue Debugging in Advertising Systems USENIX NSDI 2014, s. 43–55 Volné PDF a BibTeX: https://www.usenix.org/conference/nsdi14/technical-sessions/presentation/bhagwan Multidimenzionální lokalizace příčiny anomálie v aditivních KPI přes explanatory power, succinctness a surprise. V IoT kontextu: agregovaná spotřeba přes hierarchii budova → patro → zařízení je aditivní KPI stejného typu. Analogii v textu explicitně zdůvodni.
26. Sun, Y. et al. — HotSpot: Anomaly Localization for Additive KPIs with Multi-Dimensional Attributes IEEE Access 6:10909–10923, 2018 (open access) DOI: https://doi.org/10.1109/ACCESS.2018.2804764
27. Yan, S. et al. — CMMD: Cross-Metric Multi-Dimensional Root Cause Analysis ACM SIGKDD 2022, s. 4310–4320 ⚠ https://dl.acm.org/doi/10.1145/3534678.3539236 — ověřit Preprint: https://arxiv.org/abs/2203.11141 ⚠ ověřit
28. Roy, S., Suciu, D. — A Formal Approach to Finding Explanations for Database Queries ACM SIGMOD 2014, s. 1579–1590 DOI: https://doi.org/10.1145/2588555.2588578 Volné PDF: https://homes.cs.washington.edu/~suciu/main_explanation.pdf Formální rámec intervence: vysvětlení = odebrání n-tic, které významně mění výsledek dotazu.
Klasická OLAP explorace
29. Sathe, G., Sarawagi, S. — Intelligent Rollups in Multidimensional OLAP Data VLDB 2001, s. 531–540 Volné PDF: https://repository.ias.ac.in/128421
30. Francia, M., Marcel, P., Peralta, V., Rizzi, S. — Enhancing Cubes with Models to Describe Multidimensional Data Information Systems Frontiers, 2021 ⚠ https://doi.org/10.1007/s10796-021-10147-3 — ověřit Implementace operátoru describe z Intentional Analytics Model. Sesterský článek k položce 4.
Automatizovaná explorace dat [NOVÉ, rev. 3]
31. Milo, T., Somech, A. — Automating Exploratory Data Analysis via Machine Learning: An Overview ACM SIGMOD 2020 (tutorial), s. 2617–2622 DOI: https://doi.org/10.1145/3318464.3383126 Volné PDF: https://u.cs.biu.ac.il/~somecha/pdf/eda_tutorial.pdf Přehled automatizace EDA: od doporučení jednoho dalšího kroku přes modelování „zajímavosti" až po plně automatické session (deep RL, seq2seq). Rámec pro zařazení tvého agenta mezi přístupy k automatizované exploraci. Cituje ho NavLLM (položka 14).
32. Amer-Yahia, S. — Intelligent Agents for Data Exploration PVLDB 17(12):4521–4530, 2024 DOI: https://doi.org/10.14778/3685800.3685913 Volné PDF: https://www.vldb.org/pvldb/vol17/p4521-amer-yahia.pdf Shrnuje RL agenty pro exploraci dat (včetně roll-up a drill-down operátorů) a ptá se, zda LLM a AI plánování nahradí RL politiky bez přetrénování pro každou úlohu. Přímá opora pro volbu LLM agenta místo RL. Cituje ho NavLLM (položka 14).
Detekce anomálií v časových řadách
33. Wu, R., Keogh, E. — Current Time Series Anomaly Detection Benchmarks are Flawed and are Creating the Illusion of Progress IEEE TKDE 35(3):2421–2429, 2023 Preprint: https://arxiv.org/abs/2009.13807 ⚠ ověřit Proč nesmíš evaluovat s point-adjust protokolem.
34. Alnegheimish, S. et al. — SigLLM: Large Language Models Can Be Zero-shot Anomaly Detectors for Time Series? arXiv 2024 https://arxiv.org/abs/2405.14755 ⚠ ověřit
LLM a časové řady [NOVÉ]
35. Gruver, N. et al. — Large Language Models Are Zero-Shot Time Series Forecasters NeurIPS 2023 arXiv: https://arxiv.org/abs/2310.07820 Jak LLM zpracovávají číselné sekvence serializované jako text; vliv tokenizace čísel. Doplňuje položku 7.
36. Jin, M. et al. — Time-LLM: Time Series Forecasting by Reprogramming Large Language Models ICLR 2024 arXiv: https://arxiv.org/abs/2310.01728 Reprezentativní zástupce přístupu „adaptace LLM na časové řady". Pro vymezení: ty LLM nepoužíváš jako prediktor, ale jako orchestrátor a vypravěče.
37. Zhang, X. et al. — Large Language Models for Time Series: A Survey IJCAI 2024 arXiv: https://arxiv.org/abs/2402.01801 ⚠ ověřit Taxonomie přístupů LLM × časové řady. Rámec pro sekci o aktuálních přístupech (bod 2 zadání).
Text-to-SQL
38. The Death of Schema Linking? Text-to-SQL in the Age of Well-Reasoned Language Models arXiv 2024 https://arxiv.org/abs/2408.07702 Přímá argumentace k pokynu vedoucího ohledně schema linkingu vs. volného SQL. Klíčové pro obhajobu schema-constrained přístupu.
39. Hong, Z. et al. — Next-Generation Database Interfaces: A Survey of LLM-based Text-to-SQL IEEE TKDE, 2025 arXiv: https://arxiv.org/abs/2406.08426 Recenzovaný survey — nahradí několik dílčích citací.
40. Automatic Metadata Extraction for Text-to-SQL arXiv 2025 https://arxiv.org/abs/2505.19988
41. Gao, D. et al. — DAIL-SQL: Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation PVLDB 2024 https://arxiv.org/abs/2308.15363 ⚠ ověřit Systematická evaluace promptovacích strategií v doméně Text-to-SQL.
42. Pourreza, M., Rafiei, D. — DIN-SQL: Decomposed In-Context Learning of Text-to-SQL with Self-Correction NeurIPS 2023 https://arxiv.org/abs/2304.11015 ⚠ ověřit
Agenti a prompting
43. Wei, J. et al. — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models NeurIPS 2022, sv. 35, s. 24824–24837 arXiv: https://arxiv.org/abs/2201.11903
44. Shinn, N. et al. — Reflexion: Language Agents with Verbal Reinforcement Learning NeurIPS 2023 arXiv: https://arxiv.org/abs/2303.11366 Pro self-correction při chybně vygenerovaném dotazu.
45. Schick, T. et al. — Toolformer: Language Models Can Teach Themselves to Use Tools NeurIPS 2023 arXiv: https://arxiv.org/abs/2302.04761
46. Sahoo, P. et al. — A Systematic Survey of Prompt Engineering in Large Language Models arXiv 2024 https://arxiv.org/abs/2402.07927 ⚠ ověřit
Lokální a cloudové modely [NOVÉ]
47. Kwon, W. et al. — Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM) ACM SOSP 2023 arXiv: https://arxiv.org/abs/2309.06180 Technický základ lokálního provozu modelů (bod 4 zadání). Podklad pro diskusi propustnosti a latence lokálního nasazení vs. cloudového API.
48. Frantar, E. et al. — GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers ICLR 2023 arXiv: https://arxiv.org/abs/2210.17323 Kvantizace = hlavní důvod, proč lokální modely běží na spotřebitelském HW. Potřebuješ pro zdůvodnění výběru lokálních modelů a interpretaci rozdílů v kvalitě analýzy.
Generování textu a vizualizací nad daty
49. LIDA — automatická generace vizualizací pomocí LLM ACL 2023 (demo) https://aclanthology.org/2023.acl-demo.11.pdf Krátký demo paper, přečteš za 20 minut.
50. Shi, D. et al. — Calliope: Automatic Generation of Visual Data Stories IEEE TVCG 27(2), 2021 ⚠ https://doi.org/10.1109/TVCG.2020.3030403 — ověřit
51. Ji, Z. et al. — Survey of Hallucination in Natural Language Generation ACM Computing Surveys 55(12), 2023 Volný preprint: https://arxiv.org/abs/2202.03629 Rámec pro tvrzení o věrnosti generovaných vysvětlení.
Konverzační OLAP — doplňkové
52. Natural Language Interfaces for Databases with Deep Learning Springer, 2026 https://link.springer.com/content/pdf/10.1007/978-3-032-06905-4.pdf Monografie — používej jako referenční příručku, nečti lineárně.
53. Sémantické cachování OLAP dotazů pomocí LLM kanonizace DOLAP 2026 https://arxiv.org/pdf/2602.19811 Implementační inspirace, nikoli contribution-critical.
RAG
54. Lewis, P. et al. — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks NeurIPS 2020 arXiv: https://arxiv.org/abs/2005.11401 Podklad pro použití Qdrantu a sémantického vyhledávání ve schématu.
Evaluace modelů
55. LLM-as-a-Judge EMNLP 2025 https://aclanthology.org/2025.emnlp-main.138/
56. Zheng, L. et al. — Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena NeurIPS 2023, Datasets and Benchmarks Track arXiv: https://arxiv.org/abs/2306.05685 Původní zdroj metody.
57. Liang, P. et al. — Holistic Evaluation of Language Models (HELM) [NOVÉ] Transactions on Machine Learning Research, 2023 arXiv: https://arxiv.org/abs/2211.09110 Rámec pro vícekriteriální srovnání modelů (přesnost, efektivita, robustnost). Převezmi strukturu metrik pro bod 6b zadání.
Uživatelské testování [NOVÉ]
58. Brooke, J. — SUS: A „Quick and Dirty" Usability Scale In: Jordan, P. W. et al. (eds.), Usability Evaluation in Industry, Taylor & Francis, 1996, s. 189–194 ⚠ ověřit stránky Původní zdroj dotazníku SUS. Cituj spolu s položkou 21.
59. Likert, R. — A Technique for the Measurement of Attitudes Archives of Psychology 22(140):1–55, 1932 ⚠ ověřit Původní zdroj Likertovy škály, kterou zadání výslovně požaduje.

ÚROVEŇ 3 — DOPLŇKOVÉ (projít abstrakt, citovat jednou větou)
60. Chaudhuri, S., Dayal, U. — An Overview of Data Warehousing and OLAP Technology ACM SIGMOD Record 26(1), s. 65–74, 1997 ⚠ https://doi.org/10.1145/248603.248616 — ověřit
61. Gray, J. et al. — Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals Data Mining and Knowledge Discovery 1(1), s. 29–53, 1997 ⚠ https://doi.org/10.1023/A:1009726021843 — ověřit
62. Kimball, R., Ross, M. — The Data Warehouse Toolkit, 3. vydání Wiley, 2013 — kniha, ISBN 978-1-118-53080-1 ⚠ ověřit ISBN
63. Abuzaid, F. et al. — DIFF: A Relational Interface for Large-Scale Data Explanation PVLDB 2021 ⚠ ověřit ročník a stránky Preprint: https://arxiv.org/abs/1907.12718 ⚠ ověřit
64. Taylor, S. J., Letham, B. — Forecasting at Scale (Prophet) The American Statistician 72(1), s. 37–45, 2018 ⚠ https://doi.org/10.1080/00031305.2017.1380080 — ověřit Dokumentace nástroje: https://facebook.github.io/prophet/
65. Cleveland, R. B. et al. — STL: A Seasonal-Trend Decomposition Procedure Based on Loess Journal of Official Statistics 6(1), s. 3–73, 1990 Volné PDF: https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/stl-a-seasonal-trend-decomposition-procedure-based-on-loess.pdf ⚠ ověřit
66. Spider — benchmark pro cross-domain Text-to-SQL EMNLP 2018 https://aclanthology.org/D18-1425/ Historická reference, číst jen úvod a konstrukci datasetu.
67. Wang, L. et al. — A Survey on Large Language Model based Autonomous Agents Frontiers of Computer Science, 2024 https://arxiv.org/abs/2308.11432 Skenovat taxonomii; pro návrhová rozhodnutí použij primární zdroje (položky 17, 43–45).
68. Wang, Y. et al. — DataShot: Automatic Generation of Fact Sheets from Tabular Data IEEE TVCG 26(1), 2020 ⚠ https://doi.org/10.1109/TVCG.2019.2934398 — ověřit
69. Shen, L. et al. — Towards Natural Language Interfaces for Data Visualization: A Survey IEEE TVCG, 2023 Preprint: https://arxiv.org/abs/2109.03506 ⚠ ověřit
70. Gao, Y. et al. — Retrieval-Augmented Generation for Large Language Models: A Survey arXiv 2023 https://arxiv.org/abs/2312.10997
71. OLAP-AI — multimodální generativní OLAP s textem a obrázky ER Forum 2025 (CEUR) https://ceur-ws.org/Vol-4099/forum_paper4.pdf Pozor: CEUR forum má slabší recenzní režim. Citovat jako vision paper, nestavět na tom argument.
72. Joshi, A. et al. — Likert Scale: Explored and Explained [NOVÉ] British Journal of Applied Science & Technology 7(4):396–403, 2015 ⚠ ověřit Pro zdůvodnění volby 5- vs. 7bodové škály a ordinálního zpracování dat (medián, ne průměr). Časopis má slabší renomé — citovat jen pro metodickou poznámku.
73. Wohlin, C. — Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering EASE 2014 ⚠ https://doi.org/10.1145/2601248.2601268 — ověřit Pouze pokud v práci popisuješ metodu rešerše.

NÁSTROJE A DATA
Položky 74–77 mají regulérní publikaci a citují se normálně. Ostatní patří do implementační kapitoly.
74. Raasveldt, M., Mühleisen, H. — DuckDB: An Embeddable Analytical Database ACM SIGMOD 2019 (demonstration) ⚠ https://doi.org/10.1145/3299869.3320212 — ověřit
75. Lavin, A., Ahmad, S. — Evaluating Real-Time Anomaly Detection Algorithms: The Numenta Anomaly Benchmark [NOVÉ] IEEE ICMLA 2015, s. 38–44 ⚠ ověřit stránky arXiv: https://arxiv.org/abs/1510.03336 Data: https://github.com/numenta/NAB Anotované anomálie v reálných senzorových řadách. Doplněk k TSB-AD pro evaluaci detektoru na IoT datech.
76. Kelly, J., Knottenbelt, W. — The UK-DALE Dataset, Domestic Appliance-Level Electricity Demand and Whole-House Demand from Five UK Homes [NOVÉ] Scientific Data 2:150007, 2015 ⚠ https://doi.org/10.1038/sdata.2015.7 — ověřit Kandidát na hlavní IoT dataset: hierarchie domácnost → spotřebič, přirozeně aditivní metrika.
77. Murray, D. et al. — An Electrical Load Measurements Dataset of United Kingdom Households from a Two-Year Longitudinal Study (REFIT) [NOVÉ] Scientific Data 4:160122, 2017 ⚠ https://doi.org/10.1038/sdata.2016.122 — ověřit Alternativa k UK-DALE: 20 domácností, delší časové pokrytí.
78. Olist Brazilian E-Commerce Public Dataset [ZMĚNA — pouze doplňkový] https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce Zadání požaduje data z chytrých zařízení. Olist ponechat jen pokud ho v práci použiješ jako druhou doménu pro ověření přenositelnosti. Citovat jako dataset: autor, verze, URL, datum přístupu.
79. Použité a srovnávané nástroje — dokumentace, URL a datum přístupu Implementace: LangGraph: https://langchain-ai.github.io/langgraph/ Qdrant: https://qdrant.tech/documentation/ Streamlit: https://docs.streamlit.io/ DuckDB: https://duckdb.org/docs/ Laravel: https://laravel.com/docs React: https://react.dev/ Lokální modely [NOVÉ]: Ollama: https://ollama.com/ llama.cpp: https://github.com/ggml-org/llama.cpp vLLM: https://docs.vllm.ai/ Existující nástroje pro analýzu a vizualizaci časových řad (přehled k bodu 2) [NOVÉ]: Grafana: https://grafana.com/docs/ InfluxDB: https://docs.influxdata.com/ TimescaleDB: https://docs.timescale.com/ Kibana: https://www.elastic.co/guide/en/kibana/
80. Metabase https://www.metabase.com/ Produktová stránka — pouze zmínka o existujícím nástroji v přehledu, nikoli zdroj.

VYŘAZENO
Z původního seznamu:
Medium: „Transforming Data Warehousing with LLMs and OLAP Techniques" — blogový příspěvek, necitovatelné v DP.
github.com/google/LogicLM — repozitář bez publikace, navíc nesouvisel s arXiv:2305.12295, který byl uveden vedle něj.
metabase.com jako položka seznamu literatury — přesunuto mezi nástroje (položka 80).
NavLLM, dva duplicitní odkazy na orbit.dtu.dk — sloučeno do položky 14.
ChartInsighter, duplicita arXiv:2501.09349 — sloučeno do položky 16, cituje se publikovaná verze IEEE TVCG.
V revizi 2:
Pan, L. et al. — Logic-LM (EMNLP 2023 Findings, arXiv:2305.12295) — o symbolických solverech pro logické usuzování; zadání tuto oblast nepotřebuje. Pokud by ses k analogii „LLM formuluje → deterministický backend vykonává" chtěl vrátit, lepší oporu dává položka 38.

NEVYŘEŠENO — dohledat nebo vyřadit
https://proceedings.iclr.cc/paper_files/paper/2024/file/1766d75b077b66457040e4661771aec5-Paper-Conference.pdf ICLR 2024, název a autoři neznámí. Otevři odkaz v prohlížeči a opiš název z první stránky. Pokud jde o Time-LLM (ICLR 2024), je to duplicita položky 36.
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11198129 IEEE, název a venue neznámé. Podle čísla pravděpodobně 2025. Otevři a opiš název.
Bez identifikace jsou obě položky necitovatelné.

OPRAVY OPROTI PŘEDCHOZÍM VERZÍM
Položka 29 (Sathe, Sarawagi): stránky 531–540, nikoli 307–316. Rozsah 307–316 patří práci Sarawagi, User-Adaptive Exploration of Multidimensional Data, VLDB 2000.
Položka 3 (Sarawagi 1999): stránky 42–53. Jeden repozitář uvádí 45–53, DBLP a citace v primární literatuře shodně 42–53.
Revize 3 — převod z revize 2: 1–3 beze změny, 4–29 → +1, 30–77 → +3. Nové položky 4, 31, 32.
Převod z původní verze (před revizí 2) na revizi 3: 1→1, 2→2, 3→3, 4→5, 5→6, 6→7, 7→11, 8→12, 9→13, 10→14, 11→15, 12→16, 13→17, 14→18, 15→19, 16→20, 17→25, 18→26, 19→27, 20→28, 21→29, 22→30, 23→33, 24→10, 25→34, 26→38, 27→39, 28→40, 29→41, 30→42, 31→43, 32→44, 33→45, 34→46, 35→49, 36→50, 37→51, 38→52, 39→53, 40→54, 41→55, 42→56, 43→60, 44→61, 45→62, 46→63, 47→64, 48→65, 49→66, 50→67, 51→68, 52→69, 53→70, 54→71, 55→vyřazeno, 56→73, 57→74, 58→78, 59→79, 60→80.
SHRNUTÍ
Revize 2 doplnila pokrytí bodů zadání, které předchozí verze neřešila: IoT, teorie časových řad, vizualizace časových řad, LLM pro časové řady, lokální vs. cloudové modely, uživatelské testování, IoT datasety.
Revize 3 doplnila explain operátor boloňské skupiny (4) a automatizovanou exploraci dat (31, 32). Všechny tři ověřeny v DBLP/na stránkách vydavatele, kromě DOI položky 4.
Celkem: 80 položek.
Rozložení: úroveň 1 = 21, úroveň 2 = 38, úroveň 3 = 14, nástroje a data = 7. Volně dostupné PDF mimo arXiv: položky 2, 4, 5, 6, 9, 14, 24 (katalog), 25, 28, 29, 31, 32, 65.

KONTROLNÍ SEZNAM PŘED ODEVZDÁNÍM
Ověřit všechny položky označené ⚠ v DBLP nebo Crossref.
Citovat publikované verze místo arXiv preprintů tam, kde existují: COOL, ChartInsighter, Spider 2.0, survey Hong et al., Blázquez-García, Ji et al., Zhang et al. (IJCAI 2024), vLLM (SOSP 2023), HELM (TMLR).
Rozhodnout hlavní IoT dataset (UK-DALE, REFIT, nebo jiný) a konzultovat s vedoucím. Podle toho vyřadit nepoužitý z položek 76–77 a rozhodnout o Olistu (78).
Identifikovat nebo vyřadit dva neznámé odkazy.
Citovat datasety s verzí a datem přístupu.
Zapracovat položky 1–5, 25–32 do kapitoly Related Work dříve, než napíšeš formulaci vlastního přínosu.
Pro každý bod zadání mít v textu aspoň jednu kapitolu se zdroji ze sekce MAPOVÁNÍ — oponent to bude kontrolovat proti zadání.
