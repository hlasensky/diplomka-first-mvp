---
citekey: willardEfficientGuidedGeneration2023
title: "Efficient Guided Generation for Large Language Models"
authors: "Willard, Brandon T.; Louf, Rémi"
year: 2023
venue: "arXiv preprint arXiv:2307.09702"
kind: preprint   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [structured-output]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/GZCGGIV6)

## TL;DR
Článek přeformuluje řízené (omezené) generování textu LLM jako přechody mezi stavy konečného automatu: regulární výraz se převede na FSM a slovník modelu se předem zaindexuje tak, že pro každý stav je hned známa množina povolených tokenů, takže maska v každém kroku dekódování stojí v průměru O(1) místo O(N) přes celý slovník. Přístup rozšiřují přes zásobníkové automaty na bezkontextové gramatiky (LALR(1)), tedy i na formáty jako JSON, Python nebo SQL; implementací je knihovna Outlines, kterou srovnávají s knihovnou Guidance (viz [[structured-output]]).

## Klíčová tvrzení
- C1: Většina implementací řízeného generování upravuje skóre tokenů ve slovníku; běžný postup v každém kroku vyhodnotí celý slovník, zjistí podle omezení a dosud vygenerovaných tokenů, které tokeny jsou platné, a neplatným nastaví pravděpodobnost na nulu, což dává pevnou cenu O(N) na token (N = velikost slovníku, často řádu 10^4 a více); opakované částečné párování či parsování od začátku sekvence přidává náklady rostoucí aspoň lineárně. (s. 2, s. 4, §1, §2, §2.2)
- C2: Metoda pro regulární výrazy: regex se reprezentuje jako konečný automat (Q, Σ, δ, q0, F), jehož stav se během vzorkování průběžně sleduje, takže párování pokračuje bez čtení rostoucí sekvence od začátku; slovník se předem projde algoritmy 3 a 4 a vznikne index σ: Q → P(V), který každému stavu FSM přiřadí tokeny přijímané z tohoto stavu (uvažuje se start v každém stavu, protože token může odpovídat libovolné části výrazu). (s. 5, s. 6, s. 7, s. 8, §3)
- C3: Při uložení σ do hash mapy stojí krok výpočtu masky v průměru jen O(1); index se staví mimo vzorkování, takže jeho běhová cena je podle autorů prakticky nepodstatná, teoreticky však vyžaduje paměť rovnou počtu stavů FSM (|Q|). (s. 2, s. 7, §1, §3)
- C4: Indexování lze rozšířit na bezkontextové gramatiky a LALR(1) parsery pro populární datové formáty a programovací jazyky (např. JSON, Python, SQL): parser se formuluje jako zásobníkový automat, pro každý stav parseru se sestaví FSM jako sjednocení FSM terminálů, které stav čte, a index pak musí být trie, aby šel dotazovat podle hodnot na zásobníku parseru; v testech s mírně upravenou gramatikou Pythonu měly i naivně postavené indexy (s nevyužitými a redundantními konfiguracemi, z neredukovaných DFA) jen kolem 50 MB. (s. 2, s. 14, s. 15, s. 16, §1, §4.1, §5)
- C5: Srovnání s knihovnou Guidance, která v době psaní používala částečné párování regexu vždy od začátku sekvence a v každém kroku procházela celý slovník (N = 50 257): GPT-2 s regexem [^\W\d]\w* pro jméno proměnné v Pythonu, proměnný max_tokens, měření přes timeit s jedním během a jedním opakováním (tj. jeden vzorek na hodnotu); autoři označují pozorované škálování doby běhu s počtem generovaných tokenů za „markantní“, s výhradou možných chyb v konfiguraci, a výsledek uvádějí jen v grafu. (s. 10, s. 11, s. 12, §3.2)

## Vztah k mé práci


## Citovat pro


## Pozor
- arXiv preprint (v4, 19. 8. 2023), pokud je známo, nerecenzovaný; `litqc meta` hlásí DOI_INVALID pro 10.48550/arXiv.2307.09702 jen proto, že arXiv DOI registruje DataCite, ne Crossref (falešný poplach). Strany = strany PDF (tištěné číslování sedí).
- Fulltext bez QC problémů (žádné PAGE_REPAIRED ani PAGE_WARN). Graf srovnání s Guidance (s. 12) nemá číslo obrázku ani hodnoty v textu – čísla z něj nečti ani necituj; tvrzení abstraktu „significantly outperforms existing solutions“ stojí jen na tomto jednom grafu s jedním vzorkem na bod.
- JSON schéma článek neřeší: JSON je zmíněn jen jako příklad formátu, na který lze rozšířit CFG/LALR(1) přístup (s. 2); rozšíření na gramatiky je popsané jen konceptuálně (§4, §4.1), bez měření rychlosti, kromě velikosti indexu ~50 MB pro gramatiku Pythonu (s. 16).
- Ukázky s GPT2-medium (355M) v §3.1 (s. 8–10) dávají výstupy ve správném formátu, ale článek je nekomentuje věcně (např. rok narození Chomského „1952“, IP adresa Google DNS „2.2.6.1“) – moje poznámka: omezení zaručuje tvar, ne správnost obsahu.
- Kód v článku odpovídá API Outlines z roku 2023 (`outlines.text.generate.regex`, s. 8, s. 11); pro aktuální verzi knihovny se řiď její dokumentací.

## Obrázky
- Obr. 1 (s. 6) – maskování tokenů pomocí FSM pro regex ([0-9]*)?\.?[0-9]* se slovníkem "A", ".", "42", ".2", "1": stav automatu po vzorkování ".2" vs. "1" a odpovídající masky logitů ![[figures/willardEfficientGuidedGeneration2023/fig1.png]]
