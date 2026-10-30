---
citekey: yaoReActSynergizingReasoning2023a
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
authors: "Yao, Shunyu; Zhao, Jeffrey; Yu, Dian; Du, Nan; Shafran, Izhak; Narasimhan, Karthik R.; Cao, Yuan"
year: 2023
venue: "The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023 (OpenReview.net)"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [llm-agents]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/SSKV4DKM)

## TL;DR
ReAct nechává jazykový model střídavě generovat volně formulované myšlenky (thought) a akce v prostředí, jejichž výsledek (observation) se vrací do kontextu – myšlenky řídí plán a akce dodávají vnější informace. Na otázkách a ověřování faktů s jednoduchým Wikipedia API omezuje halucinace oproti chain-of-thought, na interaktivních úlohách ALFWorld a WebShop překonává imitační i posilované učení jen s jedním až dvěma příklady v promptu. Nejlepší výsledky v QA dává kombinace ReAct s CoT-SC; hlavní slabinou jsou zacyklení a neinformativní vyhledávání.

## Klíčová tvrzení
- C1: Uvažování LLM (chain-of-thought) a jednání (generování akcí a plánů) byly zkoumány převážně odděleně; CoT je „statická černá skříňka“, která vychází jen z vnitřních reprezentací modelu a není ukotvená ve vnějším světě, což vede k halucinaci faktů a šíření chyb, zatímco dosavadní přístupy k jednání (s výjimkou omezeného verbálního uvažování u Huang et al. 2022b) nevyužívají model k abstraktnímu uvažování o cílech ani k udržování pracovní paměti. (s. 1, Abstract; s. 2, §1)
- C2: ReAct rozšiřuje prostor akcí agenta o jazyk (Â = A ∪ L): „myšlenka“ neovlivňuje prostředí ani nevrací pozorování, jen skládá užitečné informace z kontextu a připojí se k němu (c_{t+1} = (c_t, â_t)); zmrazený PaLM-540B se few-shot promptuje lidskými trajektoriemi myšlenek, akcí a pozorování – u úloh zaměřených na uvažování se střídají kroky thought–action–observation, u rozhodovacích úloh s mnoha akcemi se myšlenky objevují řídce a o jejich umístění rozhoduje model. (s. 3, §2; s. 4, §2)
- C3: Podle autorů jsou trajektorie ReAct interpretovatelné – člověk může kontrolovat uvažování i faktickou správnost a chování agenta průběžně korigovat úpravou myšlenek (thought editing); prompty se navrhují tak, že anotátor jen dopíše své myšlenky k provedeným akcím. (s. 3, §1; s. 4, §2)
- C4: Vyhodnocení na čtyřech benchmarcích: HotpotQA (multi-hop QA) a FEVER (ověřování faktů) v režimu jen s otázkou, s Wikipedia API se třemi akcemi search[entity], lookup[string] a finish[answer] a 6, resp. 3 příklady v promptu; ALFWorld (textová hra, 6 typů úloh, 134 neviděných her) a WebShop (simulovaný e-shop s 1,18 mil. produktů a 12 tis. instrukcemi, 500 testovacích instrukcí). (s. 3, §1; s. 4, §3.1–3.2; s. 7, §4)
- C5: Na HotpotQA a FEVER je ReAct lepší než Act (27,4 vs. 25,7 EM; 60,9 vs. 58,9 Acc), proti CoT vyhrává na FEVER (60,9 vs. 56,3), ale na HotpotQA mírně zaostává (27,4 vs. 29,4); nejlepší jsou kombinace s CoT-SC (ReAct → CoT-SC 35,1 EM na HotpotQA, CoT-SC → ReAct 64,6 Acc na FEVER), které dosahují výkonu CoT-SC s 21 vzorky už se 3–5 vzorky; všechny promptovací metody přitom zůstávají daleko za supervizovaným SoTA (67,5 / 89,5). (s. 5, Tab. 1, §3.2; s. 6, §3.3)
- C6: Ruční rozbor 200 trajektorií z HotpotQA: halucinace tvoří 56 % selhání CoT a CoT má vyšší podíl falešně pozitivních úspěchů (14 % vs. 6 %); ReAct má víc chyb uvažování (47 % vs. 16 %), včetně typického zacyklení, kdy opakuje předchozí myšlenky a akce, a neinformativní vyhledávání (23 % chyb) vykolejí jeho uvažování, z čehož se těžko zotavuje. (s. 6, §3.3, Tab. 2)
- C7: V rozhodovacích úlohách dosáhl nejlepší běh ReAct na ALFWorld úspěšnosti 71 % proti 45 % (nejlepší Act) a 37 % (BUTLER, imitační učení na 10^5 expertních trajektoriích na typ úlohy) a IM-style variantu s hustou zpětnou vazbou z prostředí překonal 71 vs. 53; na WebShop zvýšil úspěšnost na 40,0 % proti 29,1 % (IL) a 28,7 % (IL+RL), lidští experti ale dosahují 59,6 %. (s. 7, §4; s. 8, §4, Tab. 3, Tab. 4)
- C8: Omezení: při promptování menších modelů (PaLM-8/62B) je ReAct ze čtyř metod nejhorší (fine-tuning na 3 000 trajektoriích ho naopak dělá nejlepší); složité úlohy s velkým prostorem akcí vyžadují více ukázek, než se vejde do vstupního limitu in-context učení; propojení LLM s akcemi ve vnějším prostředí nese rizika (vyhledání nevhodných či soukromých informací, škodlivé akce), proto experimenty omezují akce na Wikipedii a WebShop. (s. 6, §3.3; s. 9, §6; s. 10, Ethics Statement)

## Vztah k mé práci


## Citovat pro


## Pozor
- PDF je arXiv v3 (10. 3. 2023) s hlavičkou „Published as a conference paper at ICLR 2023“; `litqc meta` hlásí META_YEAR (Semantic Scholar 2022 = rok arXiv preprintu), správně je ICLR 2023. Strany = strany PDF (tištěné číslování hlavního textu sedí).
- Strany 2, 14 a 15 nahrazeny OCR textem (PAGE_REPAIRED); s. 2 obsahuje Obr. 1, jehož OCR je rozházené – příklad trajektorie viz oříznutý obrázek níže. PAGE_WARN: s. 1, 3, 27, 29 (s. 1 a 3 jen rozpalovaná písmena v nadpisech, text čitelný; C1–C4 odtud ověř v PDF, pokud bys pochyboval).
- Tabulky 1 (s. 5), 2 (s. 6), 3 a 4 (s. 8) pdftotext rozházel; jsou přepsané ve fulltextu v blocích `[Table N – ruční přepis z PDF]` (kontrolováno proti PDF a textu).
- Hlavní experimenty běží na PaLM-540B, který nebyl veřejně dostupný; výsledky s GPT-3 jsou jen v příloze A.1 (s. 10, Reproducibility). HotpotQA/FEVER jsou v režimu bez podpůrných odstavců a API je záměrně slabší než moderní retrievery (s. 4, §3.1).
- „Absolutní zlepšení o 34 %“ na ALFWorld (abstrakt) porovnává nejlepší ze 6 běhů ReAct (71 %) s nejlepším z 8 běhů BUTLER (37 %); průměr ReAct je 57 % (Tab. 3). Zlepšení o 10 % na WebShop je úspěšnost 40,0 vs. 29,1 (Tab. 4).
- Zacyklení přisuzují autoři možná suboptimálnímu greedy dekódování (s. 6, pozn. 4) – to je jejich domněnka, ne výsledek.

## Obrázky
- Obr. 1 (s. 2) – srovnání Standard / CoT / Act-only / ReAct na otázce z HotpotQA a Act-only vs. ReAct v ALFWorld (trajektorie Thought–Act–Obs) ![[figures/yaoReActSynergizingReasoning2023a/fig1.png]]
