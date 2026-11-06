---
type: qc
generated: 2026-11-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC wangChartInsighterApproachMitigating2025

Zdroj: [[wangChartInsighterApproachMitigating2025]]

**QC: FAIL** – 1 chyb, 2 varování

| úroveň | kód | nález |
|---|---|---|
| ERROR | NUMBER_NOT_FOUND | C2: čísla 3.1, 70 nejsou na citovaných stranách (převod? graf? – ověř) |
| WARN | PAGE_WARN | s. 4: shoda s OCR recall 0.77, pořadí 0.75, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 8: shoda s OCR recall 0.80, pořadí 0.80, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 6, 9 |

### Fulltext vs. OCR

13 stran PDF, 11 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 4 | WARN | 465 | 590 | 0.77 | 0.98 | 0.75 | 0.92 | 0.94 | 0/0/0 |
| 8 | WARN | 557 | 694 | 0.80 | 1.00 | 0.80 | 0.95 | 0.94 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1 | 4/4 | 1.00 |  |
| C2 | supported | 4 | 4/4 | 0.92 |  |
| C3 | supported | 4, 5 | 4/4 | 1.00 |  |
| C4 | supported | 5, 6, 7, 8 | 4/4 | 1.00 |  |
| C5 | supported | 7, 11 | 4/4 | 1.00 |  |
| C6 | supported | 2, 8, 9 | 4/4 | 1.00 |  |
| C7 | supported | 9, 10 | 4/4 | 1.00 |  |
| C8 | supported | 11, 12 | 4/4 | 1.00 |  |

