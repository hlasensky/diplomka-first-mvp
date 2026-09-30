---
name: litcheck
description: Audit citations in a thesis LaTeX chapter against the literature vault. Use when asked to check, verify or audit citations in .tex files.
---

For the given .tex file:
1. Extract every \cite{...} key together with the sentence it supports.
2. For each key, read literature/sources/<key>.md and report:
   - MISSING: key not in projekt-20-literatura-bibliography.bib or no note
   - STATUS: note is not `confirmed` + `verified: true`
   - UNSUPPORTED: no numbered claim matches the sentence. Then grep literature/fulltext/<key>.txt
     and give the best match (max 2 sentences, with page), or state that nothing was found.
3. List sentences that make a factual or comparative claim about prior work but have no \cite.

Output a table: line | key | verdict | supporting claim. Do not edit the .tex file.
