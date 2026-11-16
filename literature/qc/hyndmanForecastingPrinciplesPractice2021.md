---
type: qc
generated: 2026-11-15
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC hyndmanForecastingPrinciplesPractice2021

Zdroj: [[hyndmanForecastingPrinciplesPractice2021]]

**QC: PASS s varováními** – 0 chyb, 19 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 10: shoda s OCR recall 0.74, pořadí 0.73, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 15: shoda s OCR recall 0.80, pořadí 0.78, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 20: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 3 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 22: shoda s OCR recall 0.77, pořadí 0.77, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 32: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 4 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 35: shoda s OCR recall 0.83, pořadí 0.81, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 41: shoda s OCR recall 0.84, pořadí 0.82, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 67: shoda s OCR recall 0.83, pořadí 0.83, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 70: shoda s OCR recall 0.85, pořadí 0.85, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 71: shoda s OCR recall 0.76, pořadí 0.75, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 73: shoda s OCR recall 0.79, pořadí 0.77, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 76: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 90: shoda s OCR recall 0.83, pořadí 0.82, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 99: shoda s OCR recall 0.79, pořadí 0.78, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 111: shoda s OCR recall 0.79, pořadí 0.73, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 114: shoda s OCR recall 0.81, pořadí 0.74, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 121: shoda s OCR recall 0.76, pořadí 0.71, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 122: shoda s OCR recall 0.79, pořadí 0.75, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 127: shoda s OCR recall 0.82, pořadí 0.82, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 20, 27, 31, 32, 38, 49, 65, 76, 108 |

### Fulltext vs. OCR

134 stran PDF, 115 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 10 | WARN | 148 | 201 | 0.74 | 1.00 | 0.73 | 0.95 | 0.75 | 0/0/0 |
| 15 | WARN | 40 | 50 | 0.80 | 1.00 | 0.78 | 0.95 | 0.86 | 0/0/0 |
| 20 | WARN | 116 | 116 | 1.00 | 1.00 | 1.00 | 0.73 | 0.73 | 0/0/3 |
| 22 | WARN | 68 | 88 | 0.77 | 1.00 | 0.77 | 0.96 | 0.93 | 0/0/0 |
| 32 | WARN | 123 | 123 | 1.00 | 1.00 | 1.00 | 0.51 | 0.51 | 0/0/4 |
| 35 | WARN | 86 | 103 | 0.83 | 1.00 | 0.81 | 0.93 | 0.84 | 0/0/0 |
| 41 | WARN | 175 | 202 | 0.84 | 0.97 | 0.82 | 0.89 | 0.86 | 0/0/0 |
| 67 | WARN | 218 | 261 | 0.83 | 1.00 | 0.83 | 0.97 | 0.92 | 0/0/0 |
| 70 | WARN | 84 | 99 | 0.85 | 1.00 | 0.85 | 0.90 | 0.87 | 0/0/0 |
| 71 | WARN | 62 | 82 | 0.76 | 1.00 | 0.75 | 0.97 | 0.91 | 0/0/0 |
| 73 | WARN | 60 | 76 | 0.79 | 1.00 | 0.77 | 0.92 | 0.86 | 0/0/0 |
| 76 | WARN | 58 | 58 | 1.00 | 1.00 | 1.00 | 0.83 | 0.83 | 0/0/1 |
| 90 | WARN | 167 | 200 | 0.83 | 1.00 | 0.82 | 1.00 | 0.99 | 0/0/0 |
| 99 | WARN | 137 | 172 | 0.79 | 0.99 | 0.78 | 1.00 | 0.92 | 0/0/0 |
| 111 | WARN | 105 | 133 | 0.79 | 1.00 | 0.73 | 1.00 | 0.98 | 0/0/0 |
| 114 | WARN | 51 | 63 | 0.81 | 1.00 | 0.74 | 0.94 | 0.92 | 0/0/0 |
| 121 | WARN | 37 | 49 | 0.76 | 1.00 | 0.71 | 0.84 | 0.86 | 0/0/0 |
| 122 | WARN | 55 | 70 | 0.79 | 1.00 | 0.75 | 0.89 | 0.83 | 0/0/0 |
| 127 | WARN | 90 | 110 | 0.82 | 1.00 | 0.82 | 1.00 | 0.95 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 13 | 4/4 | 1.00 |  |
| C2 | supported | 35, 38, 39 | 4/4 | 1.00 |  |
| C3 | supported | 50 | 3/3 | 1.00 |  |
| C4 | supported | 72 | 4/4 | 1.00 |  |
| C5 | supported | 84, 85 | 3/3 | 0.90 |  |
| C6 | supported | 92 | 4/4 | 1.00 |  |
| C7 | supported | 99 | 3/3 | 1.00 |  |

