---
type: qc
generated: 2026-11-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC silvaUserCentricGuidelinesChatbot2024

Zdroj: [[silvaUserCentricGuidelinesChatbot2024]]

**QC: PASS s varováními** – 0 chyb, 4 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 12: shoda s OCR recall 0.81, pořadí 0.80, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 13: shoda s OCR recall 0.78, pořadí 0.77, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 22: shoda s OCR recall 0.99, pořadí 0.40, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 23: shoda s OCR recall 0.97, pořadí 0.57, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

24 stran PDF, 20 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 12 | WARN | 456 | 561 | 0.81 | 1.00 | 0.80 | 0.93 | 0.93 | 0/0/0 |
| 13 | WARN | 437 | 556 | 0.78 | 0.99 | 0.77 | 0.92 | 0.93 | 0/0/0 |
| 22 | WARN | 126 | 126 | 0.99 | 0.99 | 0.40 | 0.68 | 0.68 | 0/0/0 |
| 23 | WARN | 337 | 338 | 0.97 | 0.97 | 0.57 | 0.94 | 0.91 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 4, 7 | 4/4 | 1.00 |  |
| C2 | supported | 9 | 3/3 | 1.00 |  |
| C3 | supported | 11, 12 | 4/4 | 0.93 |  |
| C4 | supported | 13, 14, 15, 16 | 4/4 | 1.00 |  |
| C5 | supported | 17, 18 | 4/4 | 1.00 |  |

