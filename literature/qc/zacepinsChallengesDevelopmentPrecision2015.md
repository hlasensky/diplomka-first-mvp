---
type: qc
generated: 2026-11-06
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC zacepinsChallengesDevelopmentPrecision2015

Zdroj: [[zacepinsChallengesDevelopmentPrecision2015]]

**QC: PASS s varováními** – 0 chyb, 12 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.97, pořadí 0.87, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 2: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 3: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 4: shoda s OCR recall 0.99, pořadí 0.98, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 5: shoda s OCR recall 0.99, pořadí 0.99, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 6: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 7: shoda s OCR recall 0.90, pořadí 0.89, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 8: shoda s OCR recall 1.00, pořadí 0.98, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 9: shoda s OCR recall 0.99, pořadí 0.94, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 10: shoda s OCR recall 1.00, pořadí 0.99, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 11: shoda s OCR recall 0.99, pořadí 0.98, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 12: shoda s OCR recall 0.99, pořadí 0.99, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

12 stran PDF, 0 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 335 | 340 | 0.97 | 0.99 | 0.87 | 0.82 | 0.82 | 0/0/1 |
| 2 | WARN | 713 | 715 | 1.00 | 1.00 | 1.00 | 0.92 | 0.92 | 0/0/1 |
| 3 | WARN | 716 | 718 | 1.00 | 1.00 | 1.00 | 0.90 | 0.90 | 0/0/1 |
| 4 | WARN | 730 | 734 | 0.99 | 1.00 | 0.98 | 0.90 | 0.90 | 0/0/1 |
| 5 | WARN | 785 | 788 | 0.99 | 1.00 | 0.99 | 0.93 | 0.93 | 0/0/1 |
| 6 | WARN | 757 | 759 | 1.00 | 1.00 | 1.00 | 0.93 | 0.92 | 0/0/1 |
| 7 | WARN | 406 | 451 | 0.90 | 1.00 | 0.89 | 0.94 | 0.93 | 0/0/1 |
| 8 | WARN | 558 | 545 | 1.00 | 0.97 | 0.98 | 0.94 | 0.97 | 0/0/1 |
| 9 | WARN | 675 | 677 | 0.99 | 1.00 | 0.94 | 0.94 | 0.94 | 0/0/1 |
| 10 | WARN | 667 | 668 | 1.00 | 1.00 | 0.99 | 0.89 | 0.89 | 0/0/1 |
| 11 | WARN | 641 | 643 | 0.99 | 0.99 | 0.98 | 0.73 | 0.73 | 0/0/1 |
| 12 | WARN | 402 | 404 | 0.99 | 1.00 | 0.99 | 0.76 | 0.76 | 0/0/1 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 2 | 4/4 | 0.96 |  |
| C2 | supported | 2, 3 | 4/4 | 1.00 |  |
| C3 | supported | 3 | 4/4 | 1.00 |  |
| C4 | supported | 6, 7, 8 | 4/4 | 1.00 |  |
| C5 | supported | 10 | 4/4 | 1.00 |  |

