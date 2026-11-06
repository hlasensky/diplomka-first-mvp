# Požadavky FIT VUT na diplomovou práci

Staženo 5. 11. 2026 z webu FIT. Jde o výtah, závazné jsou směrnice uvedené na konci. Položky označené ⚠ nebyly ověřeny proti zdroji.

Zdroje:
- https://www.fit.vut.cz/study/theses/master-theses/.cs (EN verze bez `.cs`)
- https://www.fit.vut.cz/study/theses/schedule/ (harmonogram)
- https://www.fit.vut.cz/study/theses/citations/ (citace)
- https://www.fit.vut.cz/study/theses/theses-advice/ (rady k sazbě a normostraně)
- https://www.fit.vut.cz/study/study-rules/ (seznam předpisů)

## Termíny 2026/2027

| co | kdy |
|---|---|
| schválené zadání v IS | začátek listopadu 2026 (bez schváleného zadání po 1. 11. kontaktovat vedoucího) |
| semestrální projekt (technická zpráva, cca polovina rozsahu DP) | první dny zkouškového období zimního semestru, leden 2027; v IS modul „Moje závěrečná práce“, typ souboru „Semestrální část práce“; nejméně týden před obhajobou SP |
| obhajoba semestrálního projektu | od zhruba poloviny 2. týdne zkouškového do poloviny posledního týdne; termíny zveřejněny kolem poloviny prosince ⚠ (stránka uvádí „ne dříve než 12. 1. 2026“, zřejmě neaktualizováno) |
| žádost o odklad zveřejnění | nejméně měsíc před odevzdáním (duben) |
| žádost o pozdější odevzdání | nejméně 2 týdny před termínem |
| text vedoucímu | nejméně 1–2 týdny před odevzdáním; méně než cca 3 dny předem vedoucí uvede v posudku a sníží to hodnocení |
| **odevzdání DP** | **do 19. 5. 2027** (elektronicky v IS i tištěně; práce je odevzdaná až po obojím) |
| státní závěrečná zkouška (MIT) | 18.–24. 6. 2027 |

Vazbu objednat 3–7 dní předem.

## Rozsah

- Minimum 50, obvykle 80–100, maximálně 120 normostran.
- 1 normostrana = 1800 znaků včetně mezer.
- Počítá se jen jádro práce. Nepočítá se abstrakt, klíčová slova, prohlášení, obsah, literatura ani přílohy. Obrázky se odhadují podle plochy.
- Kontrola: `make normostrany` v `thesis/`, nebo https://app.fit.vut.cz/theses-checker.
- Semestrální projekt má zhruba polovinu rozsahu DP.

## Formální úprava (rady, ne závazná pravidla)

- A4, zpravidla jednostranně (oboustranně lze s různými okraji).
- Základní písmo 11 pt, řádkování 120 %; v LaTeXu ponechat výchozí nastavení šablony.
- Nejvýše tři úrovně nadpisů pod kapitolou; nadpisy malými písmeny kromě prvního.
- Obrázky a tabulky číslované po kapitolách (např. 2.7), rovnice v závorce u pravého okraje.
- Pomlčky: spojovník „Brno-město“, rozsah `23--25`, vsuvka `---`.
- Doporučen seznam zkratek a symbolů.
- Uvádět původ faktů a jasně oddělit vlastní přínos. Ich-forma je přípustná pro vymezení vlastní práce, ale ne nadužívat; „my“ je v pořádku.
- Šablona: https://www.fit.vut.cz/study/theses/sablona.zip (repo ji používá: `thesis/fitthesis.cls`).

## Citace

- Norma ČSN ISO 690:2022, číselné odkazy v hranatých závorkách [1], seznam literatury na konci práce.
- Online zdroje s datem citace (BibTeX `cited = {yyyy-mm-dd}`, typ `@website`/`@webpage`). Články z časopisů a konferencí citovat jako články, ne jako elektronické zdroje.
- Citovat vše použité, jen skutečně použité, primární zdroje, přesně.
- Krátké citace v uvozovkách, dlouhé odsazeným blokem; jinak raději parafráze s odkazem. Převzatou podkapitolu lze označit větou „Tato podkapitola je převzata z [1].“
- Převzaté úryvky kódu uvést i v textu práce, ne jen ve zdrojovém souboru.
- Porušení pravidel citování má na hodnocení výrazně horší dopad než formální nedostatky.

## Odevzdání

Tištěně:
- jeden výtisk s podepsaným prohlášením a vloženým zadáním (PDF z IS), pevná vazba, kterou nelze rozebrat;
- odevzdává se v kanceláři C208, až po elektronickém odevzdání.

Elektronicky (IS VUT, modul „Moje závěrečná práce“):
- text práce v PDF (velikost v jednotkách MB; desítky MB značí chybu, obvykle obrázky);
- abstrakt a klíčová slova česky (nebo slovensky) i anglicky;
- po zaškrtnutí finálního odevzdání už nelze nic měnit.

NextCloud FIT (https://nextcloud.fit.vutbr.cz/, odkaz se vloží do formuláře v IS):
- zdrojové texty práce se vším potřebným k vytvoření PDF;
- kompletní dokumentace (instalační a uživatelský manuál);
- zdrojové kódy programů (binárky musí jít sestavit ze zdrojů);
- programy ve spustitelné podobě.

Bez těchto součástí se práce nepovažuje za odevzdanou. Programy by měly jít přeložit a spustit v prostředí CVT FIT; pokud to není možné (např. chybí SW nebo HW), je nutné funkční řešení předvést oponentovi.

Odklad zveřejnění (až 5 let, se souhlasem proděkana): plná verze navíc na nepřepisovatelném médiu (CD-R/DVD-R v ISO9660 nebo UDF, případně SD karta) s loginem nebo jménem.

## Obhajoba a SZZ

- SZZ má dvě ústní části: obhajobu DP a zkoušku z tematických okruhů. Okruhy pro MITAI vyhlašuje fakulta každý rok (pro 2025/26: https://www.fit.vut.cz/fit/info/rozhodnuti/2026/rd13-260402.pdf ⚠ nestaženo).
- Prezentace DP **8 minut**, pak diskuse.
- Úvodní slajd: jméno, název práce, vedoucí. Číslování slajdů „aktuální/celkem“. Video vložit přímo do prezentace.
- Prezentaci přinést na flashce, ideálně ve složce pojmenované loginem.
- Šablony prezentace: LaTeX https://www.fit.vut.cz/study/theses/Sablona_prezentace_2024.zip, PowerPoint https://www.fit.vut.cz/study/theses/Sablona_prezentace_pptx_2022.zip (jiné jsou povoleny).
- Termín, místo a komise nejpozději týden předem v IS, modul „Moje komise“.
- Při neúspěšné obhajobě se neopakují předměty, jen se práce znovu odevzdá a obhajuje.

## Neověřeno ⚠

- **Směrnice děkana č. 7/2018** (úprava, odevzdání a zveřejnění prací na FIT): PDF se nepodařilo přečíst. Pravidla pro používání AI nástrojů a kritéria hodnocení mohou být tam; na webových stránkách nejsou.
- **Směrnice č. 2/2026 Závěrečné práce na VUT** (struktura, desky, titulní list) a **Směrnice č. 2/2023 Pravidla pro SZZ na FIT**: nestaženo.
- Články studijního a zkušebního řádu VUT k SZZ: EN verze uvádí čl. 23–27, CZ verze čl. 22–27.

## Předpisy

- Směrnice rektora č. 72/2017 – Úprava, odevzdávání a zveřejňování závěrečných prací
- Směrnice děkana č. 7/2018 – totéž pro FIT: https://www.fit.vut.cz/fit/info/smernice/2018/sm2018-07-uz-4-en.pdf
- Směrnice č. 2/2026 – Závěrečné práce na VUT
- Směrnice č. 2/2023 – Pravidla pro SZZ v bakalářském a magisterském studiu na FIT VUT
- Směrnice č. 13/2018 – Pravidla organizace studia na FIT (čl. 12 a 12a k SZZ)
- Studijní a zkušební řád VUT

## Otevřené body v `thesis/projekt.tex`

- `title.en={Thesis title}` – doplnit anglický název podle zadání.
- Prohlášení obsahuje šablonový text o ChatGPT a Copilotu s „[konkretizujte a upravte podle skutečnosti]“ – upravit podle skutečného použití nástrojů.
