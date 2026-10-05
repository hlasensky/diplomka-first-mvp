# Claim verifier (fresh subagent, never the agent that wrote the claims)

Input: one citekey. You did not write the note. Your job is to try to break its claims, not to confirm them.

Read:
- literature/sources/<citekey>.md, section "Klíčová tvrzení" (claims C1…)
- literature/fulltext/<citekey>.txt (pages = `=== PAGE N ===` markers, PDF pages)
- literature/fulltext/<citekey>.ocr.txt: independent OCR of the same PDF. Use it when the fulltext page is
  garbled, or to double-check numbers in tables. literature/qc/<citekey>.md lists suspicious pages.

For every claim:
1. Find the passages that support each part of it. Check every number, name, ordering and qualifier
   ("only", "always", "faster", "first") against the text. Czech wording is fine; meaning must match.
2. The page reference is `(s. N, §…)`; only the part before `|` is PDF pages. Every cited page should
   carry evidence, and the evidence must not sit on an uncited page.
3. Verdict:
   - `supported`: every part of the claim is in the paper as stated, on the cited pages
   - `partial`: some part is missing, overstated, on another page, or a number differs
   - `unsupported`: the paper does not say this
   Claims that interpret the paper beyond what it says (e.g. "the authors consider X weak") are
   `partial` unless the text says it. When in doubt, do not say `supported`.
4. Evidence: 1–4 quotes per claim, each copied **verbatim** from literature/fulltext/<citekey>.txt
   (same words in the same order, 6–40 words, from one page, no ellipses). Prefer sentences that contain
   the claim's numbers. Line breaks and hyphenation may be dropped, nothing else may change.
   A script checks each quote against the fulltext page AND against the OCR of the PDF page.

Write literature/qc/<citekey>.claims.json:

```json
{
  "citekey": "<citekey>",
  "claims": {
    "C1": {
      "verdict": "supported",
      "evidence": [{"page": 1, "quote": "exact words from the fulltext page"}],
      "note": "Czech, 1 sentence: what is wrong or missing (empty when supported)",
      "fix": "Czech, only for partial/unsupported: corrected claim text with page reference"
    }
  }
}
```

Then run `python3 literature/tools/litqc.py stamp <citekey>` and
`python3 literature/tools/litqc.py claims <citekey>`. For any QUOTE_NOT_FOUND / PAGE_MISMATCH error,
fix your quote (copy it again from the fulltext) and rerun. Do not edit the source note.

Return: per claim one line `Cn: verdict – note`, plus remaining litqc errors.
