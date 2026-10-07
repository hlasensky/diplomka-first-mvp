# Data pro DP

Stav k 2026-10-06. Rozhodnutí a jejich důvody jsou v [decisions.md](decisions.md).

## Jádro: IoT senzory z úlů (BeeObserver)

Senger et al., *Data in Brief* 52 (2024) 110015, [doi:10.1016/j.dib.2023.110015](https://doi.org/10.1016/j.dib.2023.110015). Data na Zenodo: [10.5281/zenodo.10407693](https://doi.org/10.5281/zenodo.10407693), archiv `bob_publication_data.zip`.

| Co | Hodnota |
|---|---|
| Kolonie / lokality | 78 kolonií, 34 lokalit (buňky 47,7–53,8° s. š., 6,7–13,4° v. d.), Německo |
| Období | 6/2019 – 12/2022 |
| Senzory | váha, 5 teplot v úlu (střed → okraj), venkovní teplota, vlhkost, tlak |
| Hodinová data | 151 souborů, 0,24 GB; už v `data/senger.duckdb` (`fact_hive_hourly`, 638 tis. řádků) |
| Minutová data | 151 souborů, 1,83 GB zip / 13 GB CSV, 36,0 mil. řádků; staženo v `data/raw/multi-senger/bob/`, cíl Parquet |
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

## Cílové schéma (fact constellation)

Dataset pack `multi-senger`. Hodinová data, události a dimenze úlu existují v `senger`, ostatní je návrh, který se upřesní při stavbě ETL.

### Fakty

| Tabulka | Grain (1 řádek =) | Klíče | Míry / sloupce | Stav |
|---|---|---|---|---|
| `fact_hive_minute` | úl × minuta | `colony_key`, `ts` | `weight_kg`, `t_i_1`…`t_i_5`, `t_o`, `h`, `t_bme`, `p` | návrh, Parquet podle roku |
| `fact_hive_hourly` | úl × hodina | `colony_key`, `time_key` | `weight_kg`, `weight_gain_kg`, `weight_change_raw_kg`, `t_i_1`…`t_i_5`, `t_o`, `t_diff_in_out`, `h`, `t_bme`, `p` | existuje |
| `fact_temperature` (view) | úl × hodina × senzor | `colony_key`, `time_key`, `sensor_pos` | `temp_c` | existuje |
| `agg_colony_daily` | úl × den | `colony_key`, `date` | `weight_gain_kg`, `max_hourly_drop_raw_kg`, `t_center_avg`, `t_center_std`, `t_diff_avg`, `h_avg`, `n_hours` | existuje |
| `fact_event` | 1 událost | `colony_key`, `event_ts`, `event_type` | – | existuje |
| `fact_weather` | buňka × hodina | `cell_id`, `time_key` | `temp_2m`, `precip_mm`, `rain_mm`, `wind_kmh`, `radiation_wm2`, `rh_pct` | návrh |
| `fact_bloom_phenology` | stanice × rok × druh | `station_id`, `year`, `plant_key` | `bloom_start_date`, `bloom_start_doy` | návrh |
| `fact_vegetation` | buňka × 16 dní | `cell_id`, `date` | `ndvi` | návrh |
| `fact_crop_acres` | okres × rok × plodina | `kreis_id`, `year`, `crop` | `area_ha` | návrh |
| `fact_country_apiculture` | země × rok | `country`, `year` | `hives`, `honey_t`, `winter_loss_n`, `winter_colonies_n` | návrh |

### Dimenze

| Tabulka | Hierarchie / sloupce | Stav |
|---|---|---|
| `dim_geo` (dnes `dim_colony` + `dim_cell`) | úl → buňka (`lat`, `lon`) → okres (`kreis_id`) → spolková země → stát | úl a buňka existují, okres a země z VG250 |
| `dim_time` | minuta → hodina → den → týden → měsíc → sezóna → rok | od hodiny výš existuje |
| `dim_station` | fenologická stanice (`lat`, `lon`) → nejbližší buňka (`cell_id`, `dist_km`) | návrh |
| `dim_plant` | druh → skupina (plodina / dřevina / bylina) → medonosnost | návrh |
| `dim_event_type` | `event_type` → `cause_class` | existuje |
| `dim_sensor_position` | `sensor_pos` → `zone` → `slot` | existuje |

### Propojení faktů (jen přes sdílené dimenze)

| Dvojice | Společný grain | Poznámka |
|---|---|---|
| úl × počasí | buňka × hodina | úl → `cell_id` |
| úl × kvetení | buňka × rok (+ den v roce) | buňka → nejbližší stanice v `dim_station`, limit vzdálenosti |
| úl × NDVI | buňka × 16 dní | denní data úlu agregovat na 16denní okna |
| úl × plodiny | okres (roky 2016, 2020) | potřebuje okres v `dim_geo`; plocha je atribut okresu, ne časová řada; plochy jsou podle sídla podniku |
| úl × makro data | stát × rok | jen kontext, 78 úlů nereprezentuje zemi |
| úl × události | úl × čas | jen ASOF JOIN nebo EXISTS (pravidlo R2) |

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

- **`dim_cell.state` je NULL u všech 34 buněk.** Sekce 4b v `datasets/senger/build.sql` je vypnutá, protože chybí `states.geojson`. Opraví se přiřazením buňka → okres → spolková země.
- **Počasí:** ERA5 má rozlišení ~28 km, na místní srážky je hrubé. Alternativou jsou stanice DWD.
- **Fenologie:** pozorují dobrovolníci a stanice je od úlu v mediánu 9–12 km. Přiřazení stanice k úlu je aproximace.
- **Inspekce:** jsou neúplné. Když událost chybí, neznamená to, že nenastala.
