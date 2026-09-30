#!/usr/bin/env bash
# Usage: pdf2txt.sh <input.pdf> <output.txt>
# pdftotext (reading order, not -layout: keeps two-column papers readable) with explicit "=== PAGE N ===" markers so claims can be cited by page.
set -euo pipefail
pdftotext "$1" - | awk '
BEGIN { p = 1; print "=== PAGE 1 ===" }
{
  n = split($0, a, "\f")
  for (i = 1; i <= n; i++) {
    if (i > 1) { p++; pend = 1 }
    if (pend && a[i] != "") { print "=== PAGE " p " ==="; pend = 0 }
    if (!pend) print a[i]
  }
}' > "$2"
