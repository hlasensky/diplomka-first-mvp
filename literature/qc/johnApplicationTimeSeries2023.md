---
type: qc
generated: 2026-11-05
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC johnApplicationTimeSeries2023

Zdroj: [[johnApplicationTimeSeries2023]]

**QC: FAIL** – 3 chyb, 0 varování

| úroveň | kód | nález |
|---|---|---|
| ERROR | CLAIM_PARTIAL | C1: verdikt `partial` – Článek zmírňuje: uživatel agregovaná data „may want“ (ne „potřebuje“) a načítání surových dat „can result“ v pomalém UI (ne „zpomaluje“); zařazení dat jako časových řad začíná na s. 1 a pokračuje na s. 2 – to sedí. |
| ERROR | CLAIM_PARTIAL | C4: verdikt `partial` – S. 4 popisuje PostgreSQL pro metadata senzorů jen v minulém čase (architektura před přechodem); že tam metadata senzorů jsou i nyní, říká až necitovaná s. 5 (§VI). |
| ERROR | PAGE_MISMATCH | C4: důkaz je na s. 5, claim cituje (s. 4, §V) |

### Fulltext vs. OCR

6 stran PDF, 6 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | partial | 1, 2 | 4/4 | 1.00 | Článek zmírňuje: uživatel agregovaná data „may want“ (ne „potřebuje“) a načítání surových dat „can result“ v pomalém UI  |
| C2 | supported | 3 | 4/4 | 1.00 |  |
| C3 | supported | 3, 4 | 4/4 | 1.00 |  |
| C4 | partial | 4, 5 | 4/4 | 1.00 | S. 4 popisuje PostgreSQL pro metadata senzorů jen v minulém čase (architektura před přechodem); že tam metadata senzorů  |
| C5 | supported | 4, 5 | 4/4 | 1.00 |  |

