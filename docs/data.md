# Data pro DP

Stav k 2026-10-05. Rozhodnutí a jejich důvody jsou v [decisions.md](decisions.md).

## Jádro: IoT senzory z úlů (BeeObserver)

Senger et al., *Data in Brief* 52 (2024) 110015, [doi:10.1016/j.dib.2023.110015](https://doi.org/10.1016/j.dib.2023.110015). Data na Zenodo: [10.5281/zenodo.10407693](https://doi.org/10.5281/zenodo.10407693), archiv `bob_publication_data.zip`.

| Co | Hodnota |
|---|---|
| Kolonie / lokality | 78 kolonií, 34 lokalit (buňky 47,7–53,8° s. š., 6,7–13,4° v. d.), Německo |
| Období | 6/2019 – 12/2022 |
| Senzory | váha, 5 teplot v úlu (střed → okraj), venkovní teplota, vlhkost, tlak |
| Hodinová data | 151 souborů, 0,24 GB; už v `data/senger.duckdb` (`fact_hive_hourly`, 638 tis. řádků) |
| Minutová data | 151 souborů, 1,83 GB zip / 13,8 GB CSV, ~66 mil. řádků; zatím nestažená, cíl Parquet |
| Události | inspekce včelařů (`inspections.csv`): rojení, matečníky, krmení, med, léčba, úhyn; neúplné |

## Kontextová data

| Fakt | Zdroj | Grain | Stav |
|---|---|---|---|
| `fact_weather` | [Open-Meteo archive](https://open-meteo.com/en/docs/historical-weather-api) (ERA5, nejbližší bod) | lokalita × hodina | ověřeno: bez klíče; teplota, srážky, vítr, záření, vlhkost |
| `fact_bloom_phenology` | [DWD fenologie](https://opendata.dwd.de/climate_environment/CDC/observations_germany/phenology/annual_reporters/), Jahresmelder, fáze 5 = začátek kvetení | stanice → region × rok × druh | ověřeno, pokrytí níže |
| `fact_vegetation` | MODIS NDVI MOD13Q1 přes [ORNL REST](https://daac.ornl.gov/cgi-bin/dsviewer.pl?ds_id=1252) | lokalita × 16 dní | ověřeno pro bod |
| `fact_crop_acres` | Regionalstatistik / statistické úřady zemí | okres × rok × plodina | **neověřeno** (možná registrace pro API) |
| `fact_country_apiculture` | Eurostat, FAOSTAT, COLOSS | země × rok | **neověřeno** |

Pokrytí stanicemi DWD u 34 lokalit úlů, začátek kvetení v letech 2019–2022:

| Druh | Stanic za rok | Nejbližší stanice (medián / max) | Lokalit do 15 km |
|---|---|---|---|
| Řepka (Winterraps) | ~600 | 12 / 43 km | 24/34 |
| Akát (Robinie) | ~725 | 9 / 24 km | 32/34 |
| Lípa (Sommer-Linde) | ~850 | 9 / 20 km | 33/34 |
| Pampeliška (Löwenzahn) | ~990 | 9 / 20 km | 33/34 |
| Jabloň | – | – | ovoce má jiné kódy fází, dořešit |

## Cílové schéma (fact constellation)

- **Fakty:**
  - `fact_hive_minute` / `fact_hive_hourly` (úl × čas),
  - `fact_event`,
  - `fact_weather`, `fact_bloom_phenology`, `fact_vegetation`, `fact_crop_acres`, `fact_country_apiculture`.
- **Dimenze:**
  - `dim_geo`: úl → buňka → okres → spolková země → stát,
  - `dim_time`: minuta → hodina → den → týden → měsíc → sezóna → rok,
  - `dim_plant`: druh → medonosnost,
  - `dim_event_type`.
- Fakty se spojují jen přes sdílené (conformed) dimenze, nikdy napřímo.

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
