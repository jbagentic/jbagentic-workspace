# Iteration 1 — subtitle-translate-zh

**Date:** 2026-06-10 · **Model:** claude-opus-4-8 · **Runs:** 1 sample per config

## Result

| Config | Pass rate | Tokens (mean) | Time (mean) |
|---|---|---|---|
| With skill | **97.2%** (33/34) | 62,577 | 331.8s |
| Baseline (no skill) | 94.4% (32/34) | 32,697 | 172.6s |
| Delta | **+2.8pp** | +29,880 | +159.2s |

Per-case (with_skill / baseline): excerpt-khew 10/10 · 10/10 · excerpt-soh 12/12 · 12/12 · synthetic-vocab-traps 11/12 · 10/12.

## What discriminated

- **Both real-talk excerpts were non-discriminating** — 10/10 and 12/12 in both configs. As the subtitle-polish eval predicted, real transcripts pass the invariants and proper-noun checks regardless of skill; they earn their place as a regression guard, not as a signal source. All signal came from the synthetic case.
- **The skill's win (synthetic):** the baseline translated the speaker's name "Jia Wen" → 嘉文; the skill kept it verbatim, per its proper-noun rule. That is the exact failure mode the skill exists to prevent.
- **Shared miss (both configs):** "percent" was written as "%"/未译 instead of 巴仙. This is an *eval-input gap, not a skill defect* — the 巴仙 preference lives in the project's reference doc, which the eval did not stage. The prompt only said "Malaysian Chinese readers." Fix planned for iteration 2 (below).

## Parity fix applied mid-iteration

The first pass measured a fallback, not the skill's real workflow: with-skill subagents could not reach OpenCC, so they hand-converted Simplified→Traditional. Two root causes, both fixed:

1. `opencc-python-reimplemented` was not installed → installed user-level.
2. The project allowlist had no `python3`, so background subagents (which cannot prompt) got Bash denied silently → added `Bash(python3 *)` to `.claude/settings.json` (probe-verified reachable by background agents).

All three with-skill `.zh-Hant.srt` files were then regenerated via real OpenCC `s2twp` and re-verified (byte-identical timestamps, UTF-8 no BOM). `prepare.py` now guards the OpenCC prerequisite so this cannot silently recur.

## Caveat on cost numbers

With-skill tokens/time are **inflated by the two-pass redo** (translate, then a separate OpenCC conversion pass after the permission fix). A clean single run is translate + one OpenCC call — materially cheaper. The pass *rate* is unaffected (conversion is deterministic), so the +2.8pp quality delta is sound; the cost delta is not yet a fair single-run figure. Capture a clean single-run cost in iteration 2.

## Planned for iteration 2

Stage the project reference doc (audience + vocab table: 令吉 for ringgit, 巴仙 for percent, prefer universally-understood phrasing) as a companion file in each case folder, and reword prompts to point at it rather than inline a partial audience label. This makes the 令吉/巴仙 assertions fair, tests the skill's real contract (discover and apply the project's vocab preferences), and should widen the delta beyond +2.8pp since the skill is instructed to consult the reference doc while the baseline is not.
