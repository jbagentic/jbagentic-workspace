# Iteration 2 — subtitle-translate-zh

**Date:** 2026-06-10 · **Model:** claude-opus-4-8 · **Runs:** 1 sample per config

What changed since iteration 1: the skill now **owns the audience→vocabulary know-how** (a bundled `references/audience-vocabulary.reference.md`), and zh-Hant is corrected for Taiwanese readers after OpenCC. Prompts now **only name the two audiences** (Simplified → Malaysian Chinese readers, Traditional → Taiwanese readers) — they no longer inline the vocabulary. Two new `taiwan localism` assertions were added (assertion total 34 → 36).

## Result

| Config | Pass rate | Tokens (mean) | Time (mean) |
|---|---|---|---|
| With skill | **97.2%** (35/36) | 30,052 | 430.9s |
| Baseline (no skill) | 88.9% (32/36) | 28,461 | 293.4s |
| Delta | **+8.3pp** | +1,591 | +137.5s |

Per-case (with_skill / baseline): excerpt-khew 10/10 · 10/10 · excerpt-soh 13/13 · 12/13 · synthetic-vocab-traps 12/13 · 10/13.

## What discriminated

All signal came from the **audience→vocabulary know-how the skill now owns** — exactly what the baseline lacks when handed only an audience *name*:

- **synthetic, `巴仙` (percent):** baseline did not render percent as the Malaysian `巴仙` in zh-Hans; the skill did. (Baseline FAIL, skill PASS.) This is the iteration-1 shared miss, now fixed by the refactor — the skill supplies the vocab the prompt no longer states.
- **synthetic, zh-Hant localism:** baseline left `令吉` in the Traditional file and never produced `林吉特`/`百分之`; the skill corrected both. (Baseline FAIL, skill PASS.)
- **excerpt-soh, zh-Hant localism:** baseline carried `令吉` into the Traditional file; the skill corrected it to `林吉特` (ringgit appears at cues 86/92). (Baseline FAIL, skill PASS.) This is what makes soh discriminating now where it was 12/12-tie before.

**Shared miss — watch this:** the synthetic speaker name **"Jia Wen" was transliterated by both configs** (with-skill → 嘉雯, baseline → 嘉文), failing the proper-noun check. In iteration 1 the with-skill run *kept it verbatim* — so this is a with-skill regression on that single sample. The proper-noun rule (SKILL.md "keep people's names in their original form") was **not** touched by this refactor; this is executor variance at n=1, but it cancelled the proper-noun signal this round. Re-run with more samples before trusting it either way.

**Non-discriminating:** excerpt-khew (10/10 both) — it has no money/percent localisms, so the new check vacuously passes; it stays a regression guard, as predicted.

## Why the delta widened (+2.8pp → +8.3pp)

Expected by construction, and the point of the refactor:

1. The prompt no longer hands the baseline the vocabulary, so the baseline now fails `巴仙` and the Malaysian→Taiwan corrections it used to get for free from an inline label.
2. Two new `taiwan localism` assertions test the zh-Hant audience correction — a capability the baseline does not have.

This is the contract iteration 1 said it would test: *given only an audience name, does the skill produce the right vocabulary?* It does; the baseline does not. The widening is therefore a real signal about the refactored contract, not an independent quality jump on unchanged tests.

## Retires the iteration-1 plan

Iteration 1 planned to **stage a project vocab reference doc** so the `令吉`/`巴仙` checks would be fair. This refactor makes that unnecessary: the vocabulary lives in the skill, and the prompt names only the audience — which is what a real project reference doc now supplies. No companion vocab doc is staged.

## Methodology & caveats

- **Single sample per config** — treat all deltas as directional, not significant.
- **Orchestration differs from iteration 1.** These 6 runs (3 cases × 2 configs) were driven directly via the Agent tool, graded by the deterministic `grade.py`, and the pass rates were aggregated **straight from each run's `grading.json`** — not skill-creator's `aggregate_benchmark.py`, which silently zeros in this environment (see `history.md`). `with_skill` = executor instructed to read `SKILL.md` + the references file and follow them; `without_skill` = instructed to translate without any skill.
- **Cost is a clean single-run figure** this time (no two-pass OpenCC redo), so with-skill tokens (~30k) are far below iteration-1's inflated 62.5k and are directly comparable to the baseline.
