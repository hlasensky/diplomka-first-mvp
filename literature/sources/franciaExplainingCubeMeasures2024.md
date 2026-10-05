---
citekey: franciaExplainingCubeMeasures2024
title: "Explaining Cube Measures through Intentional Analytics"
authors: "Francia, Matteo; Rizzi, Stefano; Marcel, Patrick"
year: 2024
venue: "Information Systems 121, 102338"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
chapters: []
concepts: [intentional-analytics, query-explanation, interestingness, olap]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/GFKNRTBZ)

## TL;DR
Článek konkretizuje operátor explain z Intentional Analytics Modelu: na otázku „proč má míra m tyto hodnoty?“ systém spočítá několik modelů, které m vysvětlují pomocí jiných měr (polynomiální regrese, vícerozměrná lineární regrese, křížová korelace), a jako highlight ukáže ten nejzajímavější. Zavádí syntaxi intentions, spojování kostek (drill-across) a odvozené míry. Evaluace ukazuje odezvu pod sekundu až desítky sekund, detekci vložených vzorů a pozitivní hodnocení od 86 uživatelů.

## Klíčová tvrzení
- C1: [[intentional-analytics]] (IAM) má pět operátorů; describe a assess byly rozpracovány dřív, tento článek se zaměřuje na explain. Explain odpovídá na otázku „why does measure m show these values?“ a vysvětluje cílovou míru pomocí jiných měr kostky ([[query-explanation]]). (s. 1, §1)
- C2: Tři typy modelů: polynomiální regrese (Polyfit, stupeň se zvyšuje, dokud chyba na 30% testovací části klesá; pravidlo „one in ten“ – aspoň 10 faktů na parametr), vícerozměrná lineární regrese (Recursive Feature Elimination) a křížová korelace (posun s maximální absolutní Pearsonovou korelací; jen pro jednu úroveň intervalového typu, např. datum). (s. 4, §3; s. 5–7, §4.3–4.5)
- C3: Syntaxe: `with C1..Cp explain expr [as m] by l1..ln [for P] [against ...] [using t1..tz] [range b]`. Umožňuje odvozené míry (algebraické výrazy nad mírami) a spojení více kostek se sdílenou hierarchií, analogicky k drill-across. (s. 3, §2, Def. 6; s. 5, §4.1)
- C4: [[interestingness]] komponenty je v [0, 1]: u polynomiální i vícerozměrné regrese koeficient determinace R² (u polynomiální regrese se záporné R² mapuje na 0), u křížové korelace |ρ|. Highlight je komponenta s maximálním zájmem. Tři pravidla dominance (D.1–D.3) řeší komponenty různých modelů nesoucí stejnou informaci. Křížová korelace a R² se mohou lišit: pro unitPrice/unitCost je korelace 0,90, ale R² záporné. (s. 4, §3, Def. 9; s. 7–8, §4.6–4.7)
- C5: Efektivita: na kostce SALES z dat FoodMart (Intel i7, 8 GB RAM) trvá vysvětlení kostky s téměř 87 000 fakty méně než sekundu; na syntetické kostce s 10^6 fakty a 9 kandidátními mírami kolem 10 s. Vícerozměrná regrese škáluje kvadraticky s počtem měr, ostatní lineárně. Zápis intention je o 95 % kratší (v počtu znaků) než SQL dotaz plus Python kód modelů. (s. 9–10, §6.1)
- C6: Efektivnost: na syntetických datech s vloženými vzory explain vzory najde (posun 27 místo vložených 30 dní kvůli šumu a agregaci). Na reálných datech (odchyty ploštice Halyomorpha halys) je nejzajímavější komponentou třítýdenní zpoždění dospělců za velkými nymfami (zájem 0,9). (s. 10–11, §6.2.1–6.2.2)
- C7: Test s 86 uživateli (převážně magisterští studenti se znalostí BI) hodnotil zájem nabídnutých vysvětlení a jejich celkovou hodnotu na pětibodové Likertově škále; výsledky jsou podle autorů dobré. Uživatelé navrhovali spíš kvalitativní modely (např. „unitPrice je vždy vyšší než unitCost“), které autoři považují spíš za popis než vysvětlení. (s. 11, §6.2.3)
- C8: Omezení: vysvětluje se jen pomocí jiných měr, ne členů dimenzí. Místo „correlation“ autoři používají obecný termín „relationship“, protože correlation se ve statistice používá hlavně pro lineární vztahy. Budoucí práce: modely vysvětlující hodnoty členy dimenzí, jiné metriky zájmu (succinctness, interpretability, actionability). Přístup je chápán jako modulární rámec, do kterého lze zapojit jiné metody vysvětlení (DIFF, Scorpion, LensXPlain aj.). (s. 2, pozn. 1; s. 12, §7.2–7.4, §8; s. 13, §8)

## Vztah k mé práci


## Citovat pro


## Pozor
- Stránkování: článek má číslo 102338, strany PDF 1–13 odpovídají stranám v časopise.
- Přímo cituje [[vassiliadisRollUpsDrillDownsIntentional2019]] ([1], vize IAM) a [[sarawagiExplainingDifferencesMultidimensional]] ([35], DIFF) v related work §7.1–7.2. Předchozí verze explain je [8] (polynomiální regrese mezi dvěma mírami); describe a assess jsou v [2–4].
- Výsledky uživatelského testu (C7) jsou jen v grafech obr. 11–13, konkrétní čísla v textu nejsou. Tabulka 1 (časy) je v extraktu rozházená.
- Kód: https://github.com/big-unibo/explain (Python, scikit-learn, MySQL, D3).
