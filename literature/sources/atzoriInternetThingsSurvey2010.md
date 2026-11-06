---
citekey: atzoriInternetThingsSurvey2010
title: "The Internet of Things: A survey"
authors: Atzori, Luigi; Iera, Antonio; Morabito, Giacomo
year: 2010
venue: Computer Networks (vol. 54, no. 15, pp. 2787–2805)
kind: journal
status: candidate
verified: false
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts:
  - internet-of-things
  - iot-protocols
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/3DZ8VDCE)

## TL;DR
Klasický přehledový článek o Internetu věcí z roku 2010. Vysvětluje, že pojem IoT vzniká sbíháním tří vizí („Things“, „Internet“ a „Semantic“), a probírá technologie, které ho umožňují: RFID, senzorové sítě a middleware postavený na SOA. Dále shrnuje aplikační domény a otevřené problémy, mezi něž patří standardizace, adresování, transportní protokol, QoS, bezpečnost a soukromí.

## Klíčová tvrzení
- C1: Základní myšlenkou [[internet-of-things]] je podle autorů všudypřítomnost různých věcí či objektů (RFID tagy, senzory, aktuátory, mobilní telefony), které díky jednoznačným adresovacím schématům navzájem interagují a spolupracují se sousedy na dosažení společných cílů. Sémanticky IoT znamená „celosvětovou síť propojených, jednoznačně adresovatelných objektů založenou na standardních komunikačních protokolech“ (převzato z [3]). Jako ústřední problémy autoři uvádějí plnou interoperabilitu zařízení, jejich autonomní chování, důvěru, soukromí a bezpečnost a také malé výpočetní a energetické zdroje věcí. (s. 1, s. 2, §1–2)
- C2: Nejasnost pojmu podle autorů plyne z názvu: „Internet“ vede k síťově orientované vizi, „Things“ k obecným objektům a otázky adresování, reprezentace a ukládání vyměňovaných informací přidávají třetí, „sémanticky orientovanou“ perspektivu. IoT je výsledkem konvergence těchto tří vizí (obr. 1). Vize „Things“ vychází z RFID a EPC (termín se přisuzuje Auto-ID Labs, které spolu s EPCglobal vyvíjejí EPC a průmyslové standardy pro EPCglobal Network). Vize „Internet“ je např. IPSO Alliance (IP pro chytré objekty, 6LoWPAN) a Internet 0. Sémantická vize řeší, jak reprezentovat, ukládat, propojovat, vyhledávat a organizovat informace generované IoT. (s. 2, s. 3, s. 4, §2)
- C3: Senzorové sítě podle autorů spolupracují s RFID při sledování stavu věcí (poloha, teplota, pohyb) a propojují fyzický a digitální svět. Tvoří je (i velmi velký) počet senzorových uzlů, které komunikují bezdrátově multi-hop a hlásí výsledky malému počtu uzlů (většinou jednomu), tzv. sinkům. Cílem návrhu je energetická efektivita, škálovatelnost, spolehlivost a robustnost. Většina komerčních WSN stojí na IEEE 802.15.4 (fyzická a MAC vrstva). Integraci do internetu ztěžuje nedostatek IP adres, malá velikost paketu (max. 127 bajtů na fyzické vrstvě, rámec MAC max. 102 oktetů) a to, že uzly velkou část času spí. (s. 4, s. 5, §3.1)
- C4: Middleware je softwarová vrstva mezi technologickou a aplikační úrovní, která programátora odstiňuje od detailů použitých technologií. Navrhované middleware pro IoT často vychází ze SOA. Obecně přijímaná vrstvená architektura podle autorů chybí, proto navrhují vlastní skicu (obr. 2) s vrstvami Applications (mimo middleware), Service composition, Service management (dynamické objevování objektů, monitorování stavu, konfigurace služeb) a Object abstraction (sjednocení přístupu k heterogenním zařízením přes rozhraní webových služeb). Napříč nimi vede správa důvěry, soukromí a bezpečnosti. (s. 5, s. 6, s. 7, §3.2)
- C5: Aplikace autoři dělí do čtyř domén: doprava a logistika, zdravotnictví, chytrá prostředí (domov, kancelář, závod) a osobní a sociální doména; k nim přidávají futuristické aplikace. Jako otevřené výzkumné problémy uvádějí (tab. 2) standardy, podporu mobility, pojmenování (naming), transportní protokol, charakterizaci provozu a QoS, autentizaci, integritu dat, soukromí a digitální zapomínání. TCP je podle nich pro IoT nevhodný kvůli navazování spojení, řízení zahlcení a bufferování dat, přičemž řešení zatím nikdo nenavrhl. (s. 7, s. 11, s. 14, §4, §5, §5.2)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování stran: PDF strana N = tištěná strana N + 2786 (PDF 1–19 = s. 2787–2805 v časopise). V tvrzeních jsou PDF strany, při citaci v LaTeXu použij tištěné.
- QC fulltextu: drobné PAGE_WARN jen na s. 1 (záhlaví, afiliace, abstrakt). C1 cituje úvod na s. 1 a text sedí.
- Tabulky 1 (s. 5, RFID vs. WSN vs. RSN), 2 (s. 11, otevřené problémy) a 3 (s. 12, standardy) mají ve fulltextu rozházené sloupce. Výčet problémů v C5 sedí, ale přiřazení příčin k jednotlivým problémům a hodnoty v tab. 1 a 3 ověř v PDF.
- Článek je z roku 2010. Stav standardů (RPL jako draft, nově založený ETSI M2M, 6LoWPAN drafty) a poznámka o docházejících IPv4 adresách (s. 13) odpovídají tehdejší situaci, cituj je jako historický kontext.
- V závěru (s. 17, §6) autoři zpochybňují trend přidělovat IPv6 adresu každému prvku IoT a jako možnou budoucnost uvádějí datově orientované sítě (data-centric networks). Jde o jejich výhled, ne o výsledek.
- Pro kapitolu o monitorování mohou posloužit ukázkové scénáře: monitorování podmínek (teplota, vlhkost, otřesy) u rychle se kazícího zboží (s. 8, §4.1.4) a událost při překročení prahu vibrací v průmyslovém závodě (s. 9–10, §4.3.2). Tvrzení k nim nejsou, při citaci nejdřív dopiš claim.

## Obrázky
- Obr. 1 (s. 3) – IoT jako průnik vizí „Things“, „Internet“ a „Semantic“ ![[figures/atzoriInternetThingsSurvey2010/fig1.png]]
- Obr. 2 (s. 6) – SOA architektura middleware pro IoT ![[figures/atzoriInternetThingsSurvey2010/fig2.png]]
