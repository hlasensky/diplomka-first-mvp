---
citekey: patilGorillaLargeLanguage2024
title: "Gorilla: Large Language Model Connected with Massive APIs"
authors: "Patil, Shishir G.; Zhang, Tianjun; Wang, Xin; Gonzalez, Joseph E."
year: 2024
venue: "Advances in Neural Information Processing Systems 37 (NeurIPS 2024), pp. 126544–126565"
kind: conference   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [llm-agents, llm-hallucination]
uroven: 2
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/UVWAQ44S)

## TL;DR
Gorilla je LLaMA-7B dotrénovaný na syntetických dvojicích instrukce–volání API (benchmark APIBench z ML API TorchHub, TensorFlow Hub a HuggingFace), který má z přirozeného jazyka vygenerovat správné volání API. Retriever-aware training učí model pracovat s přiloženou (i nepřesnou) dokumentací API, takže se přizpůsobí změnám dokumentace při inferenci. Halucinaci autoři měří přes shodu podstromu AST jako volání API, které v databázi vůbec neexistuje, a ukazují, že zero-shot GPT-4 a další modely takových volání generují výrazně víc než Gorilla ([[llm-hallucination]], [[llm-agents]]).

## Klíčová tvrzení
- C1: Problém a data: využít nástroje přes volání API je obtížné i pro GPT-4, hlavně protože model neví, jaká API jsou k dispozici a jak je v často aktualizované sadě nástrojů použít; APIBench obsahuje 1 645 volání API (925 z HuggingFace – top 20 v každé doméně, 626 z TensorFlow Hub v2, Torch Hub vyčerpávajícím způsobem), převedených na JSON se strukturovanými poli (api_name, api_call, api_arguments aj.), a GPT-4 metodou self-instruct z nich vygeneroval 10 dvojic instrukce–API na každé API, celkem 16 450. (s. 1, s. 4, Abstract, §3.1)
- C2: Metoda: Gorilla je LLaMA-7B standardně instrukčně dotrénovaný na těchto dvojicích; při retriever-aware training (RAT) se k promptu přidává vyhledaná dokumentace („Use this API documentation for reference: <retrieved_API_doc_JSON>“), která nemusí být správná, zatímco odpověď obsahuje správné API – model se tak učí retriever „posoudit“: relevantní dokument použít, irelevantním se nenechat rozptýlit; inference běží zero-shot nebo s retrieverem (BM25, GPT-Index), který připojí top-1 dokument. (s. 5, s. 7, §3.2, §4)
- C3: Halucinaci definují přes shodu podstromu AST jako volání API, které není podstromem žádného API v databázi („invoking an entirely imagined tool“), na rozdíl od chyby, kdy model existující API volá nesprávně; přesnost, halucinace a chyba dávají dohromady jedna; na 100 náhodných výstupech Gorilly dala metrika AST přesnost 78 %, shodně s lidským hodnocením (78 %), a 72 % vygenerovaného kódu šlo spustit. (s. 6, s. 8, s. 9, §3.3, §4.1, Tab. 3)
- C4: Bez retrieveru (zero-shot) dosahuje Gorilla celkové přesnosti 59,13 / 71,68 / 83,79 % na TorchHub / HuggingFace / TensorFlow Hub s halucinací 6,98 / 10,95 / 5,40 %, zatímco GPT-4 má přesnost 38,70 / 19,80 / 18,20 % a halucinaci 36,55 / 37,16 / 78,65 % (na HuggingFace se u modelů kromě Gorilly kontroluje jen správná doména); zero-shot promptování GPT-4/GPT-3.5 vede k „dire hallucination errors“, např. volání AutoModel.from_pretrained(dir_name) s vymyšlenými názvy repozitářů na GitHubu; autoři uvádějí, že GPT-3.5 halucinuje méně než GPT-4 na všech hubech a ve všech nastaveních retrievalu, Tab. 1 to však na TorchHub s GPT-Index a Oracle nepotvrzuje. (s. 7, s. 8, §4.1, Tab. 1)
- C5: Přidání retrievalu nepomáhá vždy a může výkon i zhoršit. Podle textu autorů zvýší dotrénování s dokumentací z oracle retrieveru přesnost o 12,37 % na Torch Hub (Tab. 2: 67,20 vs. 54,83) a „o 23,46 %“ na HuggingFace, Tab. 2 však dává 91,26 vs. 45,58; pokles s reálnými retrievery při vyhodnocení, 29,20 % (GPT-Index) a 52,27 % (BM25), odpovídá v Tab. 2 jen TensorHubu (94,16 vs. 64,96 / 41,89). Autoři shrnují, že dotrénování je lepší než naivní retrieval pro doplnění informací a dodržení syntaxe a Gorilla 0-shot v průměru překonává GPT-3.5/GPT-4 se třemi příklady v kontextu. (s. 5, s. 7, s. 8, s. 10, §3.2, §4.1, §4.4, Tab. 2, Tab. 5)

## Vztah k mé práci


## Citovat pro


## Pozor
- Strany = strany PDF (22 s., verze NeurIPS 2024 s checklistem); v tištěném sborníku jde o s. 126544–126565, takže číslo strany pro citaci je nutné přepočítat (rozsah 22 stran sedí, takže nejspíš PDF s. N = sborník s. 126543 + N; ověř v tištěné verzi).
- Tabulky 1, 2 (s. 8), 4 (s. 9) a 5 (s. 10) pdftotext vypsal po sloupcích, takže čísla jsou ve fulltextu, ale bez struktury řádků; hodnoty v C4 jsem kontroloval proti vykreslené s. 8 PDF. Ruční přepis tabulek do fulltextu (`[Table N – ruční přepis z PDF]`) se nepodařilo zapsat (zápis do fulltextu zablokován), chybí tedy `.corrected.txt`.
- Rozpor v počtu API z Torch Hub: Obr. 3 (s. 4) uvádí 94, text §3.1 (s. 4) 95 modelů; součet 1 645 odpovídá 94.
- U HuggingFace se u všech modelů kromě Gorilly kontroluje jen správný název domény (úloha se redukuje na výběr z možností), takže srovnání na HF není stejně přísné jako na TorchHub/TensorFlow Hub (s. 7, §4.1).
- Hodnotí se vždy jen jedno volání API na instrukci (s. 5, §3.3), ne vícekrokové volání nástrojů; spouštění API není předmětem článku (s. 5, §3.2). Testovací sada je holdout ze stejných self-instruct dat jako trénink (s. 7, §4).
- Baseline modely jsou staré checkpointy (gpt-4-0314, gpt-3.5-turbo-0301, claude-v1, LLaMA-7B; s. 6, §4); LLM experimenty běžely jednou, bez chybových úseček (s. 21, Checklist 7).
- Tvrzení autorů, že GPT-3.5 halucinuje méně než GPT-4 ve všech nastaveních (C4, s. 8), Tab. 1 úplně nepotvrzuje: na TorchHub s GPT-Index (1,61 vs. 1,07) a s Oracle (1,60 vs. 0,53) má GPT-4 halucinací méně. Necitovat jako obecný výsledek.
- „Zlepšení“ v §4.1 (20,43 % proti GPT-4, 10,75 % proti GPT-3.5, 83 % proti LLaMA) autoři neuvádějí s výpočtem; vztah k Tab. 1 není zřejmý, proto je v tvrzeních nepoužívám.
- Duplicitní starší záznam v Zoteru `patilGorillaLargeLanguage` (bez roku) – ignorovat, cituj tento klíč.
- Procenta v C5 (12,37 / 23,46 / 29,20 / 52,27 %) jsou čísla autorů z textu (s. 7); v Tab. 2 (s. 8) sedí 12,37 (Torch Hub, 67,20 − 54,83); 29,20 a 52,27 jsou jen ze sloupce TensorHub (94,16 − 64,96; 94,16 − 41,89); pro HF vychází z tabulky 45,68, ne 23,46. C5 to po přepisu uvádí; čísla citovat jako údaje autorů, ne obecný výsledek.
- Tab. 5 (s. 10) nesouhlasí s Tab. 1 (s. 8) pro stejná 0-shot nastavení (např. Gorilla HF 58,05 vs. 71,68; TorchHub 75,80 vs. 59,13; GPT-3.5 TorchHub 41,93 vs. 48,38) – při citaci uvádět, ze které tabulky číslo je.
- HuggingFace: autoři uvádějí top 20 modelů na doménu a 925 API, ale 36 domén × 20 = 720 – nesrovnalost v článku (s. 4).
