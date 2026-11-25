---
citekey: isenbergStudyDualScaleData2011
title: "A Study on Dual-Scale Data Charts"
authors: "Isenberg, P.; Bezerianos, A.; Dragicevic, Pierre; Fekete, Jean-Daniel"
year: 2011
venue: "IEEE Transactions on Visualization and Computer Graphics 17(12)"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [graphical-perception, time-series-visualization]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/YG5STV5G)

## TL;DR
Článek se zabývá grafy, které v jednom kartézském grafu kombinují dvě měřítka (rozlišení) jedné osy, aby zvětšily oblast zájmu (focus) a zachovaly kontext; nejde primárně o grafy se dvěma osami Y pro dvě různé veličiny. Autoři popisují prostor návrhu (bifocal, lens, broken, superimposed, cut-out) pomocí transformačních funkcí a v experimentu s 15 účastníky porovnávají čtyři takové grafy s běžným grafem na Clevelandových percepčních úlohách (pozice, délka, sklon). Nejlépe vychází cut-out graf (celý kontext + odděleně zvětšený focus), překrývaný (superimposed) graf vychází nejhůř a autoři doporučují ho nepoužívat.

## Klíčová tvrzení
- C1: Dual-Scale grafy podle autorů začleňují do jednoho grafu dvě různá datová rozlišení (měřítka, tj. počet datových jednotek na jednotku zobrazení), aby zdůraznily data v oblasti zájmu nebo umožnily porovnat data ze vzdálených oblastí; termín se často používá specificky pro překrývané grafy, autoři jím ale označují jakýkoli graf se dvěma hlavními měřítky a omezují se na grafy v ortogonálních 2D souřadnicích (čárové, sloupcové, plošné, bodové). (s. 1, Abstract, §1)
- C2: Překrývaný (superimposed) graf kreslí focus i kontext přes celou šířku grafu se společnou osou y a podle autorů se běžně používá, když dvě datové sady mají společnou jen jednu osu; jeho transformační funkce je nemonotónní a kódování hodnot nejednoznačné (možné překryvy a problémy s čitelností), výhodou je vyšší rozlišení než u ostatních variant (při zlomovém bodě uprostřed, jako v příkladech autorů, dvojnásobné pro stejnou plochu). (s. 4, §3.6)
- C3: Metoda: opakovaná měření s 15 účastníky (10 mužů, 5 žen), pět grafů (broken, cut-out, lens, regular jako základ, superimposed) se změnou měřítka na ose x, úlohy pozice, délka a sklon podle Clevelanda (odhad velikosti podnětu v procentech vůči referenčnímu objektu v datovém prostoru), tři zlomové body (ub = 2, 5, 10), 720 pokusů na účastníka, celkem 10 800; vyhodnocení ANOVA. (s. 6, §4.1; s. 7, §4.3, §4.4, §5)
- C4: U úlohy pozice (focus + context) byl běžný graf přesnější než všechny ostatní kromě cut-out a všechny grafy byly přesnější než superimposed; průměrné časy R 3,2 s, C 4 s, L 4,6 s, B 6 s, S 8,1 s. V dotazníku byl superimposed pro každou úlohu i umístění hodnocen jako poslední a cut-out jako první a u superimposed všichni účastníci uvedli, že si odpověďmi nejsou jistí. (s. 7, §5.1; s. 8, §5.4)
- C5: Autoři doporučují používat cut-out graf, jako alternativu broken graf (snadno vytvořitelný běžnými nástroji) a nepoužívat superimposed graf; jako omezení uvádějí, že testovali jen neinteraktivní grafy a nízkoúrovňové percepční úlohy a superimposed graf jen pro data výrazně odlišná v měřítku, nikoli pro data s různými jednotkami (u jiných variant předpokládají, ale neověřili, stejný výsledek). (s. 9, §6.3, §7, §8)

## Vztah k mé práci


## Citovat pro


## Pozor
- Žádná stránka nemá PAGE_WARN ani OCR opravu. Tabulka 1 (s. 6) ale v pdftotext ztratila znaky ✓ (zůstaly jen „—“), vlastnosti grafů z ní nečíst z fulltextu, jen z PDF.
- Číslování: značky `=== PAGE N ===` jsou stránky PDF; tištěné číslo = N + 2468 (s. 1 = tišt. 2469, s. 9 = tišt. 2477).
- Chybová metrika na s. 7 (§5) je ve fulltextu zkomolená („+ 18“ místo zlomku); vzorec brát z PDF.
- Experiment mění měřítko jedné proměnné na ose x (focus vs. kontext), ne dvě různé veličiny na dvou osách y; grafy se dvěma osami y pro různé jednotky výslovně netestuje (s. 9, §6.3 bod 3). Small multiples článek nezmiňuje.
