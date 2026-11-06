---
type: concept
aliases: [IoT, Internet of Things, Internet věcí, smart devices, chytrá zařízení, M2M]
---

Síť fyzických objektů vybavených senzory a aktuátory, které jsou připojené k internetu, vyměňují si data a na jejich základě poskytují služby bez přímého zásahu člověka.

## Sources
- [[al-fuqahaInternetThingsSurvey2015]] — C1: IoT jako fyzické objekty připojené k internetu, které sdílejí informace a koordinují rozhodnutí; přehled architektury (C3), domén (C7) a výzev (C8).
- [[sengerWeightTemperatureHumidity2024]] — C3: nízkonákladová DIY senzorová sada v úlu (ESP32/FiPy, přenos přes WLAN, ukládání do InfluxDB), měření každých 5–10 s.
- [[greengardInternetThings2015]] — C1: IoT jako „věci“ s UID a IP adresou propojené s internetem i mezi sebou; C2: connected devices, physical-first/digital-first, Industrial Internet (M2M, H2M, M2S), IoE; C3: termín zavedl Kevin Ashton (Auto-ID Center, MIT) v roce 1999, RFID jako předchůdce IoT.
- [[jensenTimeSeriesManagement2017]] — C1: nasazení senzorů od IoT zařízení po kyberfyzikální systémy produkuje velké objemy časových řad, pro které jsou obecné RDBMS podle autorů nevhodné.
- [[dobsonReferenceArchitectureModel2018]] — C1: hodnota dat ze senzorů a IoT plyne z dlouhodobých trendů, ale bez zaznamenaného kontextu (kalibrace, stárnutí, údržba) se data při analýze stávají čím dál zavádějícími.
- [[johnApplicationTimeSeries2023]] — C1, C4: data z IoT zařízení ve smart city jako časové řady; nasazení TSDB v platformě Logimic.
- [[chatterjeeIoTAnomalyDetection2022]] — C4: většina prací o detekci anomálií v IoT míří na bezpečnost sítí, monitorování senzorů, chytrou domácnost a smart city.

## Napětí
- [[greengardInternetThings2015]] C5 vs. [[al-fuqahaInternetThingsSurvey2015]] C2: prognóza k roku 2020 – přes 50 miliard připojených zařízení (Cisco) vs. až 212 miliard nasazených chytrých objektů (IDC). Liší se zdroj i to, co se počítá.

## Související
- [[iot-protocols]]
- [[hive-monitoring]]
