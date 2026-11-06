---
type: qc
generated: 2026-11-06
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC atzoriInternetThingsSurvey2010

Zdroj: [[atzoriInternetThingsSurvey2010]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.99, pořadí 0.97, PUA 0, rozpalovaná slova 3 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

19 stran PDF, 18 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 486 | 491 | 0.99 | 1.00 | 0.97 | 0.89 | 0.89 | 0/0/3 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 2 | 4/4 | 1.00 |  |
| C2 | supported | 2, 3, 4 | 4/4 | 1.00 |  |
| C3 | supported | 4, 5 | 4/4 | 1.00 |  |
| C4 | supported | 5, 6, 7 | 4/4 | 1.00 |  |
| C5 | supported | 7, 11, 14 | 4/4 | 1.00 |  |

