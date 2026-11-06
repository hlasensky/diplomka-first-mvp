---
citekey: dobsonReferenceArchitectureModel2018
title: "A Reference Architecture and Model for Sensor Data Warehousing"
authors: "Dobson, Simon; Golfarelli, Matteo; Graziani, Simone; Rizzi, Stefano"
year: 2018
venue: "IEEE Sensors Journal 18(18), 7659–7670"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [olap, internet-of-things]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/YWCBFXBM)

## TL;DR
Autoři přenášejí techniky datových skladů a [[olap|multidimenzionálního modelování]] na data ze senzorových sítí a [[internet-of-things|IoT]]: navrhují referenční architekturu (stream/batch zpracování, data lake, ETL, datový sklad, OLAP) a doménový model, z něhož odvozují čtyři multidimenzionální schémata (měření, údržba, kontrola stavu, zpráva). Hlavním argumentem je, že dlouhodobá analýza senzorových dat vyžaduje ukládat i kontext (zařízení, kalibrace, údržba), jinak data svádějí k chybným závěrům.

## Klíčová tvrzení
- C1: Problém: hodnota senzorových dat plyne z trendů na dlouhých časových škálách, ale data musí být kontextualizována (detaily senzorů, instalace a provozu), protože stárnutí, dekalibrace či znečištění senzoru mění hodnoty v časové řadě a bez zaznamenaného kontextu se datová sada při analýze stává čím dál zavádějící; techniky datových skladů byly v senzorových sítích použity jen v omezené míře. (s. 1, §I; s. 2, §I)
- C2: Referenční architektura: události ze senzorové sítě se zpracují proudově nebo dávkově a uloží do data lake, odkud je periodický ETL přenáší do datového skladu dostupného BI uživatelům přes OLAP; architektura rozlišuje tři typy uživatelů (data scientist, BI uživatel, technik) a navrhuje implementaci na platformě Hadoop s Apache Kylin pro OLAP. (s. 3, §III-A; s. 4, §III-A; s. 5, §III-A)
- C3: Z doménového modelu odvozují v notaci DFM čtyři fakty – Measurement, Maintenance Operation, Status Check a Message; Measurement má míry Value a Accuracy a šest dimenzí (Measure Type s úrovní Unit, Sensing Time, Reception Time, Location, Agent, Transformation); logické zařízení (např. teplotní senzor v kuchyni) zůstává stejné i po výměně vadného fyzického senzoru. (s. 5, §III-B; s. 6, §IV; s. 7, §IV)
- C4: Případové studie: monitoring kvality ovzduší u průmyslového závodu (hvězdicové schéma s fiktivními ukázkovými daty, kontingenční tabulka spojující znečištění s počasím, drill-down na denní úroveň a počet dní od poslední kalibrace) a bezdrátová síť pro sledování sesuvů půdy ve střední Itálii (únor až říjen 2013). (s. 8, §V-A; s. 9, §V-A; s. 10, §V)
- C5: Model je ilustrován na dvou případových studiích; ukázková data ve scénáři kvality ovzduší jsou podle autorů fiktivní a autoři chtějí v budoucnu myšlenky důkladněji ověřit na reálných nasazeních. (s. 9, §V-A; s. 11, §VI)

## Vztah k mé práci


## Citovat pro


## Pozor
- Tištěné stránky = PDF strana + 7658 (PDF s. 1 = tišt. 7659).
- PAGE_WARN s. 6 a 9 (schémata DFM na obr. 3, hvězdicové schéma na obr. 4); tvrzení stojí na běžném textu.
- Technologická doporučení (Hadoop, Kylin, Storm) jsou z roku 2018; dnes spíš jako kontext.
- Ukázková data v obr. 4 (kvalita ovzduší) jsou podle autorů fiktivní; studie sesuvů vychází z reálného nasazení Giorgetti et al. Ani jedna studie není kvantitativní vyhodnocení modelu.
