---
citekey: bachDashboardDesignPatterns2023
title: "Dashboard Design Patterns"
authors: "Bach, Benjamin; Freeman, Euan; Abdul-Rahman, Alfie; Turkay, Cagatay; Khan, Saiful; Fan, Yulei; Chen, Min"
year: 2023
venue: "IEEE Transactions on Visualization and Computer Graphics 29(1), 342–352"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [dashboard-design, time-series-visualization]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/KRQ6R5DR)

## TL;DR
Autoři kvalitativně okódovali 144 dashboardů a popsali 42 návrhových vzorů v osmi skupinách (obsah: datová informace, metainformace, vizuální reprezentace; kompozice: rozvržení stránky, využití plochy, struktura, interakce, barva) a šest žánrů dashboardů. Navrhují jednoduchý model [[dashboard-design|kompromisů při návrhu]] mezi abstrakcí, plochou obrazovky, počtem stránek a interakcí a vzory ověřili na dvoutýdenním workshopu s 23 účastníky. Cílem není říct, co je „dobrý“ dashboard, ale dát slovník a strukturu pro návrh.

## Klíčová tvrzení
- C1: Metoda: korpus 144 dashboardů (83 od Sarikaya et al., z nich 3 vyřazeny, plus 64 nových, z toho 36 k Covid-19) kódovali nezávisle tři autoři metodou konstantního srovnávání a schémata zpřesnili s dalšími třemi kodéry; interaktivní verze se kódovala u 61 %. Výsledkem je 42 vzorů v osmi skupinách: obsah (data information, meta information, visual representation) a kompozice (page layout, screenspace, structure, interaction, color). (s. 3, §3)
- C2: Četnosti obsahových vzorů v korpusu: detailní datová sada 94 %, jedna hodnota (např. poslední hodnota časové řady) 88 %, odvozené hodnoty 69 %, agregace 67 %, filtrování 42 %, prahy 21 %; z metainformací informace o aktualizaci s časovým razítkem 64 %/73 % a anotace 10 %, 9 % dashboardů nemá žádnou metainformaci; z reprezentací detailní vizualizace 88 %, čísla 62 %, tabulky 42 %, miniaturní grafy bez os (obdoba sparklines) 21 %, šipky trendu 13 %. (s. 3, §3.1)
- C3: Šest žánrů (dva nezávislí kodéři, neshoda u 32 dashboardů, tj. 22 %, vyřešena diskusí): statický 21 %, analytický 73 %, magazínový 2 %, infografický 6 %, repozitářový 17 % a vložený mini dashboard 4 %; analytický odpovídá Fewovu Faceted Analytic Display a používá úplné vizualizace a tabulky s explorací, navigací a drill-downem. (s. 5, §4; s. 6, §4)
- C4: Model kompromisů: dashboard kóduje menší datový prostor než zobrazovaná data; parametry abstrakce, plocha obrazovky, počet stránek a interaktivita se mají minimalizovat, ale snížení jednoho vyžaduje zvýšení jiného; na časové řadě 500 dní případů Covid-19 ukazují čtyři kódování (číslo, šipka trendu, miniaturní graf, detailní vizualizace), z nichž každé ztrácí informaci jinak. (s. 6, §5.1, obr. 6)
- C5: Dvoutýdenní workshop přes Zoom s 23 účastníky různého zaměření (asi polovina s předchozí zkušeností s Power BI/Tableau): častým tématem bylo přetížení informacemi („too much info“); jeden účastník (P1) uvedl, že vzory zúží návrh z nekonečných možností na 2–3 dobré kandidáty, jiný (P5) je použil jako kontrolní seznam. Omezení: vzory a jejich četnosti jsou reprezentativní pro analyzovaný korpus, sbírka vzorů je silně kvalitativní a cílem není doporučovat „dobré“ návrhy. (s. 7, §6; s. 8, §6.2.3; s. 9, §7.5)

## Vztah k mé práci


## Citovat pro


## Pozor
- Tištěné stránky = PDF strana + 341 (PDF s. 1 = tišt. 342). Odkazy v tvrzeních jsou PDF strany.
- Crossref vede early-access metadata (2022, s. 1–11); v Zoteru je finální vydání 2023, 29(1), 342–352 (litqc META_YEAR/META_PAGES – vědomě ponecháno). V bib je svazek 29 zapsán do pole `number` místo `volume` – opravit v Zoteru.
- Četnosti v C2 a C3 platí pro jejich korpus (silný podíl Covid-19 dashboardů), ne obecně.
- U metainformací první číslo = explicitní metainformace, druhé = včetně implicitně zřejmé z kontextu (s. 3).
- Podrobné popisy všech 42 vzorů jsou jen na webu https://dashboarddesignpatterns.github.io, ne v článku.
