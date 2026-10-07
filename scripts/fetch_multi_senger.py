"""Download the raw sources of the `multi-senger` dataset pack into data/raw/multi-senger/.

Each source writes its files and a MANIFEST.json entry (URL, access date, sha256), so the
build is reproducible and the thesis can cite every dataset with version and access date.
Sources that cannot be fetched automatically (Regionalstatistik needs an account, COLOSS
numbers live in papers) are listed in docs/data.md and added by hand.

    uv run --with remotezip python scripts/fetch_multi_senger.py [source ...]

Sources: bob_minute, geo, weather, phenology, ndvi, faostat, eurostat, crops (default: all).
`meta` only refreshes descriptions and licences in MANIFEST.json.
Re-running skips files that already exist.
"""

import csv
import hashlib
import io
import json
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "multi-senger"
SENGER_DB = ROOT / "data" / "senger.duckdb"
MANIFEST = RAW / "MANIFEST.json"

START, END = "2019-06-01", "2022-12-31"           # sensor coverage: 6/2019 - 12/2022
# ORNL answers 500 to requests without an Accept header (urllib sends none by default)
UA = {"User-Agent": "diplomka-thesis-fetch/1.0 (academic use)", "Accept": "application/json, text/csv, */*"}


# Description and licence per source, written into MANIFEST.json (checked 2026-10-06).
META = {
    "bob_minute": {
        "description": "BeeObserver: 1-minute preprocessed hive sensor data (weight, 5 in-hive temperatures, outside "
                       "temperature, humidity, pressure) of 78 colonies in Germany 2019-2022, plus beekeeper inspections.",
        "license": "not stated in the Zenodo record; dataset paper is open access in Data in Brief - cite the paper "
                   "and ask the authors before redistributing the data",
        "license_url": "https://doi.org/10.5281/zenodo.10407693",
        "citation": "Senger D., Gruber C., Kluss T., Johannsen C. (2024): Weight, temperature and humidity sensor data of "
                    "honey bee colonies in Germany, 2019-2022. Data in Brief 52, 110015. doi:10.1016/j.dib.2023.110015",
    },
    "geo": {
        "description": "BKG VG250 Ebenen (31.12.): administrative boundaries of Germany (states, districts, "
                       "municipalities) as GeoPackage, UTM32s; used for cell -> district -> state.",
        "license": "Datenlizenz Deutschland - Namensnennung - Version 2.0 (dl-de/by-2-0)",
        "license_url": "https://www.govdata.de/dl-de/by-2-0",
        "citation": "© GeoBasis-DE / BKG (2025), VG250",
    },
    "weather": {
        "description": "Hourly weather reanalysis (ERA5) at each hive cell via the Open-Meteo Historical Weather API: "
                       "temperature, precipitation, rain, wind speed, shortwave radiation, relative humidity.",
        "license": "CC BY 4.0 (Open-Meteo); underlying ERA5 data: Copernicus Climate Change Service licence",
        "license_url": "https://open-meteo.com/en/license",
        "citation": "Weather data by Open-Meteo.com; Hersbach et al. (2020), The ERA5 global reanalysis, QJRMS 146:1999-2049",
    },
    "phenology": {
        "description": "DWD phenological observations (annual reporters, historical): flowering dates of winter rape, "
                       "black locust, small-leaved lime, dandelion; station list and phase/plant code tables.",
        "license": "CC BY 4.0 (DWD Climate Data Center terms of use, May 2024)",
        "license_url": "https://opendata.dwd.de/climate_environment/CDC/Terms_of_use.pdf",
        "citation": "Deutscher Wetterdienst, Climate Data Center; Kaspar et al. (2014), Adv. Sci. Res. 11:93-99",
    },
    "ndvi": {
        "description": "MODIS Terra MOD13Q1 16-day NDVI (250 m) at each hive cell centroid via the ORNL DAAC MODIS web "
                       "service, 2019-2022.",
        "license": "NASA EOSDIS / LP DAAC data: no restrictions on use, sale or redistribution (citation requested)",
        "license_url": "https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance",
        "citation": "Didan K. (2015/2021), MOD13Q1 MODIS/Terra Vegetation Indices 16-Day L3 Global 250m SIN Grid, "
                    "NASA LP DAAC; ORNL DAAC MODIS Land Product Subsets web service",
    },
    "faostat": {
        "description": "FAOSTAT Crops and livestock products (QCL), Germany: Bees (stocks = number of hives) and "
                       "Natural honey (production, t), yearly.",
        "license": "CC BY 4.0 (FAO statistical database terms of use)",
        "license_url": "https://www.fao.org/contact-us/terms/db-terms-of-use",
        "citation": "FAO (2025), FAOSTAT: Crops and livestock products",
    },
    "eurostat": {
        "description": "Eurostat ef_lsk_bees: beehives on farms by NUTS 2 region (farm structure survey years only), "
                       "Germany.",
        "license": "Eurostat reuse policy - free reuse with source acknowledgement (CC BY 4.0)",
        "license_url": "https://ec.europa.eu/eurostat/help/copyright-notice",
        "citation": "Eurostat (2025), Beehives on farms by NUTS 2 region (ef_lsk_bees)",
    },
    "crops": {
        "description": "Regionalstatistik, districts (Kreise und krfr. Städte), manual CSV exports. "
                       "41141-02-02-4_<year>: arable land by crop type incl. winter rape, hectares, "
                       "Agrarstrukturerhebung / Landwirtschaftszählung 2016 and 2020 (holding-seat principle). "
                       "41241-01-03-4_<years>: yields (dt/ha) of 10 crops incl. winter rape, Erntestatistik, "
                       "yearly 2016-2025. '.' = suppressed (confidential), '-' = nothing.",
        "license": "Datenlizenz Deutschland - Namensnennung - Version 2.0 (dl-de/by-2-0)",
        "license_url": "https://www.govdata.de/dl-de/by-2-0",
        "citation": "© Statistische Ämter des Bundes und der Länder, Deutschland, 2026 (Regionaldatenbank, Tabellen "
                    "41141-02-02-4 and 41241-01-03-4)",
    },
}


def apply_meta() -> None:
    """Add description / licence / citation to every MANIFEST entry (no re-download)."""
    if not MANIFEST.exists():
        return
    data = json.loads(MANIFEST.read_text())
    for name, entry in data.items():
        entry.update(META.get(name, {}))
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def manifest_add(name: str, url: str, files: list[Path], note: str = "") -> None:
    data = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    data[name] = {
        "url": url,
        "accessed": date.today().isoformat(),
        "note": note,
        "files": {str(f.relative_to(RAW)): hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
        **META.get(name, {}),
    }
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def get(url: str, retries: int = 6) -> bytes:
    import urllib.error
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if attempt == retries - 1:
                raise
            # 429 = rate limit (Open-Meteo weights long hourly requests as many calls): back off for a minute+
            time.sleep(65 * (attempt + 1) if e.code == 429 else 10 * (attempt + 1))
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(url)


def cells() -> list[tuple[str, float, float]]:
    with duckdb.connect(str(SENGER_DB), read_only=True) as con:
        return con.execute("SELECT cell_id, lat, lon FROM dim_cell ORDER BY cell_id").fetchall()


# --------------------------------------------------------------------------- sources

def bob_minute() -> None:
    """1-minute preprocessed sensor files (+ inspections) from the BeeObserver Zenodo archive.
    Only the needed members are fetched with HTTP range requests (~1.8 GB of the 5.6 GB zip)."""
    from remotezip import RemoteZip

    url = "https://zenodo.org/api/records/10407693/files/bob_publication_data.zip/content"
    out = RAW / "bob"
    pre = "bob_publication_data/"
    files = []
    with RemoteZip(url) as z:
        members = [i for i in z.infolist() if not i.is_dir() and (
            ("/years/" in i.filename and "/preprocessed/" in i.filename and "_m/" in i.filename
             and i.filename.endswith(".csv"))
            or (i.filename.startswith(pre + "inspections/") and ".~lock" not in i.filename)
            or i.filename == pre + "readme.txt")]
        for n, i in enumerate(members, 1):
            dest = out / i.filename[len(pre):]
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                with z.open(i) as src, open(dest, "wb") as f:
                    f.write(src.read())
            files.append(dest)
            if n % 20 == 0:
                print(f"  bob_minute {n}/{len(members)}", flush=True)
    manifest_add("bob_minute", "https://doi.org/10.5281/zenodo.10407693", [f for f in files if f.suffix != ".csv"],
                 f"{len(files)} files (1-minute preprocessed + inspections); csv hashes omitted for size")


def geo() -> None:
    url = "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_1231/aktuell/vg250_12-31.utm32s.gpkg.ebenen.zip"
    dest = RAW / "geo" / "vg250_ebenen.zip"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(get(url))
    with zipfile.ZipFile(dest) as z:
        z.extractall(dest.parent)
    manifest_add("geo", url, [dest], "BKG VG250 Ebenen 31.12., GeoPackage UTM32s; licence dl-de/by-2-0")


def weather() -> None:
    hourly = "temperature_2m,precipitation,rain,wind_speed_10m,shortwave_radiation,relative_humidity_2m"
    files = []
    for cell_id, lat, lon in cells():
        dest = RAW / "weather" / f"{cell_id}.csv"
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "start_date": START, "end_date": END,
                                        "hourly": hourly, "timezone": "UTC", "format": "csv"})
            dest.write_bytes(get(f"https://archive-api.open-meteo.com/v1/archive?{q}"))
            time.sleep(8)                                 # stay under the free-tier minute limit
        files.append(dest)
    manifest_add("weather", "https://archive-api.open-meteo.com/v1/archive", files,
                 f"ERA5 via Open-Meteo, hourly {hourly}, UTC, {START}..{END}, one file per cell")


def phenology() -> None:
    base = "https://opendata.dwd.de/climate_environment/CDC/"
    obs = base + "observations_germany/phenology/annual_reporters/"
    sources = {
        "Winterraps.txt": obs + "crops/historical/PH_Jahresmelder_Landwirtschaft_Kulturpflanze_Winterraps_1934_2024_hist.txt",
        "Robinie.txt": obs + "wild/historical/PH_Jahresmelder_Wildwachsende_Pflanze_Robinie_1935_2024_hist.txt",
        "Sommer-Linde.txt": obs + "wild/historical/PH_Jahresmelder_Wildwachsende_Pflanze_Sommer-Linde_1925_2024_hist.txt",
        "Loewenzahn.txt": obs + "wild/historical/PH_Jahresmelder_Wildwachsende_Pflanze_Loewenzahn_1925_2024_hist.txt",
        "stations.txt": base + "help/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt",
        "phases.txt": base + "help/PH_Beschreibung_Phase.txt",
        "plants.txt": base + "help/PH_Beschreibung_Pflanze.txt",
    }
    files = []
    for name, url in sources.items():
        dest = RAW / "phenology" / name
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            # DWD files are latin-1; store as UTF-8 so DuckDB reads them directly
            dest.write_text(get(url).decode("latin-1"), encoding="utf-8")
        files.append(dest)
    manifest_add("phenology", obs, files, "DWD annual reporters, historical; converted latin-1 -> UTF-8")


def ndvi() -> None:
    api = "https://modis.ornl.gov/rst/api/v1/MOD13Q1"
    files = []
    all_cells = cells()
    # MOD13Q1 composites follow one global 16-day calendar, so the date list is fetched once
    _, lat0, lon0 = all_cells[0]
    dates = json.loads(get(f"{api}/dates?latitude={lat0}&longitude={lon0}"))["dates"]
    dates = [d["modis_date"] for d in dates if START[:4] <= d["calendar_date"][:4] <= END[:4]]
    for cell_id, lat, lon in all_cells:
        dest = RAW / "ndvi" / f"{cell_id}.csv"
        if not dest.exists():
            rows = []
            for i in range(0, len(dates), 10):                 # the service returns max 10 dates per call
                q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "band": "250m_16_days_NDVI",
                                            "startDate": dates[i], "endDate": dates[min(i + 9, len(dates) - 1)],
                                            "kmAboveBelow": 0, "kmLeftRight": 0})
                data = json.loads(get(f"{api}/subset?{q}"))
                scale = float(data.get("scale") or 0.0001)
                for s in data.get("subset", []):
                    raw = s["data"][0]
                    rows.append((s["calendar_date"], raw, round(raw * scale, 4) if raw > -3000 else None))
                time.sleep(0.5)
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["date", "ndvi_raw", "ndvi"])
                w.writerows(sorted(set(rows)))
        files.append(dest)
    manifest_add("ndvi", api, files, "MOD13Q1 250m_16_days_NDVI, pixel at cell centroid, scale 0.0001, fill <= -3000")


def faostat() -> None:
    url = "https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip"
    dest = RAW / "faostat" / "germany_bees.csv"
    if not dest.exists():
        z = zipfile.ZipFile(io.BytesIO(get(url)))
        name = next(n for n in z.namelist() if n.endswith(".csv") and "All_Data" in n)
        with z.open(name) as src:
            reader = csv.DictReader(io.TextIOWrapper(src, encoding="latin-1"))
            keep = [r for r in reader if r["Area"] == "Germany" and (r["Item"] == "Bees" or "honey" in r["Item"].lower())]
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(keep[0].keys()))
            w.writeheader()
            w.writerows(keep)
    manifest_add("faostat", url, [dest], "FAOSTAT QCL normalized, filtered to Germany, items Bees (stocks = hives) + Natural honey")


def eurostat() -> None:
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ef_lsk_bees?geo=DE&lang=en"
    dest = RAW / "eurostat" / "ef_lsk_bees_DE.json"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(get(url))
    manifest_add("eurostat", url, [dest], "Beehives on farms (farm structure survey years only), Germany")


def crops() -> None:
    """Manual source: Regionalstatistik needs an account for its API, so the CSVs are exported in the web UI
    (www.regionalstatistik.de, Werteabruf -> CSV) and saved to data/raw/multi-senger/crops/<table>.csv."""
    files = sorted((RAW / "crops").glob("*.csv"))
    if not files:
        print("  crops: no CSV in data/raw/multi-senger/crops/ - export it from regionalstatistik.de by hand")
        return
    manifest_add("crops", "https://www.regionalstatistik.de", files,
                 "manual export from the Regionaldatenbank web UI (latin-1 CSV with header/footer lines)")


SOURCES = {"bob_minute": bob_minute, "geo": geo, "weather": weather, "phenology": phenology,
           "ndvi": ndvi, "faostat": faostat, "eurostat": eurostat, "crops": crops}

if __name__ == "__main__":
    RAW.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["meta"]:
        apply_meta()
        sys.exit(0)
    for name in sys.argv[1:] or list(SOURCES):
        t = time.monotonic()
        print(f"[{name}] ...", flush=True)
        SOURCES[name]()
        print(f"[{name}] done in {time.monotonic() - t:.0f}s", flush=True)
