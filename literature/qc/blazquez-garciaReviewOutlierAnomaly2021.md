---
type: qc
generated: 2026-10-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC blazquez-garciaReviewOutlierAnomaly2021

Zdroj: [[blazquez-garciaReviewOutlierAnomaly2021]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 4: shoda s OCR recall 0.81, pořadí 0.80, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

33 stran PDF, 32 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 4 | WARN | 193 | 234 | 0.81 | 0.98 | 0.80 | 0.96 | 0.94 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 2 | 4/4 | 0.92 |  |
| C2 | supported | 4, 5, 6 | 3/3 | 1.00 |  |
| C3 | supported | 5, 6 | 4/4 | 1.00 |  |
| C4 | supported | 7, 8 | 4/4 | 1.00 |  |
| C5 | supported | 27 | 3/3 | 1.00 |  |
| C6 | supported | 29 | 4/4 | 1.00 |  |
| C7 | supported | 29 | 4/4 | 1.00 |  |

