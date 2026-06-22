# Benchmark history format — reference

The canonical layout for every eval suite's `benchmarks/history.md` — the one-row-per-iteration
trend table that answers *did this change move quality, and at what cost?* This pins the columns and
conventions so the files stay comparable; it is the schema [`benchmark-contract.reference.md`](benchmark-contract.reference.md)
§3 governs in prose. `history.md` is the **trend**; per-run and per-dimension detail lives in each
suite's `iteration-N.md`.

## Canonical columns

In order, left to right:

| group | columns |
|---|---|
| metadata | `Iteration` · `Date` · `Model` |
| quality | `Pass (w/wo)` · `Δ` |
| cost / efficiency | `Tools (w/wo)` · `Time (w/wo)` · `Tokens (w/wo)` |

Every `history.md` carries this **same column superset** — that uniformity is the point. A cell is
filled, blank, or `—` per the rules below.

- **`Iteration`** — the iteration number, linked to its note: `[3](#iteration-3)`.
- **`Pass (w/wo)`** — the blended decision rate as **rate + raw score** per arm, e.g.
  `100% (42/42) / 76.2% (32/42)`. The score exposes the sample size (`n=2` and `n=42` read very
  differently); a bare `100%` hides it.
- **`Δ`** — the pass-rate gap in **percentage points**: `+22pp`, not the bare decimal `+.22`. It is
  the difference between two percentages, so `pp` is the honest unit and it matches the `+57pp` form
  the `iteration-N.md` writeups already use.
- **`Tools` / `Time` / `Tokens` (w/wo)** — mean efficiency/cost per task, both arms. Compact units:
  tokens in `k` (`98.6k`), time in `s` (`20.2s`), tool calls as the mean (`3.71`). Means only — no
  `±` in the table (spread, if reported, goes in the iteration writeup).

## Both arms, always (`w/wo`)

Every metric column is the **with / without pair**, header-suffixed `(w/wo)` so each cell's two
numbers are self-descriptive. The file's **preamble declares the arms once** — `w = with_rule,
wo = without_rule` for the doc-rule suites, `with_skill / without_skill` for the skill suites — so
the arm names aren't repeated in every header. Single-arm `(skill)`-only columns are legacy; report
both arms whenever the baseline ran (per the contract).

## Trend, not detail — the dimension breakdown lives in `iteration-N.md`

`history.md` carries the **blended** `Pass` only. The per-dimension breakdown — `process`,
`reconcile`, `correctness`, tool-budget — stays in each `iteration-N.md` Headline table, where the
per-run detail belongs. It is **not** a `history.md` column: a discriminating dimension applies to
at most one or two suites, so a `Process`/`Reconcile` column would be blank in most files while
duplicating a number the blended `Pass` + its raw score already headline.

## blank vs `—`

Two different absences, kept distinct:

- **blank cell** — this suite **doesn't measure that metric yet**. An actionable gap the
  standardized table makes visible (e.g. the skill suites leave `Tools` blank — tool-call counting
  was never wired up). A future iteration may fill it.
- **`—`** — the metric **applies but the value doesn't exist for that row**: a hand-orchestrated
  iteration with no captured wall-clock, or a baseline that wasn't re-run. Always pair a `—` with a
  one-line reason in that row's Notes — never let it read as a suppressed number.

**Never drop a column you've reported.** A metric that appeared in a prior row stays; flag a noisy
one (see below), don't delete it. Removing a column is a format change that must be reflected here
and in the contract first — not done silently in one file.

## The `Tokens` caveat

Tokens are dominated by cache reads at small corpus sizes, so the arm-to-arm token delta is
**directional, not a clean efficiency signal** — and it often favors the *baseline* (a rule/skill
that reads more docs up front spends more). State this in the preamble where it applies, and treat
tool calls (where measured) as the cleaner efficiency signal. Report tokens anyway — directional is
not the same as droppable.

## Notes below the table

The table holds numbers only. Prose commentary lives in a `## Notes` section **below** the table,
one `### Iteration N` subsection per row:

- **Plain `### Iteration N` headers** so the GitHub anchor is stable (`#iteration-3`); put the
  descriptive title as a **bold lead-in line** in the body, not in the header.
- Each `Iteration` cell links to its note (`[3](#iteration-3)`), so the table scans the metrics and
  one click reaches the prose.

## Skeleton

Preamble (declares arms + caveats), then the table, then notes. A doc-rule suite:

```
# Context-discovery rule — benchmark history

One row per iteration. `w = with_rule, wo = without_rule` (...). Tokens are
cache-read-dominated — directional only; tool calls are the cleaner signal.

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [3](#iteration-3) | 2026-06-20 | claude-opus-4-8 | 100% (42/42) / 76.2% (32/42) | +24pp | 3.71 / 5.36 | 20.2s / 25.9s | 85.6k / 67.7k |

## Notes
### Iteration 3
**Rule extended to the nearest `AGENTS.md`.** <prose>
```

A skill suite is identical except the preamble names `with_skill / without_skill` and the `Tools`
column is blank until tool-call counting is wired up.

## Related

- [benchmark-contract.reference.md](benchmark-contract.reference.md) — §3 governs which metrics a
  writeup must report; this file fixes the `history.md` layout that satisfies it.
- [grading.guide.md](grading.guide.md) — grade the principle, not the method (what `Pass` blends).
- [../README.md](../README.md) — the run → aggregate → guard → promote workflow these tables record.
