---
citekey: romeroNeedReferenceAlgebra2007
title: "On the Need of a Reference Algebra for OLAP"
authors: "Romero, Oscar; Abelló, Alberto"
year: 2007
venue: "Data Warehousing and Knowledge Discovery (DaWaK 2007), LNCS 4654, 99–110"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [olap, summarizability]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/PLSE4WMD)

## TL;DR
Autoři porovnávají multidimenzionální algebry z literatury vůči vlastní referenční sadě [[olap|OLAP]] operátorů (Selection, Roll-up/Drill-down, ChangeBase, Drill-across, Projection, množinové operace) a hledají jejich společné jádro. Ukazují, že toto jádro lze vyjádřit jako omezenou podmnožinu relační algebry, a proto má smysl mít nad relační databází multidimenzionální sémantickou vrstvu.

## Klíčová tvrzení
- C1: Problém: multidimenzionalita je přijímána jako nejlepší řešení konceptuálního modelování datového skladu, ale chybí shoda na sadě operátorů pro práci s multidimenzionálními daty; referenční sada operátorů by pomohla s metodikami návrhu, indexováním a optimalizací dotazů. (s. 1, §1)
- C2: Referenční rámec: struktury Dimension, Level, Descriptor, Fact, Cell, Measure, Base, Cube a Star a sada operací, o níž uvádějí, že je uzavřená, úplná a minimální – Selection, Roll-up (Drill-down jen po předchozím Roll-upu), ChangeBase, Drill-across, Projection a množinové operace (Union, Difference, Intersection). (s. 2, §2)
- C3: Srovnání algeber z literatury (tab. 1) ukazuje společné jádro: Selection, Roll-up a Drill-down obsahuje každá algebra, Projection, Drill-across a množinové operace většina a ChangeBase je ve většině zastoupen částečně. (s. 3, §3, tab. 1; s. 10, §5)
- C4: Převod na relační algebru: Selection odpovídá relační selekci omezené na deskriptory, Projection projekci omezené na míry, Roll-up operaci „group by“ spolu s „aggregation“ z rozšířené grupovací algebry a Drill-across spojení dvou tabulek přes společnou bázi; neomezený kartézský součin nemá multidimenzionální smysl. (s. 7, §4; s. 8, §4; s. 9, §4)
- C5: Multidimenzionální algebra je vlastní podmnožinou relační algebry: manipulace celou relační algebrou nemusí dát kostku (relační algebra není vůči multidimenzionálnímu modelu uzavřená) nebo zavede problémy s agregací, což podle autorů zdůvodňuje sémantickou vrstvu nad RDBMS. (s. 7, §4; s. 10, §5; s. 11, §6)

## Vztah k mé práci


## Citovat pro


## Pozor
- Tištěné stránky = PDF strana + 98 (PDF s. 1 = tišt. 99). PDF je vyříznutá kapitola ze sborníku DaWaK 2007 (původně celý sborník, záznam songDataWarehousingKnowledge2007).
- Tab. 1 (s. 3) a tab. 2 (s. 8) se ve fulltextu rozpadly (symboly ✓, ∼, p, +, D); tvrzení stojí na běžném textu, konkrétní buňky ověřit v PDF.
- Uzavřenost, úplnost a minimalitu sady operátorů autoři jen uvádějí s odkazem na svou dřívější práci [5], v tomto článku ji nedokazují.
- Problémy s agregací (zachování disjunktnosti) autoři dokládají vlastní dřívější prací [18] (Romero & Abelló, JISBD 2005), ne Lenz & Shoshani; pojmově souvisí se [[summarizability]].
- C3 „každá algebra obsahuje Roll-up“ je shrnutí autorů v §5 (s. 10); v §3 (s. 7) sami uvádějí, že algebra [16] Roll-up jako operátor nemá (je součástí datové struktury). Při citaci připsat autorům.
- „Sémantická vrstva“ (s. 7) v článku znamená multidimenzionální algebru nad relační, ne samostatnou softwarovou vrstvu jako v mém enginu – nepřekrucovat.
