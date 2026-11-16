---
type: qc
generated: 2026-11-15
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC millerExplanationArtificialIntelligence2019

Zdroj: [[millerExplanationArtificialIntelligence2019]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.99, pořadí 0.96, PUA 0, rozpalovaná slova 3 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

38 stran PDF, 37 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 408 | 409 | 0.99 | 0.99 | 0.96 | 0.94 | 0.94 | 0/0/3 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 3, 8 | 3/3 | 1.00 |  |
| C2 | supported | 3 | 3/3 | 1.00 |  |
| C3 | supported | 3 | 2/2 | 1.00 |  |
| C4 | supported | 3, 29 | 4/4 | 1.00 |  |
| C5 | supported | 32 | 4/4 | 1.00 |  |

