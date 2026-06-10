#!/usr/bin/env python3
"""Guard against silently-zeroed eval benchmarks.

skill-creator's `aggregate_benchmark.py` emits all-zero pass rates **instead of
an error** when it can't match the grading artifacts it expects (wrong layout or
a missing `summary` block). That silent zero is easy to miss and has bitten us
more than once. Run this right after aggregating: it FAILS LOUDLY (exit 2) when a
benchmark looks like that silent-zero case, so a wrong number never ships.

Usage:
    python3 agentic/evals/check_benchmark.py <iteration-dir>

Fails when:
  - no benchmark.json, or it aggregated 0 runs while grading.json files exist on
    disk (the classic layout/schema drift); or
  - every configuration has a 0 pass rate (degenerate result).

See agentic/evals/README.md ("Benchmark contract") for the layout/schema the
aggregator requires.
"""
import json
import sys
from pathlib import Path


def fail(msg: str):
    print(f"BENCHMARK CHECK FAILED: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    it = Path(sys.argv[1])
    bj = it / "benchmark.json"
    if not bj.exists():
        fail(f"no benchmark.json in {it}")
    data = json.loads(bj.read_text())

    # producer signal: grading.json the agent wrote; aggregator-relevant ones live under run-*/
    all_gradings = list(it.rglob("grading.json"))
    run_gradings = [p for p in all_gradings if p.parent.name.startswith("run-")]
    runs = data.get("runs", [])

    # The exact recurring bug: artifacts on disk, but the aggregator matched none.
    if all_gradings and not runs:
        fail(
            f"{len(all_gradings)} grading.json on disk ({len(run_gradings)} under run-*/) "
            f"but benchmark aggregated 0 runs — layout/schema drift. The aggregator needs "
            f"eval-*/<config>/run-*/grading.json with a top-level "
            f"summary{{pass_rate,passed,failed,total}}. See agentic/evals/README.md "
            f"(Benchmark contract)."
        )
    if not runs:
        fail("benchmark aggregated 0 runs (no grading artifacts found at all).")

    summary = data.get("run_summary", {})
    # a config entry has pass_rate as a stats dict {mean,...}; the "delta" entry
    # has pass_rate as a string ("+0.15") — exclude it.
    configs = {k: v for k, v in summary.items()
               if k != "delta" and isinstance(v, dict) and isinstance(v.get("pass_rate"), dict)}
    if not configs:
        fail("benchmark has no per-config pass_rate — nothing was aggregated.")
    means = {c: v["pass_rate"].get("mean", 0.0) for c, v in configs.items()}
    if all(m == 0 for m in means.values()):
        fail(f"every configuration has pass_rate 0 — suspect silent failure: {means}")

    print(f"benchmark check OK — {len(runs)} runs aggregated:")
    for c, m in means.items():
        tok = configs[c].get("tokens", {}).get("mean")
        line = f"  {c}: pass_rate {m:.3f}"
        if tok:
            line += f", tokens {tok:.0f}"
        print(line)
        if tok == 0:
            print(f"    note: tokens read as 0 for {c} (check sibling timing.json total_tokens).")
    sys.exit(0)


if __name__ == "__main__":
    main()
