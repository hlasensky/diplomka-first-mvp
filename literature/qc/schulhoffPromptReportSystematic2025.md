---
type: qc
generated: 2026-11-15
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC schulhoffPromptReportSystematic2025

Zdroj: [[schulhoffPromptReportSystematic2025]]

**QC: PASS s varováními** – 0 chyb, 1 varování

| úroveň | kód | nález |
|---|---|---|
| WARN | PAGE_WARN | s. 17: shoda s OCR recall 0.75, pořadí 0.64, PUA 0, rozpalovaná slova 2 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 37, 77 |

### Fulltext vs. OCR

80 stran PDF, 79 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 17 | WARN | 172 | 60 | 0.75 | 0.26 | 0.64 | 0.53 | 0.70 | 0/0/2 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 8 | 4/4 | 1.00 |  |
| C2 | supported | 5 | 3/3 | 1.00 |  |
| C3 | supported | 5, 6 | 4/4 | 0.83 |  |
| C4 | supported | 5, 6 | 2/2 | 1.00 |  |
| C5 | supported | 7 | 4/4 | 1.00 |  |
| C6 | supported | 8, 9 | 3/3 | 0.92 | Názvy šesti kategorií jsou jen v Obr. 2.2 (s. 9); zero-shot je tam číslován jako podsekce ICL (2.2.1.3), ale graficky tv |
| C7 | supported | 18 | 3/3 | 1.00 |  |
| C8 | supported | 24 | 3/3 | 1.00 |  |

