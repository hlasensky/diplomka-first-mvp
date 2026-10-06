---
citekey: al-fuqahaInternetThingsSurvey2015
title: "Internet of Things: A Survey on Enabling Technologies, Protocols, and Applications"
authors: Al-Fuqaha, Ala; Guizani, Mohsen; Mohammadi, Mehdi; Aledhari, Mohammed; Ayyash, Moussa
year: 2015
venue: IEEE Communications Surveys & Tutorials (vol. 17, no. 4, pp. 2347–2376)
kind: journal
status: candidate
verified: false
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts:
  - internet-of-things
  - iot-protocols
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/FUGJB8V4)

## TL;DR
Přehledový článek o Internetu věcí. Popisuje, jak se IoT definuje, jaký má tržní potenciál, jak vypadají vrstvené architektury a z jakých stavebních prvků se skládá (identifikace, senzory, komunikace, výpočet, služby, sémantika). Jádrem je souhrn protokolů IETF/IEEE/EPCglobal: aplikační (CoAP, MQTT, XMPP, AMQP, DDS), service discovery (mDNS, DNS-SD) a infrastrukturní (RPL, 6LoWPAN, IEEE 802.15.4, BLE, EPCglobal). Dále probírá výzvy (dostupnost, spolehlivost, bezpečnost aj.), vztah IoT k big data, cloudu a fog computingu a navrhuje inteligentní protokolovou bránu pro horizontální integraci.

## Klíčová tvrzení
- C1: Podle autorů se rostoucí počet fyzických objektů připojuje k internetu, čímž se realizuje [[internet-of-things]]; IoT umožňuje objektům „komunikovat“, sdílet informace a koordinovat rozhodnutí. Doménově specifické aplikace tvoří vertikální trhy, doménově nezávislé služby (všudypřítomné výpočty, analytika) horizontální trhy. Podle citovaného zdroje [1] (Cisco) počet objektů připojených k internetu v roce 2010 překonal počet lidí na Zemi. (s. 1, §I; s. 2, §I)
- C2: Odhady trhu převzaté z jiných zdrojů: do konce roku 2020 až 212 miliard nasazených chytrých objektů (IDC [9]); do roku 2022 má M2M provoz tvořit až 45 % celého internetového provozu ([1], [9], [10]); celkový roční ekonomický dopad IoT do roku 2025 se odhaduje na 2,7–6,2 bilionu USD (McKinsey [11]). Zdravotnické aplikace a související služby (m-Health, telecare) mají do roku 2025 vytvářet zhruba 1,1–2,5 bilionu USD růstu ročně. (s. 2, §II)
- C3: Navržené IoT architektury zatím nekonvergovaly k referenčnímu modelu. Základní je třívrstvý model (Application, Network, Perception), běžný je pětivrstvý model: Objects (perception) → Object Abstraction → Service Management (middleware) → Application → Business. Ve vrstvě Objects senzory měří např. teplotu, vlhkost či vibrace a data digitalizují (tady vznikají IoT big data); Business vrstva podporuje rozhodování na základě analýzy big data. Pětivrstvý model autoři považují za nejpoužitelnější. (s. 3, §III; s. 4, §III)
- C4: Autoři dělí [[iot-protocols]] do čtyř kategorií: aplikační, service discovery, infrastrukturní a „other influential“. Jako aplikační protokoly probírají CoAP, MQTT, XMPP, AMQP a DDS. CoAP (IETF CoRE) je RESTful protokol nad UDP pro zařízení s nízkým výkonem a ztrátovými linkami, se čtyřmi typy zpráv (confirmable, non-confirmable, reset, acknowledgement) a zabezpečením přes DTLS. (s. 7, §V–V-A1; s. 8, §V-A1–A2; s. 9, §V-A3–A4; s. 10, §V-A5)
- C5: MQTT představili v roce 1999 Andy Stanford-Clark (IBM) a Arlen Nipper (Arcom) a v roce 2013 byl standardizován v OASIS. Jde o publish/subscribe protokol nad TCP se třemi úrovněmi QoS a třemi komponentami (publisher, subscriber, broker), vhodný pro zařízení s omezenými prostředky na nespolehlivých linkách s nízkou propustností; varianta MQTT-SN mapuje MQTT na UDP pro senzorové sítě. (s. 8, §V-A2)
- C6: Podle citované studie [78] doručuje MQTT zprávy s nižším zpožděním než CoAP při nízké ztrátovosti paketů, při vysoké ztrátovosti je lepší CoAP; jiná studie [79] v prostředí smartphonu naměřila u CoAP menší spotřebu šířky pásma a RTT než u MQTT. Komplexní srovnání všech aplikačních protokolů podle autorů neexistuje a jedno doporučení pro všechny IoT aplikace dát nelze. (s. 10, §V-A Remarks)
- C7: Jako aplikační domény IoT článek uvádí chytrou domácnost, chytré budovy (BAS), inteligentní dopravní systémy, průmyslovou automatizaci, chytré zdravotnictví, chytré sítě (smart grid) a chytré město. Aplikační vrstva pokrývá vertikální trhy jako smart home, smart building, doprava, průmyslová automatizace a zdravotnictví. (s. 3, §III-D; s. 5–6, §IV-E)
- C8: Mezi klíčové výzvy IoT autoři řadí dostupnost, spolehlivost, mobilitu, výkon, škálovatelnost, interoperabilitu, bezpečnost, správu a důvěru; na základě přehledu literatury za nejvyšší prioritu považují bezpečnost a soukromí, po nich výkon, spolehlivost a správu. IoT generuje big data, na která běžné platformy (Apache Hadoop, SciDB) podle citované práce [166] sotva stačí; potřeba je analytika v reálném čase a jako slibné autoři označují real-time techniky, které zmenšují objem vstupních dat. (s. 16, §VI; s. 18, §VII-A; s. 26, §X-A)

## Vztah k mé práci


## Citovat pro


## Pozor
- Číslování stran: PDF strana N = tištěná strana N + 2346 (PDF 1–30 = s. 2347–2376 v časopise). V tvrzeních výše jsou PDF strany; při citaci v LaTeXu použij tištěné.
- PAGE_WARN s. 5 (tabulky I a II, kategorie služeb a začátek aplikací) a s. 25 (obr. 28, tabulka IX, část „Lessons Learned“) – shoda s OCR jen 0,84 / 0,76; C7 cituje s. 5 (souhrnná věta o doménách); citát z ní sedí s fulltextem i OCR, přesto ověř v PDF.
- Podíly jednotlivých aplikací na trhu do roku 2025 jsou jen v obr. 2 (s. 3), ne v textu – fulltext je neobsahuje.
- Všechna tržní čísla (C2) jsou převzatá z jiných zdrojů (IDC [9], Cisco [1], [10], McKinsey [11]); autoři je sami neměří. Pro práci psanou v roce 2026 jde o historické prognózy.
- Sekce VI (s. 17): v extrahovaném textu jsou nadpisy D. Performance, E. Management, F. Scalability, G. Interoperability přeházené kvůli dvousloupcové sazbě – pořadí a příslušnost odstavců ověř v PDF.
- Srovnání MQTT vs. CoAP (C6) je jen převzaté z citovaných prací [78], [79]; autoři vlastní měření nedělají.
- Kategorie služeb (identity-related, information aggregation, collaborative-aware, ubiquitous) jsou na s. 5 (PAGE_WARN).
- Zmíněný TSaaaS (s. 18, §VII-A) je služba pro analýzu časových řad senzorových dat nad Time Series Database – případně dohledat původní zdroj [169].
