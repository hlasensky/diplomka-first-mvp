---
citekey: bunemanWhyWhereCharacterization2001
title: "Why and Where: A Characterization of Data Provenance"
authors: Buneman, Peter; Khanna, Sanjeev; Tan, Wang-Chiew
year: 2001
venue: Database Theory — ICDT 2001 (LNCS vol. 1973, pp. 316–330)
kind: conference
status: candidate
verified: false
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts:
  - data-provenance
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/LBR2KF98)

## TL;DR
Článek formalizuje provenienci dat vzniklých dotazem nad databází a rozlišuje dva její významy: why-provenance (která zdrojová data dokládají, že se hodnota ve výstupu vůbec objevila) a where-provenance (ze kterého místa ve zdroji byla konkrétní hodnota zkopírována). Obojí počítá syntakticky z dotazu v deterministickém modelu semistrukturovaných dat, kde má každá hodnota jednoznačnou cestu. Why-provenance je invariantní vůči přepisu dotazu, where-provenance jen pro omezenou třídu „traceable“ dotazů.

## Klíčová tvrzení
- C1: Problém: [[data-provenance]] („lineage“, „pedigree“) je popis původu dat a procesu, kterým se dostala do databáze; článek řeší, které části databáze D přispěly k hodnotě d v pohledu V = Q(D) vytvořeném dotazem Q. Klíčová otázka je, co znamená „přispěly“. (s. 1, Abstract, §1; s. 2, §1)
- C2: Autoři rozlišují why-provenance (proč je hodnota ve výstupu) a where-provenance (odkud hodnota pochází, vyžaduje identifikovat lokace ve zdrojových datech). V příkladu SELECT name, telephone … WHERE salary > průměrná mzda k existenci n-tice ("John Doe",1234) přispěla každá n-tice relace employee, kdežto telefonní číslo pochází jen z pole telephone n-tice „John Doe“. Where-provenance je podle autorů důležitá pro dohledání zdroje chyb a pro přenos anotací přes dotazy; dosud ji nikdo nestudoval. (s. 2, §1)
- C3: Metoda: deterministický model semistrukturovaných dat, v němž je každý uzel jednoznačně určen cestou hranových popisků (relace se kódují klíči jako popisky hran), a dotazovací jazyk DQL tvaru „where … collect …“ s operací deep union. DQL zachytí pozitivní (SPJU) relační dotazy a pozitivní vnořenou relační algebru; každý well-formed dotaz má normální formu a přepisovací systém R je silně normalizující (Theorem 1). (s. 3, §2; s. 6, §3; s. 7, §3)
- C4: Why-provenance je definována přes svědka (witness): hodnota s ⊑ D, pro kterou platí t ⊑ Q(s). Witness basis se odvozuje ze syntaxe dotazu (deep union vzorů z klauzule „where“ pro valuace, které vytvoří t) a algoritmus Why(t, Q, D) generuje dotaz, který po vyhodnocení nad D vrátí přesně witness basis (Theorem 2, soundness and completeness). Pro SPJU dotazy se witness basis shoduje s odvozením n-tice v práci Cui a Widom [7]. (s. 8, §5; s. 9, §5.1; s. 10, §5.1)
- C5: Witness basis není invariantní vůči ekvivalentním dotazům, ale minimal witness basis ano – pro ekvivalentní well-formed dotazy pouze s podmínkami rovnosti (Theorem 3), s rozšířením na některé podtřídy s nerovnostmi. Witness basis přes materializované pohledy je stejná jako po „composing out“ pohledů z dotazu (Theorem 4). (s. 10, §5.2; s. 11, §5.2–5.3)
- C6: Where-provenance je cesta ve vstupních datech, ze které výstupní hodnota pochází (např. Composers.{name:"G.F. Handel"}.born). Je definována jen tehdy, když lze hodnotu spojit s proměnnou ve výstupním výrazu dotazu; konstantu „zadrátovanou“ do dotazu autoři připisují samotnému dotazu. Obecně where-provenance není invariantní vůči ekvivalentním dotazům a syntaktická struktura dotazu k jejímu určení nemusí stačit. (s. 11, §6; s. 12, §6)
- C7: Pro omezenou třídu traceable dotazů (poddotazy jsou pohledy bez sdílených proměnných s vnějším dotazem, proti poddotazu smí být jen singulární vzor z různých proměnných) se where-provenance (derivation basis) při přepisu zachovává (Proposition 2) a stačí ji počítat z normální formy. Procedura Where(l:v, Q, D) generuje dotaz se stejnou klauzulí „where“ jako Q, jehož „collect“ vrací vzory (witness) a cesty k proměnné, která hodnotu vytvořila. (s. 13, §6; s. 14, §6, Def. 9)
- C8: Omezení: rámec popisují autoři v kontextu SPJU dotazů a pohledů; DQL neumí cesty s Kleeneho hvězdou a funguje jen nad hierarchickými strukturami. Nevědí o sémantické charakterizaci where-provenance ani why-provenance mimo SPJU; čistě syntaktická charakterizace where-provenance podle nich pravděpodobně nebude úplná. Budoucí práce: podmínky pro well-defined dotazy a využití omezení (např. funkčních závislostí) pro úplnější where-provenance. (s. 2–3, §1; s. 7, §3; s. 12–13, §6; s. 14–15, §7)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování stran: PDF obsahuje jen tuto kapitolu (15 stran). PDF strana N = tištěná strana N + 315 (PDF 1–15 = s. 316–330 ve sborníku LNCS 1973). V tvrzeních výše jsou PDF strany; v LaTeXu cituj tištěné.
- Bib uvádí třetí autorku jako `{Wang-Chiew}, Tan` (příjmení a jméno v Zoteru prohozené); v PDF je „Wang-Chiew Tan“. Opravit v Zoteru.
- Teoretický článek bez experimentů a bez numerických výsledků; důkazy, přepisovací systém R a převod XML/XML-QL autoři odkládají do plné verze (s. 5, s. 7, s. 10).
- Formální rámec (DQL) je definován pro SPJU dotazy; agregacemi se článek kromě úvodního příkladu s AVERAGE (s. 2), který jen ilustruje rozdíl why/where, nezabývá. Pro agregované OLAP odpovědi je to tedy koncepční opora rozlišení, ne hotový algoritmus.
- Ve fulltextu je operace deep union (⊔) přepsaná jako „t“ a ⊑ jako „v“/„@“; vzorce a Definice 6–8 ověřuj v PDF. Fulltext prošel OCR kontrolou bez ERROR i WARN.
