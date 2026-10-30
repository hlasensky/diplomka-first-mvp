---
citekey: liCanLLMAlready2023a
title: "Can LLM Already Serve as A Database Interface? A BIg Bench for Large-Scale Database Grounded Text-to-SQLs"
authors: "Li, Jinyang; Hui, Binyuan; Qu, Ge; Yang, Jiaxi; Li, Binhua; Li, Bowen; Wang, Bailin; Qin, Bowen; Geng, Ruiying; Huo, Nan; Zhou, Xuanhe; Ma, Chenhao; Li, Guoliang; Chang, Kevin; Huang, Fei; Cheng, Reynold; Li, Yongbin"
year: 2023
venue: "Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [text-to-sql]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/EQX8WPT2)

## TL;DR
BIRD je benchmark pro [[text-to-sql]] nad velkými reálnými databázemi (12 751 otázek, 95 databází, 33,4 GB), který kromě schématu zdůrazňuje špinavé hodnoty v datech, potřebu externích znalostí a efektivitu výsledného SQL (nová metrika VES). I nejlepší LLM z roku 2023 dosahují zhruba 55 % execution accuracy proti 93 % u lidí; nejčastější chyby jsou špatné propojení na schéma a nepochopení obsahu databáze.

## Klíčová tvrzení
- C1: Problém: dosavadní benchmarky (Spider, WikiSQL) se soustředí na schéma databáze s malým počtem řádků hodnot, což vytváří mezeru mezi akademickým výzkumem a praxí; BIRD proto přidává tři výzvy – velké a špinavé (noisy) hodnoty v databázích, ukotvení otázky v externích znalostech a efektivitu provádění SQL. (s. 1, Abstract; s. 2, §1)
- C2: BIRD obsahuje 12 751 párů otázka–SQL nad 95 databázemi o celkové velikosti 33,4 GB z 37 odborných domén; databáze se dělí na 69 trénovacích, 11 vývojových a 15 testovacích, pocházejí z 32 % z Kaggle, ze 48 % z CTU Prague Relational Learning Repository a z 20 % je autoři sestavili z otevřených tabulek; 15 testovacích databází autoři kurátorovali navíc pro skrytou testovací sadu, aby zabránili úniku dat. (s. 2, §1; s. 3, §3.2)
- C3: Otázky a SQL anotují crowdsourcingoví anotátoři, kteří prošli zkouškou; SQL vzniká double-blind postupem (dva anotátoři nezávisle, shodné výsledky se přijmou, jinak rozhodují experti) a pokud byla k sestavení SQL použita externí znalostní evidence, zaznamená se k němu; evidence se třídí do čtyř kategorií: numerické uvažování, doménová znalost, synonyma a popis hodnot (value illustration); popis hodnot potřebuje 70,1 % otázek. (s. 3, §3.1; s. 4, §3.3–3.4; s. 5, §4)
- C4: Metriky: execution accuracy (EX) je podíl příkladů, kde predikované a referenční SQL vrátí shodnou výslednou množinu; Valid Efficiency Score (VES) započítává jen správné (valid) dotazy a váží je odmocninou poměru efektivity referenčního a predikovaného SQL; efektivitou je v BIRD hlavně doba běhu (každé SQL se spustí 100× na stejném CPU a průměruje se po vyřazení odlehlých hodnot). (s. 5–6, §5)
- C5: Na testovací sadě s externí znalostí dosahuje GPT-4 EX 54,89 % a GPT-4 + DIN-SQL 55,90 %, zatímco lidé 92,96 % (VES: GPT-4 60,77, lidé 90,27); tytéž modely jsou na BIRD výrazně horší než na Spideru (např. DIN-SQL na dev sadě 82,8 vs. 50,7 EX). (s. 1, Abstract; s. 7, Tab. 2; s. 8, Tab. 3, Obr. 6)
- C6: Dodání externí znalostní evidence zlepšuje všechny modely (např. GPT-4 na testu 34,88 → 54,89 EX), u ChatGPT s chain-of-thought ale autoři pozorují pokles nebo jen omezené zlepšení; v jemném rozboru (Obr. 7) mají všechny LLM znatelně horší výsledky v řazení (ranking) a numerických výpočtech (math) než v doménové znalosti, synonymech a popisu hodnot, což podle autorů může naznačovat nedostatečnost současných LLM pro hlubší datově-vědní úlohy. (s. 7, Tab. 2; s. 9, §6.5–6.6)
- C7: Rozbor 500 náhodně vybraných chyb ChatGPT: špatné schema linking 41,6 %, nepochopení obsahu databáze (neexistující sloupce/tabulky, špatné hodnoty, hlavně u velkých databází) 40,8 %, nepochopení znalostní evidence 17,6 %; občas i SQL funkce z jiného dialektu (MySQL Year() místo SQLite STRFTIME()). (s. 9–10, §6.6)
- C8: Omezení: double-blind anotace je náročná na zdroje; BIRD používá SQLite, z něhož se obtížně získávají plány provádění dotazů pro přesné měření efektivity a které ztěžuje přizpůsobení jiným SQL dialektům – autoři plánují verze pro PostgreSQL a MySQL. (s. 10, §8)

## Vztah k mé práci


## Citovat pro


## Pozor
- Zotero PDF je arXiv v3 (2305.03111v3, 15. 11. 2023) s patičkou NeurIPS 2023 Datasets and Benchmarks; čísla stran = strany PDF (1–28), ne stránkování sborníku z bibu (42330–42357).
- PAGE_WARN s. 7 (Tabulka 2, EX) – sloupce v pdftotext byly přeházené, tabulka je ve fulltextu ručně přepsaná z PDF; stejně přepsaná je Tabulka 3 (VES, s. 8). PAGE_WARN s. 9 – radarový graf Obr. 7, text §6.5–6.6 je čitelný; hodnoty z grafu se nečtou.
- Abstrakt označuje GPT-4 (54,89 %) za „nejefektivnější“ model, ale v Tab. 2 má GPT-4 + DIN-SQL na testu 55,90 %. Lidský výkon je uveden jen pro testovací sadu.
- Efektivitní pokusy v §6.4 jsou malé: dvoufázová optimalizace (úspora času 77,75 %) jen na 10 příkladech od ChatGPT; „Chat w/ Database“ s indexy 87,3 % – detaily v příloze B.5 (nečteno).
- Výsledky jsou pro modely z roku 2023 (zero-shot ICL); leaderboard se od té doby posunul. Hodnota „~73 % na BIRD“ v seznam.md pochází ze Spider 2.0 (Lei et al.), ne z tohoto článku.
- Rozdělení na 9 428 / 1 534 / 1 789 příkladů je jen v příloze (s. 17, Datasheet), v hlavním textu ne.

## Obrázky
- Obr. 1 (s. 2) – tři výzvy BIRD na příkladech: špinavé hodnoty (plat jako text „US$57,500.00“), externí znalost („POPLATEK TYDNE“ = týdenní výpis) a efektivita SQL (22,4 s vs. 4,0 s) ![[figures/liCanLLMAlready2023a/fig1.png]]
