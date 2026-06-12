# Benchmark — subtitle-polish, iteration 5

- **Date:** 2026-06-12
- **Model:** claude-opus-4-8
- **Cases:** 3 real talks — `real-khewjiapeng` (916 cues, 6-slide deck), `real-kowajialiang` (875 cues, 21-slide deck), `real-sohjunwei` (806 cues, 14-slide deck).
- **Runs per case:** 1, **both configs re-run this iteration** (baseline not carried — the assertion set changed, so the old baseline number no longer applies).
- **What changed:** this measures the **rewritten skill** — three behavioural changes shipped since iter 4: (1) discourse particles (`lah`/`ya`/…) are now **removed by default** (was: thinned, kept for voice); (2) non-English speech is **translated to English** in place; (3) term-fixing is **field-grounded** — naming the talk's field unlocks the model's own knowledge of its standard jargon, so an off-slide mis-hearing like `Cortez`→`Codex` is recoverable even when no slide carries the word. The eval spec was updated to match: **40 assertions** (was 35), particle assertions flipped from "preserved/thinned" to "removed", plus a translation check (khew) and an off-slide field-jargon check (khew + kowa).

## ⚠️ Not like-for-like with iters 1–4

The trend line breaks here. Earlier iterations asserted particle **preservation** and "thin, never to zero"; iter 5 asserts particle **removal**. The assertion count went 35 → 40 and the pass/fail semantics of several assertions inverted. Compare iter 5 to iter 5 (with vs without), **not** to the iter-1–4 pass rates.

## Result

| Metric | With skill | Baseline (re-run) |
|---|---|---|
| Pass rate | **100% (40/40)** | 92.5% (37/40) |
| Tokens (mean) | 96,641 | 89,026 |
| Time (mean) | 448.8s | 313.1s |

**Delta +0.075 (40/40 vs 37/40).** Per case: khew 13/13 vs 12/13 · kowa 14/14 vs 13/14 · soh 13/13 vs 12/13.

## Where the skill earns its keep — and where it no longer shows a gap

The baseline here is the same strong Opus model with no skill guidance. That reshapes what the delta measures:

- **Off-slide field-jargon recovery — the one term assertion the baseline failed.** Khew says "Cortez" for a tool used beside "agent". With-skill recovered `Codex` (×6, `Cortez`=0, `Cortex`=0). Baseline "corrected" it to the plausible **dictionary** word `Cortex` (×5) — wrong tool, right-sounding word. This is precisely the failure the field-grounding step prevents: the model knows the *word* Cortex but, un-grounded, doesn't reach for the *field's* tool Codex.
- **SRT invariant discipline.** Both baseline misses were **empty cues** left behind (kowa 761/862/869, soh 163) — the skill drops emptied cues and renumbers; the baseline blanked the body and left the cue.
- **No measurable gap on particles or translation.** Both configs drove `lah`/`ya` to 0 and `CJK` to 0 on every talk. The strong base model strips particles and translates code-switched speech unprompted. These assertions confirm the skill is *correct*, but they do **not** discriminate it from a capable baseline this round.

Honest read: of the three new capabilities, **field-grounded jargon recovery is the one doing real discriminating work.** Particle-removal and translation are now table stakes for the base model; their value is consistency/guarantee, not raw capability.

## Cost

Mean with-skill tokens rose to ~96.6k (iter 4: 80.3k). Expected — the rewritten skill does strictly more per run (translate non-English passages, a genuine multi-pass full-file read, field-grounding in step 1). The baseline cost ~89k doing similar work, so the skill's overhead over an un-guided run is modest (~+8.5%).

## Honest caveats

- **Measurement path.** Tokens/time are the executor's `subagent_tokens`/duration from a **hand-orchestrated** run (Agent-tool executors, full SKILL.md pasted into the with-skill prompt), not the skill-creator harness. Direction is sound; magnitudes are not perfectly comparable to iters 1–3 (harness path) and only loosely to iter 4 (also `subagent_tokens`).
- **with_skill ≈ skill faithfully applied, not skill auto-triggered.** The with-skill executors were handed the full SKILL.md text rather than relying on description-triggering. This tests the *guidance*, not the *trigger*.
- **Single sample per case.** Per-case deltas are one assertion each — small margins; no variance measured.
- **The baseline is strong.** A weaker base model would likely show a larger gap on particles/translation; on Opus those are saturated.

## What's next

- If a bigger, more legible delta matters, consider a harder case: a talk whose field jargon is *dense and off-slide* (where field-grounding compounds), or grading *translation quality* (not just "no CJK remains").
- Re-run via the skill-creator harness for a clean token comparison if cost tracking matters.
- ≥2 samples per case to put error bars on the single-assertion margins.
