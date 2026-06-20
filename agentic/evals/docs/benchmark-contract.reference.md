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

## 3. Report the full metric set in every writeup

Sections 1–2 cover the machine artifacts. This one covers the **hand-authored** writeups
(`benchmarks/iteration-N.md` and `benchmarks/history.md`). They are written by hand, so a metric
can quietly disappear when an author judges it noisy and drops the column — which is exactly how
wall-clock **time** vanished from `doc-this--context-discovery` after iteration 1. The data was
never lost (it is in every `benchmark.json` `run_summary.<config>.time_seconds`); it was dropped
from the table. This contract closes that gap.

**Report both arms.** Every metric is reported as the **with-skill / without-skill pair plus the
delta** — never one arm alone. The comparison *is* the result; a single-arm number is not a
benchmark result. This is the paired `history.md` form (e.g. Time `16.8s / 26.1s` with a `Delta`
column). Older single-arm "(skill)"-only columns are legacy; report both arms whenever the baseline
ran.

Each `iteration-N.md` **Headline / Result** table and each `history.md` row must carry, for both
configs with the delta:

- **Pass rate** — the blended decision metric.
- **The eval's discriminating dimension(s)** — e.g. `process`, `reconcile`, `correctness` (per the
  eval's README).
- **Efficiency** — mean tool calls and/or mean **time (s)**.
- **Mean time (seconds)** — always, whenever `benchmark.json` has it. At small n, label it
  *directional* — do **not** drop it.
- **Mean tokens** — always, whenever available; add the cache-read caveat where it applies. Folders
  that deliberately track tool-calls instead of tokens (e.g. `context-discovery`) keep that choice,
  but consistently across iterations.

**Never drop a column you reported in a prior iteration.** Report-with-caveat, never omit. A noisy
metric is flagged, not hidden. A `—` means the value does not exist for that run (e.g. a
hand-orchestrated iteration with no `benchmark.json`) and the Notes must say why — never that an
existing number was suppressed. `check_benchmark.py` prints the time/token means for both configs
every run, so the number is always in front of you when you write the table.

## Related
- [`../check_benchmark.py`](../check_benchmark.py) — the guard described above.
- [Skill evals README](../README.md) — the run → aggregate → guard → promote workflow.
