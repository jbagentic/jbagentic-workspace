# Iteration 1 — slides-png-to-text (run under the old name slides-pdf-to-text)

**Date:** 2026-06-11 · **Model:** claude-opus-4-8 · **Runs:** 1 sample per (case × config)

First eval for the skill. Two real committed decks, one per branch:
- **textlayer-kowa** (21 slides) — a deck with a genuine PDF text layer, meant to exercise the
  cheap stdlib `extract_deck_text.py` path.
- **vision-khew** (6 slides) — an image-only deck (DCTDecode JPEGs, zero fonts); the script
  returns nothing, so the skill must transcribe the `slides/` PNGs via a one-time vision pass.

The two image-only decks in the corpus (Khew, Soh) are the *common* case for this project —
its slides are exported as raster images. Soh (14 slides) was left out as a redundant second
vision case to keep iteration-1 cheap.

## Result

| Config | Pass rate | Tokens (mean) | Time (mean) |
|---|---|---|---|
| With skill | **100%** (28/28) | 41,163 | 153.5s |
| Baseline (no skill) | 78.6% (22/28) | 22,788 | 100.5s |
| Delta | **+21.4pp** | **+18,375 (skill is dearer)** | — |

Per case (with_skill / without_skill):
- textlayer-kowa: **15/15** / 12/15 · tokens 58,343 / 26,142 · time 263.7s / 124.0s
- vision-khew: **13/13** / 10/13 · tokens 23,982 / 19,433 · time 43.2s / 76.9s

## What discriminates: the output contract, not the terms

The baseline lost the **same 3 assertions in both cases** — section parsing, the
`slide-01..slide-NN` contiguity check, and no-empty-sections — because both baselines wrote a
correct transcription in a *different shape*: `--- Slide N ---` blocks (Kowa, via `pypdf`) and
freeform per-slide blocks (Khew, via vision), not the skill's `## slide-NN` `slides.txt`
convention. **Every term assertion passed for the baseline too** — a capable model handed the
PNGs recovers `IaC`, `Terraform`, `Vue JS`, `Ruby on Rails`, etc. with exact casing unaided.

So the skill's measured value here is **convention adherence** (the reusable `slides.txt`
contract downstream skills read), not term recovery. That is a real but narrow win; the
single-sample +21.4pp rests entirely on the format checks.

## The headline finding: the cost premise inverted

The plan assumed the cheap text-layer script makes the skill cheaper than a vision baseline.
**It did not survive the real text-layer deck.** On Kowa the skill ran the script (exit 0,
~9 KB), then its own step-3 sanity-check judged the output materially lossy — a recurring
leading-`E` glyph dropout, `CLAUDE.md` truncated to `.md`, and nothing from the rasterized
screenshots on slides 7/8/16/17 — and correctly **escalated to vision** (58k tokens). The
baseline, meanwhile, found the same text layer and pulled it cheaply with `pypdf` (26k tokens).
**The skill was ~2.2× dearer on the very deck the cheap path was supposed to win.** On the
image-only Khew both sides use vision and costs are comparable (24k vs 19k).

This is a finding about the **skill**, not just the eval: the bundled stdlib
`extract_deck_text.py` is lossy on this project's real (Google-Slides-style) exports, lossy
enough that following the skill faithfully means paying for vision anyway. Leads for a later
iteration: fix the extractor's subsetted-font glyph gaps, or have the skill prefer a
`pypdf`-class extraction before falling back to vision.

## Known gap in this eval (honest caveat)

The eval's pass-rate did **not** catch the extractor's lossiness: the raw script output
contains all 8 curated Kowa terms verbatim (verified directly), so a script-only run would
also score 15/15. The losses live in terms *outside* the curated set (`CLAUDE.md`) and in
screenshots. The cost signal is only visible in `timing.json`, not the pass rate. An
iteration-2 should add trap terms the script actually drops (e.g. `CLAUDE.md`, an `E`-initial
heading) so the grader discriminates the cheap path's quality, not just the output format.

## Methodology & caveats

- **Single sample per cell**, both configs run. Treat deltas as directional.
- Real decks staged by `prepare.py` into the gitignored `runs/`; the committed `slides.txt`
  oracle is never staged (it's the source of the curated term lists, not an input).
- Deterministic, stdlib-only `grade.py`; grading.json carries both `summary` and
  `expectations`. Aggregated straight from each `grading.json` — `check_benchmark.py` is not
  run because it requires skill-creator's `benchmark.json` aggregator, which we deliberately
  bypass (it silently zeros here, per the translate-zh methodology).
- Baselines were told to ignore the installed skill; both still produced good text, just not
  the `## slide-NN` contract — the intended discrimination.
