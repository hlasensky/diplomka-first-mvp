---
type: concept
aliases: [IoT, Internet of Things, Internet věcí, smart devices, chytrá zařízení, M2M]
---

Síť fyzických objektů vybavených senzory a aktuátory, které jsou připojené k internetu, vyměňují si data a na jejich základě poskytují služby bez přímého zásahu člověka.

## Sources
- [[al-fuqahaInternetThingsSurvey2015]] — C1: IoT jako fyzické objekty připojené k internetu, které sdílejí informace a koordinují rozhodnutí; přehled architektury (C3), domén (C7) a výzev (C8).
- [[atzoriInternetThingsSurvey2010]] — C1: IoT jako všudypřítomné, jednoznačně adresovatelné objekty (RFID, senzory, aktuátory, telefony), které spolupracují na společných cílech; C2: IoT jako průnik vizí „Things“, „Internet“ a „Semantic“; C4: SOA middleware; C5: aplikační domény a otevřené problémy.
- [[sengerWeightTemperatureHumidity2024]] — C3: nízkonákladová DIY senzorová sada v úlu (ESP32/FiPy, přenos přes WLAN, ukládání do InfluxDB), měření každých 5–10 s.
- [[hadjurIntelligentEfficientBeehive2022]] — C1: IoT v precizním včelařství; připojený úl jako standardní úl se senzory připojenými k mikrokontroléru, napájený z baterie a obvykle posílající data na vzdálený server.
- [[greengardInternetThings2015]] — C1: IoT jako „věci“ s UID a IP adresou propojené s internetem i mezi sebou; C2: connected devices, physical-first/digital-first, Industrial Internet (M2M, H2M, M2S), IoE; C3: termín zavedl Kevin Ashton (Auto-ID Center, MIT) v roce 1999, RFID jako předchůdce IoT.
- [[jensenTimeSeriesManagement2017]] — C1: nasazení senzorů od IoT zařízení po kyberfyzikální systémy produkuje velké objemy časových řad, pro které jsou obecné RDBMS podle autorů nevhodné.
- [[dobsonReferenceArchitectureModel2018]] — C1: hodnota dat ze senzorů a IoT plyne z dlouhodobých trendů, ale bez zaznamenaného kontextu (kalibrace, stárnutí, údržba) se data při analýze stávají čím dál zavádějícími.
- [[johnApplicationTimeSeries2023]] — C1, C4: data z IoT zařízení ve smart city jako časové řady; nasazení TSDB v platformě Logimic.
- [[chatterjeeIoTAnomalyDetection2022]] — C4: většina prací o detekci anomálií v IoT míří na bezpečnost sítí, monitorování senzorů, chytrou domácnost a smart city.

## Napětí
- [[greengardInternetThings2015]] C5 vs. [[al-fuqahaInternetThingsSurvey2015]] C2: prognóza k roku 2020 – přes 50 miliard připojených zařízení (Cisco) vs. až 212 miliard nasazených chytrých objektů (IDC). Liší se zdroj i to, co se počítá.
- [[atzoriInternetThingsSurvey2010]] C4 vs. [[al-fuqahaInternetThingsSurvey2015]] C3: oba konstatují, že referenční vrstvená architektura IoT chybí, ale navrhují jiné vrstvy. Atzori má SOA middleware (Applications, Service composition, Service management, Object abstraction a průřezovou správu důvěry, soukromí a bezpečnosti), Al-Fuqaha pětivrstvý model s vrstvou Business nahoře.

## Související
- [[iot-protocols]]
- [[hive-monitoring]]
