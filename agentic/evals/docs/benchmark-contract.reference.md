# Benchmark contract — reference

How to write eval grading artifacts so `skill-creator`'s `aggregate_benchmark.py` reads them
correctly — and how to catch it when they don't. The aggregator reads a **fixed layout** and emits
**all-zero pass rates instead of erroring** when artifacts don't match. That silent zero is easy to
miss and has bitten us more than once. Two safeguards keep it from shipping a wrong number.

## 1. Write artifacts in the layout it expects

Per eval, per config:

```
<iteration>/eval-<name>/<config>/run-<k>/
├── grading.json
└── timing.json
```

`grading.json` carries **both** shapes, for its two readers:
- `summary` — `{pass_rate, passed, failed, total}` — what the **aggregator** reads.
- `expectations[]` — `{text, passed, evidence}` — what the **viewer** renders.

Tokens/time live in the sibling `timing.json` (`total_tokens`, `total_duration_seconds`). The
aggregator only falls back to it when `grading.json` has no inline `total_duration_seconds`, so keep
timing out of `run-*/grading.json`.

## 2. Guard the result

After aggregating, run the check; it exits non-zero (and says why) when the benchmark looks silently
zeroed (artifacts on disk but 0 runs aggregated, or every config at 0% pass):

```bash
python3 agentic/evals/check_benchmark.py <iteration-dir>
```

Treat a non-zero exit as a **failed run**, not a 0% score. The guard exists because the vendored
skill-creator tools degrade to silent zeros in this environment rather than failing loudly.

## Related
- [`../check_benchmark.py`](../check_benchmark.py) — the guard described above.
- [Skill evals README](../README.md) — the run → aggregate → guard → promote workflow.
