# Data pro DP

Stav k 2026-10-07: pack `multi-senger` je postavený (`data/multi-senger.duckdb`, 0,94 GB). Rozhodnutí a jejich důvody jsou v [decisions.md](decisions.md).

## Jádro: IoT senzory z úlů (BeeObserver)

Senger et al., *Data in Brief* 52 (2024) 110015, [doi:10.1016/j.dib.2023.110015](https://doi.org/10.1016/j.dib.2023.110015). Data na Zenodo: [10.5281/zenodo.10407693](https://doi.org/10.5281/zenodo.10407693), archiv `bob_publication_data.zip`.

| Co | Hodnota |
|---|---|
| Kolonie / lokality | 78 kolonií, 34 lokalit (buňky 47,7–53,8° s. š., 6,7–13,4° v. d.), Německo |
| Období | 6/2019 – 12/2022 |
| Senzory | váha, 5 teplot v úlu (střed → okraj), venkovní teplota, vlhkost, tlak |
| Hodinová data | 151 souborů, 0,24 GB; už v `data/senger.duckdb` (`fact_hive_hourly`, 638 tis. řádků) |
| Minutová data | 151 souborů, 1,83 GB zip / 13 GB CSV, 36,0 mil. řádků; staženo v `data/raw/multi-senger/bob/`, v DuckDB jako `fact_hive_minute` |
| Události | inspekce včelařů (`inspections.csv`): rojení, matečníky, krmení, med, léčba, úhyn; neúplné |

## Kontextová data

Stahuje je `scripts/fetch_multi_senger.py` do `data/raw/multi-senger/` (mimo git). Ke každému zdroji zapíše do `MANIFEST.json` odkaz, datum stažení a SHA-256.

| Fakt / dimenze | Zdroj | Odkaz | Grain | Stav |
|---|---|---|---|---|
| `dim_geo` (okresy, spolkové země) | BKG VG250 Ebenen 31.12., GeoPackage UTM32s, licence dl-de/by-2-0 | [vg250_12-31.utm32s.gpkg.ebenen.zip](https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_1231/aktuell/vg250_12-31.utm32s.gpkg.ebenen.zip) | polygon okresu / země | ✅ staženo |
| `fact_weather` | Open-Meteo archive (ERA5, nejbližší bod) | [API](https://open-meteo.com/en/docs/historical-weather-api) | buňka × hodina | ✅ staženo (34 lokalit) |
| `fact_bloom_phenology` + `dim_station` | DWD fenologie, Jahresmelder, fáze 5 = začátek kvetení | [data](https://opendata.dwd.de/climate_environment/CDC/observations_germany/phenology/annual_reporters/), [stanice](https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt), [fáze](https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phase.txt) | stanice × rok × druh | ✅ staženo (řepka, akát, lípa, pampeliška) |
| `fact_vegetation` | MODIS MOD13Q1 NDVI, ORNL DAAC REST | [služba](https://daac.ornl.gov/cgi-bin/dsviewer.pl?ds_id=1252), `https://modis.ornl.gov/rst/api/v1/MOD13Q1/subset` | buňka × 16 dní | ✅ staženo (92 termínů 2019–2022) |
| `fact_country_apiculture` (úly, med) | FAOSTAT QCL, položky Bees (stocks) a Natural honey | [bulk zip](https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip) | země × rok | ✅ staženo, filtr na Německo |
| `fact_country_apiculture` (úly na farmách) | Eurostat `ef_lsk_bees` | [databrowser](https://ec.europa.eu/eurostat/databrowser/view/ef_lsk_bees/default/table) | NUTS2 × rok šetření | ✅ staženo; z období dat jen rok 2020 |
| `fact_country_apiculture` (zimní ztráty) | COLOSS monitoring | [coloss.org](https://coloss.org/activities/monitoring/) | země × zima | ❌ ručně: čísla jsou jen v ročních článcích (J. Apicultural Research) |
| `fact_crop_acres` | Regionalstatistik 41141-02-02-4 (Agrarstrukturerhebung / Landwirtschaftszählung): Anbau auf dem Ackerland nach Fruchtarten, okresy, ha, licence dl-de/by-2-0 | [regionalstatistik.de](https://www.regionalstatistik.de) (ruční export CSV) | okres × rok × plodina | ✅ staženo, roky **2016 a 2020** (soubor na rok); řepka ozimá samostatně; skrytá řepka (`.`) u 84 (2016) a 102 (2020) ze 472 okresů |
| výnosy plodin | Regionalstatistik 41241-01-03-4 (Erntestatistik): Hektarerträge (dt/ha) 10 plodin vč. řepky, okresy | [regionalstatistik.de](https://www.regionalstatistik.de) (ruční export CSV) | okres × rok × plodina | ✅ staženo, **každý rok 2016–2025**; skrytá řepka jen u 1–13 okresů ročně (2016: 131) |

Pokrytí stanicemi DWD u 34 lokalit úlů, začátek kvetení v letech 2019–2022:

| Druh | Stanic za rok | Nejbližší stanice (medián / max) | Lokalit do 15 km |
|---|---|---|---|
| Řepka (Winterraps) | ~600 | 12 / 43 km | 24/34 |
| Akát (Robinie) | ~725 | 9 / 24 km | 32/34 |
| Lípa (Sommer-Linde) | ~850 | 9 / 20 km | 33/34 |
| Pampeliška (Löwenzahn) | ~990 | 9 / 20 km | 33/34 |
| Jabloň | – | – | ovoce má jiné kódy fází, dořešit |

## Schéma packu `multi-senger` (fact constellation)

Build: `DATASET=multi-senger uv run python scripts/build_db.py` (asi 20 s). Kód je v `datasets/multi-senger/build.sql`. Sekce 99 build zastaví, když nesedí grain, cizí klíč nebo počty řádků. Časy jsou všude v UTC.

### Fakty a agregáty

| Tabulka | Grain (1 řádek =) | Řádků | Míry / sloupce |
|---|---|---|---|
| `fact_hive_minute` | úl × minuta | 36 029 522 | `weight_kg`, `weight_delta_no_outlier`, `t_i_1`…`t_i_5`, `t_o`, `t_bme`, `h`, `p`, `is_outlier`, `ts_shifted_dst` |
| `fact_hive_hourly` | úl × hodina | 638 471 | průměry minut, `n_minutes`, `weight_gain_kg`, `weight_change_raw_kg`, `t_diff_in_out` |
| `fact_temperature` (view) | úl × hodina × senzor | 2,8 mil. | `temp_c` |
| `agg_colony_daily` | úl × den | 29 172 | `weight_gain_kg`, `max_hourly_drop_raw_kg`, `t_center_avg/std`, `t_diff_avg`, `h_avg`, `n_hours`, `n_minutes` |
| `fact_event` | 1 událost | 443 | `event_type`, `event_ts` |
| `fact_weather` | buňka × hodina | 1 068 960 | `air_temp_c`, `precip_mm`, `rain_mm`, `wind_kmh`, `radiation_wm2`, `air_rh_pct` |
| `agg_weather_daily` | buňka × den | 44 540 | `air_temp_avg/min/max_c`, `precip_mm`, `rain_hours`, `radiation_kwh_m2`, `wind_avg_kmh`, `air_rh_avg_pct`, `n_hours` |
| `fact_vegetation` | buňka × 16denní kompozit | 3 128 | `ndvi` |
| `fact_bloom_phenology` | stanice × rok × druh | 22 678 | `bloom_date`, `bloom_doy`, `quality_byte` (roky 2016–2022, QB 1/2/3) |
| `agg_cell_bloom` | buňka × rok × druh | 930 | medián `bloom_doy` přes stanice do 25 km, `n_stations`, `nearest_station_km` |
| `fact_crop_area` | okres × rok × plodina | 13 600 | `area_ha`, `value_status` (2016, 2020) |
| `fact_crop_yield` | okres × rok × plodina | 40 000 | `yield_dt_ha`, `value_status` (2016–2025) |
| `agg_cell_crop` | buňka × rok × plodina | 2 800 | `crop_share_pct`, `share_coverage`, `yield_w_dt_ha`, `yield_coverage` (vážené přes okresy buňky) |
| `fact_country_bees` | země × rok | 8 | `hives`, `honey_t` (FAOSTAT, 2016–2023) |
| `fact_winter_loss` | země × zima × průzkum | 4 | `n_reports`, `colonies_wintered`, `colonies_lost`, `loss_pct_mean`, `loss_pct_pooled`, CI, `citekey`, `evidence` |

### Dimenze a bridge

| Tabulka | Řádků | Hierarchie / sloupce |
|---|---|---|
| `dim_colony` | 78 | úl → buňka → okres (hlavní) → spolková země → stát; `colonies_in_cell`, `ever_swarmed`, `died` |
| `dim_cell` | 34 | `lat`, `lon`, hlavní okres a jeho váha, `n_districts`, `share_in_germany` |
| `bridge_cell_district` | 70 | buňka × okres, `box_share`, `weight` (součet 1 na buňku) |
| `dim_district`, `dim_state`, `dim_country` | 400, 16, 1 | VG250; `district` je jednoznačný název (u dvojic doplněn typ); stát jen `DE` |
| `dim_year` | 10 | roky 2016–2025, `has_hive_data`, `is_farm_survey_year`; zmenšená dimenze pro fakty na grainu rok |
| `dim_bee_winter` | 5 | zimy 2018/19–2022/23, `winter_start`/`winter_end`, `has_full_hive_data` (2018/19 a 2022/23 bez úplných dat z úlů) |
| `dim_time` | 31 440 | hodina → `date` (FK na `dim_date`), atributy dne denormalizované; jen pro hodinové fakty |
| `dim_date` | 1 461 | den (2019–2022) → týden → měsíc → rok; `season`, `is_beekeeping_season`, `bee_winter` (říjen–březen); pro denní fakty a data událostí |
| `dim_station` | 6 627 | fenologická stanice DWD (`lat`, `lon`, výška, země) |
| `dim_plant` | 4 | řepka, pampeliška, akát, lípa; skupina, období snůšky |
| `dim_crop` | 19 | plodina → `parent_crop`, `is_bee_forage` (plodiny jsou vnořené) |
| `dim_event_type`, `dim_sensor_position` | 6, 6 | jako v `senger` |

### Propojení faktů (jen přes sdílené dimenze)

| Dvojice | Společný grain | Poznámka |
|---|---|---|
| úl × počasí | buňka × den, nebo buňka × hodina | přes `dim_colony.cell_id`; denní úl jen s denním počasím (R8) |
| úl × kvetení | buňka × rok | `agg_cell_bloom`, filtrovat jeden druh |
| úl × NDVI | buňka × den → poslední kompozit | jen ASOF JOIN (R2) |
| úl × plodiny | buňka × rok | `agg_cell_crop`, vážené přes `bridge_cell_district`; vždy jedna plodina (R9) |
| úl × národní data | rok nebo zima | úly nejdřív agregovat na rok / zimu, pak spojit přes `dim_year` / `dim_bee_winter` (R10) |
| úl × události | úl × čas | jen ASOF JOIN nebo EXISTS (R2) |

Kontrola souvislostí po buildu:
- Venkovní senzor úlu proti ERA5: korelace 0,90 (po hodinách).
- Řepka: v 14 dnech před začátkem kvetení v okolí je průměrný denní přírůstek −0,02 kg, ve 14 dnech po něm +0,36 kg (příklad EX6).

## Pravidla slučování

Pravidla jsou převzatá z `bee_olap_datasets_and_merging.md`:
1. Jemnější data agregovat nahoru, hrubší nikdy nerozpočítávat dolů.
2. Pro každý grain vlastní fakt.
3. Podíly ukládat jako čitatel a jmenovatel, při roll-upu přepočítat.
4. Vážené průměry (např. podle plochy), ne prostý průměr přes regiony.
5. Chybějící hodnota je NULL, ne 0.

## Proč ne data z USA

Původní návrh počítal s US Bee OLAP (USDA, NASS, NOAA). Jsou to ale statistiky po státech a čtvrtletích, ne data z chytrých zařízení, a srovnatelná veřejná US senzorová data z úlů neexistují:

| Dataset | Proč nevyhovuje |
|---|---|
| [ASU „Predicting Honeybee Health“](https://data.mendeley.com/datasets/pbbwvjxgbc/1) (NC, UT) | jen inspekce a počasí; slibovaná váha úlů v souborech není |
| [BroodMinder / BeeCounted](https://thespoon.tech/broodminder-open-sources-beehive-data/) | velký, ale bez hromadného stažení a API pro cizí data |
| [NASA HoneyBeeNet](https://honeybeenet.gsfc.nasa.gov/Sites/SHData.htm) | jedna hodnota denně, často ruční zápis, řídké |
| BeePi / USDA ARS Tucson | 10 úlů, jedna sezóna |
| [MSPB](https://zenodo.org/records/8371700) | Kanada, bez váhy; má ale expertní fenotypy (Varroa, úmrtnost) – kandidát na ground truth pro evaluaci |

## Známé problémy

- **`senger`:** `dim_cell.state` je NULL a hodinová data mají chybu ve dnech jarní změny času. V `multi-senger` je obojí opravené (viz [decisions.md](decisions.md), 2026-10-07).
- **Okresy:** souřadnice úlů jsou zaokrouhlené. Hlavní okres buňky je jen ten s největším podílem plochy, kontext plodin se proto váží přes `bridge_cell_district`. Buňka 49.2_6.9 leží jen z 35 % v Německu.
- **Plodiny:** plocha řepky v okolí je úplná u 17 z 34 buněk (`share_coverage`). Plochy se počítají podle sídla podniku. Výnosy pro Berlín, Brémy a Hamburk nejsou.
- **Zimní ztráty** pocházejí ze zdrojů ve stavu `candidate` (neověřené). Počty u zim 2019/20 a 2020/21 jsou z OCR tabulky (s. 4) a nejsou v žádném claimu. Build ověřuje, že sedí s procenty v claimu C2.
- **Počasí:** ERA5 má rozlišení ~28 km, na místní srážky je hrubé. Alternativou jsou stanice DWD.
- **Fenologie:** pozorují dobrovolníci a stanice je od úlu v mediánu 9–12 km. Přiřazení stanice k úlu je aproximace.
- **Inspekce:** jsou neúplné. Když událost chybí, neznamená to, že nenastala.
