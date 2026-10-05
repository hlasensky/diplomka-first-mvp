---
type: qc
generated: 2026-10-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC vassiliadisRollUpsDrillDownsIntentional2019

Zdroj: [[vassiliadisRollUpsDrillDownsIntentional2019]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 60: shoda s OCR recall 0.78, pořadí 0.77, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

74 stran PDF, 73 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 60 | WARN | 217 | 272 | 0.78 | 0.98 | 0.77 | 0.96 | 0.97 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 2, 3, 8 | 3/3 | 1.00 |  |
| C2 | supported | 3, 5, 20 | 4/4 | 1.00 |  |
| C3 | supported | 16, 17, 18 | 4/4 | 1.00 |  |
| C4 | supported | 21, 22, 24, 48 | 4/4 | 1.00 |  |
| C5 | supported | 10, 25, 26 | 4/4 | 1.00 |  |
| C6 | supported | 34, 35, 36 | 4/4 | 1.00 |  |
| C7 | supported | 43, 44 | 4/4 | 1.00 |  |
| C8 | supported | 25, 44, 50, 51 | 4/4 | 0.94 |  |

