---
citekey: franciaCOOLFrameworkConversational2022
title: "COOL: A Framework for Conversational OLAP"
authors: "Francia, Matteo; Gallinucci, Enrico; Golfarelli, Matteo"
year: 2022
venue: "Information Systems 104, 101752"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [conversational-olap, text-to-sql, olap]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/XSMTNIMY)

## TL;DR
COOL překládá dialog v přirozeném jazyce na OLAP session: první dotaz je úplný GPSJ dotaz, další kroky jsou OLAP operátory (drill down, roll up, slice and dice, add, drop, replace) nad předchozím dotazem. Nepoužívá jazykový model – text mapuje na entity z automaticky naplněného metadata repository pomocí Levenshteinovy podobnosti, parsuje ho formální LL(1) gramatikou, kontroluje vůči multidimenzionálním omezením a nejednoznačnosti řeší automaticky, z logu nebo dotazem na uživatele. Na reálném benchmarku dosahuje přesnosti kolem 0,9 a v testu s 55 uživateli dopadli zkušení i nezkušení uživatelé podobně.

## Klíčová tvrzení
- C1: Problém [[conversational-olap]]: systém má převést rozhovor na OLAP session (sekvenci souvisejících dotazů), dávat zpětnou vazbu k opravě chybných dotazů a pamatovat si předchozí požadavky; autoři kladou 4 desiderata – automatizace a přenositelnost díky metadatům kostky, podpora sessions místo jednotlivých dotazů, robustnost vůči nepřesnostem uživatele a snadná konfigurace bez náročného ručního definování lexikonu. (s. 1, §1)
- C2: Offline fáze plní metadata repository (MR) automaticky dotazy nad DW a jeho datovým slovníkem (názvy měr, atributů a faktů, hodnoty kategoriálních atributů, hierarchie, povolené agregační operátory, tabulky a cizí klíče), přidává synonyma z WordNetu a volitelně ruční doplnění; MR obsahuje i doménově nezávislé entity (group by, where, select, operátory). (s. 2, §2.1; s. 3–4, §3)
- C3: Text se rozdělí na n-gramy, které se mapují na entity MR podobností založenou na normalizované Levenshteinově vzdálenosti s ohledem na permutace tokenů; počet kandidátních target sequences roste exponenciálně a omezují ho prahy α, β a top-N. Gramatika pro GPSJ dotaz (klauzule míry, group by a selekce, povinná je jen klauzule míry) je LL(1), jednoznačná a parsovatelná v lineárním čase; výsledný parse tree se přeloží na SQL (SELECT/WHERE/GROUP BY/FROM, joiny podle cizích klíčů, star i snowflake schéma) – autoři to označují jako [[text-to-sql]] přístup řízený gramatikou. (s. 1, §1; s. 4, §4; s. 5, §5.1; s. 10, §8)
- C4: Dialog má dva stavy: engage (očekává se úplný dotaz) a navigate (OLAP operátory upravují poslední dotaz uložený v Logu, dokud nepřijde reset). Gramatika OLAP operátorů definuje drill down, roll up, slice and dice, add, drop a replace; předchozí parse tree slouží jako kontext pro kontrolu a doplnění operátoru ([[olap]]). (s. 2, §2.2; s. 6, §5.2)
- C5: Parse forest se kontroluje vůči multidimenzionálním omezením a anotuje buď jako ambiguity (např. AA – hodnota patří do více atributů, AAO – míra má více agregačních operátorů, MV – nepovolená agregace míry, UC – nepřipojená klauzule), nebo jako error, který se jen oznámí uživateli. Nejednoznačnosti se řeší implicitně (jediné možné řešení z MR nebo předchozího dotazu), default-based (výchozí řešení v MR nebo nejčastější volba z logu nad prahem τ, zobrazená jako hint) nebo dotazem na uživatele podle šablon. (s. 7, §6, §6.1; s. 9–10, §7; s. 11, Tab. 4)
- C6: Benchmark: 110 ze 147 reálných analytických dotazů (75 %) odpovídá GPSJ; byly přemapovány na Foodmart (8,7·10^4 faktů) a SSB (6·10^6 faktů). Bez disambiguace je effectiveness (podobnost parse tree s ground truth) na Foodmartu 0,88–0,92 (podle N) a 0,86–0,92 (podle α), na SSB 0,88–0,90 a 0,88–0,92. Jen 58 ze 110 dotazů bylo bez nejednoznačnosti; s iterativní disambiguací roste effectiveness z 0,89 na 0,93 (Foodmart) a z 0,89 na 0,94 (SSB). Vyhledání entit přes BK-tree má složitost O(log(|MR|)); u SSB je nutné zvýšit α na 0,7, aby interpretace trvala řádově několik sekund. (s. 11, §9, §9.1; s. 13, §9.1.1–9.2)
- C7: Uživatelský test s 55 uživateli (16 bez znalosti OLAP, 39 se střední až velmi vysokou), jen nad schématem Foodmart, formal-based i goal-oriented úlohy: průměrná přesnost interpretace úplného dotazu ve formal-based testech je 0,94 pro obě skupiny; na konci goal-oriented session 0,87 (nezkušení) vs. 0,94 (zkušení); 79 % nejednoznačností COOL vyřešil správně automaticky (hint odpovídal volbě uživatele); čas na úplný dotaz (formulace uživatelem + interpretace) 141 s vs. 97 s. (s. 13, §9.3; s. 14, §9.3; s. 16, §9.3.3)
- C8: Omezení: srovnání s jinými NLIDB [7, 23, 24] (NaLIR, SQLizer, ATHENA) nebylo možné – implementace nejsou veřejné, datasety jsou s GPSJ sotva kompatibilní a některé vyžadují doménové ontologie; zbylé chyby plynou hlavně z nenalezených entit (příliš mnoho překlepů, chybějící synonymum v MR); účinnost log-based disambiguace by mohla klesnout, pokud by volby uživatelů byly méně konzistentní; speech-to-text a vizualizace výsledků jsou mimo rozsah článku. (s. 2, §2.2; s. 3, §2.2; s. 11, §9; s. 13, §9.1.2; s. 16, §9.3.3; s. 17, §10)

## Vztah k mé práci


## Citovat pro


## Pozor
- Stránkování: článek má číslo 101752, strany PDF 1–18 odpovídají tištěným stranám.
- PAGE_WARN s. 1, 6, 8 (shoda s OCR jen 0,7–0,75 na s. 6 a 8 – gramatika OLAP operátorů, Tabulka 2 a scoring). C4 cituje s. 6 – ověř v PDF. Tabulka 2 (anotace AA…UC) je v extraktu rozházená; definice anotací v C5 jsou z textu na s. 7.
- Strany 12 a 15 byly nahrazeny OCR (grafy obr. 11–14, obr. 18 a Tabulka 6 s výsledky uživatelského testu); Tabulka 6 je v extraktu nečitelná, čísla v C7 jsou z textu §9.3.3 na s. 16.
- Údaj „average accuracy of 94%“ je z abstraktu (s. 1); v §9 jsem nenašel, ze kterého měření přesně vzniká (0,94 se objevuje u SSB po disambiguaci, s. 13, a ve formal-based uživatelských testech, s. 16). Při citaci raději použij konkrétní čísla z §9.1.2.
- Předchozí verze: Francia, Gallinucci, Golfarelli, „Towards conversational OLAP“, DOLAP 2020 ([36]); tento článek ji rozšiřuje o OLAP operátory, log-based disambiguaci, vizuální rozhraní a uživatelské testy (s. 17, §10).
- Implementace v Javě, DW na Oracle 11g; Speech-to-text přes Web Speech API.
