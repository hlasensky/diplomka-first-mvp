---
type: qc
generated: 2026-11-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC dobsonReferenceArchitectureModel2018

Zdroj: [[dobsonReferenceArchitectureModel2018]]

**QC: FAIL** – 1 chyb, 2 varování

| úroveň | kód | nález |
|---|---|---|
| ERROR | CLAIM_PARTIAL | C5: verdikt `partial` – Obsah sedí, ale tvrzení o dvou případových studiích nemá oporu na citovaných s. 9 ani 11; je na necitované s. 2 (§I), resp. s. 8 (§V). |
| WARN | PAGE_WARN | s. 6: shoda s OCR recall 0.83, pořadí 0.82, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 9: shoda s OCR recall 0.81, pořadí 0.81, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |

### Fulltext vs. OCR

12 stran PDF, 10 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 6 | WARN | 428 | 516 | 0.83 | 1.00 | 0.82 | 0.97 | 0.93 | 0/0/0 |
| 9 | WARN | 585 | 718 | 0.81 | 1.00 | 0.81 | 0.98 | 0.96 | 0/0/0 |

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 1, 2 | 4/4 | 1.00 |  |
| C2 | supported | 3, 4, 5 | 4/4 | 1.00 |  |
| C3 | supported | 5, 6, 7 | 4/4 | 1.00 |  |
| C4 | supported | 8, 9, 10 | 4/4 | 1.00 |  |
| C5 | partial | 9, 11 | 2/2 | 1.00 | Obsah sedí, ale tvrzení o dvou případových studiích nemá oporu na citovaných s. 9 ani 11; je na necitované s. 2 (§I), re |

