# Spike: Cube jako semantic layer

Datum: 2026-10-07. Kód spiku byl po vyhodnocení smazán, tady je, co jsme zkoušeli a co vyšlo.

## Otázka

Umí Cube vyjádřit těžké OLAP dotazy, které potřebuje analytický protokol (baseline, drill-down, DIFF, souvislosti s kontextovými fakty), a dává správná čísla?

Kontext rozhodování:
- Dnešní stav: `semantic_layer.yaml` → prompt → **LLM píše SQL** → heuristický validátor (R1–R3) kontroluje až potom.
- Cube: YAML model → **engine kompiluje SQL**, LLM jen vybírá measures, dimenze a filtry (JSON). Správnost je daná konstrukcí, ale jen pro to, co je namodelované.
- Alternativy zvažované předem: dbt MetricFlow (Python, Apache 2.0 od 10/2025), Malloy, Wren Engine, Boring Semantic Layer. Do spiku šel jen Cube, protože po zrušení omezení na lean MVP vyšel jako nejsilnější kandidát (REST/SQL API, pre-agregace, multi-fact views).

## Setup

- Cube **v1.7.50** (Tesseract zapnutý defaultně), driver DuckDB (uvnitř DuckDB 1.5.5, kompatibilní s naším souborem, storage v0.10.2), docker compose, dev mode.
- Data: kopie tabulek `senger` (`agg_colony_daily`, `fact_hive_hourly`, `fact_event`, `dim_colony`, `dim_cell`) do samostatného souboru, protože Cube drží vlastní spojení na DuckDB.
- Navíc `fact_weather_daily` z Open-Meteo archive (ERA5) pro všech 34 buněk, 2019-06 až 2022-12 (srážky, průměrná teplota, sluneční svit; 44 540 řádků; jeden request pro všechny souřadnice, bez klíče) a `dim_date` (den).
- Model: kostky `colony_daily`, `hive_hourly`, `weather_daily`, `dates`, `cells`, `colonies` a view `hive_weather` (multi-fact).
- Testy: každý dotaz běžel přes Cube (REST nebo SQL API) a zároveň jako nezávisle napsané SQL v DuckDB. Porovnání po řádcích, klíče přesně, hodnoty s relativní tolerancí 1e-6.

## Výsledky: 16 / 17 prošlo

Latence 0,04–0,2 s na dotaz.

| ID | Co | Mechanismus v Cube | Výsledek |
|---|---|---|---|
| T01 | roll-up buňka × měsíc | REST dotaz + segment (`n_hours >= 20`) | ✓ |
| T02 | slice & dice (rojící se kolonie, 2021) | filtr na připojené dimenzi | ✓ |
| T03 | meteorologická sezóna | custom granularity (`interval: 3 months`, origin 1. 3.) | ✓ |
| T04 | meziroční srovnání | multi-stage `time_shift` | ✓ |
| T05 | klouzavých 7 dní | `rolling_window` (okno = aktuální den + 6 předchozích) | ✓ |
| T06 | peer residual (EX1): kolonie minus průměr buňky | multi-stage `grain: keep_only` | ✓ po opravě (N1) |
| T07 | podíl kolonie na přírůstku buňky | multi-stage `grain: keep_only` | ✓ po opravě (N1) |
| T08 | pořadí kolonie v buňce | `type: rank`, `grain: exclude` | ✓ |
| T09 | součet za kolonii, pak průměr přes kolonie | `grain: include` | ✓ |
| T10 | semi-aditivní poslední váha v měsíci | měřítko `arg_max` + `grain: include` | ✓ |
| T11 | drill-across úl × počasí, den | multi-fact view | ✓ |
| T12 | drill-across, měsíc (test fan trapu) | multi-fact view | ✓ |
| T13 | counterfactual (bez jedné kolonie) | filtr `notEquals` | ✓ |
| T14 | okno před událostí (EX4): 1–21 dní před rojením | kostka nad SQL s ASOF JOIN | ✓ |
| T15 | window funkce nad modelem | SQL API pushdown | ✓ |
| T16 | ROLLUP buňka → kolonie | SQL API pushdown | ✗ **tiše špatně** (N2) |
| T17 | korelace se zpožděním 0–3 dny (přírůstek ~ srážky) | řady z Cube, statistika v Pythonu | ✓ |

## Nálezy

**N1 – multi-stage `grain` s `type: number` se tiše ignoruje.** Měřítko typu `sql: "{total_gain}"`, `type: number`, `grain: keep_only: [cell_id, date]` vrátí beze změny hodnotu na úrovni kolonie, takže residual vyjde 0. Vygenerované SQL znovu použije CTE na zrnu kolonie. Stejně se chová `exclude`, staré `group_by` / `reduce_by` i dimenze z připojených kostek. Funguje to, když má grain měřítko agregační typ (`sum`, `avg`). Poměr nad ním (`share`, `residual`) může zůstat `type: number`. Vlastní příklad `keep_only` v dokumentaci používá `type: number`, takže ve verzi 1.7.50 si dokumentace a engine odporují.

```yaml
- name: cell_avg_gain          # peer baseline
  multi_stage: true
  sql: "{avg_gain}"
  type: avg                    # NE number, jinak se grain ignoruje
  grain:
    keep_only: [cell_id, date]
- name: gain_residual
  multi_stage: true
  sql: "{avg_gain} - {cell_avg_gain}"
  type: number
```

**N2 – SQL API zahodí `ROLLUP` bez chyby.** `GROUP BY ROLLUP (cell_id, colony_key)` se přepíše na `GROUP BY 1, 2`: chybí mezisoučty (44 řádků místo 69) a nepřijde žádné varování (ověřeno přes `EXPLAIN`).

**N3 – obě chyby byly tiché.** Ani jedna nevyhodila chybu, odhalilo je až srovnání s ground truth. To, že Cube dotaz přijal, nedokazuje, že je výsledek správný.

**N4 – drill-across funguje a chrání před fan trapem.** Naivní `hive JOIN weather ON cell, date` dává špatné měsíční srážky ve 162 z 217 kombinací buňka × měsíc (až 7× víc a navíc ztratí dny bez dat z úlu). Multi-fact view sedí s ground truth. Podmínka modelu: každý fakt potřebuje **přímý** join na každou sdílenou dimenzi, proto je `cell_id` denormalizované do kostky úlů.

**N5 – časová zóna.** Cube obaluje časové filtry do `timezone('UTC', col::timestamptz)`. U denních dat to nevadí. U hodinových a minutových dat je nutné vyjasnit zdrojovou zónu `time_key` před analýzou podle hodiny dne (už poznamenáno v semantic layer).

**N6 – události přes ASOF jdou namodelovat.** Kostka může mít `sql:` s libovolným dotazem, takže „dní do dalšího rojení“ je dimenze spočítaná ASOF joinem uvnitř kostky a filtruje se běžně (T14).

## Co zůstává mimo Cube

- statistika (STL, z-score, korelace se zpožděním): Python nástroje nad výsledky z Cube (T17),
- ROLLUP v jednom dotazu: smyčka přes úrovně hierarchie (DIFF a generalize nástroje stejně iterují),
- okna relativní k událostem: odvozené sloupce v SQL kostky (T14), ne ad hoc dotazy.

## Důsledky pro architekturu

- Cube je použitelný jako semantic layer i pro náročné dotazy.
- Grain měřítka vždy s agregačním typem (N1).
- Agent nikdy neposílá do Cube `ROLLUP` ani `GROUPING SETS`. Pokud by volné SQL šlo přes SQL API, validátor je musí odmítnout (N2).
- Ke každému měřítku patří regresní test proti ručně napsanému SQL (N3). Harness ze spiku je vzor: dotaz přes Cube vs. nezávislé SQL, porovnání po řádcích.
- Vygenerované SQL je dostupné přes `/v1/sql` a dá se uložit jako provenance tvrzení.
