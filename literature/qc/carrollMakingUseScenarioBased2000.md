---
type: qc
generated: 2026-11-06
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC carrollMakingUseScenarioBased2000

Zdroj: [[carrollMakingUseScenarioBased2000]]

**QC: PASS s varováními** – 0 chyb, 7 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 18: shoda s OCR recall 0.80, pořadí 0.79, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 136: shoda s OCR recall 0.84, pořadí 0.80, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 189: shoda s OCR recall 0.74, pořadí 0.72, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 234: shoda s OCR recall 0.74, pořadí 0.73, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 247: shoda s OCR recall 0.73, pořadí 0.72, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 252: shoda s OCR recall 0.75, pořadí 0.74, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 314: shoda s OCR recall 1.00, pořadí 1.00, PUA 0, rozpalovaná slova 1 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 78, 114, 120, 123, 145, 151, 158, 175, 178, 197, 201, 253, 256, 294, 296, 313, 314 |

### Fulltext vs. OCR

372 stran PDF, 365 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 18 | WARN | 195 | 243 | 0.80 | 0.99 | 0.79 | 0.97 | 0.96 | 0/0/0 |
| 136 | WARN | 198 | 231 | 0.84 | 0.98 | 0.80 | 0.92 | 0.95 | 0/0/0 |
| 189 | WARN | 150 | 201 | 0.74 | 0.99 | 0.72 | 0.97 | 0.98 | 0/0/0 |
| 234 | WARN | 154 | 206 | 0.74 | 0.99 | 0.73 | 0.97 | 0.97 | 0/0/0 |
| 247 | WARN | 172 | 230 | 0.73 | 0.98 | 0.72 | 0.97 | 0.99 | 0/0/0 |
| 252 | WARN | 139 | 183 | 0.75 | 0.99 | 0.74 | 0.97 | 0.96 | 0/0/0 |
| 314 | WARN | 211 | 211 | 1.00 | 1.00 | 1.00 | 0.87 | 0.87 | 0/0/1 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 54, 55, 56 | 4/4 | 1.00 |  |
| C2 | supported | 61, 63, 66, 67, 69, 70 | 7/7 | 1.00 |  |

