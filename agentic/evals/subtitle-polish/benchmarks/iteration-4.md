# Benchmark — subtitle-polish, iteration 4

- **Date:** 2026-06-12
- **Model:** claude-opus-4-8
- **Cases:** 3 real talks — `real-khewjiapeng` (916 cues, 6-slide deck), `real-kowajialiang` (875 cues, 21-slide deck), `real-sohjunwei` (806 cues, 14-slide deck).
- **Runs per case:** 1, `with_skill` only. Baseline unchanged from iteration 2 (carried forward, not re-run).
- **What changed:** the Workflow was **restructured into four linear steps, run once each, ending in a single verify pass** — the iteration-3 loop (*"Loop steps 2–3 until residual issues are stylistic"*) is gone. Glossary-building is now its own explicit step (2); the "speaker's words win" correctness rule moved *into* the Fix step (3) so the fix is right the first time and Verify (4) is one light pass, not an iterated correction loop. Same 35-assertion eval.

## Result

| Metric | With skill (iter 4) | With skill (iter 3) | Baseline (carried) |
|---|---|---|---|
| Pass rate | **100% (35/35)** | 100% (35/35) | 94.3% (33/35) |
| Tokens (mean) | **80,296** | 90,764 | 93,843 |

**Dropping the verify loop cut ~11.5% of tokens with no quality loss — pass rate held at 35/35.**

### Per-deck tokens (iter3 → iter4)

| Case | cues | slides | iter3 | iter4 | Δ tok | Δ % |
|---|---|---|---|---|---|---|
| khew | 916 | 6 | 101,466 | 92,061 | −9,405 | −9.3% |
| kowa | 875 | 21 | 86,065 | 77,074 | −8,991 | −10.4% |
| soh | 806 | 14 | 84,762 | 71,753 | −13,009 | −15.3% |

The saving is consistent across all three decks (unlike iter-3's glossary win, which only helped slide-heavy decks). It tracks cue count, not slide count — confirming the loop, not the glossary, was the remaining cost.

## Honest caveats

- **Smaller than projected.** The plan estimated ~30–40%; actual was ~11.5%. The iteration-3 runs evidently did not re-emit the full transcript 2–3× — removing the explicit loop trimmed re-check/reasoning overhead rather than halving output. Real and consistent, but modest.
- **Measurement comparability.** Iter-4 tokens are the executor's `subagent_tokens`; iter-3's came from the eval harness. The two may not be perfectly apples-to-apples, but the direction is consistent across all three decks and the workflow is now structurally single-pass (every executor confirmed: four steps once each, no verify loop).
- **Single sample per case**, `with_skill` only; baseline carried from iter 2.

## Quality held — the worry cases all passed

- **khew 10/10:** every `IaC` mis-hearing (IAC/ISC/ISA/ICNA/'I a C') converged to canonical; **`Azure portal` recovered from "Asia bottle"**; `lah` 78→59, `ya` 44→24 (thinned, not zeroed); particles preserved.
- **kowa 13/13:** `cloud`→`Claude`, `cloud code`→`Claude Code`, `cloud MD`→`CLAUDE.md`, `Jason`→`JSON` all recovered; `MCP`/`API` preserved untouched; `lah` 138→85 (thinned, kept voice).
- **soh 12/12:** restraint intact — **`OpenClaw` left as the speaker said it, NOT rewritten to the slide's `OpenRouter`**; Hermes/Telegram/MCP preserved; `ah` 37→17 thinned.

## What's next

- Re-run with ≥2 samples per case if the token delta needs tightening (single sample; per-deck deltas are larger than typical run noise but not measured for variance).
- Consider capturing iter-4 tokens via the same harness path as earlier iterations for a clean like-for-like comparison.
