# Skill evals

Dev-time evaluation specs and durable benchmark records for the skills in [`../skills/`](../skills/).
Everything here is **dev-time only** — skill-creator reads it while building and improving skills,
never a skill at runtime, and it lives **outside the skill folders so it never ships in the installed
`.skill`**.

## Structure

One folder per skill being evaluated, named to match the skill (e.g. `doc-this/`,
`series-youtube-metadata/`). Each holds:

- `evals.json` — the eval spec (test cases: id, prompt, expected output, fixtures).
- `fixtures/` — input materials the cases run against.
- `benchmarks/` — **committed**, the durable quality-over-time record:
  - `iteration-N.md` — curated summary of one run.
  - `history.md` — one row per iteration (pass rates, deltas).
- `runs/` — **gitignored** scratch; raw per-run outputs, disposable.

## Running and promoting evals

- Auto-discovery does not reach this path, so **point skill-creator at the eval folder explicitly**
  when running or improving a skill.
- **`subtitle-polish` stages its inputs first.** Run `python3 subtitle-polish/prepare.py` to
  materialize each talk's real `.en.raw.srt` + slide deck into `subtitle-polish/stage/`
  (gitignored) from `talk-recordings/`. The skill runs against that throwaway copy so its
  sibling output (`<slug>.en.srt`) never overwrites the committed talk folder. The decks and
  transcripts live once, in `talk-recordings/` — they are not copied into the eval.
- **`slides-pdf-to-png` stages per-run work dirs.** Its fixtures are tiny committed synthetic
  PDFs from `slides-pdf-to-png/fixtures/make_fixtures.py` (run it bare to verify, `--write` to
  regenerate). Run `python3 slides-pdf-to-png/prepare.py runs/<iteration>` **before** spawning
  executors — it stages one work dir per (case × config × run) inside the gitignored `runs/`
  and prints ready-to-paste executor prompts. The harness must save each executor's final reply
  to `<run-dir>/outputs/final-response.md` (the multi-PDF case grades on it) and its
  token/duration notification to `<run-dir>/timing.json`. Grading is the deterministic
  `python3 slides-pdf-to-png/grade.py runs/<iteration>` — stdlib-only, zero LLM tokens.
- **`subtitle-translate-zh` stages too** — same reason (the skill writes `.zh-Hans.srt` /
  `.zh-Hant.srt` siblings that would clobber the committed translations). Run
  `python3 subtitle-translate-zh/prepare.py`: it stages token-efficient **excerpts** of two
  real talks (the minimal cue range covering each talk's trap terms) plus the committed
  synthetic fixture into `subtitle-translate-zh/stage/` (gitignored). Grade with
  `python3 subtitle-translate-zh/grade.py runs/iteration-N` — stdlib-only, re-derives the
  staged sources itself.
- Direct run outputs to `agentic/evals/<skill-name>/runs/` so specs and their results stay together;
  `runs/` is gitignored and disposable.
- After aggregating a run, **promote** a curated summary to the committed
  `agentic/evals/<skill-name>/benchmarks/iteration-N.md` and append a row to `benchmarks/history.md` —
  that's the durable record; the `runs/` scratch can be thrown away.

## Benchmark contract (avoid silent zeros)

`skill-creator`'s `aggregate_benchmark.py` reads grading artifacts in a fixed
layout — and emits **all-zero pass rates instead of erroring** when they don't
match. That silent zero is easy to miss and has bitten us more than once. Two
safeguards keep it from shipping a wrong number:

**1. Write the artifacts in the layout it expects** — per eval, per config:

```
<iteration>/eval-<name>/<config>/run-<k>/
├── grading.json
└── timing.json
```

`grading.json` carries **both** shapes, for its two readers:
- `summary` — `{pass_rate, passed, failed, total}` — what the **aggregator** reads.
- `expectations[]` — `{text, passed, evidence}` — what the **viewer** renders.

Tokens/time live in the sibling `timing.json` (`total_tokens`,
`total_duration_seconds`). The aggregator only falls back to it when
`grading.json` has no inline `total_duration_seconds`, so keep timing out of the
`run-*/grading.json`.

**2. Guard the result** — after aggregating, run the check; it exits non-zero
(and says why) when the benchmark looks silently zeroed (artifacts on disk but 0
runs aggregated, or every config at 0% pass):

```bash
python3 agentic/evals/check_benchmark.py <iteration-dir>
```

Treat a non-zero exit as a **failed run**, not a 0% score. The guard exists
because the vendored skill-creator tools degrade to silent zeros in this
environment rather than failing loudly.
