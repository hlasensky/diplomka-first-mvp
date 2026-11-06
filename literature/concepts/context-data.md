---
type: concept
aliases: [context data, contextual data, kontextová data, kontext měření, environmental data, auxiliary data]
---

Data, která nejsou měřena samotným zařízením, ale dávají jeho měřením kontext – počasí, fenologie, vegetace, využití krajiny, administrativní členění, národní statistiky. V OLAP se připojují jako samostatné fakty přes sdílené dimenze (místo, čas).

## Sources
- [[hersbachERA5GlobalReanalysis2020]] — reanalýza ERA5 jako zdroj hodinového počasí pro lokality úlů (bez tvrzení, úroveň nástroje).
- [[zippenfenigOpenMeteocomWeatherAPI2024]] — Open-Meteo Historical Weather API, přes které se ERA5 stahuje (nástroj).
- [[kasparOverviewPhenologicalObservation2015]] — fenologická síť a databáze DWD, zdroj začátku kvetení (nástroj).
- [[didanMOD13Q1MODISTerra2015]] — vegetační index NDVI z MODIS MOD13Q1 (dataset).
- [[statistischeaemterdesbundesundderlaenderRegionaldatenbankDeutschlandTabellen]] — plochy a výnosy plodin po okresech (dataset).
- [[bundesamtfuerkartographieundgeodaesieVerwaltungsgebiete12502026]] — administrativní hranice okresů a spolkových zemí VG250 (dataset).
- [[foodandagricultureorganizationoftheunitednationsFAOSTATCropsLivestock]] — národní počty úlů a produkce medu (dataset).

## Související
- [[hive-monitoring]]
- [[olap]]
- [[internet-of-things]]
