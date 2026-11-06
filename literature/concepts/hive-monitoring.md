---
type: concept
aliases: [hive monitoring, precision beekeeping, sensor hives, smart hive, BeeObserver, monitoring úlů, senzorové úly, chytrý úl]
---

Průběžné měření stavu včelstva senzory umístěnými v úlu nebo pod ním (teplota, vlhkost, váha aj.), obvykle doplněné o záznamy včelaře z prohlídek.

## Sources
- [[sengerWeightTemperatureHumidity2024]] — C1–C3, C6: dataset BeeObserver, 78 včelstev v Německu 2019–2022, 5 vnitřních teplot + venkovní teplota + BME280 + váha, měření každých 5–10 s, sloučeno se 6 událostmi z prohlídek.
- [[hadjurIntelligentEfficientBeehive2022]] — C1–C3: přehled precizního včelařství (86 publikací); připojený úl = senzory + mikrokontrolér + baterie + odesílání na server; včelaři používají hlavně váhu a vnitřní/vnější teplotu a vlhkost; 8 kategorií služeb (počítání včel, rojení, škůdci, med, zdravotní stavy aj.).
- [[meikleApplicationContinuousMonitoring2015]] — C1–C5: přehled průběžného monitoringu (hodinově a déle než 2 dny); informativní jsou změny váhy, ne okamžitá váha; denní cyklus váhy (noční úbytek, přírůstek ze snůšky přes den), detrendování 25h klouzavým průměrem + sinusovky; teplota závisí na poloze čidla vůči plodišti.
- [[zacepinsChallengesDevelopmentPrecision2015]] — C1–C3, C5: definice precizního včelařství a jeho tří fází (sběr dat, analýza, aplikace); skupiny měřených parametrů (včelnice, včelstvo, jednotlivé včely), co lze vyčíst z teploty a váhy a jejich omezení (vliv okolní teploty, vlhkost dřevěných úlů, rozlišení 100 g nestačí v zimě); PB se nerozšířilo kvůli nejasné návratnosti, složitosti a nevyzrálým DSS.
- [[sengerWeightTemperatureHumidity2023]] — dataset BeeObserver na Zenodu (minutová data, prohlídky); citovat jako zdroj dat, tvrzení z článku [[sengerWeightTemperatureHumidity2024]].

## Napětí

## Související
- [[internet-of-things]]
- [[colony-loss]]
- [[anomaly-detection]]
