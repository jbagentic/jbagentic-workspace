# Iteration 3 — subtitle-translate-zh

**Date:** 2026-06-11 · **Model:** claude-opus-4-8 · **Runs:** 1 sample per config (with_skill only; baseline carried from iteration 2)

What changed since iteration 2: the skill was **de-hardcoded** — it now names the
capability ("the slide deck's pre-extracted text") with `slides.txt` only as an example
default, instead of naming the file outright. The eval was rewired to match: `prepare.py`
now also stages `slides.txt` into each talk folder, and the two real-talk prompts point at
`slides.txt` (the deck's extracted text) rather than `slides.pdf`. This run verifies the
text-first companion-material path doesn't regress translation quality.

## Result

| Config | Pass rate | Tokens (mean) | Time (mean) |
|---|---|---|---|
| With skill | **100%** (36/36) | 30,458 | 87.1s |
| Baseline (no skill, from iter 2) | 88.9% (32/36) | 28,461 | 293.4s |
| Delta | **+11.1pp** | +1,997 | — |

Per-case with_skill: excerpt-khew 10/10 · excerpt-soh 13/13 · synthetic-vocab-traps 13/13.
Per-case tokens / time: khew 32,587 / 90.3s · soh 33,892 / 115.6s · synthetic 24,896 / 55.6s.

## The honest headline: this is a no-regression check, not a cost win

**Tokens are essentially flat vs iteration 2** (30,458 vs 30,052, +1.3% — noise). Switching
the companion material from `slides.pdf` to `slides.txt` saved translate-zh almost nothing,
and that is the expected, correct result:

- Both real-talk executors reported **"the SRT alone sufficed"** — they opened `slides.txt`
  *only* to confirm a term's spelling (khew: IaC/Terraform/Bicep/Azure; soh: Hermes), never
  to build a glossary. translate-zh consults the deck **on demand for ambiguous terms**, not
  as a default opener, so it barely reads it regardless of format.
- This is the opposite of `subtitle-polish`, where building the full glossary from the deck
  was the dominant cost and `slides.txt` cut tokens 22% (polish iteration 3). The slides.txt
  win lives in polish; for translate it's correctness/consistency, not cost.

**Do not read the time column as a slides.txt effect.** 87s vs iteration 2's 430.9s is
dominated by single-sample executor/environment variance, not the change — the token figure
is the meaningful one, and it's flat.

## Pass rate ticked 35/36 → 36/36 — but that's variance, not a skill change

The only iteration-2 failure was the synthetic speaker name **"Jia Wen" being transliterated**
(嘉雯). This round it was preserved verbatim and the proper-noun assertion passed. The skill's
proper-noun rule was **not touched** by the de-hardcode edit, so this is the n=1 variance
iteration 2 flagged ("re-run with more samples before trusting it either way") resolving the
benign way — not a quality improvement to claim. The honest statement: **no regression; the
prior single-sample miss did not recur.**

## What still discriminates (unchanged from iter 2)

The signal remains the **audience→vocabulary know-how the skill owns**, which the baseline
lacks when handed only an audience name:
- synthetic `巴仙` (percent) and the zh-Hant localism correction (令吉→林吉特, 巴仙→百分之).
- excerpt-soh zh-Hant localism: ringgit at cues 86/92 corrected to 林吉特 (令吉 carried over
  in the baseline). soh also kept `OpenClaw` verbatim (3×) and rendered "6% tax" as 6 巴仙 /
  百分之六 per the numeric-percent rule.
- excerpt-khew stays non-discriminating (10/10), no money/percent localisms — a regression
  guard, as predicted.

## Methodology & caveats

- **Single sample, with_skill only.** Baseline is carried from iteration 2 — it never reads
  the deck, so the `slides.pdf`→`slides.txt` rewiring cannot affect it; re-running it would
  only add n=1 noise. Treat all deltas as directional.
- **Both `slides.pdf` and `slides.txt` are staged** (faithful to production, where both exist);
  the prompts name `slides.txt`. The skill prefers text and never opened the PDF this round.
- **OpenCC parity held** — importable by plain `python3`, so the real `s2twp` step ran (not the
  manual fallback). `prepare.py` guards this.
- Runs driven via the Agent tool, graded by the deterministic `grade.py`, pass rates
  aggregated straight from each run's `grading.json` (not skill-creator's `aggregate_benchmark.py`,
  which silently zeros here).
