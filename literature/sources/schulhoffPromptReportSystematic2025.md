---
citekey: schulhoffPromptReportSystematic2025
title: "The Prompt Report: A Systematic Survey of Prompt Engineering Techniques"
authors: "Schulhoff, Sander; Ilie, Michael; Balepur, Nishant; et al. (31 autorů)"
year: 2025
venue: "arXiv:2406.06608 (v6, 26. 2. 2025)"
kind: preprint   # journal | conference | preprint | book | misc
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts: [prompt-engineering, structured-output, llm-agents]
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/BRFSIDY3)

## TL;DR
Systematický přehled (PRISMA) literatury o [[prompt-engineering|promptování]], který sjednocuje terminologii (prompt, šablona promptu, technika promptování, prompt engineering, řetězení promptů) a třídí 58 textových technik do 6 kategorií. Popisuje také složky promptu, [[structured-output|formátování a extrakci odpovědi]] (answer engineering) a rozšíření promptování na [[llm-agents|agenty s nástroji]].

## Klíčová tvrzení
- C1: Přehled předkládá slovník 33 pojmů, taxonomii 58 technik promptování LLM a 40 technik pro jiné modality; vychází ze systematické rešerše podle PRISMA nad arXiv, Semantic Scholar a ACL, kde ze 4 247 unikátních záznamů vybrali 1 565 relevantních. (s. 1, Abstract; s. 8, §2.1)
- C2: Prompt je vstup do generativního modelu, který řídí jeho výstup; šablona promptu (prompt template) je funkce s jednou nebo více proměnnými, po jejichž nahrazení vznikne prompt jako instance šablony. (s. 5, §1.1)
- C3: Běžné složky promptu jsou pokyn (directive, jádro záměru), příklady (exemplars, shots), formátování výstupu, stylové pokyny, role (persona) a doplňující informace; autoři nedoporučují pro doplňující informace používat přetížený pojem „context“. (s. 5–6, §1.2.1)
- C4: K formátování výstupu autoři uvádějí, že strukturování výstupu může na některých úlohách snížit výkon (Tam et al., 2024), ale Kurt (2024) ukazuje nedostatky této studie a že strukturování výstupu může výkon naopak zlepšit. (s. 5–6, §1.2.1)
- C5: Technika promptování je předpis, jak strukturovat prompt nebo dynamickou posloupnost více promptů (včetně větvení a paralelismu); prompt engineering je iterativní proces vývoje promptu úpravou nebo změnou použité techniky; řetězení promptů (prompt chain) jsou dvě nebo více šablon za sebou, kde výstup jedné parametrizuje další. (s. 7, §1.2.2)
- C6: 58 textových technik je rozděleno do 6 hlavních kategorií: zero-shot, few-shot (učení v kontextu), generování myšlenek (thought generation), dekompozice, ensembling a sebekritika (self-criticism); učení v kontextu (ICL) znamená, že se model naučí úlohu z příkladů nebo pokynů v promptu bez úpravy vah. (s. 8, §2.2–2.2.1; s. 9, Obr. 2.2)
- C7: Answer engineering je iterativní vývoj nebo výběr algoritmů, které z výstupu LLM extrahují přesnou odpověď; zahrnuje tři rozhodnutí: prostor odpovědi, tvar odpovědi a extraktor (pravidlo, např. regulární výraz, nebo samostatný LLM). (s. 18, §2.5)
- C8: Agenti jsou generativní systémy, které plní cíle uživatele akcemi zasahujícími do systémů mimo samotný model; nástroje mohou být symbolické (kalkulačka, interpret kódu) i neuronové (jiný LLM) a MRKL je jedna z nejjednodušších formulací agenta, LLM router s přístupem k více nástrojům. (s. 24, §4.1–4.1.1)

## Vztah k mé práci


## Citovat pro


## Pozor
- Preprint na arXivu (v6, 26. 2. 2025), recenzovaná verze zatím neznámá; DOI 10.48550/arXiv.2406.06608 registruje DataCite (Crossref ho nezná, `meta` hlásí DOI_INVALID – uživatel potvrdil, že je v pořádku).
- Dvousloupcová sazba: v textovém přepisu se sloupce místy prolínají, tvrzení ověřit proti PDF.
- Fulltext: strany 37 a 77 nahrazeny OCR, PAGE_WARN na s. 17 (tabulka); tvrzení z nich nejsou.
- C4 je spor citovaný autory (Tam vs. Kurt), ne vlastní měření přehledu.
- Text-based techniky jsou pro prefixové prompty (hard prefix prompts); trénování gradientem je mimo rozsah (s. 8).
