---
type: qc
generated: 2026-10-30
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC liCanLLMAlready2023a

Zdroj: [[liCanLLMAlready2023a]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 9: shoda s OCR recall 0.98, pořadí 0.94, PUA 25, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

28 stran PDF, 27 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 9 | WARN | 484 | 456 | 0.98 | 0.92 | 0.94 | 0.93 | 0.95 | 0/25/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 2 | 4/4 | 1.00 |  |
| C2 | supported | 2, 3 | 4/4 | 1.00 |  |
| C3 | supported | 3, 4, 5 | 4/4 | 1.00 |  |
| C4 | supported | 6 | 4/4 | 0.89 |  |
| C5 | supported | 1, 7, 8 | 4/4 | 1.00 |  |
| C6 | supported | 7, 9 | 4/4 | 1.00 |  |
| C7 | supported | 9, 10 | 4/4 | 1.00 |  |
| C8 | supported | 10 | 2/2 | 0.96 |  |

