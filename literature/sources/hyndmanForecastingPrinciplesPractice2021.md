---
citekey: hyndmanForecastingPrinciplesPractice2021
title: "Forecasting: Principles and Practice"
authors: "Hyndman, Rob J.; Athanasopoulos, George"
year: 2021
venue: "OTexts, Melbourne, 3. vydání"
kind: book   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [time-series-analysis, anomaly-detection]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/HB8XLVWD)

## TL;DR
Volně dostupná učebnice předpovídání časových řad. Pro práci jsou podstatné kapitoly 2 (grafy a vzory v časových řadách, autokorelace, bílý šum), 3 (aditivní a multiplikativní [[time-series-analysis|dekompozice]] na trend-cyklus, sezónní složku a zbytek, metoda STL) a 5 (jednoduché referenční předpovědi, vlastnosti reziduí, predikční intervaly), které dávají teoretický základ pro popis dat z úlů a pro očekávanou hodnotu, vůči které se hledají [[anomaly-detection|anomálie]].

## Klíčová tvrzení
- C1: Trend je dlouhodobý (nemusí být lineární) růst nebo pokles dat; sezónní vzor je vyvolán sezónními faktory (roční období, den v týdnu) a má vždy pevnou a známou periodu; cyklus jsou vzestupy a poklesy bez pevné frekvence, obvykle trvající alespoň 2 roky. (s. 13, §2.3)
- C2: Autokorelace měří lineární vztah mezi zpožděnými hodnotami časové řady; řada bez autokorelace je bílý šum a u ní se očekává, že 95 % hodnot ACF leží v mezích ±1,96/√T, kde T je délka řady. (s. 35, §2.8; s. 38–39, §2.9)
- C3: Aditivní dekompozice y_t = S_t + T_t + R_t (sezónní složka, trend-cyklus, zbytek) je vhodná, když velikost sezónních výkyvů nebo variabilita kolem trendu nezávisí na úrovni řady; když je jí úměrná, je vhodnější multiplikativní dekompozice y_t = S_t × T_t × R_t, kterou lze získat i aditivní dekompozicí logaritmu dat. (s. 50, §3.2)
- C4: STL (Seasonal and Trend decomposition using Loess) zvládne jakýkoli typ sezónnosti, sezónní složka se může v čase měnit, hladkost trendu volí uživatel a robustní varianta zajistí, že občasná neobvyklá pozorování neovlivní odhad trendu ani sezónní složky, projeví se jen ve zbytku; nevýhodou je, že automaticky neřeší kalendářní vlivy a nabízí jen aditivní dekompozici. (s. 72, §3.6)
- C5: Jako referenční (benchmark) metody kniha používá jednoduché předpovědi, mezi nimi naivní (všechny předpovědi = poslední pozorování) a sezónní naivní (předpověď = poslední pozorovaná hodnota ze stejné sezóny, např. stejného měsíce předchozího roku). (s. 84–85, §5.2)
- C6: Dobrá předpovědní metoda má rezidua nekorelovaná a s nulovým průměrem (jinak v nich zbývá informace, resp. předpovědi jsou vychýlené); užitečné, ale ne nutné je, aby měla konstantní rozptyl a normální rozdělení. (s. 92–93, §5.4)
- C7: Predikční interval udává interval, ve kterém s danou pravděpodobností očekáváme budoucí hodnotu; při normálním rozdělení je 95% interval pro předpověď h kroků dopředu ŷ ± 1,96 σ̂_h, kde σ̂_h je odhad směrodatné odchylky rozdělení předpovědi. (s. 99, §5.5)

## Vztah k mé práci


## Citovat pro


## Pozor
- Kniha je volně online (https://otexts.com/fpp3/), bez DOI. Přiložené PDF je tisk webových kapitol 2, 3 a 5 z prohlížeče (stav 15. 11. 2026, 134 stran): strany v tvrzeních jsou strany tohoto PDF, ne tištěné knihy. **Citovat podle sekcí** (§2.3 atd.), v práci uvést URL a datum přístupu.
- Webová verze se průběžně aktualizuje a není totožná s tištěným vydáním 2021 (např. §3.6 cituje Bandara et al. 2025); citovaný text odpovídá webu k datu přístupu.
- Fulltext: strany 20, 27, 31, 32, 38, 49, 65, 76, 108 nahrazeny OCR (grafy); PAGE_WARN na s. 67, 70, 71, 73, 90, 99, 111, 114, 121, 122, 127 a další (vzorce, kód, grafy). C2 (s. 38, OCR) a C7 (s. 99, vzorec) ověřit proti PDF.
- Předchozí položka v Zoteru měla přiložené slajdy z přednášky „3.3 Hierarchical forecasting“, ne knihu; nová položka je založená jako Book.
- Kniha používá R (fable, tsibble); kód a cvičení nejsou zdrojem tvrzení.
