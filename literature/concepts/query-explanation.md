---
type: concept
aliases: [explanation, why query, why queries, explaining aggregates, explain operator, DIFF operator, data explanation, root cause of aggregate change]
---

Automatické vysvětlení, proč má agregovaná hodnota (nebo změna mezi dvěma hodnotami) takovou velikost, formou malého souboru řádků, faktorů nebo modelů místo ručního drill-downu.

## Sources
- [[sarawagiExplainingDifferencesMultidimensional]] — C1–C3: operátor diff vrátí nejvýše N řádků (detailních i agregovaných s poměrem změny), které nejlépe vysvětlí rozdíl dvou buněk; výběr minimalizuje délku popisu v bitech.
- [[franciaExplainingCubeMeasures2024]] — C1, C2: operátor explain v IAM vysvětluje cílovou míru jinými měrami (polynomiální a lineární regrese, křížová korelace) a nejzajímavější model ukáže jako highlight.

## Související
- [[olap]]
- [[intentional-analytics]]
- [[anomaly-detection]]
- [[guided-data-exploration]]
