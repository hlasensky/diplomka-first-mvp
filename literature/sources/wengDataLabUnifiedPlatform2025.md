---
citekey: wengDataLabUnifiedPlatform2025
title: "DataLab: A Unified Platform for LLM-Powered Business Intelligence"
authors: "Weng, Luoxuan; Tang, Yinghao; Feng, Yingchaojie; Chang, Zhuo; Chen, Ruiqin; Feng, Haozhe; Hou, Chen; Huang, Danqing; Li, Yang; Rao, Huaming; Wang, Haonan; Wei, Canshi; Yang, Xiaofeng; Zhang, Yuhui; Zheng, Yifeng; Huang, Xiuqi; Zhu, Minfeng; Ma, Yuxin; Cui, Bin; Chen, Peng; Chen, Wei"
year: 2025
venue: "2025 IEEE 41st International Conference on Data Engineering (ICDE)"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [llm-data-agents, text-to-sql, conversational-olap]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/A5EKXMDB)

## TL;DR
DataLab (Tencent) spojuje víceagentní LLM framework s rozšířeným Jupyter notebookem, aby jedno prostředí pokrylo přípravu dat, analýzu i vizualizaci pro inženýry, vědce i analytiky. Jádrem jsou tři moduly: automatické generování doménových znalostí z historie SQL/Python skriptů a překlad dotazu do JSON DSL, strukturovaná komunikace agentů řízená konečným automatem a výběr kontextu podle DAG závislostí buněk. Na firemních datech uvádí až +58,58 % přesnosti NL2DSL a −61,65 % tokenů na dotaz.

## Klíčová tvrzení
- C1: DataLab tvoří dvě části: víceagentní LLM framework (specializovaní agenti pro BI úlohy, každý jako DAG komponent, a proxy agent, který s uživatelem komunikuje a přiděluje úlohy) a notebook rozšiřující JupyterLab o buňky SQL, Python/PySpark, Markdown a Chart s LLM asistencí na úrovni notebooku i buňky; uživatel výsledek agentů přijme, upraví, nebo odmítne. (s. 3–4, §III)
- C2: Při průzkumu u Tencentu 85 % tabulek postrádalo úplná metadata, ale byly navázané na SQL/Python skripty; DataLab proto z historie skriptů, schématu a data lineage generuje LLM v procesu Map-Reduce se self-calibration (LLM hodnotí výsledek skórem 1–5, pod prahem se generuje znovu) popisy, použití, tagy a výpočetní logiku odvozených sloupců na úrovni databáze, tabulky a sloupce a ukládá je do znalostního grafu s uzly pro aliasy. (s. 5, §IV-A; s. 6, §IV-A–B)
- C3: Dotaz se nejprve přepíše (doplní se kontext předchozích kol, časové výrazy jako „last year“ se standardizují vůči aktuálnímu času), pak se coarse-to-fine vyberou relevantní uzly znalostí a LLM dotaz přeloží do JSON DSL ([[text-to-sql]], [[conversational-olap]]) (MeasureList, DimensionList, ConditionList) validovaného JSON Schema, které se pravidly převádí na SQL nebo Vega-Lite; když znalosti chybí, nastupuje Data Profiling (statistiky a vzorky sloupců + LLM popis). (s. 6–7, §IV-C)
- C4: Na reálných datech Tencentu (439 dvojic dotaz–tabulka–sloupec, 326 dvojic dotaz–DSL) vzrostl s veškerými vygenerovanými znalostmi Recall@5 schema linkingu o 38,47 % (41,02 → 79,49) a přesnost NL2DSL o 58,58 % (32,52 → 91,10) oproti nastavení jen se schématem; samotné popisy, použití a tagy (S2) přinesly +30,77 % a +29,14 %. (s. 9, §VII; s. 11, §VII-C, Tab. II)
- C5: Výběr kontextu podle DAG závislostí buněk snížil na 150 dotazech z 50 notebooků spotřebu tokenů na dotaz o 61,65 % (10,69 K → 4,10 K) při poklesu přesnosti o 4,67 % (86,67 → 82,00 %), který autoři přičítají občas nenalezeným Markdown buňkám kvůli omezením embedding podobnosti. (s. 11–12, §VII-E, Tab. IV)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování: fulltext s. N = tištěná strana 4345 + N (článek je na s. 4346–4359 sborníku ICDE 2025).
- PAGE_WARN s. 4 (text obrázku Fig. 2 se míchá do sloupce); próza použitá v C1 zkontrolována proti vyrenderované stránce PDF.
- Tab. II–IV (s. 11–12) pdftotext rozházel; ve fulltextu jsou ručně přepsané z PDF. Přírůstky v C4 jsou rozdíly v procentních bodech, i když je článek uvádí jako „%“.
- Na veřejných benchmarcích (Tab. I, s. 10, GPT-4) DataLab nevede ve všech úlohách: na Spider má 80,70 EX proti 87,80 (PURPLE) a autoři sami píší, že některé baselines vynikají v jednotlivých úlohách (např. NL2SQL) (s. 9, §VII-A). Necitovat jako SOTA pro text-to-SQL.
- Výsledky C4 a C5 (a ablace komunikace agentů, Tab. III: úspěšnost 73 → 92 %, přesnost 56 → 84 % na 100 otázkách, s. 11) jsou na proprietárních datech Tencentu, nereprodukovatelné. U C4 článek neuvádí, který LLM byl použit.
- Komunikace agentů (FSM + strukturované informační jednotky, §V) a uživatelská zpětná vazba z nasazení (§VIII) nejsou v claims; při úrovni 2 vynechány.

## Obrázky
- Obr. 1 (s. 3) – architektura DataLabu: agentní framework, notebook a tři moduly (znalosti, komunikace agentů, kontext buněk) ![[figures/wengDataLabUnifiedPlatform2025/fig1.png]]
