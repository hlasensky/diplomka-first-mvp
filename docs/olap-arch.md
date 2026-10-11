Na stavbu OLAP enginu neexistuje jedna učebnice. Nejlepší inspirace jsou open-source enginy, které dělají totéž co ty: z modelu kostky (YAML s fakty, dimenzemi, hierarchiemi a mírami) skládají SQL nad relační databází. Seřadil jsem je podle toho, jak moc se blíží tvému případu.

1. Nejbližší tvému návrhu

Cubes (Python, Stefan Urbanek): dokumentace (https://cubes.readthedocs.io/), Wikipedia (https://en.wikipedia.org/wiki/Cubes_(OLAP_server)), slidy z EuroPythonu (https://ep2012.europython.eu/media/conference/slides/cubes-light-weight-olap-framework-and-server.pdf)
- Malý ROLAP framework: model kostky (fakty, dimenze, hierarchie, míry a jejich agregace) a „aggregation browser“, který zpracuje agregační dotazy včetně slice & dice a drill-down a přeloží je do SQL. Dá se použít jako HTTP server s JSON API nebo přímo z Pythonu.
- Co převzít: objekt „cell“ (aktuální řez kostkou) a operace nad ním (slice, drilldown, aggregate). Je to přesně ten stav „kde v kostce jsem“, který potřebuješ pro navigaci. Kód je malý a dá se přečíst celý. Projekt je dnes starší a moc se nevyvíjí, ber ho jako vzor, ne jako závislost.

Mondrian (Java, Pentaho): architektura (https://mondrian.pentaho.com/documentation/architecture.html), přehled od Juliana Hydea (https://workshop.perforce.com/view/guest/julian_hyde/mondrian/doc/overview.html)
- Klasický ROLAP engine: MDX přeloží do SQL a výsledky drží v cache.
- Co převzít: rozdělení na vrstvy (schéma → dotaz → vyhodnocení → SQL), „matcher“, který vybírá agregované tabulky, a cache buněk. Je to referenční architektura do kapitoly o návrhu.

2. Moderní sémantické vrstvy (model → SQL, fan trapy)

dbt MetricFlow: join logika (https://docs.getdbt.com/docs/build/join-logic), jak funguje (https://getdbt.com/blog/how-the-dbt-semantic-layer-works)
- Ze sémantických modelů postaví graf (uzly = modely, hrany = join cesty) a SQL skládá až při dotazu. Typ joinu volí podle typu entity (klíče), aby nevznikl fan-out ani chasm trap. U dotazu přes více faktů používá FULL OUTER JOIN.
- Co převzít: hledání join cesty v grafu a pravidla proti fan trapu. Přímo se to hodí na tvoje R7–R10 a na drill-across.

Malloy: dokumentace a blog (https://docs.malloydata.dev/blog/2024-01-09-whats-next-in-2024), úvod (https://www.hackernoon.com/what-the-heck-is-malloy)
- Od zakladatele Lookeru. Hlídá dvojí započítání při agregaci přes joiny (symmetric aggregates) a umí vnořené dotazy na více úrovních najednou.
- Co převzít: jak korektně agregovat míru přes join 1:N bez předagregace.

Boring Semantic Layer (Python + Ibis): představení (https://juhache.substack.com/p/the-boring-semantic-layer), v2 (https://juhache.substack.com/p/boring-semantic-layer-v2), s MCP (https://juhache.substack.com/p/boring-semantic-layer-mcp)
- Dimenze a míry jsou výrazy v Ibisu, ze kterých se kompiluje SQL pro DuckDB i další databáze. Je stavěná přímo pro LLM agenty: LLM SQL nepíše, jen volí dimenze a míry.
- Co převzít: nejbližší architektura k „LLM jako orchestrátor“. Pokud bys zůstal v Pythonu, Ibis jako generátor SQL ti ušetří psaní SQL řetězců ručně.

Cube (TypeScript/Node): máš s ním vlastní spike (docs/spike_cube.md).
- Generování SQL je v balíčku cubejs-schema-compiler (třída BaseQuery, zmínka (https://mcp.depscope.dev/pkg/npm/cube-schema-compiler)), nový plánovač Tesseract je v Rustu.
- Co převzít: jelikož ti víc sedí TypeScript, je to nejrealističtější kód ke čtení. Ukazuje, jak se definice kostky překládá na SQL, včetně multi-stage měr (měr počítaných z jiných měr na jiném grainu).

3. Optimalizace (až bude potřeba)

Apache Calcite – lattices: dokumentace (https://calcite.apache.org/docs/lattice.html), paper (https://arxiv.org/pdf/1802.10233)
- Lattice je deklarace hvězdicového schématu. Planner pak sám pozná, kdy dotaz zodpoví z předpočítaného agregátu („tile“).
- Co převzít: princip „aggregate navigation“. Tvoje agg_colony_daily a agg_weather_daily jsou takové tiles a engine by je měl volit sám, ne LLM.

Jak to použít

Pro tvůj engine bych četl v tomhle pořadí:
1. COOL C2–C5 (už je ve vaultu): metadata kostky, gramatika operátorů a kontroly proti modelu. Dává ti to, co engine má umět.
2. Cubes: jak v kódu vypadá „cell“ a operace nad ní.
3. MetricFlow, join logika: jak z YAML grafu vybrat join cestu bez fan trapu.
4. Cube (TS) nebo BSL (Python): jak se to dělá prakticky dnes, podle jazyka, ve kterém engine napíšeš.
5. Calcite lattices: až budeš chtít, aby engine sám vybíral agregované tabulky.

Tohle všechno jsou nástroje a dokumentace, ne recenzované zdroje. Do práce patří na úroveň „nástroje“ (s URL a datem přístupu), teoretická opora zůstává COOL, Lenz & Shoshani a Kimball. Nalezené odkazy jsem jen prošel ve výsledcích vyhledávání, jejich obsah jsem do hloubky neověřoval.

Sources:
- Cubes – OLAP Framework (docs) (https://cubes.readthedocs.io/)
- Cubes (OLAP server) – Wikipedia (https://en.wikipedia.org/wiki/Cubes_(OLAP_server))
- Cubes – EuroPython 2012 slides (https://ep2012.europython.eu/media/conference/slides/cubes-light-weight-olap-framework-and-server.pdf)
- Mondrian architecture (https://mondrian.pentaho.com/documentation/architecture.html)
- Mondrian overview (Julian Hyde) (https://workshop.perforce.com/view/guest/julian_hyde/mondrian/doc/overview.html)
- dbt MetricFlow join logic (https://docs.getdbt.com/docs/build/join-logic)
- How the dbt Semantic Layer works (https://getdbt.com/blog/how-the-dbt-semantic-layer-works)
- Malloy blog (https://docs.malloydata.dev/blog/2024-01-09-whats-next-in-2024)
- What the heck is Malloy (https://www.hackernoon.com/what-the-heck-is-malloy)
- The Boring Semantic Layer (https://juhache.substack.com/p/the-boring-semantic-layer)
- Boring Semantic Layer v2 (https://juhache.substack.com/p/boring-semantic-layer-v2)
- Boring Semantic Layer + MCP (https://juhache.substack.com/p/boring-semantic-layer-mcp)
- cube-schema-compiler (https://mcp.depscope.dev/pkg/npm/cube-schema-compiler)
- Apache Calcite lattices (https://calcite.apache.org/docs/lattice.html)
- Apache Calcite paper (https://arxiv.org/pdf/1802.10233)
