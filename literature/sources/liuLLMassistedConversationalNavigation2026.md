---
citekey: liuLLMassistedConversationalNavigation2026
title: "LLM-Assisted Conversational Navigation over Multidimensional Data Cubes"
authors: "Liu, Xiufeng; Yang, Yanyan"
year: 2026
venue: "Expert Systems with Applications 328, 132958"
kind: journal   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [conversational-olap, guided-data-exploration, olap, interestingness, llm-data-agents]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/JX5GASIW)

## TL;DR
NavLLM řeší doporučení dalšího pohledu při navigaci v OLAP kostce: kostka je graf pohledů propojených drill-down, roll-up, slice a dice a v každém kroku se vybere top-k sousedů podle váženého součtu datové zajímavosti (počítá OLAP engine), preferenčního skóre od LLM z rozhovoru a diverzity vůči navštíveným pohledům. LLM nepočítá žádná čísla, vidí jen popisy pohledů a předpočítané statistiky a vrací skóre a vysvětlení. V automatických simulacích na třech kostkách má NavLLM vyšší kumulativní zajímavost než LLM-only i čistě datové heuristiky, článek ale obsahuje řadu vnitřních nesrovnalostí v číslech (viz Pozor).

## Klíčová tvrzení
- C1: Problém: navigace v [[olap]] kostce je převážně ruční volba v exponenciálně velkém prostoru pohledů, takže analytik prochází redundantní či neinformativní pohledy a přehlíží vzory; LLM jako end-to-end analytický engine je nevhodný, protože halucinuje fakta a vysvětlení a bez varování počítá čísla špatně. Autoři proto definují next-view recommendation problem: z aktuálního pohledu a historie rozhovoru doporučit další pohledy, které maximalizují užitek explorace při omezeném počtu interakcí. (s. 1, §1; s. 2, §1)
- C2: Metoda: navigační prostor je orientovaný graf pohledů, jehož hrany jsou primitivní OLAP akce (drill-down, roll-up, slice, dice); session je posloupnost stavů ⟨V_t, u_t, a_t⟩ (pohled, promluva uživatele, akce) a v každém kroku se z kandidátů Cand(V_t) vybírá top-k podle užitku U = λ_data·I_data + λ_pref·I_pref + λ_div·I_div. I_data měří odchylku agregovaných hodnot od rodičovského pohledu ([[interestingness]]), I_pref ∈ [0, 1] odhaduje LLM z rozhovoru a popisů pohledů, I_div je nejkratší vzdálenost v grafu k už navštívenému pohledu. Autoři to označují za první formální model konverzační navigace nad vícerozměrnými kostkami ([[conversational-olap]], [[guided-data-exploration]]). (s. 2, §1; s. 3–4, §3.2–3.4, Def. 5, 6, 8–11; s. 6, §5.2; s. 7, §5.4)
- C3: Oddělení rolí: LLM nespouští dotazy ani nepočítá agregace či testy, vidí jen popisy pohledů na úrovni schématu a souhrnné statistiky předpočítané cube enginem (např. průměr, CV, počet outlierů, binovaná odchylka) a vrací skóre relevance v JSON a krátká vysvětlení k top-k doporučením; I_data i I_div se počítají deterministicky. Proti text-to-SQL autoři argumentují, že jediný halucinovaný token tam může dát neplatný dotaz, kdežto zde vede halucinované skóre nanejvýš k doporučení platného pohledu ([[llm-data-agents]]). (s. 3, §2.3; s. 6, §4.3–4.4; s. 7, §5.3, §5.5; s. 8, §6.2)
- C4: Implementace: in-memory cube engine v pandas, LLM DeepSeek-V3 (temperature 0,3), nejvýš 30 kandidátů na krok, latence 2–4 s na krok (LLM volání 1,5–3 s). Neplatná JSON odpověď LLM se zopakuje s přísnějším promptem, jinak fallback na I_pref = 0,5; chybovost byla 2,3 % volání (18 z 782; 14 vyřešeno opakováním, 4 fallbackem). Výchozí váhy 0,4/0,4/0,2 vybrala pilotní studie na 6 odložených úlohách se 4 účastníky. (s. 7, §6.1; s. 9, §6.2–6.3, Tab. 1; s. 10, §6.5; s. 11, §7.1.3)
- C5: Evaluace: tři kostky po 3 dimenzích – SalesCube (M5, Walmart, ~1M řádků), syntetická ManufacturingCube (~394K) a AirQualityCube z veřejných senzorových dat o kvalitě ovzduší (~2,5M, 5 let); 20 úloh v přirozeném jazyce (8/6/6) s cílovými pohledy anotovanými dvěma výzkumníky (κ = 0,82); automatické simulace s rozpočtem 12 kroků, 2 běhy na úlohu = 40 session na metodu; srovnání s LLM-Only, Heuristic-Nav, SeeDB, Voyager, Smart Drill-Down, DeepEye, Greedy-Best, BFS a Random-Nav; Welchův t-test. (s. 10, §7.1.1–7.1.2; s. 11, §7.1.3, Tab. 2)
- C6: Výsledky (Tab. 3): NavLLM má nejvyšší striktní hit rate 0,525 (LLM-Only 0,300, BFS 0,350; vůči LLM-Only p = 0,041) a kumulativní zajímavost 13,21 proti 7,74 u LLM-Only (p = 0,002, +71 %), 6,88 u Heuristic-Nav a 5,96 u Random-Nav (obojí p < 0,001); abstrakt to uvádí jako +92 % proti čistě datovým heuristikám. V relaxed hit rate je NavLLM (0,800) pod LLM-Only (0,875) i Heuristic-Nav (0,950), vůči Random-Nav není rozdíl v hit rate signifikantní (p = 0,194). Redundance 55,4 % vs. 66,5 % u LLM-Only. (s. 1, abstrakt; s. 11, §7.2.1, Tab. 3; s. 12, §7.2.2, §7.2.4, Tab. 4, Tab. 6)
- C7: Ablace a robustnost: bez I_pref klesne hit rate z 0,53 na 0,36, bez I_data na 0,40 (ale s nejvyšším pokrytím 12,7 a kumulativní zajímavostí 11,3), bez I_div na 0,30 s redundancí 0,72 (Tab. 7). I_data a I_pref se na top-1 kandidátovi neshodnou v 66,1 % ze 112 kroků; v 74 konfliktech zasáhne cíl kandidát preferovaný I_pref v 35,1 %, I_data v 13,5 % a hybrid v 27,0 %. Parafráze promluv nemění kumulativní zajímavost (p > 0,63; hit rate netestován, striktní kolísá 0,100–0,275), záměna DeepSeek-V3 za GPT-4o nedává signifikantní rozdíl (p > 0,29) a pět opakovaných běhů dává 11,18 ± 0,42; tyto robustnostní experimenty ale vycházejí z jiné úrovně než Tab. 3 (NavLLM/DeepSeek-V3: striktní hit rate 0,275, CI 11,32 vs. 0,525 a 13,21) a článek rozdíl nevysvětluje. (s. 12, §7.3; s. 13, Tab. 7, Tab. 9, Tab. 10, §7.5.1–7.5.4; s. 14, Tab. 11)
- C8: Omezení podle autorů: jen kostky s malým počtem dimenzí (2–5 měr), in-memory engine do 30M řádků, cílové pohledy odrážejí operacionalizaci autorů, automatické simulace s předem danými promluvami místo studie se skutečnými analytiky, jediný LLM v hlavních experimentech, kvalita vysvětlení nebyla formálně hodnocena, nutnost čistého star schématu s hierarchiemi a citlivost LLM na formulaci promptu a pořadí kandidátů. Na ManufacturingCube vede datová heuristika (Heuristic-Nav, hit rate 0,667). (s. 12, §7.2.3; s. 15, §8.1, §8.3; s. 16, §8.3)

## Vztah k mé práci


## Citovat pro


## Pozor
- Tab. 6 (s. 12): p-hodnoty pro hit rate („NavLLM = Heuristic“, p = 1,000; p = 0,194 vs. Random-Nav) neodpovídají hodnotám v Tab. 3 (0,525 vs. 0,300 a 0,175 při n = 40). Hit-rate p-hodnoty z Tab. 6 necitovat.
- Existuje 4stránkové demo téhož systému: Liu, Liu, Yang, „NavLLM: Interactive LLM-Assisted Navigation over Multidimensional Data Cubes“, EDBT 2026 (citekey liuNavLLMInteractiveLLMAssisted2026, není ingestované). Tento časopisecký článek demo necituje. Abstrakt dema (v bib) mluví o čtyřech reálných kostkách, článek má tři, z toho jednu syntetickou.
- Stránkování: článek má číslo 132958, strany PDF 1–19 odpovídají tištěným stranám.
- PAGE_WARN s. 1, 5 a 8 (abstrakt, obr. 1 a 2 a šablona promptu ve dvou sloupcích); próza z s. 5 a 8 použitá v C2–C3 zkontrolována proti vyrenderovaným stránkám. S. 9 (obr. 3, Tab. 1, §6.2–6.3) nahrazena OCR; čísla v C4 ověřena proti vyrenderované stránce.
- Tab. 3 (s. 11) a Tab. 7 (s. 13) jsou ve fulltextu ručně přepsané z PDF; fulltext je jen pro čtení, záloha `fulltext/…corrected.txt`. Tab. 5, 6, 8–11 zůstaly rozházené, čísla v claims jsou z textu nebo zkontrolována v PDF.
- Počet metod a session nesedí: abstrakt, §1 a §10 uvádějí 280 session a 7 metod, §7.1.3 devět baselines a 400 session přes 10 metod (Tab. 3 má 10 řádků). Citovat raději „40 session na metodu“.
- „72 % vyšší hit rate než náhodná explorace“ z abstraktu jsem v těle nenašel (Tab. 3: striktně 0,525 vs. 0,175, relaxed 0,800 vs. 0,625; Tab. 6: rozdíl v hit rate vůči Random-Nav p = 0,194). Necitovat.
- §8 (s. 14–15) si protiřečí s §7: tvrdí, že LLM-Only má nejvyšší striktní hit rate 0,525 a NavLLM 0,300 (Tab. 3 je opačně), a uvádí jiná čísla citlivosti vah (hit rate 0,28 / 0,38 / 0,33, redundance 0,52) než §7.4 a Tab. 8 (0,48 / 0,38 / 0,53, redundance 0,55). Text ablace uvádí redundanci plného modelu 0,63, Tab. 7 0,55; §8 píše, že ablace běžela na menším LLM, §7.3 že na DeepSeek-V3.
- Pilotní studie: text §6.3 uvádí hit rate 0,75 a redundanci 18,2 %, Tab. 1 pro tutéž konfiguraci 0,79 a 15,7 % (s. 9).
- Robustnostní experimenty (Tab. 9–11) mají pro NavLLM s DeepSeek-V3 striktní hit rate 0,275 a kumulativní zajímavost 11,32, ne 0,525 a 13,21 jako Tab. 3; rozdíl článek nevysvětluje.
- Obr. 3 (s. 9) mluví o „User Study“, „participant“, „PostgreSQL cube engine“ a 30M řádcích M5, ale evaluace je jen automatická simulace, engine je pandas (§6.1) a SalesCube má podle Tab. 2 ~1M řádků. Práh pro vyřazení malých pohledů je jednou < 3 n-tic (§5.1, s. 6), jinde < 5 (§6.4–6.5, s. 10). Rozsah dimenzí v omezeních: jednou 3–4, jednou 3–5, Tab. 2 má všude 3.
- Tab. 5 (per-cube) uvádí jen baselines, ne NavLLM; „ManufacturingCube failure“ v budoucí práci (s. 16) není jinde popsaný. Odkazy na robustnostní experimenty míří na §7.4, správně je §7.5.
- Na obr. 1 vede šipka Res(V) do Explanation Generatoru, popisek a §4.1 ji vedou do Data-Interestingness Scoreru.
- Data nejsou sdílena; kód: https://github.com/xiufengliu/NAVLLM (s. 18). Článek necituje COOL ani VOOL; z IAM linie cituje Vassiliadis et al. 2019 a Francia et al. 2022 (explain operator).

## Obrázky
- Obr. 1 (s. 5) – architektura NavLLM: LLM doména (generátor kandidátů, tři scorery, utility ranker, generátor vysvětlení) vs. datová doména (cube engine) ![[figures/liuLLMassistedConversationalNavigation2026/fig1.png]]
