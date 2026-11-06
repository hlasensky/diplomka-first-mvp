---
type: qc
generated: 2026-11-06
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC gengJSONSchemaBenchRigorousBenchmark2025

Zdroj: [[gengJSONSchemaBenchRigorousBenchmark2025]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 17: shoda s OCR recall 0.80, pořadí 0.77, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 19, 21 |

### Fulltext vs. OCR

32 stran PDF, 30 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 17 | WARN | 113 | 142 | 0.80 | 1.00 | 0.77 | 0.90 | 0.80 | 0/0/0 |
| 19 | BAD | 91 | 91 | 1.00 | 1.00 | 1.00 | 0.56 | 0.56 | 0/0/10 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 3, 4, 5 | 4/4 | 1.00 |  |
| C2 | supported | 5, 6, 7 | 4/4 | 1.00 |  |
| C3 | supported | 7, 8, 9 | 4/4 | 0.88 |  |
| C4 | supported | 8, 10 | 4/4 | 1.00 |  |
| C5 | supported | 11, 12 | 4/4 | 1.00 |  |

