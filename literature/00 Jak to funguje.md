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
| `fulltext/<citekey>.ocr.txt` | Nezávislé OCR každé strany PDF (tesseract), slouží jako kontrola fulltextu | `tools/litqc.py` |
| `qc/<citekey>.md` | Report kontroly: fulltext vs. OCR po stranách, ověření claims, verdikt PASS/FAIL | `tools/litqc.py`, needitovat |
| `qc/<citekey>.claims.json` | Výstup ověřovacího agenta: verdikt a doslovné citace z fulltextu ke každému claimu | ověřovací agent |
| `seznam.md` | Aktuální seznam literatury (úrovně). Při revizi nahraď celý text | ty |
| `qc/_plan.md` | Seznam × Zotero × vault: stav každé položky a souhrn podle úrovní | `tools/litqc.py plan` |
| `qc/_metadata.md` | Metadata ze Zotera porovnaná s Crossref a Semantic Scholar (DOI, rok, stránky, venue, preprint → publikovaná verze) | `tools/litqc.py meta` |
| `literatura.base` | Obsidian Bases: zdroje podle úrovně, neověřené | – |
| `qc/_vault.md` | Kontrola celého vaultu (bib, citekeye, odkazy koncept ↔ zdroj, rozbité `[[odkazy]]`) | `tools/litqc.py` |
| `inbox/` | PDF, která ještě nejsou v Zoteru | ty |
| `_templates/` | Šablony `source.md` a `concept.md` | – |
| `tools/pdf2txt.sh` | Převod PDF → fulltext se značkami stran | – |
| `tools/litqc.py` | Deterministické kontroly (bez LLM), viz níže | – |
| `../thesis/projekt-20-literatura-bibliography.bib` | Jediný zdroj citekeyů. Generuje ho Zotero, **ručně neupravovat** | Zotero (Better BibTeX) |

Fulltexty a PDF z inboxu jsou v `.gitignore` (autorská práva), do repa se necommitují.

## Postup pro nový zdroj

0. **Seznam:** zdroj má být v `seznam.md`. Párování jde přes DOI nebo název, ne přes číslo položky, takže přečíslování mezi revizemi nevadí. Když se nespáruje, doplň do položky DOI.
1. **Zotero:** přidej článek i s PDF. Zkontroluj, že má rok, venue a strany. Když metadata doplníš později, Better BibTeX může změnit citekey a poznámku pak bude potřeba přejmenovat.
   U preprintu (arXiv) použij v Zoteru pravým tlačítkem „Update to a published one“ (plugin zotero-arxiv-workflow).
2. **Export:** auto-export (formát „Better BibTeX“, ne BibLaTeX, „Keep updated“) zapíše záznam do bibu v `thesis/`.
3. **`/ingest`** (spusť Claude z kořene repa). Nejdřív zkontroluje metadata (`litqc.py meta`): když nesedí, zastaví se a řekne, co opravit v Zoteru. Opravy mění citekey, proto **metadata vždy před ingestem**. Hloubka zpracování se řídí úrovní v seznamu (1: 5–8 claims, 2: 3–5, 3: 1–2, nástroje: bez claims). Zpracuje záznamy z bibu, které ještě nemají poznámku, a PDF v `inbox/`. Pro konkrétní zdroje: `/ingest <citekey>`.
   - vytvoří fulltext a porovná každou stranu s nezávislým OCR; rozbité strany nahradí OCR textem
   - vytvoří source note (`status: candidate`, `verified: false`), TL;DR a 3–8 claims se stranou a sekcí
   - propojí zdroj s concept notes, případně založí nové; rozpory mezi zdroji zapíše do „Napětí“
   - **jiný** agent (ne ten, který claims psal) každý claim ověří a doloží doslovnými citacemi
   - `litqc.py` citace mechanicky zkontroluje (viz níže), nevyhovující claims se opraví (max. 2 kola)
   - výsledek je v `qc/<citekey>.md`
4. **Ty:** otevři `qc/<citekey>.md`. Při PASS stačí namátková kontrola, jinak řeš nalezené problémy. Projdi claims proti PDF (odkaz „otevřít v Zoteru“ nahoře v poznámce), vyplň „Vztah k mé práci“ a „Citovat pro“. Když sedí, přepni `verified: true` a `status: confirmed`.
5. **Psaní:** cituj jen `confirmed` + `verified: true`. Každý `\cite` má odpovídat konkrétnímu claimu.
6. **`/litcheck <soubor.tex>`:** zkontroluje citace v kapitole – chybějící klíče, neověřené zdroje, QC FAIL, věty bez opory v claims nebo silnější než claim a tvrzení bez citace. Soubor needituje.

## Automatická kontrola (`litqc.py`)

Co se kontroluje mechanicky, bez LLM:

- **Fulltext vs. PDF:** každá strana PDF se znovu přečte OCR a porovná s fulltextem (podíl shodných slov, pořadí slov, znaky `(cid:…)`/`�`, rozpalovaný text „t h a t“). BAD = fulltext je na straně rozbitý, WARN = tabulka/vzorec/sloupce, ověř v PDF.
- **Claims:** každá citace od ověřovatele musí doslova být ve fulltextu na uvedené straně **a** zároveň v OCR téže strany PDF. Strana důkazu musí patřit mezi strany citované v claimu. Každé číslo z claimu musí být na citovaných stranách.
- **Zastarání:** po ověření se uloží otisk (hash) každého claimu. Když claim později změníš, QC hlásí `CLAIM_STALE`. Pak spusť `/litverify <citekey>`.
- **Vault:** citekey existuje v bibu, odkaz do Zotera sedí s přílohou, `concepts:` ↔ Sources v konceptu oběma směry, Cn v konceptu existuje, žádné rozbité `[[odkazy]]`, osiřelé fulltexty.

`verified` a `status` dál přepínáš jen ty. QC jen zúží, co musíš kontrolovat ručně.

## Stavy poznámky

- `candidate` – navržený zdroj, zatím neověřený. Claude ho smí navrhnout, ale musí ho označit jako neověřený.
- `confirmed` – zdroj používáš a claims sedí.
- `rejected` – nepoužívat; v poznámce má být proč.
- `verified: true` – claims jsi sám ověřil proti PDF.

Jak daleko jsi paper četl (`precteno`, nová poznámka začíná na `ne`):

| hodnota | význam |
|---|---|
| `ne` | nečteno, znáš jen poznámku od Clauda |
| `abstrakt` | abstrakt (a případně TL;DR) |
| `uvod-zaver` | úvod a závěr, kostra článku |
| `prolet` | proletěno celé – nadpisy, obrázky, tabulky, výsledky |
| `cele` | přečteno celé |

Přehled po úrovních ze seznamu literatury je v `qc/_plan.md` (sloupce „čteno víc než abstrakt“ a „čteno celé“). QC upozorní, když je zdroj `confirmed`, ale `precteno` je jen `ne` nebo `abstrakt`.

TL;DR, „Vztah k mé práci“, `status`, `verified` a `precteno` v existujících poznámkách mění jen ty, Claude na ně nesahá.

## Claims a strany

- Formát: `C3: tvrzení … (s. 7, §3.1)`. Strana je **strana PDF** podle značek ve fulltextu.
- Když se tištěné strany liší, je převod v „Pozor“ (např. Sarawagi 1998: tištěná = PDF + 167). V LaTeXu cituj tištěné strany.
- U Vassiliadise je PDF arXiv long-version; claims mají obě čísla: `s. …` (arXiv) a `IS s. …` (časopis).
- Tabulky, grafy a vzorce bývají ve fulltextu rozbité – čísla ověřuj v PDF.

## Specifika a pasti

- **Fulltext Sarawagi 1998** je ručně opravené OCR, nastavené jen pro čtení, záloha je v `fulltext/…corrected.txt`. `pdf2txt.sh` i `litqc.py --repair` soubory jen pro čtení nepřepíšou.
- **DBLP API** je za anti-bot ochranou, skripty na něj nedosáhnou. `meta` proto používá Crossref (DOI), Semantic Scholar (venue, DBLP klíč, stránky) a jako zálohu OpenAlex. Odpovědi se cachují v `qc/.cache/` (gitignore).
- **betterbib** (aktuální verze) je placený a uzavřený, **rebiber** zná jen konference z DBLP snapshotu. Proto vlastní `meta`.
- **tesseract běží ve firejailu** bez přístupu do Zotera. `litqc.py` mu proto posílá obrázek strany přes stdin (`pdftoppm | tesseract stdin stdout`). OCR jednoho článku trvá zhruba 10–50 s a ukládá se do cache.
- **pdftotext běží ve firejailu.** Přístup do `~/Zotero/storage` (jen čtení) povoluje `~/.config/firejail/pdftotext.local`. Když extrakce hlásí „Couldn't open file“, zkontroluj tenhle soubor.
- **Změna citekeye** (např. po doplnění roku v Zoteru): přejmenovat source note a fulltext a opravit `[[odkazy]]` v concepts.
- **Neúplný bib záznam:** [[sarawagiExplainingDifferencesMultidimensional]] nemá v Zoteru rok ani venue.

## Příkazy

| Příkaz | Co dělá |
|---|---|
| `/ingest` | zpracuje všechny nové záznamy z bibu a PDF z `inbox/` |
| `/ingest <citekey>` | zpracuje jen zadané zdroje |
| `/litcheck <soubor.tex>` | audit citací v kapitole |
| `/litverify <citekey>` / `--all` | znovu ověří existující poznámky (OCR, ověřovací agent, QC); u `verified: true` jen navrhne opravy |
| `python3 literature/tools/litqc.py check --all` | celé QC bez LLM, přepíše reporty v `qc/` |
| `python3 literature/tools/litqc.py lint` | jen kontrola vaultu |
| `python3 literature/tools/litqc.py plan` | stav seznamu podle úrovní; `--sync` zapíše `uroven` do poznámek |
| `python3 literature/tools/litqc.py meta` | metadata v Zoteru proti Crossref a Semantic Scholar (bib nemění) |
| `literature/tools/pdf2txt.sh <pdf> <out.txt>` | ruční extrakce fulltextu |
