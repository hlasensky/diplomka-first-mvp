Perfektní — to je nejchytřejší přístup pro DP. Jeden dataset, jeden use case, funkční demo. Tady je konkrétní plán.

---

## Dataset: Olist Brazilian E-commerce

Použij Olist — máš ho zmíněný v paměti z dřívějších rozhovorů a je ideální protože je zdarma na Kaggle, má přirozené OLAP dimenze (čas, produkt, kategorie, stát, seller), obsahuje časové řady objednávek vhodné pro detekci anomálií, a je dostatečně velký aby demo vypadalo reálně (~100k objednávek).

---

## Jeden use case: Sales Performance Analysis

Konkrétně: uživatel se ptá na prodejní výkonnost, naviguje přes OLAP operace, systém detekuje anomálie v časové řadě tržeb a vysvětlí je přirozeným jazykem s grafem.

Tři demonstrovatelné věci na obhajobě:
- drill-down z kategorie → produkt
- slice podle státu nebo časového období  
- detekce anomálie v tržbách s narativním vysvětlením

---

## MVP architektura — co vynechat, co zachovat

Oproti plné architektuře MVP vynechá Laravel Queue/WebSocket (synchronní HTTP stačí), Qdrant (jednoduchý YAML přímo v paměti), anomály detektor bude statistický (Z-score nebo IQR, ne full AXIS framework), a frontend bude Chainlit místo React+Laravel.

```
Chainlit (chat UI + Plotly grafy jako message elementy)
    ↕ HTTP
FastAPI (LangGraph agent)
    ↕
DuckDB (Olist Parquet) + YAML sémantické schema + Claude (Sonnet)
```

Tři soubory konfigurace, žádný Docker nutný pro vývoj, spustíš lokálně za hodinu.

---

## Fáze MVP — 6 týdnů

**Týden 1 — data a schema**

Stáhni Olist z Kaggle, načti do DuckDB jako Parquet. Napiš YAML sémantické schema — definuj 5 metrik (revenue, orders, avg\_order\_value, cancellation\_rate, delivery\_time) a 4 dimenze (čas, kategorie, stát, seller). Toto je základ všeho ostatního.

```yaml
metrics:
  revenue:
    label: "Celkové tržby"
    sql: "SUM(payment_value)"
  orders:
    label: "Počet objednávek"  
    sql: "COUNT(order_id)"

dimensions:
  category:
    label: "Kategorie produktu"
    column: "product_category_name"
  state:
    label: "Stát zákazníka"
    column: "customer_state"
```

**Týden 2 — LangGraph agent**

Jeden stavový graf se třemi uzly: `parse_intent` (LLM rozhodne jaká OLAP operace), `execute_query` (DuckDB přes schema), `generate_response` (LLM vysvětlení + chart spec). State drží aktuální filtry a dimenzi.

Tohle rozšířím o další uzly prompt, rag, improve_prompt, clarify_intent, execute_query, generate_response možná další.

**Týden 3 — Chainlit UI**

`@cl.on_message` napojený na LangGraph agenta, Plotly graf pod každou odpovědí jako `cl.Plotly()` element, sidebar/starter zprávy se stavem aktuální analýzy (aktivní filtry). Pár hodin práce pokud znáš Python.

**Týden 4 — OLAP operace**

Drill-down a slice jako explicitní nástroje (LangChain tools) které agent volá. Otestuj 10 konverzačních scénářů ručně.

**Týden 5 — anomálie**

Z-score nad časovou řadou tržeb po týdnech. Pokud Z > 2.5, LLM dostane kontext anomálie a vygeneruje narativní vysvětlení. Stačí 30 řádků Pythonu.

**Týden 6 — evaluace**

Připrav 20 testovacích dotazů nad Olist daty, změř přesnost OLAP operací (správná dimenze? správný filtr?). Toto jsou tvá čísla do experimentální kapitoly DP.

---
