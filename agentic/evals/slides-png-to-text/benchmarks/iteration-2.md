# Iteration 2 — slides-png-to-text

**Date:** 2026-06-11 · **Model:** claude-opus-4-8 · **Runs:** 1 sample per (case × config)

What changed since iteration 1: the skill was **simplified to a single path** and **renamed**
`slides-pdf-to-text` → `slides-png-to-text`. It no longer runs a hand-rolled `zlib`+regex PDF
text-layer parser (deleted); it just **transcribes the rendered slide PNGs with the vision
model**. Rationale: 2 of 3 real decks are image-only, the PNGs already exist upstream from
`slides-pdf-to-png`, and the talk runs ~monthly so the parser's occasional token saving wasn't
worth its fragility. The two eval cases were renamed `textlayer-kowa`→`kowa`, `vision-khew`→`khew`
(both decks are now handled the same way), and a grounded quality trap term was added — see below.

## Result

| Config | Pass rate | Tokens (mean) | Time (mean) |
|---|---|---|---|
| With skill | **100%** (29/29) | 38,915 | 141.3s |
| Baseline (no skill) | 79.3% (23/29) | 38,216 | 152.6s |
| Delta | **+20.7pp** | ~0 | — |

Per case (with_skill / without_skill): kowa **16/16** / 13/16 · khew **13/13** / 10/13.
Per case tokens / time (with_skill): kowa 57,909 / 252.8s · khew 19,921 / 29.8s.

## No regression; the discriminator is still the output contract

Both baselines lost the **same 3 format assertions** as iteration 1 — section parsing, the
`slide-01..slide-NN` contiguity check, no-empty-sections — because they wrote `=== Slide N ===`
blocks, not the skill's `## slide-NN` `slides.txt` convention. Every term assertion passed for the
baseline too. So the skill's measured value remains **convention adherence**, not term recovery.
The simplified single-path skill holds 100% — the rewrite did not regress anything.

## The grounded quality win: screenshot text the old parser could not read

The new trap term is `CLAUDE.md`. It is genuinely on the deck — the **editor-view screenshot on
slide 7** (verified by eye) — but **absent from the project's committed `slides.txt`**, which is
**byte-identical to the old parser's output** (0 diff lines). A PDF text-layer parser cannot read
rasterized screenshot text; the vision skill can, and `with_skill` recovered `CLAUDE.md` (kowa
16/16). This is the real, grounded improvement of the rewrite over the old parser-based skill —
independent of cost.

**Honest caveat on the trap this run:** it did *not* separate `with_skill` from `without_skill`
here, because this run's baseline had **no `pypdf` available** and so *also* transcribed the PNGs
via vision, recovering `CLAUDE.md` too. The trap discriminates **new skill vs the old parser**,
not new-skill vs this particular baseline. (In iteration 1 the baseline *did* find `pypdf` and used
the cheap text layer — so it would have failed this `CLAUDE.md` assertion. Which tool a baseline
reaches for is environment-dependent.)

## No cost story this run — and that's fine

With-skill and baseline tokens are ~equal (38.9k vs 38.2k) because both transcribed PNGs via vision
this run. There is no cost win to claim, and none is needed: at ~monthly cadence the one-time
extraction cost (kowa ~58k, khew ~20k, amortized across every later subtitle/metadata run) is
immaterial. The rewrite buys **simplicity and robustness** (one path, no fragile parser, uniform
handling of image-only decks) plus the screenshot-text recovery above — not cost.

## Methodology & caveats

- **Single sample per cell**, both configs run (the `CLAUDE.md` assertion is new, so iter-1's
  baseline count isn't directly comparable — hence a fresh baseline). Treat deltas as directional.
- Real decks staged by `prepare.py` into the gitignored `runs/`; the committed `slides.txt` is
  never staged.
- Deterministic, stdlib-only `grade.py`; grading.json carries `summary` + `expectations`.
  Aggregated straight from each `grading.json`.
