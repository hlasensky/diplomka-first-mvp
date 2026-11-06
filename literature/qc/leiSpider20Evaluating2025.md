---
type: qc
generated: 2026-11-06
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC leiSpider20Evaluating2025

Zdroj: [[leiSpider20Evaluating2025]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 19: shoda s OCR recall 0.84, pořadí 0.83, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 18, 26 |

### Fulltext vs. OCR

45 stran PDF, 44 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 19 | WARN | 244 | 292 | 0.84 | 1.00 | 0.83 | 0.93 | 0.83 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 2 | 4/4 | 1.00 |  |
| C2 | supported | 1, 2, 3, 6 | 4/4 | 1.00 |  |
| C3 | supported | 3, 4, 5 | 4/4 | 1.00 |  |
| C4 | supported | 1, 6, 7 | 4/4 | 1.00 |  |
| C5 | supported | 7 | 3/3 | 1.00 |  |
| C6 | supported | 8 | 4/4 | 0.86 |  |
| C7 | supported | 8, 9 | 4/4 | 1.00 |  |
| C8 | supported | 1, 9, 10 | 4/4 | 1.00 |  |

