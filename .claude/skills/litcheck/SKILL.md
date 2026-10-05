---
name: litcheck
description: Audit citations in a thesis LaTeX chapter against the literature vault. Use when asked to check, verify or audit citations in .tex files.
---

For the given .tex file:
1. Extract every \cite{...} key together with the sentence it supports.
2. Run `python3 literature/tools/litqc.py check <all cited keys that have a note>` and read
   literature/qc/<key>.md for each.
3. For each key, read literature/sources/<key>.md and report:
   - MISSING: key not in projekt-20-literatura-bibliography.bib or no note
   - STATUS: note is not `confirmed` + `verified: true`
   - QC: literature/qc/<key>.md is FAIL (name the error codes)
   - UNSUPPORTED: no numbered claim matches the sentence. Then grep literature/fulltext/<key>.txt
     and give the best match (max 2 sentences, with page), or state that nothing was found.
   - OVERSTATED: a claim matches, but the sentence says more than the claim (stronger wording,
     other numbers, generalisation).
   - PAGES: the sentence cites pages (\cite[s.~X]{key}) that do not match the claim's printed pages
     (convert PDF → printed pages using "Pozor").
   The supporting claim must itself be `supported` in literature/qc/<key>.claims.json.
4. List sentences that make a factual or comparative claim about prior work but have no \cite.

Output a table: line | key | verdict | supporting claim. Do not edit the .tex file.
