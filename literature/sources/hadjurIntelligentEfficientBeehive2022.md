---
citekey: hadjurIntelligentEfficientBeehive2022
title: "Toward an Intelligent and Efficient Beehive: A Survey of Precision Beekeeping Systems and Services"
authors: Hadjur, Hugo; Ammar, Doreid; Lefèvre, Laurent
year: 2022
venue: Computers and Electronics in Agriculture 192, 106604
kind: journal
status: candidate
verified: false
precteno: ne
chapters: []
concepts:
  - hive-monitoring
  - internet-of-things
  - anomaly-detection
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/7D9XVP4F)

## TL;DR
Přehledový článek o precizním včelařství (precision beekeeping, PB), který prochází celý řetězec od hardwaru připojeného úlu (senzory, mikrokontrolér, síť, napájení) přes náklady a sběr dat až po modely strojového učení nad daty z úlů. U každé vrstvy hodnotí výhody a nevýhody řešení z literatury a upozorňuje na zkreslení krátkých a malých datových sad, nízkou reprodukovatelnost a kompromis mezi „inteligencí“ v úlu a spotřebou energie.

## Klíčová tvrzení
- C1: Přehled popisuje PB jako systémy a služby (senzory, sítě, zdroje napájení, sběr a využití dat, výkon služeb, udržitelnost z hlediska škálovatelnosti, efektivity a ceny), cituje 86 publikací včetně 7 jiných přehledů a na rozdíl od nich zahrnuje celý datový řetězec od návrhu systému a sběru dat po modely strojového učení; připojený úl ([[hive-monitoring]], [[internet-of-things]]) je ve všech pracích standardní úl se senzory připojenými k mikrokontroléru, napájený z baterie a obvykle připojený k síti, která posílá data na vzdálený server. (s. 1, s. 2, s. 3, §Abstract, §1.3, §2.1)
- C2: Profesionální včelaři, kteří používají technologie, se opírají o dvě hlavní kategorie metrik: váhu úlu (indikátor vývoje snůšky a kvetení) a vnitřní a vnější teplotu a vlhkost (sledování zdraví a vývoje včelstva); abnormální změny váhy mohou souviset s blížícím se rojením a nárůst vnitřní teploty lze korelovat s rojením, přičemž v zimě udržuje chumáč včel teplotu mezi 32 °C a 37 °C. (s. 2, s. 4, §1.3, §2.2)
- C3: Bibliometrická analýza prací, které používají data z úlů v modelu učení, rozlišuje osm kategorií služeb: počítání včel a odhad populace (13 prací), detekce a predikce rojení (13), detekce škůdců (5), produkce medu (4), klasifikace zdravotních stavů definovaných v každé práci jinak (10, vše kombinací teploty, vlhkosti, CO2 a srážek), detekce pylu (4, obraz), sledování (9, obraz) a detekce matky (5, audio); výzkum se zaměřuje na složitější data jako obraz a zvuk, zatímco existující instalace pro včelaře spoléhají na externí senzory jako váhy. (s. 9, §4.3.2, §4.4)
- C4: Pro detekci stavů úlu z teplotních a dalších dat přehled uvádí: fuzzy inferenční systém (Kviesis et al., 2020) nad vnitřní a okolní teplotou, jejich rozdílem, vývojem vnitřní teploty a ročním obdobím rozlišuje normální, abnormální stav a úhyn s F1-score 98 %; autoenkodéry ze dvou LSTM (Davidson et al., 2020) detekují všechna rojení, ale spouštějí je i jiné anomálie, hlavně zásahy včelaře (léčení varroázy, kontrolní prohlídka) ([[anomaly-detection]]); rozhodovací strom ID3 (Murphy et al., 2016) klasifikuje přes 95 % stavů správně, zatímco dřívější prahová metoda dosáhla na stejných datech nejvýše 89 %. (s. 14, §5.3)
- C5: Hlavní výzvou sběru dat pro statistické modely je zkreslení (bias): sebraná data obvykle pokrývají několik minut až několik dní a výzkum, který chce porozumět životu včel, musí zahrnout data alespoň za celý rok; pro nezkreslené a obecné výsledky je nutný sběr přes několik celých sezón z různých včelnic a přesné značení (labeling), přičemž většina projektů zatím není reprodukovatelná. (s. 7, s. 14, §4.1, §5.4, §6.2)

## Vztah k mé práci


## Citovat pro


## Pozor
- Úroveň 2 – přehledový článek; čísla v C3 a C4 jsou výsledky citovaných prací, jak je survey shrnuje, ne vlastní měření autorů. Pro konkrétní výsledek (např. F1 98 % u Kviesis et al., 2020) citovat ideálně primární zdroj.
- Čísla stran: PDF strany 1–16 odpovídají tištěným stranám v zápatí (1–16); článek má číslo 106604, takže tištěné stránkování je jen v rámci článku. V C1–C5 použity PDF strany.
- PAGE_WARN s. 1 (dvousloupcová titulní strana) – text abstraktu v C1 sedí s OCR (.ocr.txt).
- Text je dvousloupcový a místy rozházený (např. konec §2.2 a §2.3 na s. 5, §5.3/§6 na s. 13–15 se prolínají s referencemi); čísla v §4.3.2 (s. 9) a §5.3 (s. 14) zkontrolovat proti PDF.
- Obrázky: Fig. 1 (mapa), Fig. 2 (sloupcový graf) a Fig. 3 (koláčové grafy služeb a typů dat) jsou grafy, nevyřezávány; čísla k Fig. 3 jsou převzata z textu na s. 9.
- Další údaje mimo claims (nepřevzaté): 70 % (51 ze 73) prací o IoT systému nebo AI modelu neuvádí energii ani cenu (s. 5–6, §3); přehled sítí WPAN/LPWAN/celulární (s. 5, §2.3); prohlídky včelaře v průměru jednou týdně (s. 8, §4.2).
