---
citekey: malinowskiOLAPHierarchiesConceptual2004
title: "OLAP Hierarchies: A Conceptual Perspective"
authors: "Malinowski, Elzbieta; Zimányi, Esteban"
year: 2004
venue: "Advanced Information Systems Engineering (CAiSE 2004), LNCS 3084, 477–491"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [olap, summarizability]
uroven: 3
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/QR7XMSIB)

## TL;DR
Autoři navrhují konceptuální klasifikaci hierarchií dimenzí v [[olap|OLAP]] (jednoduché symetrické, asymetrické a generalizované, vícenásobné a paralelní) s grafickou notací odvozenou z ER modelu. Striktnost chápou jako ortogonální vlastnost: hierarchie je nestriktní, pokud potomek může patřit k více rodičům (vazba M:N), a její instance pak netvoří strom, ale graf.

## Klíčová tvrzení
- C1: OLAP nástroje obvykle zvládají jen hierarchie, které zajišťují sumarizovatelnost nebo je lze transformovat tak, aby její podmínky platily; autoři proti tomu navrhují konceptuální přístup (rozšíření ER modelu) a klasifikaci hierarchií: hierarchie je množina binárních vztahů mezi úrovněmi; jednoduché (symetrické, asymetrické, generalizované vč. non-covering), vícenásobné (inkluzivní, alternativní) a paralelní (nezávislé, závislé), přičemž každá jednoduchá může být striktní nebo nestriktní. (s. 2, s. 4, s. 11, §1, §2, §2.5)
- C2: Hierarchie je nestriktní, má-li na úrovni schématu aspoň jednu kardinalitu M:N mezi rodičovskou a podřízenou úrovní (např. zaměstnanec v několika odděleních, týden patřící do dvou měsíců), striktní, jsou-li všechny 1:N; striktnost je ortogonální k typu hierarchie, instance tvoří graf a na logické úrovni ji lze řešit bridge tabulkou, převodem na striktní hierarchii nebo dimenzionální normální formou. (s. 7, §2.2)

## Vztah k mé práci


## Citovat pro


## Pozor
- Tištěné stránky = PDF strana + 476 (PDF s. 1 = tišt. 477). PDF je vyříznutá kapitola ze sborníku CAiSE 2004.
- Rozdělování míry mezi rodiče (symbol ÷) zavádějí jen pro vícenásobné inkluzivní hierarchie (s. 8, §2.3), ne pro nestriktní. U nestriktních hierarchií váhy ani dvojí započítání při roll-upu neřeší; bridge tabulku jen zmiňují s odkazem na Kimball [9] (s. 7). Váhy v bridge tabulce tímto článkem nedokládat.
- Převod hierarchií do relačního modelu a analýzu sumarizovatelnosti uvádějí jako budoucí práci (s. 14, §4); [[summarizability]] zde slouží jen jako motivace (s. 2).
- Tab. 1 (s. 12) se ve fulltextu rozpadla (symboly ±, ¥ a názvy hierarchií v jednotlivých modelech); konkrétní buňky ověřit v PDF. Text obrázků (s. 3–10) je rozházený, tvrzení stojí na běžném textu.
