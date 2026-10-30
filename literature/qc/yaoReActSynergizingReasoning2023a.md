---
type: qc
generated: 2026-10-30
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC yaoReActSynergizingReasoning2023a

Zdroj: [[yaoReActSynergizingReasoning2023a]]

**QC: PASS s varováními** – 0 chyb, 4 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.98, pořadí 0.96, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 3: shoda s OCR recall 0.99, pořadí 0.98, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 27: shoda s OCR recall 0.98, pořadí 0.72, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 29: shoda s OCR recall 1.00, pořadí 0.84, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 2, 14, 15 |

### Fulltext vs. OCR

33 stran PDF, 29 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 427 | 428 | 0.98 | 0.98 | 0.96 | 0.87 | 0.88 | 0/0/1 |
| 3 | WARN | 585 | 586 | 0.99 | 0.99 | 0.98 | 0.95 | 0.95 | 0/0/1 |
| 27 | WARN | 124 | 124 | 0.98 | 0.98 | 0.72 | 0.94 | 0.95 | 0/0/1 |
| 29 | WARN | 329 | 330 | 1.00 | 1.00 | 0.84 | 0.76 | 0.76 | 0/0/1 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 2 | 4/4 | 1.00 |  |
| C2 | supported | 3, 4 | 4/4 | 1.00 |  |
| C3 | supported | 3, 4 | 4/4 | 1.00 |  |
| C4 | supported | 3, 4, 7 | 4/4 | 0.88 |  |
| C5 | supported | 5, 6 | 4/4 | 1.00 |  |
| C6 | supported | 6 | 4/4 | 1.00 |  |
| C7 | supported | 7, 8 | 4/4 | 1.00 |  |
| C8 | supported | 6, 9, 10 | 4/4 | 1.00 |  |

