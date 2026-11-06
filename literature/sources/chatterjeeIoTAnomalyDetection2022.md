---
citekey: chatterjeeIoTAnomalyDetection2022
title: "IoT anomaly detection methods and applications: A survey"
authors: "Chatterjee, Ayan; Ahmed, Bestoun S."
year: 2022
venue: "Internet of Things 19, 100568"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [anomaly-detection, internet-of-things]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/29T34HG9)

## TL;DR
Přehled [[anomaly-detection|detekce anomálií]] v [[internet-of-things|IoT]] nad 64 články z let 2019–2021: kategorizuje metody podle přístupu, aplikace, typu anomálie a latence a prochází aplikační domény (časové řady, stav strojů, senzory, smart city, bezpečnost sítí). Závěr: neexistuje jeden nejlepší obecný algoritmus a otevřenými problémy jsou chybějící anotovaná data, drift dat a integrace různých senzorů.

## Klíčová tvrzení
- C1: Metoda: nejde o systematický přehled, ale postup přebírá mnoho jeho technik; trendy klíčových slov z názvů 8348 článků (2011–2020), pak 2242 nalezených článků z let 2019 – 7/2021 → 1670 po odstranění duplicit a přehledů → 986 unikátních → 194 podrobněji posouzených → 64 vybraných; IEEE, Elsevier, Springer a MDPI tvoří 76,1 % publikací. (s. 4, §2.2; s. 5, §3; s. 6, §3.2)
- C2: Metody detekce anomálií v IoT dělí do čtyř kategorií: podle metody (geometrické, statistické, strojové a hluboké učení), podle aplikace (konstruktivní, destruktivní, čištění dat), podle typu anomálie (bodová, kontextová, kolektivní) a podle latence (online vs. offline). (s. 2, §2.1; s. 3, §2.1; s. 4, §2.1)
- C3: Anomálie jsou vzácné události, které se výrazně odchylují od běžného chování v jednom bodě, v určitém kontextu či časovém úseku (např. sezóna) nebo v celé datové sadě a vznikají z vnějších příčin, jako je porucha senzoru nebo útok; „normální“ chování se navíc v čase mění (např. změna obsazenosti domácnosti mění spotřebu). (s. 2, §1, §2.1)
- C4: Většina publikací spadá do bezpečnosti sítí a infrastruktury, monitorování senzorů, chytré domácnosti a smart city; podle autorů neexistuje jeden nejlepší obecný algoritmus, ale řada metod specifických pro danou aplikaci. (s. 1, Abstract; s. 12, §5)
- C5: Otevřené problémy: získat anotovaná data je drahé a ne vždy možné, proto jsou žádoucí samo-, polo- a neřízené online metody; integrace dat z více typů senzorů; drift dat a konceptu (model by se měl proaktivně přizpůsobovat) a augmentace dat tam, kde chybí dostatek dat. (s. 12, §5; s. 13, §5)

## Vztah k mé práci


## Citovat pro


## Pozor
- Výběr 64 článků je jen z let 2019 – 7/2021, s důrazem na co nejodlišnější aplikační domény; velká část jsou bezpečnostní aplikace (útoky, botnety), které se mé práce netýkají.
- Sekce 4 je převážně výčet jednotlivých článků (jedna věta – jedna metoda); pro konkrétní metodu citovat primární zdroj.
- Pro detekci anomálií v časových řadách z IoT je možná přímější zdroj, který článek cituje: Cook, Mısırlı, Fan – Anomaly Detection for IoT Time-Series Data: A Survey, IEEE IoT Journal 7(7), 2020 (ref. [9], neověřeno).
- Číslování stran PDF odpovídá číslům stran článku (1–17).
