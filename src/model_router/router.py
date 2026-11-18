from __future__ import annotations

import re
from dataclasses import dataclass

COMPLEX = re.compile(
    r"(compara|analiza|explica a detalle|multi[- ]?paso|razona|trade-?off|arquitectura)",
    re.I,
)
OUT_OF_SCOPE = re.compile(
    r"(viaje a marte|interplanetario|precio secreto|2099|olvidar tus reglas)",
    re.I,
)
SIMPLE = re.compile(
    r"(cuál es|cual es|qué es|que es|límite|limite|descuento|requisito|horario)",
    re.I,
)

COST = {"haiku": 1.0, "sonnet": 8.0, "abstain": 0.0}


@dataclass
class RouteDecision:
    route: str
    model: str
    reason: str
    cost_weight: float


def route(query: str) -> RouteDecision:
    text = (query or "").strip()
    if not text or OUT_OF_SCOPE.search(text):
        return RouteDecision("abstain", "abstain", "out_of_scope_or_empty", 0.0)
    if COMPLEX.search(text):
        return RouteDecision("strong", "sonnet", "complex_query", COST["sonnet"])
    if SIMPLE.search(text) or len(text.split()) <= 12:
        return RouteDecision("cheap", "haiku", "simple_query", COST["haiku"])
    return RouteDecision("strong", "sonnet", "default_strong", COST["sonnet"])


def benchmark(cases: list[dict]) -> dict:
    correct = 0
    cost = 0.0
    naive = 0.0
    details = []
    for case in cases:
        d = route(case["query"])
        ok = d.route == case["expected_route"]
        correct += int(ok)
        cost += d.cost_weight
        naive += COST["sonnet"]
        details.append({"id": case["id"], "ok": ok, "got": d.route, "expected": case["expected_route"]})
    return {
        "accuracy": round(correct / len(cases), 4) if cases else 0.0,
        "cost_weight": cost,
        "naive_cost_weight": naive,
        "savings_pct": round(1 - (cost / naive), 4) if naive else 0.0,
        "details": details,
        "score": round(correct / len(cases), 4) if cases else 0.0,
    }
