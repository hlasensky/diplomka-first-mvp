---
citekey: greengardInternetThings2015
title: "The Internet of Things"
authors: "Greengard, Samuel"
year: 2015
venue: "MIT Press, Cambridge, Massachusetts (MIT Press Essential Knowledge Series)"
kind: book
status: candidate   # confirmed | candidate | rejected
verified: false     # true = tvrzení ověřená proti PDF mnou
precteno: ne         # ne | abstrakt | uvod-zaver | prolet | cele – jak daleko jsem paper četl (mění jen já)
chapters: []
concepts:
  - internet-of-things
uroven: 1
---

PDF: [otevřít v Zoteru](zotero://open-pdf/library/items/A549WK5P)

## TL;DR
Populárně-naučná kniha z edice MIT Press Essential Knowledge o Internetu věcí. Úvod a první dvě kapitoly vysvětlují, co se IoT rozumí („věci“ s identifikátorem a IP adresou připojené k internetu i k sobě navzájem), odkud se pojem vzal (Auto-ID Center na MIT, Kevin Ashton 1999, RFID) a proč se rozvinul až s komerčním internetem, chytrými telefony, cloudem a big data. Kniha je psaná novinářsky a čísla přebírá od firem (Cisco, ABI Research, IDC, Gartner), sama nic neměří.

## Klíčová tvrzení
- C1: Autor definuje [[internet-of-things]] doslova jako „věci“ či objekty, které se připojují k internetu i k sobě navzájem (počítač, chytrý telefon, fitness náramek, žárovka, zámek, motor letadla…). Každá taková věc má jedinečné identifikační číslo (UID) a IP adresu, připojuje se kabelem nebo bezdrátově (satelity, mobilní sítě, Wi-Fi, Bluetooth) přes vestavěnou elektroniku nebo dodatečně přidané RFID/NFC čipy a tagy. Podstatou IoT je pohyb dat, který umožňuje procesy na dálku. (s. 14, §Defining the Terms, Understanding the Concept)
- C2: Kniha rozlišuje několik souvisejících pojmů. „Connected devices“ jsou zařízení, která si vyměňují data po síti, i soukromé nebo uzavřené. Podle ABI Research (2014) existují objekty „physical-first“, které data samy negenerují, a „digital-first“, které data generují a předávají už ze své podstaty. „Industrial Internet“ tvoří stroje vybavené senzory a komunikace v něm probíhá jako M2M, H2M a M2S. Propojení s lidmi autor nazývá Internet of Humans (IoH) a souhrn všeho Internet of Everything (IoE, termín firmy Cisco), kde fyzický a digitální svět splývají. (s. 14–15, §Defining the Terms)
- C3: Myšlenka propojených zařízení se podle autora objevila na začátku devadesátých let ve výzkumu Auto-ID Center na MIT. Termín „Internet of Things“ zavedl v roce 1999 Kevin Ashton, spoluzakladatel Auto-ID Center, který už v roce 1997 zvažoval RFID pro dodavatelský řetězec firmy P&G. RFID tehdy výzkumníci považovali za nutného předchůdce IoT. Ashton v článku pro RFID Journal (2009) uvádí, že IoT mění vstup dat z čistě lidského na lidský i strojový, protože lidé mají omezený čas, pozornost a přesnost a počítače musí umět sbírat informace o světě samy. (s. 15–16, §Defining the Terms)
- C4: Za základ IoT autor považuje internet, který podle něj slouží jako „elektrické vedení“ IoT a umožňuje komunikaci a sdílení dat v reálném čase v masovém měřítku. Internet a WWW byly komercializovány v roce 1995. Jedinou spouštěcí událost podle autora určit nelze, za krystalizující moment ale považuje uvedení iPhonu (2007), které spolu s iPadem (2010) „zapálilo“ dnešní IoT. Dnes každé připojené zařízení dostává IP adresu a IP je standardním kanálem komunikace. Podle modelu adopce technologií (Bohlen, Beal, Rogers, 1957) se IoT v době psaní nachází mezi fází inovátorů a early adopters. (s. 9, §Introduction; s. 10, §Introduction; s. 12–13, §A Brief Look at How We Got Here)
- C5: Kniha přebírá odhady firmy Cisco: v dubnu 2014 bylo v provozu přibližně 12,1 miliardy zařízení připojených k internetu, do roku 2020 má jejich počet přesáhnout 50 miliard. Dnes se připojí asi 100 „věcí“ za sekundu, do roku 2020 to má být 250 za sekundu. Ve fyzickém světě existuje přes 1,5 bilionu „věcí“ a 99 % z nich se má nakonec stát součástí sítě. Autor sám poznamenává, že teprve čas ukáže, zda je tento odhad přehnaně optimistický. (s. 14, §A New Deal)
- C6: Jako omezení autor uvádí, že IoT je teprve v počátcích a čeká ho řada technických problémů: lepší a výdržnější baterie, menší zařízení s více senzory, zabudování senzorů do oblečení i strojů, lepší algoritmy pro třídění všech dat (doslova „keep the signal-to-noise ratio low“) a standardy a platformy pro sdílení dat a kompatibilitu. IoT podle něj také zvyšuje bezpečnostní rizika a přináší nové hrozby. Podle průzkumu ISACA (2013) má 92 % veřejnosti obavy z informací, které sbírají zařízení připojená k internetu. (s. 16, §Defining the Terms; s. 17, §A Sense of Security)
- C7: Připojená zařízení podle autora průběžně hlásí využití, provozní chování, stav a další informace, takže vytvářejí velké množství dat, která lze analyzovat a podle nich jednat. Samotná mobilní zařízení a sítě by ale IoT nevytvořily. Teprve propojení mobility s cloudem, sociálními médii a big data vytváří silnější platformu. Cloud autor popisuje jako distribuované výpočetní prostředí běžící přes rozsáhlou síť, jako je internet. Podle něj by žádná organizace ani vláda nedokázala sama vybudovat úložnou infrastrukturu pro IoT. API umožňují zařízením a systémům komunikovat, i když používají různé standardy nebo protokoly. (s. 20, §How Mobile Technology Changes Everything; s. 21, §A Clearer View through Clouds)
- C8: Big data autor vysvětluje třemi složkami podle Douga Laneyho (2001): objem (volume), rychlost (velocity) a rozmanitost (variety). IoT podle něj exponenciálně zvyšuje počet datových zdrojů i všechna tři V a patří do něj vše, co dokáže streamovat data do cloudu a do analytických systémů pracujících v reálném čase. Výzvou je najít ta správná data a efektivně je využít. Podle Cisco rostou objemy dat o 50–60 % ročně a IDC předpovídá do roku 2020 celosvětově 40 zettabajtů dat. (s. 22, §Big Data = Big Results; s. 23, §Big Data = Big Results)

## Vztah k mé práci


## Citovat pro


## Pozor
- Kniha si v datu odporuje: Auto-ID Center klade do „early 1990s“, ale na téže straně (s. 15) píše, že centrum vzniklo dva roky po roce 1997, tedy 1999. C3 přebírá první údaj, citovat opatrně.
- Rozsah ingestu: na pokyn uživatele jsou tvrzení jen z úvodu a kapitol 1–2. Fulltext obsahuje celou knihu (kap. 3–7, glosář, poznámky, rejstřík), ale ty jsem nezpracoval.
- PDF má 73 stran, ale jde o celou knihu, ne o výňatek. Je to převod e-booku z Calibre (Calibre 5.22.1, formát letter) s hustou sazbou bez tištěného stránkování. Obsahuje obsah, úvod, kapitoly 1–7, glosář (PDF s. 62–64), poznámky (s. 65–66), další literaturu (s. 67) a rejstřík (s. 68–73).
- Rozsah zpracovaných částí v PDF: úvod = PDF s. 9–10, kap. 1 „The Internet Changes Everything“ = PDF s. 11–17, kap. 2 „Mobility, Clouds, and Digital Tools Usher in a Connected World“ = PDF s. 18–24.
- Čísla stran: v PDF nejsou tištěná čísla stran, všechna „s. N“ výše jsou strany PDF. Tištěné vydání (asi 200 stran) má jiné stránkování a z tohoto PDF ho nelze odvodit. Pro LaTeX buď dohledej tištěné strany v papírovém vydání, nebo cituj kapitolu.
- ISBN v bib (978-0-262-52773-6) se shoduje s tiráží (PDF s. 5), kde je uvedené jako „hardcover“. E-book má ISBN 978-0-262-32894-4. DOI kniha nemá. litqc meta (OpenAlex přiřadil článek ze Scientific American z roku 2004) je falešně pozitivní, uživatel to přijal.
- Fulltext: 0 stran přepsaných OCR, 0 PAGE_WARN. Kniha nemá tabulky ani obrázky.
- Kniha je populárně-naučná a novinářská. Téměř všechna čísla (C5, C6, C8) přebírá od firem a průzkumů (Cisco, ABI Research, ISACA, IDC, Gartner) a poznámky odkazují většinou na firemní blogy a whitepapery (PDF s. 65). Prognózy k roku 2020 jsou z pohledu roku 2026 historické. Pro přesná čísla raději cituj primární zdroj nebo odbornou literaturu.
- Ashtonův citát (C3) pochází z článku „That ‘Internet of Things’ Thing“ (RFID Journal, 2009). Kniha ho cituje v pozn. 4 kap. 1 (PDF s. 65).
