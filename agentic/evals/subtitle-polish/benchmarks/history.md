# subtitle-polish — benchmark history

One row per iteration; the trend is the point — does each change to the skill move
quality, and at what cost. `w = with_skill`, `wo = without_skill` (baseline). Per-run
and per-dimension detail lives in `iteration-N.md`; raw outputs in the gitignored
`runs/`. `Tools` is blank — tool-call counting isn't wired up for this suite yet.
Format: [history.reference.md](../../docs/history.reference.md).

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [1](#iteration-1) | 2026-06-08 | claude-opus-4-8 | 93.3% (28/30) / 96.7% (29/30) | −3pp |  | 245.6s / 169.7s | 50.7k / 46.1k |
| [2](#iteration-2) | 2026-06-11 | claude-opus-4-8 | 97.1% (34/35) / 94.3% (33/35) | +3pp |  | 903.5s / 464.2s | 116.0k / 93.8k |
| [3](#iteration-3) | 2026-06-11 | claude-opus-4-8 | 100% (35/35) / 94.3% (33/35) | +5.7pp |  | 446.5s / 464.2s | 90.8k / 93.8k |
| [4](#iteration-4) | 2026-06-12 | claude-opus-4-8 | 100% (35/35) / 94.3% (33/35) | +5.7pp |  | — / 464.2s | 80.3k / 93.8k |
| [5](#iteration-5) | 2026-06-12 | claude-opus-4-8 | 100% (40/40) / 92.5% (37/40) | +7.5pp |  | 448.8s / 313.1s | 96.6k / 89.0k |

## Notes

### Iteration 1
**First run, single sample.** Skill trails baseline on raw pass rate but its loss is an
over-correction (rewrote spoken "OpenClaw" → slide's "OpenRouter") while baseline's loss
is the failure the skill prevents (scrubbed "ya"/"okay" particles). Real 916-cue case
non-discriminating (both 10/10); synth cases carry all signal.

### Iteration 2
**Skill rewrite:** principle-based restraint + phonetic-only term gate + particle "thin,
never to zero" (sharpened heavy-user trigger). All-real eval (35 assertions, not
like-for-like with iter 1). **Iter-1 over-correction fixed** — skill kept spoken "Open
Claw" (≠ slide "OpenRouter"). **Thinning now works** — Kowa's 138 `lah` → 106 with-skill
vs 138 baseline (new discriminator); also fixed a grader brittleness (spaced "Open Claw":
32→33). Skill's only booked miss ("Jason B"→`jsonb`, the truer answer) is an
expected-answer artifact — correct it and delta is +6pp. Baseline's misses: scrubbed
"ah", un-thinned `lah`. Single sample; Kowa with-skill cost ~20 min.

### Iteration 3
**Cost cut, quality up.** Glossary now from a reusable `slides.txt` (deck text extracted
once by the `slides-pdf-to-text` skill) instead of slide-PNG vision. −22% tokens (now
*below* the carried baseline) and ~half the time vs iter 2, pass rate 35/35. Per-deck
token saving scales with slide count: kowa (21 slides) −48.6k, soh (14) −32.3k, khew (6)
+5k (saving < noise). Quality held — `Azure portal` still recovered from "Asia bottle"
(anchored by `Bicep`) though `slides.txt` lacks "Azure". `with_skill` only; **baseline
carried from iter 2** (93.8k / 464.2s). Single sample.

### Iteration 4
**Loop removed.** Workflow restructured into 4 linear steps (strip → build glossary → fix
w/ "speaker's words win" folded in → single verify pass); the iter-3 verify *loop* is
gone. −11.5% tokens vs iter 3, consistent across all decks (khew −9.3%, kowa −10.4%, soh
−15.3%) and tracking cue-count not slide-count — confirms the loop, not the glossary, was
the remaining cost. Pass held 35/35; worry cases intact. **Honest:** smaller than the
~30–40% projected. `with_skill` only; **baseline carried** (93.8k / 464.2s). Iter-4
tokens are `subagent_tokens` (not the harness path iter-3 used) — direction consistent,
magnitude not perfectly like-for-like. Time is `—`: the hand-orchestrated subagent path
captured tokens but no wall-clock.

### Iteration 5
**⚠️ Not like-for-like with 1–4** — assertion set changed (35→40); particle assertions
flipped from *preserved/thinned* to **removed by default**. Measures the rewritten skill:
particles removed by default · non-English **translated** to English · **field-grounded**
term fixes. **Baseline re-run, not carried.** Discriminating value is now narrower and
clearer: **off-slide field-jargon recovery** (khew "Cortez"→`Codex` ×6; baseline mis-fixed
to the dictionary word `Cortex` ×5 — the only term assertion baseline failed) + **invariant
discipline** (both baseline misses were empty cues left behind). **Honest:** particle-removal
and translation no longer discriminate — the strong Opus baseline does both unprompted.
Tokens up vs iter 4 (skill now does more: translate + true multi-pass full-file read);
hand-orchestrated `subagent_tokens`, not harness path. Single sample per case.
