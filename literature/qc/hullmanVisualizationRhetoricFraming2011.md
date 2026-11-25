---
type: qc
generated: 2026-11-25
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC hullmanVisualizationRhetoricFraming2011

Zdroj: [[hullmanVisualizationRhetoricFraming2011]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 5: shoda s OCR recall 0.84, pořadí 0.83, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

10 stran PDF, 9 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 5 | WARN | 615 | 735 | 0.84 | 1.00 | 0.83 | 0.93 | 0.90 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 3 | 3/3 | 1.00 |  |
| C2 | supported | 3, 4 | 5/5 | 1.00 |  |
| C3 | supported | 4 | 4/4 | 1.00 |  |
| C4 | supported | 6 | 4/4 | 1.00 |  |
| C5 | supported | 6, 9 | 4/4 | 1.00 |  |

