## Literature

Vault: `literature/` (Obsidian). One note per source: `literature/sources/<citekey>.md`.
Concept hubs: `literature/concepts/<concept>.md`. Fulltext with page markers: `literature/fulltext/<citekey>.txt`.
`thesis/projekt-20-literatura-bibliography.bib` is the only source of citekeys (Zotero auto-export, format "Better BibTeX", not BibLaTeX). Never edit it by hand.

Citing rules:
- Only cite keys that exist in projekt-20-literatura-bibliography.bib AND have a note with `status: confirmed` and `verified: true`.
- `candidate` or `verified: false`: may be proposed, but flag it explicitly as unverified.
- `rejected`: never cite or suggest. The note says why.
- Every \cite must map to a numbered claim (C1, C2…) in the note. If none fits, grep the fulltext.
  If it's not there either, say so. Never infer what a paper "probably" says.
- Never invent citekeys, page numbers, venues or authors.
- Before relying on a source, check `literature/qc/<citekey>.md` (run `python3 literature/tools/litqc.py check <citekey>`).
  A claim that is not `supported` there must not back a \cite; flag it.

Editing notes:
- You may create new source notes (always `status: candidate`, `verified: false`) and concept notes.
- Never change TL;DR, "Vztah k mé práci", `status`, `verified` or `precteno` in existing source notes. Those are mine.
- `precteno` (ne | abstrakt | uvod-zaver | prolet | cele) is how far I have read the paper. When proposing a source, mention it if it is `ne` or `abstrakt`.
