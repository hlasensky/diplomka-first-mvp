---
type: guide
---

# Čtení

Přehled zdrojů ve vaultu podle `precteno` (ne → abstrakt → uvod-zaver → prolet → cele). Hodnotu měníš v Properties dané poznámky. Položky ze seznamu literatury, které ještě nejsou v Zoteru, najdeš v `qc/_plan.md`. Tabulky vykresluje plugin Dataview.

## Souhrn podle úrovně

```dataview
TABLE WITHOUT ID
  uroven AS "Úroveň",
  length(rows) AS "Zdrojů",
  length(filter(rows.precteno, (p) => p != "ne" AND p != "abstrakt")) AS "Víc než abstrakt",
  length(filter(rows.precteno, (p) => p = "cele")) AS "Celé",
  length(filter(rows, (r) => r.status = "confirmed" AND r.verified = true)) AS "Ověřeno"
FROM "sources"
GROUP BY uroven
SORT uroven ASC
```

## Zbývá přečíst

Nečtené nebo jen s přečteným abstraktem, nejdřív povinné.

```dataview
TABLE WITHOUT ID
  file.link AS "Zdroj",
  uroven AS "Úroveň",
  precteno AS "Přečteno",
  year AS "Rok"
FROM "sources"
WHERE precteno = "ne" OR precteno = "abstrakt"
SORT uroven ASC, year DESC
```

## Všechny zdroje

```dataview
TABLE WITHOUT ID
  file.link AS "Zdroj",
  uroven AS "Úroveň",
  precteno AS "Přečteno",
  status AS "Status",
  verified AS "Ověřeno"
FROM "sources"
SORT uroven ASC, choice(precteno = "cele", 5, choice(precteno = "prolet", 4, choice(precteno = "uvod-zaver", 3, choice(precteno = "abstrakt", 2, 1)))) DESC
```
