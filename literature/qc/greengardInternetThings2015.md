---
type: qc
generated: 2026-10-30
---

> Generováno `literature/tools/litqc.py`, needitovat ručně.

# QC greengardInternetThings2015

Zdroj: [[greengardInternetThings2015]]

**QC: FAIL** – 2 chyb, 0 varování

| úroveň | kód | nález |
|---|---|---|
| ERROR | CLAIM_PARTIAL | C3: verdikt `partial` – „Z čistě lidského“ přehání: kniha píše „human-based“ a citovaný Ashton výslovně „almost wholly dependent on human beings“ (s. 16), tedy převážně, ne čistě; ostatní části sedí. |
| ERROR | CLAIM_PARTIAL | C7: verdikt `partial` – Kniha píše „virtually impossible“ (s. 21), tvrzení tuto výhradu vypouští a říká kategoricky, že by to žádná organizace ani vláda nedokázala; ostatní části (s. 20–21) sedí. |

### Fulltext vs. OCR

73 stran PDF, 73 bez nálezu. recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.

### Claims

| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |
|---|---|---|---|---|---|
| C1 | supported | 14 | 4/4 | 1.00 |  |
| C2 | supported | 14, 15 | 4/4 | 1.00 |  |
| C3 | partial | 15, 16 | 4/4 | 1.00 | „Z čistě lidského“ přehání: kniha píše „human-based“ a citovaný Ashton výslovně „almost wholly dependent on human beings |
| C4 | supported | 9, 10, 13 | 4/4 | 1.00 | Další části ověřeny: komercializace internetu a WWW v roce 1995 (s. 12), Bohlen, Beal a Rogers 1957 (s. 9), každé zaříze |
| C5 | supported | 14 | 4/4 | 1.00 |  |
| C6 | supported | 16, 17 | 4/4 | 1.00 |  |
| C7 | partial | 20, 21 | 4/4 | 1.00 | Kniha píše „virtually impossible“ (s. 21), tvrzení tuto výhradu vypouští a říká kategoricky, že by to žádná organizace a |
| C8 | supported | 22, 23 | 4/4 | 1.00 |  |

