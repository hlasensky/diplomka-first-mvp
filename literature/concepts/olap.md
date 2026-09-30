---
type: concept
aliases: [OLAP, data cube, OLAP cube, drill-down, roll-up, multidimensional database]
---

On-Line Analytical Processing: analýza dat organizovaných do vícerozměrné kostky (dimenze s hierarchiemi a numerické míry), navigovaná operacemi drill-down, roll-up a selection.

## Sources
- [[sarawagiDiscoverydrivenExplorationOLAP1998]] — C1: ruční drill-down/roll-up hledání anomálií v kostce je kvůli velikosti prostoru a maskování v agregacích obtížné.
- [[vassiliadisRollUpsDrillDownsIntentional2019]] — C1: navrhuje nahradit roll-up/drill-down intentional operátory (describe, assess, explain, predict, suggest).
- [[sarawagiExplainingDifferencesMultidimensional]] — C1: 5–7 dimenzí a hierarchie dělají ruční hledání důvodů změny agregátu drill-downem zdlouhavým; navrhuje operátor diff.
- [[franciaExplainingCubeMeasures2024]] — C3: explain intention nad kostkou včetně spojení kostek (analogie drill-across) a odvozených měr.

## Související
- [[anomaly-detection]]
- [[guided-data-exploration]]
- [[query-explanation]]
