---
type: qc
generated: 2026-10-30
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC sengerWeightTemperatureHumidity2024

Zdroj: [[sengerWeightTemperatureHumidity2024]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.99, pořadí 0.97, PUA 0, rozpalovaná slova 3 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

11 stran PDF, 10 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 285 | 288 | 0.99 | 1.00 | 0.97 | 0.86 | 0.86 | 0/0/3 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 8 | 4/4 | 1.00 |  |
| C2 | supported | 5, 7 | 4/4 | 0.93 |  |
| C3 | supported | 7, 8 | 4/4 | 1.00 |  |
| C4 | supported | 9 | 4/4 | 1.00 |  |
| C5 | supported | 5, 6 | 4/4 | 1.00 |  |
| C6 | supported | 6, 8 | 4/4 | 1.00 |  |
| C7 | supported | 6, 9 | 4/4 | 1.00 |  |
| C8 | supported | 8, 10 | 4/4 | 1.00 |  |

