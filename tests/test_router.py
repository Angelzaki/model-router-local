from pathlib import Path
import json

from model_router.router import benchmark, route

ROOT = Path(__file__).resolve().parents[1]


def test_routes():
    assert route("¿Cuál es el límite comercial?").route == "cheap"
    assert route("Compara A1 y A2 y explica trade-offs de arquitectura").route == "strong"
    assert route("viaje a marte 2099").route == "abstain"


def test_bench():
    cases = [json.loads(l) for l in (ROOT / "samples" / "cases.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    report = benchmark(cases)
    assert report["accuracy"] >= 0.8
    assert report["savings_pct"] > 0
