---
type: qc
generated: 2026-11-25
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC clevelandGraphicalPerceptionTheory1984

Zdroj: [[clevelandGraphicalPerceptionTheory1984]]

**QC: PASS s varováními** – 0 chyb, 5 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 6: shoda s OCR recall 0.87, pořadí 0.76, PUA 0, rozpalovaná slova 2 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 7: shoda s OCR recall 0.99, pořadí 0.84, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 13: shoda s OCR recall 0.97, pořadí 0.95, PUA 0, rozpalovaná slova 4 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 15: shoda s OCR recall 0.97, pořadí 0.90, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 17: shoda s OCR recall 0.95, pořadí 0.87, PUA 0, rozpalovaná slova 2 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

25 stran PDF, 20 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 6 | WARN | 301 | 342 | 0.87 | 0.98 | 0.76 | 0.95 | 0.94 | 0/0/2 |
| 7 | WARN | 85 | 86 | 0.99 | 1.00 | 0.84 | 0.95 | 0.95 | 0/0/1 |
| 13 | WARN | 373 | 380 | 0.97 | 0.99 | 0.95 | 0.97 | 0.97 | 0/0/4 |
| 15 | WARN | 483 | 475 | 0.97 | 0.96 | 0.90 | 0.96 | 0.99 | 0/0/1 |
| 17 | WARN | 145 | 147 | 0.95 | 0.96 | 0.87 | 0.98 | 0.97 | 0/0/2 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 2, 7, 15 | 3/3 | 1.00 |  |
| C2 | supported | 10, 15 | 4/4 | 1.00 |  |
| C3 | supported | 15, 23 | 4/4 | 1.00 |  |
| C4 | supported | 16, 17, 18 | 4/4 | 1.00 |  |
| C5 | supported | 23, 24 | 4/4 | 1.00 |  |

