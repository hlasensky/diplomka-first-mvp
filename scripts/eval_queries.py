"""Evaluace přesnosti OLAP operací (týden 6 z plánu) - 20 testovacích dotazů.

Pro každý dotaz zkontroluje, že agent rozpoznal očekávanou metriku/fact+agg/dimenzi/filtry
a že dotaz nad DuckDB proběhl bez chyby. Nekontroluje přesné znění `answer` (to je na LLM),
jen strukturovaný `intent` a úspěšnost provedení.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from graph import graph, build_graph, ensure_read_only_select  # noqa: E402

TEST_CASES = [
    {"question": "Jaké jsou celkové tržby?", "expected": {"metric": "revenue", "dimension": None}},
    {"question": "Kolik bylo objednávek v roce 2017?", "expected": {"metric": "orders"}},
    {"question": "Jaká je průměrná hodnota objednávky?", "expected": {"metric": "avg_order_value"}},
    {"question": "Jaká je míra zrušených objednávek?", "expected": {"metric": "cancellation_rate"}},
    {"question": "Jak dlouho v průměru trvá doručení?", "expected": {"metric": "delivery_time"}},
    {"question": "Ukaž mi tržby podle kategorie", "expected": {"metric": "revenue", "dimension": "category"}},
    {"question": "Rozděl počet objednávek podle státu", "expected": {"metric": "orders", "dimension": "state"}},
    {"question": "Jaké jsou tržby podle týdnů?", "expected": {"metric": "revenue", "dimension": "time"}},
    {"question": "Jaké jsou tržby podle měsíců?", "expected": {"metric": "revenue", "dimension": "time", "granularity": "month"}},
    {"question": "Kolik jsme vydělali na kráse a zdraví?", "expected": {"metric": "revenue", "category_filter": "beleza_saude"}},
    {"question": "Jaké byly tržby v kategorii cama_mesa_banho ve třetím čtvrtletí 2018?", "expected": {"metric": "revenue", "category_filter": "cama_mesa_banho"}},
    {"question": "Jaké byly tržby v SP?", "expected": {"metric": "revenue", "state_filter": "SP"}},
    {"question": "Jaká je průměrná cena dopravy?", "expected": {"fact": "freight_value", "agg": "avg"}},
    {"question": "Jaká je maximální cena produktu podle kategorie?", "expected": {"fact": "price", "agg": "max", "dimension": "category"}},
    {"question": "Jaký je celkový součet cen produktů podle sellera?", "expected": {"fact": "price", "agg": "sum", "dimension": "seller"}},
    {"question": "Kolik vyděláváme na sportovním vybavení?", "expected": {"metric": "revenue", "category_filter": "esporte_lazer"}},
    {"question": "Jaké jsou tržby podle sellera?", "expected": {"metric": "revenue", "dimension": "seller"}},
    {"question": "Jaká je průměrná doba doručení v RJ?", "expected": {"metric": "delivery_time", "state_filter": "RJ"}},
    {"question": "Jaké bylo počasí včera v Praze?", "expected": {"unclear": True}},
    {"question": "asdkjaskdj nesmyslny text xyz", "expected": {"unclear": True}},
]


def check(intent, expected: dict) -> list[str]:
    mismatches = []
    if expected.get("unclear"):
        if intent is not None and intent.has_metric():
            mismatches.append(f"čekal jsem 'unclear', ale intent má metric/fact+agg: {intent}")
        return mismatches

    for field, value in expected.items():
        actual = getattr(intent, field, None) if intent is not None else None
        if actual != value:
            mismatches.append(f"{field}: čekal '{value}', dostal '{actual}'")
    return mismatches


MULTI_TURN_CASES = [
    {
        "questions": [
            "Jaké jsou tržby a počet objednávek podle kategorie?",
            "ukaž mi průběh objednávek v čase pro kategorii cama_mesa_banho",
        ],
        "expected_last": {"dimension": "time", "category_filter": "cama_mesa_banho"},
    },
]


def run_multi_turn():
    passed = 0
    for i, case in enumerate(MULTI_TURN_CASES, 1):
        thread = {"configurable": {"thread_id": f"eval-multiturn-{i}"}}
        results = [graph.invoke({"question": q}, config=thread) for q in case["questions"]]
        result = results[-1]

        intent = result.get("intent")
        mismatches = check(intent, case["expected_last"])
        if result.get("validation_error"):
            mismatches.append(f"SQL chyba: {result['validation_error']}")
        if result.get("rows") == results[0].get("rows"):
            mismatches.append("rows stejné jako v prvním tahu - druhý dotaz asi neproběhl s novým intentem")

        ok = not mismatches
        passed += ok
        status = "OK " if ok else "FAIL"
        print(f"[{status}] multi-turn {i}. {' -> '.join(case['questions'])}")
        for m in mismatches:
            print(f"        - {m}")

    print(f"Multi-turn přesnost: {passed}/{len(MULTI_TURN_CASES)}")
    return passed == len(MULTI_TURN_CASES)


def guardrail_checks() -> bool:
    """Rychlé unit checky pro `ensure_read_only_select` (bez LLM/DB)."""
    must_reject = [
        "DROP TABLE orders;",
        "SELECT 1; DROP TABLE orders",
        "UPDATE orders SET price = 0",
        "DELETE FROM orders",
        "INSERT INTO orders VALUES (1)",
        "PRAGMA database_list",
        "ATTACH 'evil.db'",
        "",
    ]
    must_pass = [
        "SELECT product_category_name, SUM(payment_value) AS revenue FROM orders GROUP BY 1",
        "WITH t AS (SELECT * FROM orders) SELECT COUNT(*) FROM t",
    ]
    passed = 0
    total = len(must_reject) + len(must_pass)
    for sql in must_reject:
        try:
            ensure_read_only_select(sql)
            print(f"[FAIL] guardrail should have rejected: {sql!r}")
        except ValueError:
            passed += 1
    for sql in must_pass:
        try:
            out = ensure_read_only_select(sql)
            assert "limit" in out.lower(), "chybí vynucený LIMIT"
            passed += 1
        except (ValueError, AssertionError) as e:
            print(f"[FAIL] guardrail should have passed: {sql!r} ({e})")
    print(f"Guardrail checks: {passed}/{total}")
    return passed == total


def run_freesql() -> bool:
    """Free Text-to-SQL eval: bez `intent` kontrolujeme jen úspěšné provedení a neprázdný výsledek."""
    fs_graph = build_graph("freesql")
    passed = 0
    for i, case in enumerate(TEST_CASES, 1):
        thread = {"configurable": {"thread_id": f"eval-freesql-{i}"}}
        result = fs_graph.invoke({"question": case["question"]}, config=thread)

        unclear = case["expected"].get("unclear", False)
        error = result.get("validation_error")
        rows = result.get("rows") or []

        if unclear:
            ok = True  # nesmyslné dotazy jen nesmí spadnout tvrdě; prázdný/degradovaný výstup je OK
        else:
            ok = error is None and len(rows) > 0

        passed += ok
        status = "OK " if ok else "FAIL"
        print(f"[{status}] free-SQL {i:2d}. {case['question']}")
        if not ok and error:
            print(f"        - SQL chyba: {error}")
        elif not ok:
            print("        - prázdný výsledek")

    print(f"\nFree-SQL úspěšnost: {passed}/{len(TEST_CASES)} ({100 * passed / len(TEST_CASES):.0f}%)")
    return passed == len(TEST_CASES)


def main():
    passed = 0
    for i, case in enumerate(TEST_CASES, 1):
        thread = {"configurable": {"thread_id": f"eval-{i}"}}
        result = graph.invoke({"question": case["question"]}, config=thread)

        intent = result.get("intent")
        mismatches = check(intent, case["expected"])

        exec_ok = not case["expected"].get("unclear") and result.get("validation_error") is None
        if case["expected"].get("unclear"):
            exec_ok = True  # unclear dotazy se do execute_query vůbec nedostanou

        ok = not mismatches and exec_ok
        passed += ok

        status = "OK " if ok else "FAIL"
        print(f"[{status}] {i:2d}. {case['question']}")
        if mismatches:
            for m in mismatches:
                print(f"        - {m}")
        if not case["expected"].get("unclear") and result.get("validation_error"):
            print(f"        - SQL chyba: {result['validation_error']}")

    print(f"\nPřesnost: {passed}/{len(TEST_CASES)} ({100 * passed / len(TEST_CASES):.0f}%)")

    print()
    run_multi_turn()


if __name__ == "__main__":
    # `--freesql` = eval free Text-to-SQL režimu (potřebuje běžící LLM); guardrail checky jsou vždy.
    if "--freesql" in sys.argv:
        guardrail_checks()
        print()
        run_freesql()
    else:
        guardrail_checks()
        print()
        main()
