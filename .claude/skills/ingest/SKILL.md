---
name: ingest
description: Turn papers into Obsidian source notes linked to concept notes. Use when asked to ingest, process or import papers/PDFs into the literature vault.
---

Work set: entries in thesis/projekt-20-literatura-bibliography.bib that have no literature/sources/<citekey>.md yet,
plus any PDF in literature/inbox/. If the user names specific citekeys, do only those.

PDF location: the entry's `file = {...}` field in projekt-20-literatura-bibliography.bib; otherwise match a PDF in
literature/inbox/ to an entry by title. A PDF with no bib entry: stop and report it. Never invent citekeys.

Per paper (one paper per subagent when there are more than 3):
1. `literature/tools/pdf2txt.sh <pdf> literature/fulltext/<citekey>.txt`
   Work from this file, not the PDF. Page numbers = the "=== PAGE N ===" markers
   (these are PDF pages; if the printed page numbers differ, note it under "Pozor").
2. Create literature/sources/<citekey>.md from literature/_templates/source.md:
   - frontmatter from projekt-20-literatura-bibliography.bib; `status: candidate`, `verified: false`
   - PDF line: append the attachment key to `zotero://open-pdf/library/items/`. The key is the
     8-character folder name in the `file` path (…/Zotero/storage/<KEY>/…). No Zotero file
     (PDF only in inbox/): delete the line.
   - TL;DR: 2–3 sentences in Czech, own words
   - 3–8 numbered claims (C1…), each with page and section, each verifiable by grep in the fulltext
   - claims should cover: problem, method, key results with numbers, stated limitations
   - leave "Vztah k mé práci" and "Citovat pro" empty
3. Concepts: list literature/concepts/ first and link to existing notes where they fit
   (check aliases). Create a new concept note from _templates/concept.md only if nothing fits.
   Concept names: English, kebab-case (e.g. anomaly-explanation, text-to-sql).
   Add `[[concept]]` links to the source note's `concepts:` and to the body where relevant,
   and add the source with its relevant claim to each concept note's "Sources" list.
4. If the PDF came from inbox/, leave it there and report it (the user will add it to Zotero).

Finish with a table: citekey | pages | claims | concepts linked | new concepts | problems.
Then list all newly created concept notes so the user can merge duplicates.
