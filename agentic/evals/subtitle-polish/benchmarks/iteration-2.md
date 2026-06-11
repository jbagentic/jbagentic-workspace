# Benchmark — subtitle-polish, iteration 2

- **Date:** 2026-06-11
- **Model:** claude-opus-4-8
- **Cases:** 3 real talks — `real-khewjiapeng` (916 cues), `real-kowajialiang` (875 cues), `real-sohjunwei` (806 cues). Each input is the talk's genuine auto-transcript + slide deck.
- **Runs per case:** 1 (per case × config), executed via the Agent tool.
- **Baseline:** same prompt + same files, no skill.
- **What changed since iter 1:** the skill itself — principle-based restraint (the speaker's words win over supporting materials), a phonetic-only term-replace gate, light-touch discourse-marker removal, and particle "thin, never to zero." Also a grader-brittleness fix (see below). The eval moved to all-real cases after iter 1, so the assertion set differs (34 vs iter-1's 30) — cross-iteration pass rates are directional, not a like-for-like delta.

## Result

| Metric | With skill | Baseline | Delta |
|---|---|---|---|
| Pass rate (assertions) | 97.1% (33/34) | 97.1% (33/34) | **0.00** |
| Time (mean) | 662.5s | 464.2s | +198.3s |
| Tokens (mean) | 109,841 | 93,843 | +15,998 |

The raw delta is **0.00**, but the number understates the result: the skill's one
remaining "miss" is a grader/expected-answer artifact where the skill is actually
*more* correct, while the baseline's one miss is a genuine quality failure the skill
prevents. Read the per-case breakdown — the failure *kind* is the signal, as in iter 1.

## Per-case breakdown

| Case | With skill | Baseline | Discriminating? |
|---|---|---|---|
| real-khewjiapeng | 10/10 | 10/10 | No — both recover IaC/Azure/Terraform cleanly |
| real-kowajialiang | 11/12 | 12/12 | Yes — but the skill's "miss" is the truer answer (see below) |
| real-sohjunwei | 12/12 | 11/12 | Yes — baseline scrubbed a particle the skill kept |

## The headline bug is fixed

Iteration 1's regression was the skill rewriting the speaker's spoken "OpenClaw" to
the slide's "OpenRouter". **It did not recur.** On the real Soh transcript the speaker
genuinely says *both* "Open Claw" (an agent, raw cues 487/519/1135/2723) and "open
router" (an LLM gateway, raw cues 959–1007) — two different things. The with-skill run
kept "Open Claw" ×8 as spoken and only wrote "OpenRouter" where the speaker actually
said it. The principle-based "speaker's words win" guard held.

## Two grader/expected-answer artifacts — verified against the raw

1. **OpenClaw spacing (fixed in the grader).** The shipped restraint check used
   `\bOpenClaw\b`, which can't match the spaced rendering "Open Claw" — so it emitted a
   *false* "wrongly removed" against the with-skill run even though the term is present
   8×. Fixed `grade.py` to compare space/case-insensitively (`chk_restraint`): a
   speaker's term is preserved in any rendering; the assertion's point is that it wasn't
   rewritten to the slide word, not that it was spelled solid. This flipped the booked
   score from 32/34 → 33/34 with-skill (baseline unaffected — it already spelled it solid).

2. **"jsonb" vs "JSON" (left unscored, flagged for iter 3).** On Kowa the raw says "set
   up through Jason" + "B files only" (cues 448–449) — i.e. the speaker said **"jsonb
   files."** The with-skill run correctly merged "Jason B" → `jsonb` across the cue
   boundary; the baseline dropped the B to plain "JSON". The eval's assertion expects the
   literal "JSON", so it books the *more faithful* output as a fail. **I did not
   retroactively re-score this** — booking it honestly keeps with-skill at 33/34 — but
   the assertion's expected answer is wrong and should accept `jsonb` in iteration 3. If
   credited, with-skill is 34/34 (+0.03).

## The baseline's real miss

On Soh the baseline scrubbed the particle "ah" (0 in output vs 3 in the with-skill run)
— the exact over-correction the skill's "keep as voice" convention prevents. The
with-skill run preserved all of `lah`/`ya`/`ah`. This is a genuine, grader-captured win
for the skill.

## Particle thinning ("thin, never to zero")

The new policy behaved as designed: with-skill runs thinned redundant particles but kept
a representative voice (Soh: 3× `ah` survived; `lah`/`ya` preserved across all cases).
No case in this eval is a *heavy* particle user, so the thinning path (dropping on
reading-speed / stacked-particle triggers) is only lightly exercised — **flag for a
future fixture** with a high-particle-density speaker to test thinning directly.

## Honest scoreboard

- Shipped grader (as-was): with-skill 32/34 vs baseline 33/34 → **−0.03**.
- After the OpenClaw grader-bug fix (verified false-negative): **33/34 vs 33/34 → 0.00**.
- If the jsonb assertion is corrected (verified, deferred): **34/34 vs 33/34 → +0.03**.

The honest read: the skill is **at least as good as baseline on raw score and strictly
better on failure kind** — its only booked miss is a correct answer the grader rejects,
while the baseline's miss is a real particle scrub. The iter-1 over-correction is gone.

## Comparison to iteration 1

| | Iter 1 | Iter 2 | Note |
|---|---|---|---|
| Eval set | 3 cases (1 real + 2 synthetic), 30 assertions | 3 real cases, 34 assertions | not like-for-like |
| With-skill pass | 93.3% (28/30) | 97.1% (33/34) | different test set |
| Baseline pass | 96.7% (29/30) | 97.1% (33/34) | — |
| Delta | −0.03 | 0.00 (booked) / +0.03 (jsonb-corrected) | over-correction fixed |
| Headline bug | skill rewrote OpenClaw→OpenRouter | **not reproduced** | the fix worked |

## Caveats

- **Single sample per case** — no variance estimate; run ≥3× per case for a reliable
  stddev before treating the 0.00/+0.03 as settled.
- **Coarse on the non-discriminating case.** Khew (10/10 both) grades on invariants +
  term spot-checks, so it can't separate two strong polishes.
- **Slower and pricier.** +198s and +16k tokens — the skill reads slides, builds a
  glossary, and verifies; the baseline does less. Acceptable for a publishing-quality
  pass, but worth watching.
- **iter-3 to-dos:** (1) fix the jsonb assertion to accept the truer recovery; (2) add a
  heavy-particle fixture to exercise thinning; (3) consider a sampled gold-diff on the
  real cases to sharpen the non-discriminating one.
