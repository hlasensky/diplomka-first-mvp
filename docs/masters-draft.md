# Analýza časových řad v IoT pomocí LLM

## Úvod

## Internet věcí, chytrá zařízení a časové řady

### Charakteristiky senzorických dat z IoT zařízení

### Základní pojmy a vlastnosti časových řad

## Vizualizace a nástroje pro analýzu časových řad

### Přístupy k vizualizaci časových řad

### Existující nástroje a platformy

### OLAP a vícerozměrný datový model

Úvod do OLAP stručně, 1–1,5 strany.

#### Průzkum datové kostky řízený výjimkami a míry zajímavosti

#### Vysvětlování agregovaných hodnot a jejich změn

#### Analýza řízená záměrem a konverzační OLAP

### Existující nástroje pro OLAP nad daty z IoT

## Velké jazykové modely pro práci s daty

### Převod přirozeného jazyka na dotazy a volání nástrojů

### Agentní přístupy a řízení vícekrokové analýzy

### Využití jazykových modelů pro analýzu časových řad a vysvětlování anomálií

### Lokálně provozované a cloudové modely

### Halucinace a ověřitelnost výstupů

## Analýza požadavků

### Datová sada a požadavky na data

Vlastní datová sada (BeeObserver + kontext): proč je dostatečně složitá, požadavky na data, IoT zařízení.

### Cíloví uživatelé a scénáře užití

### Požadované operace OLAP nad časovými řadami

### Uložení dat v databázi časových řad a relační databázi

Požadavky na systém, když jsou data v databázi časových řad i v relační databázi; ověření, zda to jde a jak.

### Požadavky na analýzu augmentovanou pomocí jazykových modelů

### Analýza jazykových modelů

Co model musí umět a proč: tool calling, strukturovaný výstup, vícekrokové plánování, délka kontextu, věrnost číslům, jazyk, lokální provoz a cloud. Na konci kritéria výběru, kandidátní modely a co se u nich měří (navazuje na srovnání modelů v testování).

### Nefunkční požadavky

## Návrh platformy pro vykonávání a vysvětlování dotazů

### Návrh interakce s jazykovým modelem

Celý průběh komunikace uživatel – LLM – engine.

### Architektura platformy

### Datový model

### Vrstva analytických operací

### Detekce anomálií a jejich vysvětlení

### Integrace jazykových modelů a volba mezi lokálními a cloudovými modely

Výběr konkrétních modelů, přepínání backendu, degradace podle schopností, nástroje podle modelu.

### Návrh interaktivních vizualizací

### Uživatelské rozhraní

## Implementace

### Sestavení datové sady

## Testování a vyhodnocení

### Funkční testování

### Uživatelské testování

### Srovnání jazykových modelů z hlediska výkonu a kvality analýzy

### Diskuse výsledků a omezení řešení

## Závěr
