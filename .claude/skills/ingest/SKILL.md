---
name: ingest
description: Turn papers into Obsidian source notes linked to concept notes, with automatic fulltext and claim verification. Use when asked to ingest, process or import papers/PDFs into the literature vault.
---

Work set: entries in thesis/projekt-20-literatura-bibliography.bib that have no literature/sources/<citekey>.md yet,
plus any PDF in literature/inbox/. If the user names specific citekeys, do only those.

PDF location: the entry's `file = {...}` field in projekt-20-literatura-bibliography.bib; otherwise match a PDF in
literature/inbox/ to an entry by title. A PDF with no bib entry: stop and report it. Never invent citekeys.

QC tool: `python3 literature/tools/litqc.py` (deterministic, no LLM). Reports land in literature/qc/.

**Before any paper:**
- `python3 literature/tools/litqc.py meta <citekeys>`: compares the bib entries with Crossref and Semantic Scholar.
  ERROR (bad DOI, retraction) or WARN PREPRINT_PUBLISHED / META_PAGES / META_YEAR / META_NO_VENUE: stop that paper
  and tell the user what to fix in Zotero. Fixing it there changes the citekey, so ingesting first would leave
  orphaned notes. Continue only when the user says the remaining warnings are fine.
- `python3 literature/tools/litqc.py plan`: pairs literature/seznam.md (the user's reading list) with the bib.
  The paper's `uroven` (level) decides the depth:

  | uroven | fulltext + OCR | claims | verifier |
  |---|---|---|---|
  | 1 | yes | 5–8: problem, method, results with numbers, limitations | yes |
  | 2 | yes | 3–5: method and key results | yes |
  | 3 | yes | 1–2: what the thesis cites it for (usually the abstract-level contribution) | yes |
  | nastroje | no (docs/datasets have no pages) | none; note with URL, version, access date in "Pozor" | no |
  | not in seznam | ask the user for the level before ingesting |

  Books: ingest only the chapters the list names (e.g. Hyndman ch. 2–3, 5); claims cite those pages.

Per paper (one writer subagent per paper when there are more than 3):

1. **Fulltext.** `literature/tools/pdf2txt.sh <pdf> literature/fulltext/<citekey>.txt`, then
   `python3 literature/tools/litqc.py fulltext <citekey> --repair`.
   This OCRs every PDF page independently and compares it with the pdftotext output page by page.
   Pages that are clearly broken get replaced by OCR text (marked `=== PAGE N === (OCR)`).
   - ERROR PAGE_BAD left: stop this paper and report it, do not write claims from a broken fulltext.
   - WARN PAGE_WARN (tables, formulas, columns): claims from that page must be checked against the OCR
     file or the PDF; mention the page under "Pozor".
   Work from the fulltext, not the PDF. Page numbers = the "=== PAGE N ===" markers (PDF pages; if the
   printed page numbers differ, note it under "Pozor").
2. **Note.** Create literature/sources/<citekey>.md from literature/_templates/source.md:
   - frontmatter from projekt-20-literatura-bibliography.bib; `status: candidate`, `verified: false`, `precteno: ne`
   - PDF line: append the attachment key to `zotero://open-pdf/library/items/`. The key is the
     8-character folder name in the `file` path (…/Zotero/storage/<KEY>/…). No Zotero file
     (PDF only in inbox/): delete the line.
   - TL;DR: 2–3 sentences in Czech, own words
   - 3–8 numbered claims (C1…), one line each, ending with `(s. N, §…)`; every page you cite must carry
     the evidence. Claims should cover: problem, method, key results with numbers, stated limitations.
     Keep numbers as in the paper (decimal comma is fine). State only what the paper says.
   - leave "Vztah k mé práci" and "Citovat pro" empty
   - `uroven`: run `python3 literature/tools/litqc.py plan --sync` after creating the note
3. **Concepts.** List literature/concepts/ first and link to existing notes where they fit
   (check aliases). Create a new concept note from _templates/concept.md only if nothing fits.
   Concept names: English, kebab-case (e.g. anomaly-explanation, text-to-sql).
   Add `[[concept]]` links to the source note's `concepts:` and to the body where relevant,
   and add the source with its relevant claim to each concept note's "Sources" list.
   If the new source disagrees with a source already listed in the concept (different result,
   definition or claim), add a line to the concept's "Napětí" section (create it above "Související"):
   `- [[a]] C2 vs. [[b]] C4: what differs`.
4. **Verify (writer ≠ reviewer).** Spawn a fresh subagent that did not write the note, with the
   instructions in .claude/skills/ingest/verifier.md and the citekey. Never verify your own claims.
5. **Fix loop (max 2 rounds).** Run `python3 literature/tools/litqc.py claims <citekey>`.
   For each claim that is not `supported` or has an error: rewrite it from the verifier's `fix` and the
   fulltext (correct page, number, wording) or delete it if the paper does not support it; renumber.
   Then spawn a fresh verifier again. After 2 rounds, leave remaining problems in the report.
6. `python3 literature/tools/litqc.py check <citekey>` → writes literature/qc/<citekey>.md and qc/_vault.md.
   Fix every vault ERROR you caused (broken links, concept backlinks).
7. If the PDF came from inbox/, leave it there and report it (the user will add it to Zotero).

Never set `verified: true`, `status: confirmed` or change `precteno`; that stays with the user, who now only has to check
claims the QC flagged plus a spot check.

Finish with a table: citekey | uroven | pages | OCR-repaired pages | warn pages |
claims (supported/total) | fix rounds | concepts linked | new concepts | QC verdict.
Then run `python3 literature/tools/litqc.py plan` and report how many list items are now done per level.
Then list newly created concept notes (for merging duplicates) and new "Napětí" lines.
