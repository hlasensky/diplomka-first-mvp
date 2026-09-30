---
type: guide
---

# Jak funguje literární vault

Vault drží poznámky ke zdrojům diplomky. Každé tvrzení, které v textu cituješ, má mít poznámku, číslované tvrzení (claim) a stranu v PDF, podle které ho ověříš.

## Co je co

| Složka / soubor | Co obsahuje | Kdo to píše |
|---|---|---|
| `sources/<citekey>.md` | Jedna poznámka na zdroj: frontmatter, odkaz na PDF, TL;DR, claims C1…, vztah k práci, „Pozor“ | Claude založí, ty doplníš a ověříš |
| `concepts/<pojem>.md` | Tematické huby (např. [[olap]], [[query-explanation]]) se seznamem zdrojů a claimů k pojmu | Claude, ty slučuješ duplicity |
| `fulltext/<citekey>.txt` | Text PDF se značkami `=== PAGE N ===`. Slouží Claudovi pro grep, v Obsidianu se nezobrazuje | `tools/pdf2txt.sh` |
| `inbox/` | PDF, která ještě nejsou v Zoteru | ty |
| `_templates/` | Šablony `source.md` a `concept.md` | – |
| `tools/pdf2txt.sh` | Převod PDF → fulltext se značkami stran | – |
| `../thesis/projekt-20-literatura-bibliography.bib` | Jediný zdroj citekeyů. Generuje ho Zotero, **ručně neupravovat** | Zotero (Better BibTeX) |

Fulltexty a PDF z inboxu jsou v `.gitignore` (autorská práva), do repa se necommitují.

## Postup pro nový zdroj

1. **Zotero:** přidej článek i s PDF. Zkontroluj, že má rok, venue a strany. Když metadata doplníš později, Better BibTeX může změnit citekey a poznámku pak bude potřeba přejmenovat.
2. **Export:** auto-export (formát „Better BibTeX“, ne BibLaTeX, „Keep updated“) zapíše záznam do bibu v `thesis/`.
3. **`/ingest`** (spusť Claude z kořene repa). Zpracuje záznamy z bibu, které ještě nemají poznámku, a PDF v `inbox/`. Pro konkrétní zdroje: `/ingest <citekey>`.
   - vytvoří fulltext a source note (`status: candidate`, `verified: false`)
   - napíše TL;DR a 3–8 claims se stranou a sekcí
   - propojí zdroj s concept notes, případně založí nové
4. **Ty:** projdi claims proti PDF (odkaz „otevřít v Zoteru“ nahoře v poznámce), vyplň „Vztah k mé práci“ a „Citovat pro“. Když sedí, přepni `verified: true` a `status: confirmed`.
5. **Psaní:** cituj jen `confirmed` + `verified: true`. Každý `\cite` má odpovídat konkrétnímu claimu.
6. **`/litcheck <soubor.tex>`:** zkontroluje citace v kapitole – chybějící klíče, neověřené zdroje, věty bez opory v claims a tvrzení bez citace. Soubor needituje.

## Stavy poznámky

- `candidate` – navržený zdroj, zatím neověřený. Claude ho smí navrhnout, ale musí ho označit jako neověřený.
- `confirmed` – zdroj používáš a claims sedí.
- `rejected` – nepoužívat; v poznámce má být proč.
- `verified: true` – claims jsi sám ověřil proti PDF.

TL;DR, „Vztah k mé práci“, `status` a `verified` v existujících poznámkách mění jen ty, Claude na ně nesahá.

## Claims a strany

- Formát: `C3: tvrzení … (s. 7, §3.1)`. Strana je **strana PDF** podle značek ve fulltextu.
- Když se tištěné strany liší, je převod v „Pozor“ (např. Sarawagi 1998: tištěná = PDF + 167). V LaTeXu cituj tištěné strany.
- U Vassiliadise je PDF arXiv long-version; claims mají obě čísla: `s. …` (arXiv) a `IS s. …` (časopis).
- Tabulky, grafy a vzorce bývají ve fulltextu rozbité – čísla ověřuj v PDF.

## Specifika a pasti

- **Fulltext Sarawagi 1998** je ručně opravené OCR, nastavené jen pro čtení, záloha je v `fulltext/…corrected.txt`. `pdf2txt.sh` na něj nespouštěj, přepsal by opravy.
- **pdftotext běží ve firejailu.** Přístup do `~/Zotero/storage` (jen čtení) povoluje `~/.config/firejail/pdftotext.local`. Když extrakce hlásí „Couldn't open file“, zkontroluj tenhle soubor.
- **Změna citekeye** (např. po doplnění roku v Zoteru): přejmenovat source note a fulltext a opravit `[[odkazy]]` v concepts.
- **Neúplný bib záznam:** [[sarawagiExplainingDifferencesMultidimensional]] nemá v Zoteru rok ani venue.

## Příkazy

| Příkaz | Co dělá |
|---|---|
| `/ingest` | zpracuje všechny nové záznamy z bibu a PDF z `inbox/` |
| `/ingest <citekey>` | zpracuje jen zadané zdroje |
| `/litcheck <soubor.tex>` | audit citací v kapitole |
| `literature/tools/pdf2txt.sh <pdf> <out.txt>` | ruční extrakce fulltextu |
