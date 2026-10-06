---
citekey: zhouCanLLMsUnderstand2025
title: "Can LLMs Understand Time Series Anomalies?"
authors: "Zhou, Zihao; Yu, Rose"
year: 2025
venue: "International Conference on Learning Representations (ICLR 2025)"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [anomaly-detection, llm-time-series]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/R6AKJ8UQ)

## TL;DR
Kontrolovaná studie, zda (multimodální) LLM rozumí časovým řadám, zkoumaná přes zero-shot a few-shot detekci anomálií na syntetických datech. Autoři testují hypotézy převzaté z literatury o LLM pro predikci: LLM detekují anomálie lépe z obrázku grafu než z čísel v textu, chain-of-thought výkon nezlepšuje, delší vstup výkon zhoršuje a schopnosti se mezi modely výrazně liší. Jednoduché anomálie LLM najdou, pro jemné reálné anomálie autoři důkaz nemají.

## Klíčová tvrzení
- C1: Studie zkoumá, zda LLM rozumí časovým řadám, přes zero-shot a few-shot [[anomaly-detection]]; testuje hypotézy převzaté z výzkumu LLM pro predikci časových řad řízenými experimenty a hodnotí hlavně affinity F1. (s. 1, Abstract, §1)
- C2: Experimenty používají čtyři M-LLM (Qwen-VL-Chat, InternVL2-Llama3-76B, GPT-4o-mini, Gemini-1.5-Flash) s 21 variantami promptu (13 textových, 8 vizuálních) na syntetických datasetech s bodovými, rozsahovými, frekvenčními a trendovými anomáliemi; syntetická data volí kvůli problémům se značením veřejných benchmarků, výsledky na reálném Yahoo S5 jsou podle autorů konzistentní. (s. 7, §5.1; s. 8, §5.1)
- C3: Explicitní chain-of-thought výkon nezlepšuje: podle hlavního textu výkon v detekci anomálií při CoT promptech klesá napříč modely i typy anomálií; příloha však uvádí výjimku – GPT-4o-mini se s CoT téměř nemění a u frekvenčních anomálií se mírně zlepší. (s. 2, §1; s. 9, §5.2; s. 24, App. C)
- C4: M-LLM najdou anomálie mnohem lépe z vizualizované časové řady (obrázku) než z čísel v textu; výjimkou jsou frekvenční anomálie u proprietárních modelů. (s. 2, §1; s. 9–10, §5.2)
- C5: Schopnost LLM rozpoznat vzory v časových řadách nevychází z repetition bias ani z aritmetiky: přidání šumu sníží výkon u textu i obrázku podobně a při snížení přesnosti sčítání pětimístných čísel na 12 % zůstává detekce anomálií převážně stejná. (s. 9, §5.2)
- C6: LLM fungují hůř u delších vstupů: zkrácení řady interpolací z 1000 na 300 kroků výkon konzistentně zlepšuje; chování jednotlivých modelů se výrazně liší (např. GPT méně trpí delšími sekvencemi, Qwen lépe zvládá obrazový vstup). (s. 10, §5.2)
- C7: Jako sanity check autoři uvádějí, že LLM s vhodným promptem a obrazovým vstupem překonávají Isolation Forest a prahování na bodových, rozsahových a trendových datech; frekvenční anomálie jsou pro LLM obtížné a doporučují předzpracování Fourierovou analýzou. (s. 24, Obs. 9; s. 25, Obs. 9; s. 10, §6)
- C8: Omezení: LLM podle autorů zvládnou triviální anomálie, ale nemají důkaz, že rozumí jemnějším reálným anomáliím; schopnost LLM rozumět numerickým časovým řadám a uvažovat o nich je značně omezená a autoři vyzývají k opatrnosti. (s. 1, Abstract; s. 2, §1)

## Vztah k mé práci


## Citovat pro


## Pozor
- PAGE_WARN s. 24–38 (přílohy s grafy a tabulkami). C7 cituje s. 24–25 (Observation 9); text z nich je čitelný, čísla ověř v PDF.
- Hlavní metrika je affinity F1 (LLM vracejí intervaly, ne skóre), takže VUS-PR z [[liuElephantRoomReliable2024]] tu nejde použít.
- „Překonávají“ v C7 platí pro affinity F1 (obr. 19); v klasickém F1 má Isolation Forest v příkladu na s. 8 vyšší skóre než LLM.
- Data jsou syntetická (kromě přílohy s Yahoo S5); závěry jsou o schopnostech modelů z roku 2024.
- Semantic Scholar uvádí rok 2024 (arXiv preprint), cituj ICLR 2025.
