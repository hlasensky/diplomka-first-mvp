---
type: reading-list
---

> Aktuální znění seznamu literatury. Při nové revizi nahraď celý obsah pod touto poznámkou.
> `python3 literature/tools/litqc.py plan` ho spáruje se Zoterem a poznámkami (podle DOI / názvu, ne podle čísla položky) → `qc/_plan.md`.
> Parser čte jen nadpisy „ÚROVEŇ N“ / „NÁSTROJE A DATA“ a položky ve tvaru `N. …`. Ostatní text ignoruje.

Seznam literatury s odkazy — seřazeno podle důležitosti
Diplomová práce: Konverzační OLAP systém s LLM integrací nad časovými řadami z chytrých zařízení FIT VUT | verze 5. 10. 2026 (rev. 4 — data BeeObserver místo elektřiny, nové vymezení přínosu, prameny ze zadání)
Značka ⚠ = neověřeno, ověř přes `litqc.py meta` nebo DBLP/Crossref. [NOVÉ, rev. 4] = doplněno v revizi 4. Čísla položek platí jen v rámci této revize.

ÚROVEŇ 1 — POVINNÉ (číst celé)
Bez těchto zdrojů nelze obhájit přínos práce ani splnit zadání. Řazeno podle naléhavosti čtení.
1. Sarawagi, S., Agrawal, R., Megiddo, N. — Discovery-Driven Exploration of OLAP Data Cubes EDBT 1998, LNCS 1377, s. 168–182 DOI: https://doi.org/10.1007/BFb0100984 Zavádí anotaci buněk kostky mírou překvapení (SelfExp, InExp, PathExp) a navádění uživatele k anomáliím. Přesně tvůj pilíř 2+3 bez LLM. Číst jako první.
2. Vassiliadis, P., Marcel, P., Rizzi, S. — Beyond Roll-Up's and Drill-Down's: An Intentional Analytics Model to Reinvent OLAP Information Systems, sv. 85, s. 68–91, 2019 DOI: https://doi.org/10.1016/j.is.2019.03.011 Volný preprint: https://www.cs.uoi.gr/~pvassil/publications/2019_IS_IntentionalModel/IS2019_VassiliadisMarcelRizzi_CR_PreprintUoI.pdf Rozšířená verze (arXiv): https://arxiv.org/abs/1812.07854 Definuje pět intenčních operátorů: describe, assess, explain, predict, suggest. Od stejné skupiny jako COOL a VOOL. Nelze se vymezovat vůči boloňské škole a neznat jejich vlastní explain operátor.
3. Sarawagi, S. — Explaining Differences in Multidimensional Aggregates VLDB 1999, s. 42–53 Záznam: https://netman.aiops.org/~peidan/ANM2023/8.AnomalyLocalization/ReadingLists/Explaining%20differences%20in%20multidimensional%20aggregates.pdf Operátor DIFF — hledá vysvětlení rozdílu dvou agregátů pomocí drill-downu. Doslova „OLAP-aware explanation".
4. Francia, M., Rizzi, S., Marcel, P. — Explaining Cube Measures Through Intentional Analytics [NOVÉ, rev. 3] Information Systems 121:102338, 2024 (open access) DOI: https://doi.org/10.1016/j.is.2023.102338 Implementace operátoru explain z Intentional Analytics Model (položka 2) — vysvětluje míru kostky pomocí jiných měr a modelů nad nimi. Bez znalosti tohoto článku se nelze vymezit vůči boloňské skupině. Vymezení (rev. 4): jejich explain vysvětluje cílovou míru jinými měrami téže kostky na žádost uživatele; tvůj systém pracuje s IoT časovými řadami, hlásí anomálie proaktivně, hledá souvislosti přes jiné fakty (drill-across přes sdílené dimenze) a LLM orchestruje detekci, drill-down i vysvětlení. Tatáž skupina má i operátor predict: Francia, Rizzi, Golfarelli, Marcel — Predicting Multidimensional Cubes Through Intentional Analytics, Information Systems 136:102628, 2026. Citovat jednou větou.
5. Wu, E., Madden, S. — Scorpion: Explaining Away Outliers in Aggregate Queries PVLDB 6(8):553–564, 2013 DOI: https://doi.org/10.14778/2536354.2536356 Volné PDF (MIT): https://dspace.mit.edu/bitstream/1721.1/89076/1/scorpion-vldb13.pdf Kanonická práce o vysvětlování outlierů v agregacích. Najde predikát, který po aplikaci na vstupní data outlier odstraní. Tvůj agent dělá LLM-řízenou variantu.
6. Zhou, Z., Yu, R. — Can LLMs Understand Time Series Anomalies? ICLR 2025 arXiv: https://arxiv.org/abs/2410.05440 Stránka konference: https://iclr.cc/virtual/2025/poster/30008 LLM rozumí časovým řadám lépe jako obrázkům než jako textu; explicitní reasoning prompt výkon nezlepší, spíš zhorší. Číst před návrhem architektury agenta.
7. Alnegheimish, S. et al. — SigLLM: Large Language Models Can Be Zero-shot Anomaly Detectors for Time Series? arXiv 2024 https://arxiv.org/abs/2405.14755 ⚠ ověřit [rev. 4: povýšeno z úrovně 2 — s položkou výše odůvodňuje dělbu práce: deterministická detekce, LLM orchestruje a vysvětluje]
8. Greengard, S. — The Internet of Things [NOVÉ, rev. 4] MIT Press, 2015, ISBN 978-026-2527-736. Základní literární pramen ze zadání. Pojmy a vize IoT pro kapitolu o chytrých zařízeních (bod 1).
9. John, P. — Optimising processes in IoT [NOVÉ, rev. 4] Pojednání o tématu disertační práce, FIT VUT v Brně, 2024, vedoucí prof. Ing. Tomáš Hruška, CSc. Základní literární pramen ze zadání. Ukazuje, jak na IoT procesy nahlíží skupina vedoucího.
10. Senger, D., Gruber, C., Kluss, T., Johannsen, C. — Weight, Temperature and Humidity Sensor Data of Honey Bee Colonies in Germany, 2019–2022 [NOVÉ, rev. 4] Data in Brief 52:110015, 2024 DOI: https://doi.org/10.1016/j.dib.2023.110015 Data: https://doi.org/10.5281/zenodo.10407693 Článek k hlavnímu datasetu (BeeObserver): senzory, předzpracování, inspekce, omezení.
11. Al-Fuqaha, A. et al. — Internet of Things: A Survey on Enabling Technologies, Protocols, and Applications [NOVÉ] IEEE Communications Surveys & Tutorials 17(4):2347–2376, 2015 ⚠ https://doi.org/10.1109/COMST.2015.2444095 — ověřit Hlavní zdroj pro kapitolu o IoT (bod 1 zadání). Architektura IoT, protokoly (MQTT, CoAP), aplikační domény včetně chytrých budov a energetiky.
12. Hyndman, R. J., Athanasopoulos, G. — Forecasting: Principles and Practice, 3. vydání [NOVÉ] OTexts, 2021 Volně online: https://otexts.com/fpp3/ Teoretický základ kapitoly o časových řadách: složky (trend, sezónnost, cykly), dekompozice, stacionarita, autokorelace. Čti kapitoly 2–3 a 5; zbytek referenčně.
13. Blázquez-García, A. et al. — A Review on Outlier/Anomaly Detection in Time Series Data [POVÝŠENO z úrovně 2] ACM Computing Surveys 54(3), 2021 Volný preprint: https://arxiv.org/abs/2002.04236 Taxonomie anomálií (bodové, subsekvenční, celé řady; uni- vs. multivariátní). Páteř teoretické části o anomáliích v časových řadách.
14. Jensen, S. K., Pedersen, T. B., Thomsen, C. — Time Series Management Systems: A Survey IEEE TKDE 29(11):2581–2600, 2017 ⚠ https://doi.org/10.1109/TKDE.2017.2740932 — ověřit Přehled TSDB a systémů pro správu senzorových dat. Podklad pro zdůvodnění volby DuckDB oproti InfluxDB/TimescaleDB a pro analýzu požadavků (bod 3). [rev. 4: povýšeno z úrovně 2 — analýza požadavků (bod 3) a volba DuckDB]
15. Francia, M., Gallinucci, E., Golfarelli, M. — COOL: A Framework for Conversational OLAP, Information Systems 104:101752, 2022 DOI: https://doi.org/10.1016/j.is.2021.101752 https://www.sciencedirect.com/science/article/pii/S0306437921000211 Nejbližší prior work. Musíš přesně vědět, co dělá a co nedělá.
16. VOOL — přirozenojazyková vokalizace výsledků OLAP sessions Information Systems, 2025 https://dl.acm.org/doi/10.1016/j.is.2024.102496 Přímý předchůdce pilíře 3. Převezmi jejich evaluační protokol.
17. NavLLM — interaktivní LLM navigace nad multidimenzionálními daty EDBT 2026 Volné PDF: https://backend.orbit.dtu.dk/ws/portalfiles/portal/437649807/paper-316.pdf Záznam: https://orbit.dtu.dk/en/publications/navllm-interactive-llm-assisted-navigation-over-multidimensional-/
18. ChartInsighter — redukce halucinací při shrnutí grafů časových řad IEEE TVCG, 2025 https://ieeexplore.ieee.org/document/11113164 Preprint: https://arxiv.org/abs/2501.09349 Metodika proti halucinacím při popisu časových řad = přímo pilíř 3.
19. Yao, S. et al. — ReAct: Synergizing Reasoning and Acting in Language Models ICLR 2023 arXiv: https://arxiv.org/abs/2210.03629 Projekt: https://react-lm.github.io/ Tvůj drill-down agent je v podstatě ReAct smyčka. Primární zdroj pro návrhové rozhodnutí.
20. BIRD — benchmark pro Text-to-SQL nad rozsáhlými reálnými databázemi NeurIPS 2023 https://arxiv.org/abs/2305.03111
21. Lei, F. et al. — Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows ICLR 2025 (Oral) arXiv: https://arxiv.org/abs/2411.07763 Na realistických schématech padá execution accuracy z ~91 % (Spider 1.0) a ~73 % (BIRD) na ~21 %. Musíš explicitně vymezit podmínky, za nichž platí tvoje očekávaná přesnost.
22. Schulhoff, S. et al. — The Prompt Report: A Systematic Survey of Prompt Engineering Techniques arXiv 2024 https://arxiv.org/abs/2406.06608 Terminologický a taxonomický rámec pro kapitolu o promptingu.
23. Lewis, J. R. — The System Usability Scale: Past, Present, and Future [NOVÉ] International Journal of Human–Computer Interaction 34(7):577–590, 2018 ⚠ https://doi.org/10.1080/10447318.2018.1455307 — ověřit Uživatelské testování je podle zadání primární evaluace. Tento zdroj ti dá standardizovaný dotazník (SUS), normy pro interpretaci skóre a argumentaci pro jeho použití vedle vlastních Likertových položek.
24. Lenz, H.-J., Shoshani, A. — Summarizability in OLAP and Statistical Data Bases [NOVÉ, rev. 4] SSDBM 1997 ⚠ ověřit Klasická podmínka korektní agregace (neaditivní a semi-aditivní míry). Teoretická opora pro validátor nad sémantickou vrstvou.
25. Buneman, P., Khanna, S., Tan, W.-C. — Why and Where: A Characterization of Data Provenance [NOVÉ, rev. 4] ICDT 2001 ⚠ ověřit Rozlišení why- a where-provenance. Opora pro odkaz každého tvrzení odpovědi na dotaz, který ho podložil (vysvětlování dotazů ze zadání).

ÚROVEŇ 2 — DŮLEŽITÉ (číst metodu a related work)
IoT a správa časových řad
26. Atzori, L., Iera, A., Morabito, G. — The Internet of Things: A Survey Computer Networks 54(15):2787–2805, 2010 ⚠ https://doi.org/10.1016/j.comnet.2010.05.010 — ověřit Historicky nejcitovanější survey IoT. Pro vymezení pojmu a vizí; technické detaily ber z položky 8.
Monitoring úlů (precision beekeeping) [NOVÉ, rev. 4]
27. Zacepins, A. et al. — Challenges in the Development of Precision Beekeeping [NOVÉ, rev. 4] Biosystems Engineering 130:60–71, 2015 ⚠ https://doi.org/10.1016/j.biosystemseng.2014.12.001 — ověřit Doména: co senzory v úlu měří a jak interpretovat signály (rojení, zimování).
28. Meikle, W. G., Holst, N. — Application of Continuous Monitoring of Honeybee Colonies [NOVÉ, rev. 4] Apidologie 46:10–22, 2015 ⚠ https://doi.org/10.1007/s13592-014-0298-x — ověřit Interpretace váhy a teploty úlu v čase: denní cyklus váhy, snůška, teplota plodiště. Podklad pro význam anomálií.
29. Hadjur, H., Ammar, D., Lefèvre, L. — Toward an Intelligent and Efficient Beehive: A Survey of Precision Beekeeping Systems and Services [NOVÉ, rev. 4] Computers and Electronics in Agriculture 192:106604, 2022 ⚠ https://doi.org/10.1016/j.compag.2021.106604 — ověřit Přehled IoT systémů pro monitoring úlů. Spojuje bod 1 zadání s doménou dat.
Vizualizace časových řad
30. Aigner, W., Miksch, S., Schumann, H., Tominski, C. — Visualization of Time-Oriented Data Springer, 2011 (2. vydání 2023 ⚠ ověřit) ⚠ https://doi.org/10.1007/978-0-85729-079-3 — ověřit Standardní monografie k bodu 2 zadání. Taxonomie vizualizací časových dat; z přehledu technik (TimeViz Browser) si vyber ty relevantní pro senzorová data. Online katalog technik: https://browser.timeviz.net/
Vysvětlování anomálií a dotazů
31. Yan, S. et al. — CMMD: Cross-Metric Multi-Dimensional Root Cause Analysis ACM SIGKDD 2022, s. 4310–4320 ⚠ https://dl.acm.org/doi/10.1145/3534678.3539236 — ověřit Preprint: https://arxiv.org/abs/2203.11141 ⚠ ověřit
32. Roy, S., Suciu, D. — A Formal Approach to Finding Explanations for Database Queries ACM SIGMOD 2014, s. 1579–1590 DOI: https://doi.org/10.1145/2588555.2588578 Volné PDF: https://homes.cs.washington.edu/~suciu/main_explanation.pdf Formální rámec intervence: vysvětlení = odebrání n-tic, které významně mění výsledek dotazu.
33. AXIS — vysvětlitelná detekce anomálií v časových řadách pomocí LLM arXiv 2025 https://arxiv.org/abs/2509.24378 Jediný zdroj pokrývající průnik pilířů 2 a 3. [rev. 4: sníženo z úrovně 1 — arXiv bez recenze, nestavět na tom argument]
Provenance [NOVÉ, rev. 4]
34. Cheney, J., Chiticariu, L., Tan, W.-C. — Provenance in Databases: Why, How, and Where [NOVÉ, rev. 4] Foundations and Trends in Databases 1(4), 2009 ⚠ https://doi.org/10.1561/1900000006 — ověřit Přehled provenance v databázích. Doplňuje Buneman et al.
Klasická OLAP explorace
35. Sathe, G., Sarawagi, S. — Intelligent Rollups in Multidimensional OLAP Data VLDB 2001, s. 531–540 Volné PDF: https://repository.ias.ac.in/128421
36. Francia, M., Marcel, P., Peralta, V., Rizzi, S. — Enhancing Cubes with Models to Describe Multidimensional Data Information Systems Frontiers, 2021 ⚠ https://doi.org/10.1007/s10796-021-10147-3 — ověřit Implementace operátoru describe z Intentional Analytics Model. Sesterský článek k položce 4.
Proaktivní insighty [NOVÉ, rev. 4]
37. Tang, B., Han, S., Yiu, M. L., Ding, R., Zhang, D. — Extracting Top-K Insights from Multi-dimensional Data [NOVÉ, rev. 4] ACM SIGMOD 2017 DOI: https://doi.org/10.1145/3035918.3035922 Automatické hledání zajímavých pozorování v kostce. Opora pro proaktivní hlášení anomálií.
38. Ding, R. et al. — QuickInsights: Quick and Automatic Discovery of Insights from Multi-Dimensional Data [NOVÉ, rev. 4] ACM SIGMOD 2019 ⚠ https://doi.org/10.1145/3299869.3314037 — ověřit Proaktivní insighty nasazené v Power BI. Srovnání pro proaktivní režim.
Automatizovaná explorace dat
39. Milo, T., Somech, A. — Automating Exploratory Data Analysis via Machine Learning: An Overview ACM SIGMOD 2020 (tutorial), s. 2617–2622 DOI: https://doi.org/10.1145/3318464.3383126 Volné PDF: https://u.cs.biu.ac.il/~somecha/pdf/eda_tutorial.pdf Přehled automatizace EDA: od doporučení jednoho dalšího kroku přes modelování „zajímavosti" až po plně automatické session (deep RL, seq2seq). Rámec pro zařazení tvého agenta mezi přístupy k automatizované exploraci. Cituje ho NavLLM (položka 14).
40. Amer-Yahia, S. — Intelligent Agents for Data Exploration PVLDB 17(12):4521–4530, 2024 DOI: https://doi.org/10.14778/3685800.3685913 Volné PDF: https://www.vldb.org/pvldb/vol17/p4521-amer-yahia.pdf Shrnuje RL agenty pro exploraci dat (včetně roll-up a drill-down operátorů) a ptá se, zda LLM a AI plánování nahradí RL politiky bez přetrénování pro každou úlohu. Přímá opora pro volbu LLM agenta místo RL. Cituje ho NavLLM (položka 14).
Detekce anomálií v časových řadách
41. Liu, Q., Paparrizos, J. — The Elephant in the Room: Towards A Reliable Time-Series Anomaly Detection Benchmark (TSB-AD) NeurIPS 2024, Datasets and Benchmarks Track Volné PDF: https://proceedings.neurips.cc/paper_files/paper/2024/file/c3f3c690b7a99fba16d0efd35cb83b2c-Paper-Datasets_and_Benchmarks_Track.pdf Stránka konference: https://neurips.cc/virtual/2024/poster/97690 Kód a data: https://pypi.org/project/TSB-AD/ 1070 časových řad ze 40 datasetů. Určí ti evaluační metriku (VUS-PR, nikoli F1 s point-adjustem) a doloží, že statistický detektor pro MVP stačí. Číst před návrhem detektoru. [rev. 4: sníženo z úrovně 1 — hlavně argument pro metriku VUS-PR]
42. Wu, R., Keogh, E. — Current Time Series Anomaly Detection Benchmarks are Flawed and are Creating the Illusion of Progress IEEE TKDE 35(3):2421–2429, 2023 Preprint: https://arxiv.org/abs/2009.13807 ⚠ ověřit Proč nesmíš evaluovat s point-adjust protokolem.
LLM a časové řady
43. Gruver, N. et al. — Large Language Models Are Zero-Shot Time Series Forecasters NeurIPS 2023 arXiv: https://arxiv.org/abs/2310.07820 Jak LLM zpracovávají číselné sekvence serializované jako text; vliv tokenizace čísel. Doplňuje položku 7.
44. Jin, M. et al. — Time-LLM: Time Series Forecasting by Reprogramming Large Language Models ICLR 2024 arXiv: https://arxiv.org/abs/2310.01728 Reprezentativní zástupce přístupu „adaptace LLM na časové řady". Pro vymezení: ty LLM nepoužíváš jako prediktor, ale jako orchestrátor a vypravěče.
45. Zhang, X. et al. — Large Language Models for Time Series: A Survey IJCAI 2024 arXiv: https://arxiv.org/abs/2402.01801 ⚠ ověřit Taxonomie přístupů LLM × časové řady. Rámec pro sekci o aktuálních přístupech (bod 2 zadání).
Text-to-SQL a sémantická vrstva
46. The Death of Schema Linking? Text-to-SQL in the Age of Well-Reasoned Language Models arXiv 2024 https://arxiv.org/abs/2408.07702 Přímá argumentace k pokynu vedoucího ohledně schema linkingu vs. volného SQL. Klíčové pro obhajobu schema-constrained přístupu.
47. Hong, Z. et al. — Next-Generation Database Interfaces: A Survey of LLM-based Text-to-SQL IEEE TKDE, 2025 arXiv: https://arxiv.org/abs/2406.08426 Recenzovaný survey — nahradí několik dílčích citací.
48. Sequeda, J., Allemang, D., Jacob, B. — A Benchmark to Understand the Role of Knowledge Graphs on Large Language Model's Accuracy for Question Answering on Enterprise SQL Databases [NOVÉ, rev. 4] arXiv 2023 https://arxiv.org/abs/2311.07509 Empirická opora pro sémantickou vrstvu: přesnost odpovědí nad holým SQL vs. nad sémantickou reprezentací. Čísla ověřit v PDF.
49. Automatic Metadata Extraction for Text-to-SQL arXiv 2025 https://arxiv.org/abs/2505.19988
50. Gao, D. et al. — DAIL-SQL: Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation PVLDB 2024 https://arxiv.org/abs/2308.15363 ⚠ ověřit Systematická evaluace promptovacích strategií v doméně Text-to-SQL.
51. Pourreza, M., Rafiei, D. — DIN-SQL: Decomposed In-Context Learning of Text-to-SQL with Self-Correction NeurIPS 2023 https://arxiv.org/abs/2304.11015 ⚠ ověřit
Agenti a prompting
52. Wei, J. et al. — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models NeurIPS 2022, sv. 35, s. 24824–24837 arXiv: https://arxiv.org/abs/2201.11903
53. Shinn, N. et al. — Reflexion: Language Agents with Verbal Reinforcement Learning NeurIPS 2023 arXiv: https://arxiv.org/abs/2303.11366 Pro self-correction při chybně vygenerovaném dotazu.
54. Schick, T. et al. — Toolformer: Language Models Can Teach Themselves to Use Tools NeurIPS 2023 arXiv: https://arxiv.org/abs/2302.04761
55. Sahoo, P. et al. — A Systematic Survey of Prompt Engineering in Large Language Models arXiv 2024 https://arxiv.org/abs/2402.07927 ⚠ ověřit
Lokální a cloudové modely
56. Frantar, E. et al. — GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers ICLR 2023 arXiv: https://arxiv.org/abs/2210.17323 Kvantizace = hlavní důvod, proč lokální modely běží na spotřebitelském HW. Potřebuješ pro zdůvodnění výběru lokálních modelů a interpretaci rozdílů v kvalitě analýzy.
Generování textu a vizualizací nad daty
57. LIDA — automatická generace vizualizací pomocí LLM ACL 2023 (demo) https://aclanthology.org/2023.acl-demo.11.pdf Krátký demo paper, přečteš za 20 minut.
58. Shi, D. et al. — Calliope: Automatic Generation of Visual Data Stories IEEE TVCG 27(2), 2021 ⚠ https://doi.org/10.1109/TVCG.2020.3030403 — ověřit
59. Ji, Z. et al. — Survey of Hallucination in Natural Language Generation ACM Computing Surveys 55(12), 2023 Volný preprint: https://arxiv.org/abs/2202.03629 Rámec pro tvrzení o věrnosti generovaných vysvětlení.
Konverzační OLAP — doplňkové
60. Natural Language Interfaces for Databases with Deep Learning Springer, 2026 https://link.springer.com/content/pdf/10.1007/978-3-032-06905-4.pdf Monografie — používej jako referenční příručku, nečti lineárně.
RAG
61. Lewis, P. et al. — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks NeurIPS 2020 arXiv: https://arxiv.org/abs/2005.11401 Podklad pro použití Qdrantu a sémantického vyhledávání ve schématu.
Evaluace modelů
62. LLM-as-a-Judge EMNLP 2025 https://aclanthology.org/2025.emnlp-main.138/
63. Zheng, L. et al. — Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena NeurIPS 2023, Datasets and Benchmarks Track arXiv: https://arxiv.org/abs/2306.05685 Původní zdroj metody.
64. Liang, P. et al. — Holistic Evaluation of Language Models (HELM) [NOVÉ] Transactions on Machine Learning Research, 2023 arXiv: https://arxiv.org/abs/2211.09110 Rámec pro vícekriteriální srovnání modelů (přesnost, efektivita, robustnost). Převezmi strukturu metrik pro bod 6b zadání.
Uživatelské testování
65. Brooke, J. — SUS: A „Quick and Dirty" Usability Scale In: Jordan, P. W. et al. (eds.), Usability Evaluation in Industry, Taylor & Francis, 1996, s. 189–194 ⚠ ověřit stránky Původní zdroj dotazníku SUS. Cituj spolu s položkou 21.
66. Likert, R. — A Technique for the Measurement of Attitudes Archives of Psychology 22(140):1–55, 1932 ⚠ ověřit Původní zdroj Likertovy škály, kterou zadání výslovně požaduje.

ÚROVEŇ 3 — DOPLŇKOVÉ (projít abstrakt, citovat jednou větou)
67. Chaudhuri, S., Dayal, U. — An Overview of Data Warehousing and OLAP Technology ACM SIGMOD Record 26(1), s. 65–74, 1997 ⚠ https://doi.org/10.1145/248603.248616 — ověřit
68. Gray, J. et al. — Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals Data Mining and Knowledge Discovery 1(1), s. 29–53, 1997 ⚠ https://doi.org/10.1023/A:1009726021843 — ověřit
69. Kimball, R., Ross, M. — The Data Warehouse Toolkit, 3. vydání Wiley, 2013 — kniha, ISBN 978-1-118-53080-1 ⚠ ověřit ISBN
70. Abuzaid, F. et al. — DIFF: A Relational Interface for Large-Scale Data Explanation PVLDB 2021 ⚠ ověřit ročník a stránky Preprint: https://arxiv.org/abs/1907.12718 ⚠ ověřit
71. Taylor, S. J., Letham, B. — Forecasting at Scale (Prophet) The American Statistician 72(1), s. 37–45, 2018 ⚠ https://doi.org/10.1080/00031305.2017.1380080 — ověřit Dokumentace nástroje: https://facebook.github.io/prophet/
72. Cleveland, R. B. et al. — STL: A Seasonal-Trend Decomposition Procedure Based on Loess Journal of Official Statistics 6(1), s. 3–73, 1990 Volné PDF: https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/stl-a-seasonal-trend-decomposition-procedure-based-on-loess.pdf ⚠ ověřit
73. Spider — benchmark pro cross-domain Text-to-SQL EMNLP 2018 https://aclanthology.org/D18-1425/ Historická reference, číst jen úvod a konstrukci datasetu.
74. Wang, L. et al. — A Survey on Large Language Model based Autonomous Agents Frontiers of Computer Science, 2024 https://arxiv.org/abs/2308.11432 Skenovat taxonomii; pro návrhová rozhodnutí použij primární zdroje (položky 17, 43–45).
75. Wang, Y. et al. — DataShot: Automatic Generation of Fact Sheets from Tabular Data IEEE TVCG 26(1), 2020 ⚠ https://doi.org/10.1109/TVCG.2019.2934398 — ověřit
76. Shen, L. et al. — Towards Natural Language Interfaces for Data Visualization: A Survey IEEE TVCG, 2023 Preprint: https://arxiv.org/abs/2109.03506 ⚠ ověřit
77. Gao, Y. et al. — Retrieval-Augmented Generation for Large Language Models: A Survey arXiv 2023 https://arxiv.org/abs/2312.10997
78. Wohlin, C. — Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering EASE 2014 ⚠ https://doi.org/10.1145/2601248.2601268 — ověřit Pouze pokud v práci popisuješ metodu rešerše.
79. Bhagwan, R. et al. — Adtributor: Revenue Debugging in Advertising Systems USENIX NSDI 2014, s. 43–55 Volné PDF a BibTeX: https://www.usenix.org/conference/nsdi14/technical-sessions/presentation/bhagwan Multidimenzionální lokalizace příčiny anomálie v aditivních KPI přes explanatory power, succinctness a surprise. V IoT kontextu: agregovaná spotřeba přes hierarchii budova → patro → zařízení je aditivní KPI stejného typu. Analogii v textu explicitně zdůvodni. [rev. 4: sníženo — analogie s aditivní spotřebou u úlů neplatí, citovat jen pojem lokalizace anomálie]
80. Sun, Y. et al. — HotSpot: Anomaly Localization for Additive KPIs with Multi-Dimensional Attributes IEEE Access 6:10909–10923, 2018 (open access) DOI: https://doi.org/10.1109/ACCESS.2018.2804764 [rev. 4: sníženo, viz výše]
81. Text-to-MDX — generování MDX dotazů z přirozeného jazyka pomocí GPT-4o ER 2025 https://link.springer.com/chapter/10.1007/978-3-032-08623-5_9 [rev. 4: sníženo — systém generuje SQL, ne MDX]
82. Kwon, W. et al. — Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM) ACM SOSP 2023 arXiv: https://arxiv.org/abs/2309.06180 Technický základ lokálního provozu modelů (bod 4 zadání). Podklad pro diskusi propustnosti a latence lokálního nasazení vs. cloudového API. [rev. 4: sníženo — lokální modely běží přes Ollamu/llama.cpp, ne vLLM]

NÁSTROJE A DATA
Datasety a datové zdroje citovat s verzí a datem přístupu. Dokumentace nástrojů patří do implementační kapitoly.
83. Raasveldt, M., Mühleisen, H. — DuckDB: An Embeddable Analytical Database ACM SIGMOD 2019 (demonstration) ⚠ https://doi.org/10.1145/3299869.3320212 — ověřit
84. Lavin, A., Ahmad, S. — Evaluating Real-Time Anomaly Detection Algorithms: The Numenta Anomaly Benchmark [NOVÉ] IEEE ICMLA 2015, s. 38–44 ⚠ ověřit stránky arXiv: https://arxiv.org/abs/1510.03336 Data: https://github.com/numenta/NAB Anotované anomálie v reálných senzorových řadách. Doplněk k TSB-AD pro evaluaci detektoru na IoT datech.
85. Hersbach, H. et al. — The ERA5 Global Reanalysis [NOVÉ, rev. 4] Quarterly Journal of the Royal Meteorological Society 146(730):1999–2049, 2020 ⚠ https://doi.org/10.1002/qj.3803 — ověřit Zdroj počasí u lokalit úlů (přes Open-Meteo archive API, https://open-meteo.com/en/docs/historical-weather-api).
86. Kaspar, F. et al. — An Overview of the Phenological Observation Network and the Phenological Database of Germany's National Meteorological Service (Deutscher Wetterdienst) [NOVÉ, rev. 4] Advances in Science and Research 11:93–99, 2014 ⚠ https://doi.org/10.5194/asr-11-93-2014 — ověřit Zdroj fenologie (začátek kvetení řepky, akátu, lípy, pampelišky). Data: https://opendata.dwd.de/climate_environment/CDC/observations_germany/phenology/
87. Didan, K. — MOD13Q1 MODIS/Terra Vegetation Indices 16-Day L3 Global 250m SIN Grid [NOVÉ, rev. 4] NASA LP DAAC (dataset) ⚠ https://doi.org/10.5067/MODIS/MOD13Q1.006 — ověřit verzi Zdroj NDVI u lokalit úlů (bodový subset přes ORNL DAAC REST). Citovat s verzí a datem přístupu.
88. Zhu, Y. et al. — MSPB: A Longitudinal Multi-Sensor Dataset with Phenotypic Trait Measurements from Honey Bees [NOVÉ, rev. 4] Scientific Data, 2024 DOI: https://doi.org/10.1038/s41597-024-03695-1 Data: https://zenodo.org/records/8371700 Podmíněně: jen pokud ho použiješ jako ground truth (Varroa, zimní úmrtnost) pro evaluaci anomálií. ⚠ ověřit autory
89. Olist Brazilian E-Commerce Public Dataset [rev. 4: podmíněně] https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce Zadání požaduje data z chytrých zařízení. Olist ponechat jen pokud ho v práci použiješ jako druhou doménu pro ověření přenositelnosti. Citovat jako dataset: autor, verze, URL, datum přístupu.
90. Použité a srovnávané nástroje — dokumentace, URL a datum přístupu Implementace: LangGraph: https://langchain-ai.github.io/langgraph/ Chainlit: https://docs.chainlit.io/ FastAPI: https://fastapi.tiangolo.com/ (Qdrant, Streamlit, Laravel, React: jen podle zvoleného UI stacku) DuckDB: https://duckdb.org/docs/ Lokální modely [NOVÉ]: Ollama: https://ollama.com/ llama.cpp: https://github.com/ggml-org/llama.cpp vLLM: https://docs.vllm.ai/ Existující nástroje pro analýzu a vizualizaci časových řad (přehled k bodu 2) [NOVÉ]: Grafana: https://grafana.com/docs/ InfluxDB: https://docs.influxdata.com/ TimescaleDB: https://docs.timescale.com/ Kibana: https://www.elastic.co/guide/en/kibana/
91. Metabase https://www.metabase.com/ Produktová stránka — pouze zmínka o existujícím nástroji v přehledu, nikoli zdroj.

MAPOVÁNÍ NA BODY ZADÁNÍ
Bod 1 — IoT, chytrá zařízení, časové řady: 8, 9, 10, 11, 12, 13, 14, 26, 27, 28, 29, 71, 72
Bod 2a — vizualizace a nástroje pro analýzu časových řad: 30, 57, 58, 75, 76, 90
Bod 2b — LLM nad daty: 6, 7, 16, 19, 20, 21, 22, 43, 44, 45, 46, 47, 48, 61, 81
Bod 3 — OLAP nad časovými řadami, požadavky na LLM augmentaci: 1, 2, 3, 4, 5, 15, 17, 24, 35, 36, 37, 38, 39, 40, 67, 68
Bod 4 — návrh platformy, vysvětlování dotazů, lokální vs. cloudové modely: 19, 25, 34, 56, 83, 90
Bod 6a — uživatelské testování, scénáře, Likertova škála: 23, 65, 66
Bod 6b — srovnání modelů (výkonnost, kvalita analýzy): 41, 42, 62, 63, 64, 84

VYŘAZENO
V revizi 4: UK-DALE a REFIT (hlavní dataset je BeeObserver); Sémantické cachování OLAP dotazů (DOLAP 2026, nesouvisí s přínosem); OLAP-AI (CEUR forum, slabá recenze); Joshi et al. — Likert Scale: Explored and Explained (slabý časopis, stačí Likert a Lewis).
Starší vyřazené položky viz revize 3.

NEVYŘEŠENO — dohledat nebo vyřadit
Dva neidentifikované odkazy z revize 3 (ICLR 2024 PDF 1766d75b…, IEEE arnumber 11198129). Bez identifikace necitovatelné.

KONTROLNÍ SEZNAM PŘED ODEVZDÁNÍM
Ověřit všechny položky s ⚠ (`python3 literature/tools/litqc.py meta`). Citovat publikované verze místo preprintů. Greengard a John (prameny ze zadání) musí být v práci citované. Pro každý bod zadání aspoň jedna kapitola se zdroji z mapování.

SHRNUTÍ
Revize 4: celkem 91 položek — úroveň 1 = 25, úroveň 2 = 41, úroveň 3 = 16, nástroje a data = 9. Předchozí revize: scratchpad zálohy / git historie vaultu.
