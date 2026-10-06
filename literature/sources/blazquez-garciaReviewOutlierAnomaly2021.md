---
citekey: blazquez-garciaReviewOutlierAnomaly2021
title: "A Review on Outlier/Anomaly Detection in Time Series Data"
authors: "Blázquez-García, Ane; Conde, Angel; Mori, Usue; Lozano, Jose A."
year: 2021
venue: "ACM Computing Surveys 54(3), Article 56, 33 pp."
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [anomaly-detection]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/XWZL5VSZ)

## TL;DR
Přehledový článek o nesupervizované detekci odlehlých hodnot a anomálií v časových řadách. Navrhuje taxonomii podle tří os: typ vstupu (jednorozměrná/vícerozměrná řada), typ odlehlé hodnoty (bod, podsekvence, celá řada) a povaha metody (jednorozměrná/vícerozměrná), a podle ní třídí metody a dostupný software. Všechny metody podle autorů stojí na stejné myšlence: najít části řady, které se výrazně liší od očekávané hodnoty.

## Klíčová tvrzení
- C1: Pro odlehlé hodnoty v časových řadách neexistuje shoda v terminologii (anomálie, discords, exceptions, surprises…); autoři vycházejí z Hawkinsovy definice (pozorování tak odlišné, že vzbuzuje podezření na jiný generující mechanismus) a rozlišují dva účely: odstranit nežádoucí data (šum, chyby senzorů) vs. najít zajímavé události ([[anomaly-detection]]). (s. 2, §1)
- C2: Taxonomie metod má tři osy: typ vstupních dat (jednorozměrná vs. vícerozměrná řada), typ odlehlé hodnoty (bodová, podsekvence, celá časová řada) a povaha metody (jednorozměrná vs. vícerozměrná). (s. 4, §2; s. 5, §2.1–2.2; s. 6, §2.3)
- C3: Bodová odlehlá hodnota se vymyká buď všem hodnotám řady (globální), nebo sousedům (lokální); podsekvence je souvislý úsek, jehož společné chování je neobvyklé, i když jednotlivé body odlehlé být nemusí; celou odlehlou řadu lze najít jen ve vícerozměrných datech. Každá globální odlehlá hodnota je i lokální, ale ne naopak. (s. 5, §2.2; s. 6, §2.2)
- C4: Pro bodové odlehlé hodnoty v jednorozměrných řadách jsou nejběžnější model-based metody: bod je odlehlý, pokud |x_t − x̂_t| > τ. Estimation modely počítají očekávanou hodnotu z předchozích i následujících bodů, prediction modely jen z minulých, a proto je lze použít na streamovaná data; estimation modely jen tehdy, když nepoužívají budoucí body (k2 = 0). (s. 7, §3.1; s. 8, §3.1, Tab. 1)
- C5: Všechny přehledové metody podle autorů stojí na stejné myšlence – detekovat části řady (bod, podsekvenci, celou řadu), které se výrazně liší od očekávané hodnoty; výsledky silně závisí na volbě prahu a jen málo technik ho určuje automaticky, takže dynamická a adaptivní volba prahu je otevřený směr. (s. 27, §7)
- C6: Detekce bodových odlehlých hodnot je nejprozkoumanější úloha; podsekvence a celé řady se řeší méně. Nikdo neověřil, zda metody, které teoreticky umí rozhodnout při příchodu nového bodu, skutečně odpovídají v reálném čase; neexistují techniky pro periodické odlehlé podsekvence ve vícerozměrných řadách. (s. 29, §7)
- C7: Omezení vícerozměrné detekce: zobecnění jednorozměrných technik (např. density-based) na vektory nezohledňuje složité korelace mezi proměnnými, takže může přehlédnout pozorování, která vypadají normálně v každé proměnné, ale porušují jejich korelační strukturu; aplikace jednorozměrné techniky na každou proměnnou zvlášť korelace ignoruje a při mnoha proměnných je výpočetně náročná. Odlehlé hodnoty šířící se v čase mezi proměnnými podle autorů zatím literatura neřešila (alespoň ne pod názvem outlier/anomaly detection). (s. 29, §7)

## Vztah k mé práci


## Citovat pro


## Pozor
- Tištěné strany = 56:1–56:33 (article 56), odpovídají stranám PDF 1–33.
- PAGE_WARN s. 4 (obr. 2 s taxonomií); claim C2 cituje s. 4 jen pro text úvodu §2, samotný obrázek ověř v PDF.
- Přehled pokrývá literaturu 2000–2019 a jen nesupervizované metody; neobsahuje deep learning po roce 2019 ani LLM.
- Software (Tab. 9, s. 28) je v extraktu rozházený, odkazy ověř v PDF.
