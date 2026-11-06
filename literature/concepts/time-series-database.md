---
type: concept
aliases: [time series database, TSDB, time series management system, TSMS, časově-řadová databáze, databáze časových řad, InfluxDB, TimescaleDB]
---

Systém vyvinutý nebo rozšířený pro ukládání a dotazování dat ve formě časových řad (posloupností datových bodů uspořádaných podle času), typicky senzorových dat.

## Sources
- [[jensenTimeSeriesManagement2017]] — C2, C4: definice TSMS a klasifikace systémů do tří architektur (interní úložiště, externí DBMS/DFS, rozšíření RDBMS); C5: kompromisy architektur; C8: výzkumné směry a vize s datovou kostkou nad modely časových řad.
- [[sengerWeightTemperatureHumidity2024]] — C3: senzorová data BeeObserver se ukládala na centrálním serveru do časově-řadové databáze InfluxDB.
- [[johnApplicationTimeSeries2023]] — C2–C3: srovnání PostgreSQL, DynamoDB, MongoDB a InfluxDB na IoT datech (350MB sada: PostgreSQL 787 MB vs. InfluxDB 69 MB); C4: přechod platformy Logimic z DynamoDB na InfluxDB; C5: omezení InfluxDB.
- [[raasveldtDuckDBEmbeddableAnalytical2019]] — nástroj: sloupcová vestavěná analytická databáze použitá pro datový pack; alternativa k TSDB (bez tvrzení).

## Související
- [[internet-of-things]]
- [[olap]]
- [[hive-monitoring]]
