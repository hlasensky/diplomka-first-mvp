---
type: concept
aliases: [MQTT, CoAP, AMQP, XMPP, DDS, 6LoWPAN, IoT protokoly, publish/subscribe]
---

Komunikační protokoly pro IoT zařízení s omezenými prostředky, od aplikační vrstvy (publish/subscribe a RESTful zasílání zpráv) po síťovou a linkovou vrstvu (6LoWPAN, RPL, IEEE 802.15.4, BLE).

## Sources
- [[al-fuqahaInternetThingsSurvey2015]] — C4: dělí IoT protokoly na aplikační (CoAP, MQTT, XMPP, AMQP, DDS), service discovery, infrastrukturní a ostatní; C5–C6: MQTT jako publish/subscribe nad TCP a srovnání s CoAP.
- [[atzoriInternetThingsSurvey2010]] — C3: WSN nad IEEE 802.15.4 a překážky jejich integrace do IP (127 B paket, 102 oktetů MAC rámec, spánek uzlů); C5: TCP podle autorů pro IoT nevhodný (navazování spojení, řízení zahlcení, bufferování).

## Napětí
- [[atzoriInternetThingsSurvey2010]] C5 vs. [[al-fuqahaInternetThingsSurvey2015]] C5: Atzori (2010) považuje TCP pro IoT za nevhodný, Al-Fuqaha (2015) popisuje MQTT nad TCP jako vhodný pro zařízení s omezenými prostředky. Mezi články je pět let.

## Související
- [[internet-of-things]]
