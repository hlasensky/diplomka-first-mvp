---
type: qc
generated: 2026-10-06
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC Infobrief2020_29Jahresruckblick

Zdroj: [[Infobrief2020_29Jahresruckblick]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.84, pořadí 0.68, PUA 7, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

3 stran PDF, 2 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 289 | 291 | 0.84 | 0.84 | 0.68 | 0.12 | 0.13 | 0/7/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1 | 1/1 | 0.82 |  |
| C2 | supported | 2, 3 | 4/4 | 0.80 |  |

