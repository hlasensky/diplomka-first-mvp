---
citekey: sarawagiDiscoverydrivenExplorationOLAP1998
title: Discovery-Driven Exploration of OLAP Data Cubes
authors: Sarawagi, Sunita; Agrawal, Rakesh; Megiddo, Nimrod
year: 1998
venue: Advances in Database Technology — EDBT'98 (vol. 1377, pp. 168–182)
kind: conference
status: candidate
verified: true
chapters: []
concepts:
  - olap
  - anomaly-detection
  - guided-data-exploration
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/W8XSP9PH)

## TL;DR
Článek navrhuje místo ručního „hypothesis-driven“ procházení OLAP kostky (drill-down/roll-up) přístup „discovery-driven“: výjimky se předpočítají ve všech agregacích a analytika pak při navigaci vedou. Výjimka je buňka, která se výrazně liší od hodnoty očekávané log-lineárním modelem, který kombinuje efekty všech group-by, do nichž buňka patří. Ke každé buňce se počítají ukazatele SelfExp, InExp a PathExp, které říkají, kde a ve kterém směru drillovat. Výpočet je přepsaný tak, aby šel spojit s běžným výpočtem agregací kostky.

## Klíčová tvrzení
- C1: Ruční „hypothesis-driven“ hledání anomálií v [[olap]] kostce je obtížné: kostka mívá 5–8 dimenzí, hierarchie 2–8 úrovní hluboké a desítky až stovky členů na úroveň. Anomálie se navíc na vyšších agregacích nemusí projevit kvůli vzájemnému vyrušení více výjimek nebo velkému množství agregovaných dat. (s. 2, §1)
- C2: Hodnota v buňce je výjimka ([[anomaly-detection]]), pokud se výrazně liší od hodnoty očekávané statistickým modelem. Model kombinuje trendy podél všech dimenzí a group-by, do nichž buňka patří, a je inspirovaný metodami „table analysis“ [HMJ88]. Výjimky se hledají na všech úrovních agregace samostatným fitem modelu pro každé group-by. (s. 2, §1; s. 7, §3.1–3.2)
- C3: Za výjimku se považuje buňka se standardizovaným reziduem nad prahem τ = 2,5, což odpovídá pravděpodobnosti 99 % v normálním rozdělení. (s. 7, §3.1)
- C4: Použitá je multiplikativní forma modelu, převedená logaritmem na aditivní; na OLAP datech podle autorů sedí lépe než aditivní. Koeficienty se odhadují robustně 75% trimmed mean (ořízne se 25 % extrémních hodnot). Rozptyl se modeluje jako mocnina p očekávané hodnoty, odhadnutá maximální věrohodností; klasický ANOVA odhad (stejný rozptyl pro všechny buňky) dával na OLAP datech špatné fity. (s. 8–9, §3.3–3.5)
- C5: Výjimky se sumarizují do tří hodnot na buňku, které vedou [[guided-data-exploration]]. SelfExp je překvapení buňky samotné. InExp je maximum SelfExp přes všechny buňky pod ní, tedy „stojí za to drillovat sem“. PathExp je maximum SelfExp přes buňky dosažitelné drill-downem podél dané dimenze, tedy „kterým směrem drillovat“. (s. 3, §2; s. 9–10, §3.6)
- C6: Na ukázkovém datasetu (Essbase sample, dimenze Product × Market × Time) má Diet-Soda v regionu „E“ výjimečný pokles o 40 % v srpnu a 33 % v říjnu. V rovině Product-Time agregované přes regiony se to téměř neprojeví a analytika k tomu dovede až InExp. Kontextový model navíc označí i buňky s malou absolutní změnou (např. Birch-B v prosinci −10 %), protože se liší od chování ostatních produktů v témž měsíci. (s. 3–6, §2–3)
- C7: Výpočet má tři fáze: agregace kostky, fit modelu a sumarizace výjimek. Přepis modelové rovnice (Eq. 5) snižuje počet join/odečítacích operací z 2^n − 1 na nejvýše n a umožňuje počítat rezidua současně s agregacemi kostky. Podle autorů to přináší zrychlení zhruba 3–4×; samotné experimenty jsou ale jen v plné verzi [SAM98], ne v tomto článku. (s. 10, §4; s. 13, §4.1; s. 15, §5)
- C8: Omezení: při chybějících datech se rezidua podle Eq. 3 a Eq. 5 mohou lišit (Lemma 1 platí jen pro data bez chybějících hodnot); přesný least-squares fit by vyžadoval iterativní výpočet koeficientů, který autoři zamítají, protože vyžaduje více průchodů daty (často 10 a více). Implementace proto chybějící hodnoty při průměrování ignoruje. Jako budoucí práci autoři uvádějí výběr modelu a uživatelské přizpůsobení definice výjimky. (s. 12, §4.1; s. 15, §5)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování stran: PDF strana N = tištěná strana N + 167 (PDF 1–15 = s. 168–182 ve sborníku). V tvrzeních výše jsou PDF strany; při citaci v LaTeXu použij tištěné.
- Jde o zkrácenou verzi („abridged version“) technické zprávy [SAM98] (IBM RJ 10102). Výkonnostní experimenty, reálné datasety, práce s hierarchiemi a časem a řešení rovnice pro p jsou jen tam, v tomto textu ne.
- Fulltext je OCR ze skenu, ručně opravený proti PDF strana po straně. Vzorce (Eq. 1–5) jsou přepsané lineárně (ŷ_{i1...in}, γ^AB_ij, …). Tabulky z obr. 1–4 a diagramy obr. 6–7 ve fulltextu nejsou, tabulka obr. 5 ano. Znovu spuštěný pdf2txt.sh opravy přepíše.
- Prototyp: front-end Microsoft Excel s makry, backend Arbor Essbase (s. 3, §2).
