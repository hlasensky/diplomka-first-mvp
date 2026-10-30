---
citekey: alnegheimishLargeLanguageModels2024
title: "Large Language Models Can Be Zero-Shot Anomaly Detectors for Time Series?"
authors: "Alnegheimish, Sarah; Nguyen, Linh; Berti-Equille, Laure; Veeramachaneni, Kalyan"
year: 2024
venue: "arXiv preprint arXiv:2405.14755 (v3, 31 Oct 2024)"
kind: preprint   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [anomaly-detection, llm-time-series]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/W4LDJ2XP)

## TL;DR
Framework SigLLM zkouší, zda předtrénované textové LLM (GPT-3.5, Mistral-7B) umí bez dalšího trénování najít anomálie v univariátních časových řadách převedených na text. Porovnává dva přístupy: přímý dotaz na anomálie (PROMPTER) a detekci z odchylky mezi signálem a předpovědí LLM (DETECTOR). Předpověď je výrazně lepší než přímý dotaz a LLM překonají klouzavý průměr i Anomaly Transformer, ale za hlubokým učením (AER) zaostávají zhruba o 30 % a jsou pomalé a drahé.

## Klíčová tvrzení
- C1: Studie zkoumá, zda předtrénované textové LLM dokážou přímo, v zero-shot režimu bez dalšího trénování či fine-tuningu, odhalit anomálie v univariátních časových řadách ([[anomaly-detection]], [[llm-time-series]]); motivací je použít je jako hotové detektory a vynechat časově náročné trénování modelů hlubokého učení. (s. 1, Abstract, §1; s. 2, §1; s. 3, §2)
- C2: SigLLM převádí řadu na text vratnými kroky: posun o minimum do nezáporných hodnot, kvantizace zaokrouhlením na celá čísla, rozdělení do klouzavých oken kvůli limitu kontextu a tokenizace (u GPT s mezerami mezi číslicemi); škálování dává lepší výsledky než bez něj, GPT funguje lépe s mezerami, Mistral bez nich. (s. 3, §3; s. 5, §3)
- C3: PROMPTER žádá LLM promptem přímo o výpis anomálních hodnot v okně; pro každé okno generuje 10 vzorků a výsledky slučuje dvěma prahy α (podíl vzorků) a β (podíl překrývajících se oken); nejlepší F1 dalo α = 0,4 a β = 0,9 pro Mistral a α = 0,2 a β = 0,9 pro GPT. (s. 5, §4.1; s. 7, §5.1)
- C4: DETECTOR využívá schopnost LLM předpovídat řadu: z překrývajících se předpovědí (okno 140, krok 1, horizont 5) rekonstruuje signál, spočte bodová rezidua (absolutní nebo kvadratická chyba), vyhladí je exponenciálně váženým klouzavým průměrem a za anomálie označí chyby nad prahem čtyř směrodatných odchylek od průměru v posuvném okně. (s. 5, §4.2; s. 6, §4.2; s. 7, §5)
- C5: Vyhodnocení proběhlo na 11 datasetech (NASA SMAP a MSL, Yahoo S5 A1–A4, NAB) s 492 řadami a 2349 anomáliemi, s modely Mistral-7B-Instruct-v0.2 (PROMPTER i DETECTOR) a gpt-3.5-turbo-instruct (jen PROMPTER, DETECTOR s GPT kvůli nákladům jen na 5% vzorku); metrikou je F1, při níž se částečná i úplná detekce anomálie počítá jako správná. (s. 6, §5; s. 7, §5)
- C6: DETECTOR dosáhl průměrného F1 0,525 oproti 0,223 (PROMPTER s Mistralem) a 0,133 (PROMPTER s GPT), autoři uvádějí zlepšení o 135 % v F1; PROMPTER trpí falešnými poplachy (průměrná přesnost 0,219), které filtrace prahy α a β neodstraní. (s. 2, §1; s. 7, §5.1, Tab. 3; s. 8, §5.3)
- C7: Podle autorů mohou metody založené na LLM překonat transformerové metody o 12,5 %, výslovně to ale platí jen pro DETECTOR (lepší než Anomaly Transformer v 7 z 11 datasetů); „naše metody“ mají F1 o 14,6 % vyšší než klouzavý průměr MAvg a o 10,9 % nižší než ARIMA (DETECTOR sám překonává MAvg v 6 a ARIMA ve 4 z 11 datasetů). Nejlepší model hlubokého učení AER (F1 0,753) je o 30 % lepší než přístupy založené na LLM a LLM nemají nejvyšší skóre na žádném datasetu; PROMPTER (F1 0,223 / 0,133) zaostává i za AT a MAvg. (s. 8, §5.2; s. 9, Tab. 5)
- C8: Omezení: kvůli omezenému kontextovému oknu LLM je nutné dělit řadu do klouzavých oken, což je neefektivní a drahé a ztěžuje rozšíření na vícerozměrné řady; na odpověď modelu se čeká půl hodiny až dvě hodiny (modely hlubokého učení se přitom trénují pod hodinu) a PROMPTER s GPT stál zhruba 834,11 USD (1,69 USD na signál), DETECTOR v menším experimentu 4,3 USD na signál. (s. 8, §6; s. 9, §6, §7)

## Vztah k mé práci


## Citovat pro


## Pozor
- **Nerecenzovaný arXiv preprint** (v3, 31. 10. 2024), recenzovaná verze nebyla dohledána. `litqc meta` hlásí DOI_INVALID, ale jde o falešný poplach: arXiv DOI (10.48550/…) jsou registrovaná u DataCite, ne v Crossref (uživatel přijal 2026-10-30).
- PAGE_WARN žádné. Tabulky 2, 3 a 5 vytáhl pdftotext po sloupcích; jsou přepsané ve fulltextu v blocích `[Table N – ruční přepis z PDF]` (kontrolováno proti PDF i sloupcovému pořadí). Tabulka 4 (s. 9, varianty DETECTORu) přepsaná není, čísla z ní ověřuj v PDF.
- Procenta v C7 (12,5 %, 14,6 %, 10,9 %, 30 %) podle mého přepočtu z Tab. 5 odpovídají průměrnému F1 DETECTORu (0,525), i když text píše obecně o „LLM-based methods“. Na s. 8 je navíc „deep learning … better than LLM-based methods by 18% on average“ (průměr metod hlubokého učení, ne jen AER) a závěr (s. 9) uvádí, že LLM za hlubokým učením zaostávají „by a factor of ×1.2“.
- Hodnocení používá F1 se započtením částečné detekce (Tatbul et al.), tedy jinou metriku než VUS-PR z [[liuElephantRoomReliable2024]] nebo affinity F1 z [[zhouCanLLMsUnderstand2025]] – čísla nejsou přímo srovnatelná.
- Vstup je čistě textový a univariátní; DETECTOR s GPT běžel jen na 5% vzorku. Autoři sami připouštějí riziko, že benchmarky byly v trénovacích datech LLM; argumentují jen tím, že textová reprezentace je unikátní (s. 8, §6).
- Text odkazuje na „Section III.A“ (s. 5), myslí tím §3. Na s. 1 je ve větě „A follow-up question ari QWERT]śes“ artefakt přímo v PDF (OCR ho čte stejně), ne chyba extrakce.
- Strany = strany PDF (tištěné číslování v preprintu chybí).

## Obrázky
- Obr. 2 (s. 2) – obecná pipeline nesupervizované detekce anomálií: trénink, generování signálu, chyba, extrakce anomálií ![[figures/alnegheimishLargeLanguageModels2024/fig2.png]]
- Obr. 4 (s. 4) – dva přístupy SigLLM: (a) PROMPTER, (b) DETECTOR ![[figures/alnegheimishLargeLanguageModels2024/fig4.png]]
