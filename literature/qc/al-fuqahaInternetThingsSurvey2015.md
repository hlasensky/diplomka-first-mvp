---
type: qc
generated: 2026-10-30
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC al-fuqahaInternetThingsSurvey2015

Zdroj: [[al-fuqahaInternetThingsSurvey2015]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 25: shoda s OCR recall 0.80, pořadí 0.75, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

30 stran PDF, 29 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 25 | WARN | 222 | 265 | 0.80 | 0.95 | 0.75 | 0.86 | 0.79 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 2 | 4/4 | 1.00 |  |
| C2 | supported | 2 | 4/4 | 0.91 |  |
| C3 | supported | 3, 4 | 4/4 | 1.00 |  |
| C4 | supported | 7, 8, 9, 10 | 4/4 | 1.00 |  |
| C5 | supported | 8 | 4/4 | 1.00 |  |
| C6 | supported | 10 | 4/4 | 1.00 |  |
| C7 | supported | 3, 5, 6 | 4/4 | 1.00 |  |
| C8 | supported | 16, 18, 26 | 4/4 | 1.00 |  |

