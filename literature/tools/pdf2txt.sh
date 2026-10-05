#!/usr/bin/env bash
# Usage: pdf2txt.sh <input.pdf> <output.txt>
# pdftotext (reading order, not -layout: keeps two-column papers readable) with explicit "=== PAGE N ===" markers so claims can be cited by page.
# Ligatures (ﬁ, ﬂ, ﬀ …) and soft hyphens are normalized so the text greps cleanly.
# Afterwards run `litqc.py fulltext <citekey> --repair` to compare every page with an independent OCR.
set -euo pipefail
if [[ -e "$2" && ! -w "$2" ]]; then
  echo "pdf2txt: $2 is read-only (hand-corrected fulltext), not overwriting" >&2
  exit 1
fi
pdftotext "$1" - | sed 's/ﬀ/ff/g; s/ﬁ/fi/g; s/ﬂ/fl/g; s/ﬃ/ffi/g; s/ﬄ/ffl/g; s/\xc2\xad//g' | awk '
BEGIN { p = 1; print "=== PAGE 1 ===" }
{
  n = split($0, a, "\f")
  for (i = 1; i <= n; i++) {
    if (i > 1) { p++; pend = 1 }
    if (pend && a[i] != "") { print "=== PAGE " p " ==="; pend = 0 }
    if (!pend) print a[i]
  }
}' > "$2"
