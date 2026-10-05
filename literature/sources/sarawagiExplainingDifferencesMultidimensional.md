---
citekey: sarawagiExplainingDifferencesMultidimensional
title: Explaining Differences in Multidimensional Aggregates
authors: Sarawagi, Sunita
year: 1999
venue: Proceedings of the 25th VLDB Conference, Edinburgh, pp. 42–53
kind: conference
status: candidate
verified: true
chapters: []
concepts:
  - olap
  - query-explanation
  - guided-data-exploration
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/P8FPTLFI)

## TL;DR
Článek zavádí OLAP operátor „diff“: analytik označí dvě agregované buňky (např. tržby 1990 vs. 1991) a systém jedním krokem vrátí krátký seznam řádků, které rozdíl nejlépe vysvětlují, místo ručního drill-downu. Odpověď kombinuje detailní i agregované řádky s poměrem změny a vybírá se informačně-teoreticky, tak aby příjemce co nejlevněji (v bitech) zrekonstruoval druhou podkostku z první. Hledá ji dynamické programování v jednom průchodu dat, integrované do ROLAP serveru.

## Klíčová tvrzení
- C1: Ruční hledání důvodů změny agregátu drill-downem je zdlouhavé a náchylné k chybám: typický [[olap]] dataset má 5–7 dimenzí s průměrně tříúrovňovými hierarchiemi a přes milion řádků. Autorka proto navrhuje jediný operátor „diff“, který vrátí shrnuté důvody poklesu nebo nárůstu mezi dvěma buňkami ([[query-explanation]]). Navazuje na předchozí práci o výjimkách [SAM98] = [[sarawagiDiscoverydrivenExplorationOLAP1998]]. (s. 1–2, §1)
- C2: Odpověď A je nejvýše N řádků (uživatel volí, typicky kolem tuctu) z detailní i agregovaných úrovní. Ke každému agregovanému řádku patří poměr r, který platí pro všechny jeho potomky, pokud nejsou v A uvedeni zvlášť. V příkladu IDC dat o softwaru vysvětluje pokles v „Rest of World“ 1990→1991 odpověď, jejíž první řádek říká, že po odečtení vyjmenovaných řádků tržby ve skutečnosti vzrostly o 10 %. (s. 2–3, §1.2; s. 3, §2; s. 4–5, §2.1)
- C3: Výběr A je formulován informačně-teoreticky: odesílatel posílá podkostku C_b příjemci, který zná C_a a A, a minimalizuje se počet bitů −log Pr[C_b | C_a, A] (Shannon). Pro počty se používá Poissonovo rozdělení, pro ostatní míry normální. Chybějící hodnoty se řeší zvlášť (Laplaceova korekce u Poissona). (s. 4–6, §2.1–2.1.2)
- C4: Oproti naivnímu „detail-N“ (N největších změn na detailní úrovni) je odpověď kompaktnější: v příkladu „Vertical Apps“ 1992→1993 vysvětluje detail-N jen asi 900 z celkového rozdílu cca 5000, kdežto odpověď diff přes 4500. (s. 3–4, §2)
- C5: Počáteční greedy algoritmus potřebuje tolik průchodů dat, kolik je N, a v některých častých případech nenajde optimum. Dynamické programování zpracuje data v jednom průchodu, je optimální za předpokladu správně odhadnutých poměrů (Lemma 3.1) a jeho paměť O(N·L·R) nezávisí na počtu řádků. (s. 6, §3.1; s. 7–9, §3.2, §4.1; s. 12, §5)
- C6: Prototyp běží jako stored procedure nad DB2/UDB (ROLAP) s Excel frontendem. Na OLAP Council benchmarku (1,36 mil. záznamů) zvládne i podkostku se čtvrt milionem záznamů zhruba za minutu. Samotný operátor zabere méně než 20 % času, zbytek je přístup k datům v databázi. (s. 9–11, §4; s. 12, §5)
- C7: Předpoklady a rozsah: operátor porovnává dvě agregované buňky kostky. Optimalita DP je zaručena při správně odhadnutých poměrech (Lemma 3.1, formulováno pro jednu dimenzi s hierarchií). U více dimenzí se úrovně předem seřadí podle B_ld, informačně-teoretické míry (počet bitů při shrnutí úrovně do rodiče), s cílem pořadí minimalizujícího celkový počet bitů. Experimenty měří proveditelnost a škálovatelnost (čas zpracování). (s. 3, §2; s. 9, §3.2.2–3.2.3; s. 10–12, §4.2)

## Vztah k mé práci


## Citovat pro


## Pozor
- Bib záznam je neúplný: chybí rok, venue i stránky. Rok 1999, VLDB Edinburgh a s. 42–53 jsou převzaté z PDF (patička s. 1) a z citace v [[franciaExplainingCubeMeasures2024]] [35]. Doplň je v Zoteru. Pozor: Better BibTeX pak nejspíš vygeneruje nový citekey (s rokem 1999); poznámku a fulltext bude potřeba přejmenovat.
- Číslování stran: tištěná strana = PDF strana + 41 (PDF 1–12 = s. 42–53). V claims jsou PDF strany.
- Tabulky a grafy (obr. 2–13, 16–18) jsou v extraktu rozházené, čísla ověřuj v PDF. Článek neuvádí, že vysvětlení tvoří jen řádky kostky (ne vztahy mezi mírami), ani že chybí uživatelské hodnocení kvality – to jsou vlastní pozorování (dříve v C7), patří do „Vztah k mé práci“.
- Cituje [[sarawagiDiscoverydrivenExplorationOLAP1998]] jako [SAM98] (s. 2 a reference). Samotný DIFF citují [[vassiliadisRollUpsDrillDownsIntentional2019]] ([3]) a [[franciaExplainingCubeMeasures2024]] ([35]).
