---
citekey: sengerWeightTemperatureHumidity2024
title: "Weight, Temperature and Humidity Sensor Data of Honey Bee Colonies in Germany, 2019–2022"
authors: "Senger, Diren; Gruber, Clemens; Kluss, Thorsten; Johannsen, Carolin"
year: 2024
venue: "Data in Brief 52, 110015"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [hive-monitoring, internet-of-things, colony-loss, anomaly-detection]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/AL224BGC)

## TL;DR
Datový článek k datasetu projektu BeeObserver: senzorová data (5 vnitřních teplot, venkovní teplota, teplota/vlhkost/tlak z BME280 a váha) ze 78 včelstev v Německu za roky 2019–2022, doplněná o záznamy z prohlídek, které včelaři zapisovali do webové aplikace. Popisuje DIY senzorovou sadu, vzorkování a agregace (surová data, minuta, hodina, den), strukturu adresářů na Zenodu, předzpracování (prahové vyřazení chybných hodnot, korekce skoků ve váze) a omezení dat.

## Klíčová tvrzení
- C1: Dataset obsahuje senzorová data ze 78 včelstev v Německu sebraná v rámci občanského vědeckého (citizen science) projektu BeeObserver ([[hive-monitoring]]); data mají pomoci pochopit vývoj a zdraví včelstev a dají se zapojit do systémů pro podporu rozhodování a varování včelařů. (s. 1, §Abstract; s. 8, §3.3)
- C2: Každý úl měl 5 vnitřních teplotních čidel DS18B20 v každé druhé uličce mezi rámky (t_i_1 … t_i_5, t_i_3 uprostřed, t_i_1 a t_i_5 na okraji), jedno venkovní DS18B20 (t_o), senzor BME280 mezi rámky (teplota t, relativní vlhkost h, tlak p) a jednobodový tenzometr Bosche H30/H40 s převodníkem HX711 pod úlem (weight_kg). (s. 5, §2.1, Tab. 1; s. 7, §3.1)
- C3: Jde o nízkonákladovou DIY sadu ([[internet-of-things]]): čidla jsou připojena k desce s mikrokontrolérem ESP32 (FiPy od Pycom) ve vodotěsné krabičce mimo úl, měří se každých 5–10 s, data se výchozím způsobem posílají přes WLAN na centrální server a ukládají do časově-řadové databáze InfluxDB. (s. 7–8, §3.1)
- C4: Kromě surových dat (interval 5–10 s) poskytují autoři agregace: minutová data jako medián všech měření v dané minutě a hodinová a denní data jako průměr minutových hodnot; nezpracovaná (unprocessed) data existují jen pro minutový interval a surová data. (s. 9, §3.4)
- C5: Data jsou na Zenodu uspořádána dvojím způsobem: složka years (2019 až 2022) a složka events se 3měsíčními úseky před pozorovanou událostí (rojení, úhyn včelstva) a stejně dlouhými úseky z podobného období roku od včelstev bez této události; každá složka má podsložky unprocessed a processed, zpracovaná data jsou v intervalech _m, _h a _d a každé včelstvo má vlastní CSV soubor pojmenovaný klíčem úlu (u událostí i časem události). (s. 5–6, §2.2, Fig. 2)
- C6: Prohlídky včelaři zapisovali ve webové aplikaci (fork open-source platformy BEEP, data v MySQL), celkem přes 2600 prohlídek; do senzorových dat bylo sloučeno 6 stavů a událostí (matečník, rojení, přikrmování, medobraní, léčení, úhyn [[colony-loss]]), pro každou 4 sloupce: časové razítko posledního a příštího výskytu a jejich časová vzdálenost v sekundách. (s. 6, §2.3, Tab. 2; s. 8, §3.2)
- C7: Předzpracování: ruční vyřazení období bez kalibrované váhy nebo nedokončené instalace, vyřazení hodnot váhy nad 150 kg a pod −50 kg, teploty nad 85 °C a pod −40 °C a vlhkosti mimo 0–100 (chyby senzorů; prahové [[anomaly-detection]]) a korigovaná váha (weight_kg_noOutlier), která vynechá změny větší než 0,3 kg za minutu (obvykle zásahy včelaře, např. přidání či odebrání nástavků nebo kameny zatěžující úl proti větru) a vzniká kumulativním součtem, takže začíná na 0 kg. (s. 9, §3.4; s. 6–7, §2.3, Tab. 3)
- C8: Omezení: souřadnice včelnic jsou kvůli ochraně proti krádežím a vandalismu zaokrouhleny na jedno desetinné místo (přesnost 5–7 km ve směru zeměpisné délky pro střední Evropu), interval prohlídek se mezi včelstvy liší a včelař mohl důležitou událost (např. rojení) přehlédnout, některá včelstva nemají žádná nebo jen omezená metadata, a projekt neměl výběrovou strategii (např. podle polohy). (s. 10, §Limitations; s. 8, §3.3)

## Obrázky
- Obr. 1 (s. 4) – rozmístění senzorů v úlu: čidla DS18B20 (1), tenzometr (2), BME280 (3), mikrokontrolér (4) ![[figures/sengerWeightTemperatureHumidity2024/fig1.png]]

## Vztah k mé práci


## Citovat pro


## Pozor
- Úroveň 1 – hlavní dataset práce (BeeObserver). Data: Zenodo, https://doi.org/10.5281/zenodo.10407693.
- Nesoulad DOI datasetu: v „Data accessibility“ (s. 3) je „Data identification number: 10.5281/zenodo.8389137“, ale přímá URL je https://zenodo.org/records/10407693 a reference [1] (s. 11) uvádí doi:10.5281/zenodo.10407693. Ověřeno na Zenodu (2026-10-30): 10.5281/zenodo.8389137 je concept DOI (všechny verze), 10.5281/zenodo.10407693 je verze v2 z 20. 12. 2023, podle API poslední. Pro reprodukovatelnost citovat DOI verze, kterou jsi stáhl.
- Nesoulad intervalu měření: abstrakt (s. 1) píše „measurement interval of up to 5 s“, tabulka specifikací (s. 2) a §3.1/§3.4 (s. 8–9) „5–10 s“ (s. 9 i „usually 5 or 10 s“). V C3/C4 použito 5–10 s.
- Licence: článek je open access pod CC BY-NC-ND 4.0 (s. 1–2). Licenci samotného datasetu článek neuvádí a záznam na Zenodu ji také neuvádí (jen „Open“, ověřeno 2026-10-30). Podmínky použití případně vyjasnit s autory.
- Počet včelstev 78 (abstrakt, s. 1; tabulka lokalit na s. 2–3 má 78 řádků s klíči úlů). Počet různých včelnic článek neuvádí; tabulka má jen zaokrouhlené souřadnice, které se u mnoha včelstev opakují.
- Mezery v datech článek nekvantifikuje (žádné procento chybějících hodnot); zmiňuje jen sloupec no_jump (dostupnost předchozího minutového měření, Tab. 3, s. 7), soubor all_info.csv s počátečními a koncovými daty použitými k vyřazení testovacích měření (s. 7) a omezená metadata u některých včelstev (s. 10).
- Soubory s inspekcemi: dump_june_2023_rounded_coordinates.csv (originál), wideJune23.csv (wide formát), all_info.csv (s. 7); hodinová/denní zpracovaná data obsahují zprůměrované hodnoty (s. 7).
- PAGE_WARN s. 1 (abstrakt, dvousloupcová titulní strana) – C1 ověřen proti vyrenderované stránce PDF, text sedí.
- Tabulky 1–3 a Fig. 2 (strom adresářů) byly v textovém extraktu rozházené; ve fulltextu jsou ručně přepsané z PDF v blocích `[Table N – ruční přepis z PDF]` / `[Fig. 2 – ruční přepis z PDF]`. Čísla stran = PDF strany = tištěné strany.
- Datový článek (Data in Brief): neobsahuje analýzu ani výsledky, jen popis dat; financováno BMBF (s. 10).
