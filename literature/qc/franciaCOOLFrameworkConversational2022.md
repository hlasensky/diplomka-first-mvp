---
type: qc
generated: 2026-10-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC franciaCOOLFrameworkConversational2022

Zdroj: [[franciaCOOLFrameworkConversational2022]]

**QC: PASS s varováními** – 0 chyb, 5 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.98, pořadí 0.96, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 6: shoda s OCR recall 0.74, pořadí 0.70, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 8: shoda s OCR recall 0.75, pořadí 0.67, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | REF_UNSUPPORTED | C8: citovaná s. 3 nemá žádný důkaz |
| WARN | REF_UNSUPPORTED | C8: citovaná s. 17 nemá žádný důkaz |
| INFO | PAGE_OCR | strany z OCR: 12, 15 |

### Fulltext vs. OCR

18 stran PDF, 15 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 584 | 588 | 0.98 | 0.99 | 0.96 | 0.89 | 0.89 | 0/0/1 |
| 6 | WARN | 331 | 444 | 0.74 | 0.99 | 0.70 | 0.90 | 0.76 | 0/0/0 |
| 8 | WARN | 380 | 494 | 0.75 | 0.97 | 0.67 | 0.89 | 0.82 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1 | 4/4 | 1.00 |  |
| C2 | supported | 2, 3, 4 | 4/4 | 1.00 |  |
| C3 | supported | 1, 4, 5, 10 | 4/4 | 1.00 |  |
| C4 | supported | 2, 6 | 4/4 | 1.00 |  |
| C5 | supported | 7, 9, 10, 11 | 4/4 | 1.00 |  |
| C6 | supported | 11, 13 | 4/4 | 1.00 |  |
| C7 | supported | 13, 14, 16 | 4/4 | 1.00 |  |
| C8 | supported | 2, 11, 13, 16 | 4/4 | 1.00 |  |

