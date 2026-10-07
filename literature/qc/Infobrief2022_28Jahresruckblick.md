---
type: qc
generated: 2026-10-06
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC Infobrief2022_28Jahresruckblick

Zdroj: [[Infobrief2022_28Jahresruckblick]]

**QC: PASS s varováními** – 0 chyb, 3 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.81, pořadí 0.64, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 3: shoda s OCR recall 0.83, pořadí 0.75, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 5: shoda s OCR recall 0.82, pořadí 0.72, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 4 |

### Fulltext vs. OCR

5 stran PDF, 2 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 507 | 524 | 0.81 | 0.84 | 0.64 | 0.16 | 0.16 | 0/0/0 |
| 3 | WARN | 164 | 188 | 0.83 | 0.95 | 0.75 | 0.10 | 0.11 | 0/0/0 |
| 5 | WARN | 248 | 267 | 0.82 | 0.88 | 0.72 | 0.15 | 0.20 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 2 | 2/2 | 1.00 |  |
| C2 | supported | 1 | 1/1 | 0.86 |  |

