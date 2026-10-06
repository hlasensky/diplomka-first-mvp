---
type: qc
generated: 2026-10-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC liuElephantRoomReliable2024

Zdroj: [[liuElephantRoomReliable2024]]

**QC: PASS s varováními** – 0 chyb, 3 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 19: shoda s OCR recall 0.99, pořadí 0.50, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 24: shoda s OCR recall 1.00, pořadí 0.48, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 26: shoda s OCR recall 0.73, pořadí 0.69, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 29, 30, 31 |

### Fulltext vs. OCR

31 stran PDF, 28 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 19 | WARN | 186 | 183 | 0.99 | 0.98 | 0.50 | 0.65 | 0.66 | 0/0/0 |
| 24 | WARN | 270 | 268 | 1.00 | 0.99 | 0.48 | 0.64 | 0.64 | 0/0/0 |
| 26 | WARN | 125 | 168 | 0.73 | 0.98 | 0.69 | 0.48 | 0.42 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 3, 4 | 4/4 | 1.00 |  |
| C2 | supported | 1, 5, 7 | 5/5 | 1.00 |  |
| C3 | supported | 5, 9 | 3/3 | 1.00 |  |
| C4 | supported | 9, 10 | 3/3 | 1.00 |  |
| C5 | supported | 10 | 3/3 | 0.89 |  |

