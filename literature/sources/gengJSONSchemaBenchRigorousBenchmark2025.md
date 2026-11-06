---
citekey: gengJSONSchemaBenchRigorousBenchmark2025
title: "JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models"
authors: "Geng, Saibo; Cooper, Hudson; Moskal, Michał; Jenkins, Samuel; Berman, Julian; Ranchin, Nathan; West, Robert; Horvitz, Eric; Nori, Harsha"
year: 2025
venue: "arXiv preprint arXiv:2501.10868"
kind: preprint   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [structured-output, llm-agents]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/PFEQUQ74)

## TL;DR
JSONSchemaBench je benchmark pro omezené dekódování (constrained decoding, viz [[structured-output]]) složený z přibližně 10 tisíc reálných JSON schémat (signatury funkcí pro volání nástrojů, API služeb, konfigurace Kubernetes), doplněný oficiální JSON Schema Test Suite. Autoři na něm srovnávají šest frameworků (Guidance, Outlines, Llamacpp, XGrammar, OpenAI, Gemini) ve třech osách – efektivita, pokrytí funkcí JSON Schema a kvalita výstupu. Frameworky se v reálné podpoře schémat výrazně liší, uzavřená API pokrývají málo schémat, ale ta přijatá splní téměř vždy, a omezené dekódování v jejich úlohách přesnost mírně zvyšuje, nikoli snižuje.

## Klíčová tvrzení
- C1: Benchmark a metoda: JSONSchemaBench obsahuje 10K reálných JSON schémat z několika zdrojů (kolekce ~6K schémat z GitHubu od Baazizi et al., JSON Schema Store, GlaiveAI function calling V2, konfigurace Kubernetes aj.) uspořádaných do 10 datasetů různé složitosti (Tab. 1 uvádí celkem 9558 schémat; GitHub-Trivial a GitHub-Ultra jsou z experimentů vyřazeny jako příliš snadné/těžké); je spárovaný s oficiální JSON Schema Test Suite a autoři na něm hodnotí šest frameworků omezeného dekódování (Guidance, Outlines, Llamacpp, XGrammar, OpenAI, Gemini) ve třech osách: efektivita, pokrytí (coverage) a kvalita. (s. 1, s. 3, s. 4, s. 5, §1, §3.1, Tab. 1)
- C2: Efektivita se měří jako doba kompilace gramatiky (GCT), čas do prvního tokenu (TTFT) a čas na výstupní token (TPOT) s Llama-3.1-8B-Instruct na backendu llama.cpp (jedna A100, batch 1, mediány, jen na průniku schémat pokrytých všemi frameworky kvůli zkreslení ve prospěch frameworků s nižším pokrytím); Guidance má GCT 0,00–0,01 s a TPOT 6,37–9,47 ms, tedy nižší než samotný LM (15,32–16,68 ms) díky přeskakování (fast-forwarding) kroků generování, Llamacpp má TPOT 27,22–29,98 ms a Outlines, který převádí schémata na regulární výrazy, má výrazně nejvyšší GCT (3,48–8,05 s) a TPOT 30,33–46,57 ms; s backendem HF Transformers má XGrammar TPOT 65,20–66,78 ms proti 35,88–44,21 ms u Guidance. (s. 5, s. 6, s. 7, §4, §4.1, Tab. 2, Tab. 3)
- C3: Pokrytí se měří jako deklarované, empirické a míra souladu (compliance rate = empirické/deklarované) s Llama-3.2-1B-Instruct, greedy dekódováním a timeoutem 40 s na kompilaci a 40 s na generování; Guidance má nejvyšší empirické pokrytí na 6 z 8 datasetů (Llamacpp na Washington Post a JSON Schema Store); uzavřená API mají podle textu nejnižší empirické pokrytí („poslední na všech datasetech kromě jednoho“, s. 8), podle Tab. 4 ale OpenAI není poslední na Kubernetes ani GitHub Hard, a empirické pokrytí open-source enginů a OpenAI/Gemini není podle autorů přímo srovnatelné kvůli jiným modelům; mají velmi vysokou míru souladu (OpenAI 0,92–1,00), tedy podle autorů konzervativně implementují jen podmnožinu funkcí; LM bez omezení má podle textu nejnižší míru souladu, v Tab. 4 je však na GitHub Hard a Washington Post nižší Outlines (0,06; 0,23), u něhož autoři nízkou míru přičítají hlavně timeoutům. (s. 7, s. 8, s. 9, §5, §5.1, §5.2, Tab. 4)
- C4: Na JSON Schema Test Suite (45 kategorií funkcí) musí framework vygenerovat každou platnou instanci a zablokovat každou neplatnou; selhání se dělí na chybu kompilace, přeomezení (over-constrained, odmítá platné instance) a podomezení (under-constrained, propustí neplatné); Guidance má plné pokrytí ve 13 kategoriích a aspoň středně velké (>50 %) ve 21, Llamacpp a XGrammar plné pokrytí jen v 1 kategorii, Outlines v žádné; XGrammar má nejméně chyb kompilace (3 kategorie), ale nejvíce podomezení (38), Guidance podomezení jen v 1 kategorii. (s. 8, s. 10, §5.3, §5.3.1, Tab. 5, Tab. 6)
- C5: Kvalita: na třech úlohách (Last Letter, Shuffle Objects, GSM8K) s výstupem jako JSON objekt {"reasoning", "answer"} a modelem Llama-3.1-8B-Instruct dosahuje omezené dekódování podle autorů vyšší přesnosti než neomezené generování bez ohledu na framework (v Tab. 8 je jedinou výjimkou Llamacpp na Shuffle Objects se shodnými 52,6 %); nejlepší je Guidance (54,0 %, 55,9 %, 83,8 % proti 50,7 %, 52,6 %, 80,1 % u samotného LM), což autoři přičítají pravděpodobně jeho implementaci token healing. (s. 11, s. 12, §6.1, §6.2, Tab. 8)

## Vztah k mé práci


## Citovat pro


## Pozor
- arXiv preprint (v3, 27. 2. 2025, „Preprint. Under review.“), nerecenzovaný; `litqc meta` hlásí DOI_INVALID pro 10.48550/arXiv.2501.10868 jen proto, že arXiv DOI registruje DataCite, ne Crossref (falešný poplach). Strany = strany PDF (tištěné číslování sedí), hlavní text s. 1–12, dále reference a přílohy.
- Většina autorů má afiliaci Microsoft, benchmark je zveřejněn pod github.com/guidance-ai a Guidance podle článku překonává ostatní frameworky ve všech třech osách (Obr. 1, s. 2) – moje poznámka: možný střet zájmů, srovnání ověřuj i z nezávislých zdrojů.
- Fulltext: s. 19 a 21 (příloha) nahrazeny OCR; PAGE_WARN s. 17 (příloha A.2–A.3: Tab. 10 s verzemi draftů a grafy Obr. 2) – tvrzení z ní nečerpají, hodnoty z grafů nečti. Tabulky 2, 4, 6 a 8 (s. 6, 9, 10, 12) byly v pdftotext rozházené po sloupcích a jsou ve fulltextu ručně přepsané z PDF; Tab. 3 (s. 7) a Tab. 5 (s. 10) nepřepsané, hodnoty v C2/C4 ověřeny proti renderu PDF.
- Empirické pokrytí open-source frameworků (Llama 3.2-1B) a OpenAI/Gemini (vlastní modely) podle autorů nelze přímo srovnávat (Tab. 4); Gemini je vynecháno u datasetů s podporou < 1 %; XGrammar na Snowplow NA. Výsledky platí pro verze knihoven z přelomu 2024/2025.
- Úvod shrnuje výsledky zaokrouhleně: omezené dekódování může zrychlit generování „o 50 %“, nejlepší framework podporuje „dvakrát víc“ schémat než nejhorší a zlepšení úloh „až o 4 %“ (s. 3) – pro konkrétní čísla cituj tabulky.
- Úlohy kvality mají záměrně jednoduchou strukturu (izolace vlivu na uvažování), nejde o složitá schémata typu volání nástrojů.
