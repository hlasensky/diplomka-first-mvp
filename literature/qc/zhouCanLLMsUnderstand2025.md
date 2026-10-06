---
type: qc
generated: 2026-10-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC zhouCanLLMsUnderstand2025

Zdroj: [[zhouCanLLMsUnderstand2025]]

**QC: PASS s varováními** – 0 chyb, 15 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 24: shoda s OCR recall 0.94, pořadí 0.90, PUA 0, rozpalovaná slova 4 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 25: shoda s OCR recall 0.91, pořadí 0.85, PUA 0, rozpalovaná slova 4 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 26: shoda s OCR recall 0.77, pořadí 0.52, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 27: shoda s OCR recall 0.79, pořadí 0.53, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 28: shoda s OCR recall 0.80, pořadí 0.58, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 29: shoda s OCR recall 0.79, pořadí 0.54, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 30: shoda s OCR recall 0.77, pořadí 0.52, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 31: shoda s OCR recall 0.81, pořadí 0.56, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 32: shoda s OCR recall 0.79, pořadí 0.56, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 33: shoda s OCR recall 0.78, pořadí 0.53, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 34: shoda s OCR recall 0.80, pořadí 0.54, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 35: shoda s OCR recall 0.80, pořadí 0.55, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 36: shoda s OCR recall 0.80, pořadí 0.54, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 37: shoda s OCR recall 0.79, pořadí 0.55, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 38: shoda s OCR recall 0.74, pořadí 0.45, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

39 stran PDF, 24 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 24 | WARN | 435 | 446 | 0.94 | 0.97 | 0.90 | 0.87 | 0.85 | 0/0/4 |
| 25 | WARN | 351 | 369 | 0.91 | 0.96 | 0.85 | 0.89 | 0.85 | 0/0/4 |
| 26 | WARN | 175 | 175 | 0.77 | 0.77 | 0.52 | 0.79 | 0.59 | 0/0/0 |
| 27 | WARN | 169 | 169 | 0.79 | 0.79 | 0.53 | 0.78 | 0.57 | 0/0/0 |
| 28 | WARN | 174 | 174 | 0.80 | 0.80 | 0.58 | 0.80 | 0.60 | 0/0/0 |
| 29 | WARN | 170 | 170 | 0.79 | 0.79 | 0.54 | 0.78 | 0.57 | 0/0/0 |
| 30 | WARN | 178 | 178 | 0.77 | 0.77 | 0.52 | 0.80 | 0.57 | 0/0/0 |
| 31 | WARN | 168 | 168 | 0.81 | 0.81 | 0.56 | 0.78 | 0.59 | 0/0/0 |
| 32 | WARN | 152 | 152 | 0.79 | 0.79 | 0.56 | 0.79 | 0.58 | 0/0/0 |
| 33 | WARN | 177 | 177 | 0.78 | 0.78 | 0.53 | 0.86 | 0.64 | 0/0/0 |
| 34 | WARN | 172 | 172 | 0.80 | 0.80 | 0.54 | 0.83 | 0.62 | 0/0/0 |
| 35 | WARN | 173 | 173 | 0.80 | 0.80 | 0.55 | 0.83 | 0.63 | 0/0/0 |
| 36 | WARN | 173 | 173 | 0.80 | 0.80 | 0.54 | 0.83 | 0.62 | 0/0/0 |
| 37 | WARN | 164 | 164 | 0.79 | 0.79 | 0.55 | 0.86 | 0.65 | 0/0/0 |
| 38 | WARN | 101 | 101 | 0.74 | 0.74 | 0.45 | 0.79 | 0.53 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1 | 4/4 | 1.00 |  |
| C2 | supported | 7, 8 | 4/4 | 0.82 |  |
| C3 | supported | 2, 9, 24 | 4/4 | 1.00 |  |
| C4 | supported | 2, 9, 10 | 3/3 | 1.00 |  |
| C5 | supported | 9 | 4/4 | 1.00 |  |
| C6 | supported | 10 | 4/4 | 0.92 |  |
| C7 | supported | 10, 24, 25 | 4/4 | 0.86 |  |
| C8 | supported | 1, 2 | 3/3 | 1.00 |  |

