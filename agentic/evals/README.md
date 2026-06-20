# Skill evals

Dev-time evaluation specs and durable benchmark records for the skills in [`../skills/`](../skills/).
Everything here is **dev-time only** — skill-creator reads it while building and improving skills,
never a skill at runtime, and it lives **outside the skill folders so it never ships in the installed
`.skill`**.

## Structure

One folder per skill (or rule) being evaluated, named to match it. Each holds:

- `evals.json` — the eval spec (cases: id, prompt, expected output, assertions).
- `prepare.py` / `grade.py` — stage inputs; grade outputs deterministically (stdlib, zero LLM
  tokens). Several evals also stage per-run work dirs — see the eval's own README.
- `fixtures/` — committed input materials (where used).
- `benchmarks/` — **committed** durable record: `iteration-N.md` (one run's summary) + `history.md`
  (one row per iteration).
- `runs/` — **gitignored** scratch; raw per-run outputs, disposable.

A bigger eval is its own
[contextful folder](../skills/doc-this/references/contextful-folder.reference.md) with its own README
(linked below); simpler ones are covered here.

## Evals in this suite

| Eval | What it measures |
|------|------------------|
| [doc-this](doc-this/) | the doc-this skill — documenting a folder to the Contextful Folder spec. |
| [doc-this--context-discovery](doc-this--context-discovery/) | rule eval — the always-on "How to Discover Context" rule (read side). |
| [doc-this--context-maintenance](doc-this--context-maintenance/) | rule eval — the always-on "How to Document Context" rule (write side). |
| [series-youtube-metadata](series-youtube-metadata/) | the series-youtube-metadata skill — YouTube titles / description / chapters from a transcript. |
| [slides-pdf-to-png](slides-pdf-to-png/) | the slides-pdf-to-png skill — render a deck PDF into PNG frames. |
| [slides-png-to-text](slides-png-to-text/) | the slides-png-to-text skill — transcribe slide PNGs into `slides.txt`. |
| [subtitle-polish](subtitle-polish/) | the subtitle-polish skill — clean a raw talk SRT. |
| [subtitle-translate-zh](subtitle-translate-zh/) | the subtitle-translate-zh skill — translate an SRT into zh-Hans + zh-Hant. |

Each linked folder with its own README documents that eval's staging, run, and grading specifics.
`doc-this` and `series-youtube-metadata` are covered here and follow the generic flow below.

## Running & promoting

1. **Point skill-creator at the eval folder explicitly** — auto-discovery doesn't reach this path.
2. **Prepare → run → grade** per the eval's own README (several stage inputs or per-run work dirs
   first; the exact commands differ — see the eval).
3. **Aggregate**, then **guard**: `python3 agentic/evals/check_benchmark.py <iteration-dir>` — the
   aggregator silently zeros on mismatched artifacts, so treat a non-zero exit as a failed run (see
   [benchmark contract](docs/benchmark-contract.reference.md)).
4. **Promote** a curated summary to the eval's committed `benchmarks/iteration-N.md` and append a row
   to `benchmarks/history.md`. The `runs/` scratch is disposable.

## Deeper docs

- [docs/benchmark-contract.reference.md](docs/benchmark-contract.reference.md) — grading-artifact layout + the silent-zero guard.
- [docs/environment-parity.reference.md](docs/environment-parity.reference.md) — no runtime `pip`; pre-provision deps so runs match production.
- [docs/grading.guide.md](docs/grading.guide.md) — grade the principle, not the method.
