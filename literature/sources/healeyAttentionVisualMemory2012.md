---
citekey: healeyAttentionVisualMemory2012
title: "Attention and Visual Memory in Visualization and Computer Graphics"
authors: "Healey, C. G.; Enns, J. T."
year: 2012
venue: "IEEE Transactions on Visualization and Computer Graphics"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [graphical-perception]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/G66GYYNW)

## TL;DR
Přehledový článek o výzkumu zrakové pozornosti a vizuální paměti z pohledu vizualizace. Shrnuje teorie preatentivního zpracování (které vizuální vlastnosti systém zachytí bez sériového hledání a proč konjunkce obvykle ne), hierarchii vlastností a jevy jako slepota ke změně či nepozornostní slepota. Závěrem ukazuje, jak tyto poznatky využít při volbě vizuálních kódování, zvýrazňování důležitých hodnot a směrování pozornosti.

## Klíčová tvrzení
- C1: Za preatentivní se obvykle považují úlohy, které lze na displejích s mnoha prvky provést za méně než 200–250 ms; protože zahájení sakády trvá nejméně 200 ms, divák úlohu zvládne jediným pohledem. Cíl s jedinečnou vizuální vlastností (např. červený kruh mezi modrými, nebo kruh mezi čtverci díky zakřivení) „vyskočí“ z displeje a je snadno detekovatelný bez ohledu na počet distraktorů. (s. 2 | tišt. 1171; §2)
- C2: Obr. 2 uvádí příklady vizuálních vlastností identifikovaných jako preatentivní: orientace, délka, uzavřenost, velikost, zakřivení, hustota, počet, odstín (hue), jas (luminance), průsečíky, zakončení čar, 3D hloubka, blikání, směr pohybu, rychlost pohybu a směr osvětlení. Některé vlastnosti jsou asymetrické (šikmá čára mezi svislými je preatentivní, svislá mezi šikmými ne). (s. 3, s. 4 | tišt. 1172, 1173; §2 Obr. 2, §3.1)
- C3: Cíl definovaný spojením dvou či více vlastností (konjunkce, např. červený kruh mezi červenými čtverci a modrými kruhy) většinou nelze najít preatentivně a divák musí displej sériově prohledat. Nízkoúrovňové procesy mohou ve vizualizaci přitáhnout pozornost k potenciálně zajímavým oblastem, ale ne ad hoc: vlastnosti přiřazené atributům musí odpovídat potřebám analýzy a nesmí vytvářet interferenční efekty (např. konjunkční hledání), které informaci zamaskují. (s. 2 | tišt. 1171; §2)
- C4: Existuje hierarchie vlastností: při detekci hranic zrak upřednostňuje barvu před tvarem – náhodné variace barvy zpomalí (ne zcela znemožní) vnímání tvarových vzorů, opačně interference nepůsobí; nalezeny jsou i preference jasu před odstínem a odstínu před texturou. Nejdůležitější atributy dat se proto mají zobrazovat nejvýraznějšími vlastnostmi. V experimentu autorů s glyfy náhodná variace textury neovlivnila detekci cílů podle odstínu, ale náhodná variace odstínu zhoršila detekci podle velikosti a hustoty. (s. 7, s. 14 | tišt. 1176, 1183; §3.7, §5.1.1)
- C5: Modely vidění se shodují, že vlastnosti barvy jsou preatentivní, ale neurčují, jak velký barevný rozdíl je potřeba pro rozlišitelné barvy (obecně u preatentivních vlastností nemusí určovat rozdíl potřebný pro rozlišitelné instance vlastnosti). Healeyho experiment s vizuálním hledáním ukázal, že divák dokáže rychle volit mezi nejvýše sedmi izoluminantními barvami. (s. 13 | tišt. 1182; §5, §5.1.1)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování: tištěná strana = PDF strana + 1169 (PDF 2 = tišt. 1171). Odkazy v tvrzeních jsou na strany PDF, tištěné za `|`.
- Přehledový článek: většina výsledků jsou zprávy o cizích studiích (např. Treisman, Callaghan, Healey [119]); při citaci konkrétního čísla zvaž primární zdroj.
- Fulltext bez PAGE_WARN a bez OCR náhrad. Popisky Obr. 2 (seznam preatentivních vlastností, s. 3) se v extraktu ztratily – ručně přepsané ve fulltextu (`[Fig. 2 – ruční přepis z PDF]`), soubor uzamčen a zkopírován do `healeyAttentionVisualMemory2012.corrected.txt`.
- Výsledky pocházejí z psychofyzikálních experimentů s umělými podněty (2012), ne s grafy časových řad; článek sám uvádí, že pro návrh vizualizací jsou nutné navazující experimenty (s. 13).
