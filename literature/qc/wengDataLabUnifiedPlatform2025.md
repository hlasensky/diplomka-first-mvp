---
type: qc
generated: 2026-10-30
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC wengDataLabUnifiedPlatform2025

Zdroj: [[wengDataLabUnifiedPlatform2025]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 4: shoda s OCR recall 0.74, pořadí 0.71, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

14 stran PDF, 13 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 4 | WARN | 553 | 736 | 0.74 | 0.98 | 0.71 | 0.90 | 0.85 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 3, 4 | 4/4 | 0.91 |  |
| C2 | supported | 5, 6 | 4/4 | 1.00 |  |
| C3 | supported | 6, 7 | 4/4 | 1.00 |  |
| C4 | supported | 9, 11 | 4/4 | 0.80 |  |
| C5 | supported | 11, 12 | 4/4 | 0.86 |  |

