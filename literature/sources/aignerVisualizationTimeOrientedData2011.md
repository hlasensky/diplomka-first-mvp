---
citekey: aignerVisualizationTimeOrientedData2011
title: "Visualization of Time-Oriented Data"
authors: "Aigner, Wolfgang; Miksch, Silvia; Schumann, Heidrun; Tominski, Christian"
year: 2011
venue: "Springer London, Human-Computer Interaction Series"
kind: book   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [time-series-visualization]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/GHQTKLBE)

## TL;DR
Monografie o vizualizaci časově orientovaných dat ([[time-series-visualization]]). Kapitola 3 systematizuje, jak modelovat čas (měřítko, rozsah, uspořádání, pohled, granularity, časové primitivy, neurčitost) a jak charakterizovat data vázaná na čas; kapitola 4 z toho staví rámec tří otázek co / proč / jak, podle kterého se navrhuje vizualizace. Zjednodušenou verzí tohoto rámce (data – čas – vis) pak kapitola 7 třídí rozsáhlý přehled technik.

## Klíčová tvrzení
- C1: Pro modelování času v informačních systémech neexistuje jediný správný model; autoři (podle Franka 1998 a Goralwally et al. 1998) popisují ortogonální návrhové aspekty času: měřítko (ordinální / diskrétní / spojité, přičemž diskrétní model s nejmenší jednotkou je v IS nejběžnější), rozsah (bodový / intervalový), uspořádání (lineární / cyklické) a pohled (uspořádaný / větvený / více perspektiv) ([[time-series-visualization]]). (s. 60, s. 61, s. 64–65 | tišt. 46, 47, 50–51; §3.1, §3.1.1, §3.1.1)
- C2: Čistě cyklická data (bez lineárního postupu času) jsou vzácná, mnohem běžnější jsou sériově periodická data (periodicita + lineární postup, např. měsíční průměry teplot za několik let). Na denních počtech případů chřipky autoři ukazují, že čárový graf ukáže špičky, ale cyklus jen naznačí, kdežto spirálová časová osa s délkou cyklu 28 dní odhalí týdenní vzor (s 24 dny ne) – kromě volby lineární/cyklické reprezentace je nutná i vhodná parametrizace. (s. 65, s. 98 | tišt. 51, 84; §3.1.1, §4.2.1)
- C3: Abstrakce času: granularity (žádná / jedna / více) jsou lidské abstrakce času (minuty, dny, týdny…); většina IS používá diskrétní model s nejmenší granularitou, jejíž nedělitelné jednotky (chronony) se seskupují do granulí, a systém granularit v mřížce tvoří kalendář; mapování mezi granularitami je pravidelné (sekundy → minuty) nebo nepravidelné (dny → měsíce). Časové primitivy jsou ukotvené (instant, interval) a neukotvený span; neurčitost (determinacy) vzniká při neúplné informaci o čase nebo při převodu mezi granularitami. (s. 67–68, s. 70, s. 74 | tišt. 53–54, 56, 60; §3.1.2, §3.1.2, §3.1.2)
- C4: Data vázaná na čas charakterizují měřítkem (kvantitativní / kvalitativní), referenčním rámcem (abstraktní / prostorová), druhem (události / stavy) a počtem proměnných (jednorozměrná / vícerozměrná; pro vícerozměrná data je metod výrazně méně). Podle vnitřního času (kdy informace platí) a vnějšího času (jak se datová sada vyvíjí) rozlišují statická netemporální, statická temporální (běžné časové řady, na které míří většina technik), dynamická netemporální (streamovaná data, hlavně monitorování) a dynamická temporální (bitemporální, např. denně doplňovaná zdravotní či klimatická data) – ta jsou mimo rozsah knihy. (s. 76–77, s. 78–79 | tišt. 62–63, 64–65; §3.2, §3.3)
- C5: Problém vizualizace strukturují třemi otázkami: co (čas a data), proč (úlohy uživatele) a jak (vizuální reprezentace); odpovědi na první dvě určují třetí a žádná technika nepokryje všechny aspekty času a dat najednou. „Jak“ dělí podle mapování času (čas → prostor = statická reprezentace, čas → čas = dynamická, např. animace; interakce na zařazení vliv nemá) a dimenzionality (2D / 3D). Přehled technik v kap. 7 používá zjednodušenou klasifikaci data (referenční rámec, proměnné) – čas (uspořádání, časové primitivy) – vis (mapování, dimenzionalita), podle níž jsou techniky seřazeny a v Tab. 7.1 lze hledat techniku pro zadaná kritéria. (s. 84, s. 90, s. 113, s. 160 | tišt. 70, 76, 99, 148; §4.1, §4.1.3, §4.3, §7–7.1)

## Vztah k mé práci


## Citovat pro


## Pozor
- Kniha (297 stran PDF); ingestovány jen části: kap. 3 „Time & Time-Oriented Data“ = PDF s. 59–82, kap. 4 „Visualization Aspects“ = PDF s. 83–117, úvod kap. 7 + začátek §7.1 (kategorizace technik, Tab. 7.1, první technika Point Plot) = PDF s. 159–164. Tvrzení z jiných částí knihy nejsou ověřená.
- Číslování: tištěná strana = PDF strana − 12 (PDF 161 = tišt. 149). Odkazy v tvrzeních jsou na strany PDF, tištěné za `|`.
- Strany 73, 75, 80, 91 jsou ve fulltextu nahrazené OCR (obrázky: relace mezi primitivy, neurčitost/PlanningLines, Obr. 3.31, statická mapování času Obr. 4.2).
- PAGE_WARN (obrázky/tabulky/sloupce): s. 62, 63, 67, 114, 163. C3 cituje s. 67 – text o granularitách ověřen proti OCR. Obr. 3.31 (s. 80) a Obr. 4.21 (s. 114) jsou nově ručně přepsané ve fulltextu (2026-11-05).
- Tab. 7.1 (s. 161–163, přehled technik a jejich zařazení) ztratila v extraktu všechna zaškrtnutí – kategorizaci konkrétních technik ověř v PDF.
- Kniha je z roku 2011: neobsahuje novější techniky ani nic o LLM. Dynamická temporální data (průběžně doplňované řady, typicky senzorová) výslovně nepokrývá (C4).

## Obrázky
- Obr. 3.31 (s. 80) – přehled návrhových aspektů času, dat a vztahu data–čas ![[figures/aignerVisualizationTimeOrientedData2011/fig3.31.png]]
- Obr. 4.21 (s. 114) – tři klíčové otázky vizualizace: co / proč / jak ![[figures/aignerVisualizationTimeOrientedData2011/fig4.21.png]]
