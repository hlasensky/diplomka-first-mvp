---
name: litverify
description: Re-verify existing literature source notes - fulltext vs. OCR check and independent claim verification with litqc. Use when asked to verify, re-check or QC existing notes in the literature vault.
---

Work set: the citekeys given, or all literature/sources/*.md for `--all`.

Per citekey:
1. `python3 literature/tools/litqc.py fulltext <citekey>` (OCRs the PDF on first run, cached in
   fulltext/<citekey>.ocr.txt). Add `--repair` only if the fulltext file is writable and the user did not
   correct it by hand (read-only fulltexts are hand-corrected: never repair, report instead).
2. Spawn a fresh subagent with .claude/skills/ingest/verifier.md and the citekey (one per paper, in parallel).
3. `python3 literature/tools/litqc.py check <citekey>`.
4. Fixes:
   - note with `verified: false`: apply the fix loop from .claude/skills/ingest/SKILL.md step 5.
   - note with `verified: true`: do not touch the claims. The user verified them; list the proposed
     fixes (claim, problem, verifier's `fix`) and let the user decide.

Finish with a table: citekey | verified | fulltext QC | claims supported/total | errors | warnings,
then the proposed fixes for verified notes.
