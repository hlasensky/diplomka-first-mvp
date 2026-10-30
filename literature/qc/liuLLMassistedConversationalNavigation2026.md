---
type: qc
generated: 2026-10-30
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC liuLLMassistedConversationalNavigation2026

Zdroj: [[liuLLMassistedConversationalNavigation2026]]

**QC: FAIL** – 1 chyb, 3 varování

| úroveň | kód | nález |
|---|---|---|
| ERROR | NOT_VERIFIED | chybí qc/liuLLMassistedConversationalNavigation2026.claims.json – claims neprošly ověřovacím agentem |
| WARN | PAGE_WARN | s. 1: shoda s OCR recall 0.98, pořadí 0.96, PUA 0, rozpalovaná slova 3 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 5: shoda s OCR recall 0.83, pořadí 0.79, PUA 0, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| WARN | PAGE_WARN | s. 8: shoda s OCR recall 0.85, pořadí 0.81, PUA 2, rozpalovaná slova 0 (tabulka/vzorec/sloupce?) – ověř v PDF, než z ní cituješ |
| INFO | PAGE_OCR | strany z OCR: 9 |

### Fulltext vs. OCR

19 stran PDF, 16 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WARN | 605 | 612 | 0.98 | 0.99 | 0.96 | 0.90 | 0.89 | 0/0/3 |
| 5 | WARN | 583 | 685 | 0.83 | 0.98 | 0.79 | 0.93 | 0.88 | 0/0/0 |
| 8 | WARN | 478 | 555 | 0.85 | 0.98 | 0.81 | 0.94 | 0.91 | 0/2/0 |

