---
type: qc
generated: 2026-10-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC sarawagiDiscoverydrivenExplorationOLAP1998

Zdroj: [[sarawagiDiscoverydrivenExplorationOLAP1998]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 5: shoda s OCR recall 0.82, pořadí 0.78, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

15 stran PDF, 14 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 5 | WARN | 183 | 217 | 0.82 | 0.97 | 0.78 | 0.97 | 0.93 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 2 | 3/3 | 1.00 |  |
| C2 | supported | 2, 7 | 4/4 | 1.00 |  |
| C3 | supported | 7 | 2/2 | 1.00 |  |
| C4 | supported | 8, 9 | 4/4 | 1.00 |  |
| C5 | supported | 3, 9, 10 | 4/4 | 1.00 |  |
| C6 | supported | 3, 5, 6 | 4/4 | 1.00 |  |
| C7 | supported | 10, 13, 15 | 4/4 | 1.00 |  |
| C8 | supported | 12, 15 | 4/4 | 1.00 |  |

