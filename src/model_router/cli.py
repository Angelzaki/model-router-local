from __future__ import annotations

import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from model_router.router import benchmark, route

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="model-router")
    sub = parser.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("route")
    r.add_argument("query")
    b = sub.add_parser("bench")
    b.add_argument("--cases", default="samples/cases.jsonl")
    b.add_argument("--results", default="results")
    args = parser.parse_args(argv)

    if args.cmd == "route":
        d = route(args.query)
        print(json.dumps(d.__dict__, ensure_ascii=False, indent=2))
        return 0

    cases = [json.loads(l) for l in Path(args.cases).read_text(encoding="utf-8").splitlines() if l.strip()]
    report = benchmark(cases)
    out = Path(args.results)
    out.mkdir(parents=True, exist_ok=True)
    (out / "router_bench.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    table = Table(title="Model Router")
    table.add_column("metric")
    table.add_column("value", justify="right")
    table.add_row("accuracy", f"{report['accuracy']:.0%}")
    table.add_row("savings", f"{report['savings_pct']:.0%}")
    console.print(table)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
