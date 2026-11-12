---
type: qc
generated: 2026-11-11
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC hersbachERA5GlobalReanalysis2020

Zdroj: [[hersbachERA5GlobalReanalysis2020]]

**QC: PASS s varováními** – 0 chyb, 21 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 4: shoda s OCR recall 0.92, pořadí 0.90, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 6: shoda s OCR recall 0.92, pořadí 0.89, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 16: shoda s OCR recall 0.78, pořadí 0.41, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 17: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 18: shoda s OCR recall 0.92, pořadí 0.90, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 22: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 2 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 25: shoda s OCR recall 0.91, pořadí 0.87, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 26: shoda s OCR recall 0.79, pořadí 0.71, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 27: shoda s OCR recall 0.91, pořadí 0.90, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 28: shoda s OCR recall 0.85, pořadí 0.83, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 29: shoda s OCR recall 0.78, pořadí 0.75, PUA 0, rozpalovaná slova 2 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 30: shoda s OCR recall 0.92, pořadí 0.89, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 31: shoda s OCR recall 0.86, pořadí 0.85, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 32: shoda s OCR recall 0.84, pořadí 0.80, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 33: shoda s OCR recall 0.81, pořadí 0.76, PUA 0, rozpalovaná slova 2 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 34: shoda s OCR recall 0.92, pořadí 0.90, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 35: shoda s OCR recall 0.93, pořadí 0.90, PUA 0, rozpalovaná slova 2 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 36: shoda s OCR recall 0.85, pořadí 0.75, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 37: shoda s OCR recall 0.91, pořadí 0.87, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 38: shoda s OCR recall 0.83, pořadí 0.80, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 42: shoda s OCR recall 0.91, pořadí 0.59, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 14, 17, 19, 22 |

### Fulltext vs. OCR

51 stran PDF, 30 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 4 | WARN | 598 | 599 | 0.92 | 0.92 | 0.90 | 0.93 | 0.89 | 0/0/1 |
| 6 | WARN | 548 | 538 | 0.92 | 0.90 | 0.89 | 0.94 | 0.91 | 0/0/1 |
| 16 | WARN | 179 | 178 | 0.78 | 0.77 | 0.41 | 0.53 | 0.42 | 0/0/1 |
| 17 | WARN | 359 | 359 | 1.00 | 1.00 | 1.00 | 0.75 | 0.75 | 0/0/1 |
| 18 | WARN | 547 | 547 | 0.92 | 0.92 | 0.90 | 0.90 | 0.86 | 0/0/1 |
| 22 | WARN | 177 | 177 | 1.00 | 1.00 | 1.00 | 0.49 | 0.49 | 0/0/2 |
| 25 | WARN | 521 | 525 | 0.91 | 0.91 | 0.87 | 0.89 | 0.85 | 0/0/1 |
| 26 | WARN | 217 | 220 | 0.79 | 0.80 | 0.71 | 0.82 | 0.70 | 0/0/1 |
| 27 | WARN | 491 | 490 | 0.91 | 0.91 | 0.90 | 0.95 | 0.90 | 0/0/1 |
| 28 | WARN | 372 | 393 | 0.85 | 0.90 | 0.83 | 0.94 | 0.85 | 0/0/1 |
| 29 | WARN | 309 | 344 | 0.78 | 0.87 | 0.75 | 0.91 | 0.84 | 0/0/2 |
| 30 | WARN | 658 | 650 | 0.92 | 0.91 | 0.89 | 0.94 | 0.92 | 0/0/1 |
| 31 | WARN | 430 | 450 | 0.86 | 0.90 | 0.85 | 0.94 | 0.88 | 0/0/1 |
| 32 | WARN | 363 | 382 | 0.84 | 0.88 | 0.80 | 0.90 | 0.82 | 0/0/1 |
| 33 | WARN | 231 | 226 | 0.81 | 0.80 | 0.76 | 0.87 | 0.79 | 0/0/2 |
| 34 | WARN | 601 | 601 | 0.92 | 0.92 | 0.90 | 0.95 | 0.91 | 0/0/1 |
| 35 | WARN | 667 | 669 | 0.93 | 0.93 | 0.90 | 0.91 | 0.88 | 0/0/2 |
| 36 | WARN | 395 | 399 | 0.85 | 0.86 | 0.75 | 0.87 | 0.80 | 0/0/1 |
| 37 | WARN | 515 | 516 | 0.91 | 0.91 | 0.87 | 0.90 | 0.86 | 0/0/1 |
| 38 | WARN | 433 | 474 | 0.83 | 0.91 | 0.80 | 0.90 | 0.84 | 0/0/1 |
| 42 | WARN | 425 | 424 | 0.91 | 0.91 | 0.59 | 0.77 | 0.72 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 2 | 2/2 | 1.00 |  |
| C2 | supported | 1 | 2/2 | 1.00 |  |
| C3 | supported | 10 | 2/2 | 1.00 |  |

