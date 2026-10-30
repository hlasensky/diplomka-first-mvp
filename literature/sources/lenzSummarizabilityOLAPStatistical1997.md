---
citekey: lenzSummarizabilityOLAPStatistical1997
title: Summarizability in OLAP and Statistical Data Bases
authors: Lenz, H.-J.; Shoshani, A.
year: 1997
venue: Proceedings. Ninth International Conference on Scientific and Statistical Database Management (pp. 132–143)
kind: conference
status: candidate
verified: false
precteno: ne
chapters: []
concepts:
  - summarizability
  - olap
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/IUWIYQDV)

## TL;DR
Článek formuluje, kdy je sumarizace (agregace přes dimenzi nebo hierarchii) v OLAP a statistických databázích korektní. Statistický objekt se nejdřív popíše ve třech krocích (mikrodata, prvky objektu, hierarchie z funkčních závislostí) a nad ním autoři definují tři nutné podmínky: disjunktnost, úplnost a typovou kompatibilitu míry, dimenze a funkce. Postačitelnost podmínek jen neformálně zdůvodňují a upozorňují, že ani splněné podmínky nechrání před Simpsonovým paradoxem při analýze závislostí.

## Klíčová tvrzení
- C1: [[summarizability]] označuje podmínky, za kterých dává sumarizační operace nad vícerozměrnými daty ([[olap]], statistické databáze) správný výsledek. Nesprávná a ne vždy zjevná sumarizace vede k chybné analýze a rozhodnutím, proto je podle autorů nutné uživatele upozornit, když se pokouší o nesumarizovatelnou operaci. Sumarizovatelnost platí vůči některým dimenzím a vůči jiným ne a závisí na typu míry i na sumarizační funkci. (s. 1–2, §1)
- C2: Ilustrační příklad: počet postgraduálních studentů podle katedry a roku při dvouletém studiu. Součet za tři roky 15+17+13=45 je chybný, skutečný počet studentů informatiky je 15+2+11=28. Míra „počet studentů“ je typu stock a přes rok sumarizovatelná není, kdežto počet studentů prvního ročníku (flow) ano; přes katedry sčítat lze, dokud neexistuje společný program dvou kateder (pak se student počítá dvakrát). U nesumarizovatelných měr lze součty získat jen z mikrodat. (s. 2–3, §2.1–2.2)
- C3: Metoda: statistický objekt se definuje ve třech krocích. (1) rámec mikrodat: třída objektů, jejich atributy a textový popis; (2) prvky objektu: summary attribute (míra), category attributes s výčtem hodnot, statistická funkce přiřazená objektu (nesmí být „null“) a implicitní kategoriální atributy; (3) analýza funkčních závislostí mezi kategoriálními atributy, která určí, co tvoří nezávislé dimenze vícerozměrného prostoru a co klasifikační hierarchie (např. month → year, county → state). (s. 4–7, §3.1–3.3)
- C4: Podmínka 1, disjunktnost: kategoriální atributy musí dělit jednotlivce/objekty do disjunktních podmnožin (student patří jen do jedné katedry). U listových uzlů se testuje vůči mikrodatům, u nelistových vůči uzlu pod nimi; porušením jsou např. nejednoznačná jména měst napříč státy, řešitelná přejmenováním (Rome-NY). Test lze provést ze sémantické znalosti nebo přímo nad daty, datový test ale platí jen pro aktuální data. (s. 7–8, §4.1)
- C5: Podmínka 2, úplnost: sjednocení shluků musí pokrýt všechny jednotlivce/objekty a každý musí být přiřazen do nějaké kategorie. Úplnost závisí na míře: hierarchie město → stát je neúplná pro „počet smrtelných nehod“ (státy zahrnují i venkov), ale úplná pro „počet muzeí“, pokud muzea existují jen ve městech. Neúplnost se v praxi řeší umělou kategorií „other“ nebo „unknown“. (s. 3–4, §2.3; s. 8–9, §4.2)
- C6: Podmínka 3, typová kompatibilita: kombinace typu míry (flow, stock, value-per-unit), typu kategoriálního atributu (temporální, netemporální) a statistické funkce musí být sumarizovatelná. Podle tabulek (Fig. 7–8) je sum nepřípustný pro stock přes čas a pro value-per-unit v obou případech; min, max, avg a range jsou přípustné všude, přičemž avg vyžaduje nést s sebou count a range hodnoty min a max. Flow a stock se rozlišují podle toho, co se zaznamenává (kumulativní efekt za období vs. stav v okamžiku), ne kdy. (s. 9–10, §5, §5.1)
- C7: Průměr nelze sumarizovat z předchozích průměrů, ale je sumarizovatelný, pokud se nese součet a počet; obdobně směrodatná odchylka (součet čtverců, součet, počet) a obecně každá statistika vyjádřitelná komponentními agregáty. Medián, percentily a trimmed mean jsou ze své podstaty nesumarizovatelné a musí se počítat z mikrodat; přístup k výběru předpočítaných agregací [1] podle autorů platí jen pro objekty sumarizovatelné vůči všem kategoriálním atributům. (s. 4, §2.4; s. 10, §5.1)
- C8: Omezení: i při splnění všech tří podmínek může sumarizace přes atribut zkreslit strukturu závislostí zbylých atributů (Simpsonův paradox). V příkladu (pohlaví × rok × věková skupina) podíl mužů roste v obou věkových skupinách (4/7 < 8/13, 2/5 < 12/27), po sečtení přes věk je ale v obou letech 1/2; je proto nutné kontrolovat podmínky kolapsibility. Postačitelnost tří podmínek autoři formálně nedokazují, jen ji neformálně zdůvodňují. (s. 10–11, §6; s. 11–12, §7)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování stran: PDF strana N = tištěná strana N + 131 (PDF 1–12 = s. 132–143 ve sborníku). V tvrzeních jsou PDF strany; při citaci v LaTeXu použij tištěné.
- Fulltext je dvousloupcový text s promíchaným pořadím odstavců (pdftotext); QC nehlásilo PAGE_WARN ani PAGE_BAD. Tabulky Fig. 7–10 (s. 10–11) byly z textu ztracené a jsou do fulltextu ručně přepsané z PDF (blok `[Fig. N – ruční přepis z PDF]`). Tabulky Fig. 1–3 a schémata Fig. 5–6 ve fulltextu nejsou; čísla v C2 pochází z textu §2.1.
- Abstrakt v bib i v PDF obsahuje OCR/tiskové chyby („is m a extremely“, „WE defined“) – necitovat doslovně.
- Pojmy „stock“, „flow“, „value-per-unit“ odpovídají v dnešní terminologii zhruba semi-aditivní / aditivní / neaditivní míře; tuto korespondenci ale článek sám neuvádí.

## Obrázky
- Obr. 4 (s. 7) – statistický objekt v grafové notaci (S/X/C uzly); vliv funkční závislosti dealer → county na dimenze vs. hierarchie ![[figures/lenzSummarizabilityOLAPStatistical1997/fig4.png]]
- Obr. 7–8 (s. 10) – tabulky sumarizovatelnosti podle funkce a typu míry, temporální a netemporální ![[figures/lenzSummarizabilityOLAPStatistical1997/fig7-8.png]]
