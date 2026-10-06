---
citekey: liuElephantRoomReliable2024
title: "The Elephant in the Room: Towards A Reliable Time-Series Anomaly Detection Benchmark"
authors: "Liu, Qinghua; Paparrizos, John"
year: 2024
venue: "Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Datasets and Benchmarks Track"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [anomaly-detection, llm-time-series]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/Z48GNHBX)

## TL;DR
Benchmark TSB-AD pro detekci anomálií v časových řadách: 1070 ručně kurátorovaných řad ze 40 datasetů, 40 detekčních algoritmů (statistické, neuronové, foundation modely) a rozbor 10 evaluačních měr. Autoři ukazují, že rozšířený point-adjustment zvýhodňuje i náhodné skóre, a jako nejspolehlivější míru doporučují VUS-PR. Jednodušší a statistické metody často vycházejí lépe než složité neuronové architektury.

## Klíčová tvrzení
- C1: Obor detekce [[anomaly-detection]] v časových řadách podle autorů trpí vadnými datasety (chybné značení, run-to-failure bias, jediná anomálie na řadu, nerealistický podíl anomálií), zkreslenými evaluačními měrami a nekonzistentní praxí benchmarků. (s. 1, §1; s. 3–4, §3.1)
- C2: TSB-AD obsahuje 1070 kurátorovaných časových řad ze 40 datasetů (870 jednorozměrných, 200 vícerozměrných), vybraných ve třech krocích (sběr, vyřazení vadných řad, ověření kvality značení algoritmy) s konsenzem čtyř anotátorů, a 40 detekčních algoritmů; 15 % dat z každého datasetu slouží k ladění hyperparametrů. (s. 1, Abstract; s. 5, §4.1.1, Obr. 3; s. 7, §5.1)
- C3: Point adjustment (PA) zvýhodňuje šumová skóre: náhodné skóre se pod PA-F1 umístilo na 26. místě ve srovnání s 32 detektory. Jako nejrobustnější (nejméně citlivou na posun), nejpřesnější a nejférovější míru autoři určili VUS-PR. (s. 5, §3.2; s. 9, §5.2.1)
- C4: Mezi 12 nejlepšími metodami na TSB-AD-U jsou z více než poloviny statistické přístupy a vede Sub-PCA; na TSB-AD-M jsou úspěšnější neuronové sítě (CNN, OmniAnomaly), ale statistické metody zůstávají silné. Jednodušší architektury (CNN, LSTM) obecně překonávají složité transformery. (s. 9, §5.2.2; s. 10, §5.2.4)
- C5: Foundation modely ([[llm-time-series]]) jsou silné na bodové anomálie, ale slabé na sekvenční (předpovídají jen jednu hodnotu na krok s omezeným oknem); pokus integrovat LLM do detekce anomálií v časových řadách dal neuspokojivé výsledky. Ruční kontrola dat stojí na omezeném počtu zkušených uživatelů. (s. 10, §5.2.3–5.2.4)

## Vztah k mé práci


## Citovat pro


## Pozor
- Strany 29–31 (přílohy) jsou nahrazeny OCR textem; PAGE_WARN s. 19, 24, 26 (tabulky v přílohách). Claims citují jen hlavní text (s. 1–10).
- Tabulky a grafy (Tab. 1, Obr. 5–8) jsou v extraktu rozházené; pořadí metod v C4 je z textu, ne z grafu.
- Text (s. 9) uvádí CNN a OmniAnomaly na TSB-AD-M na 2. a 3. místě, obr. 7(b) je ale řadí na 1. a 2. (PCA 3.). Pořadí necituj bez kontroly v PDF.
- „Neuspokojivý“ pokus o integraci LLM (C5) se opírá o jedinou citovanou práci [114] (OFA).
- Benchmark je na univariátních i multivariátních řadách obecně, ne na datech z úlů; pro tvoji evaluaci jde hlavně o argument pro metriku VUS-PR a proti PA-F1.
