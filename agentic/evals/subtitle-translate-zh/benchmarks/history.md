# subtitle-translate-zh — benchmark history

One row per iteration; the trend is the point — does each change to the skill move
quality, and at what cost. `w = with_skill`, `wo = without_skill` (baseline). Per-run
and per-dimension detail lives in `iteration-N.md`; raw outputs in the gitignored
`runs/`. `Tools` is blank — tool-call counting isn't wired up for this suite yet.
Format: [history.reference.md](../../docs/history.reference.md).

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [1](#iteration-1) | 2026-06-10 | claude-opus-4-8 | 97.2% (33/34) / 94.4% (32/34) | +3pp |  | 331.8s / 172.6s | 62.6k / 32.7k |
| [2](#iteration-2) | 2026-06-10 | claude-opus-4-8 | 97.2% (35/36) / 88.9% (32/36) | +8pp |  | 430.9s / 293.4s | 30.1k / 28.5k |
| [3](#iteration-3) | 2026-06-11 | claude-opus-4-8 | 100% (36/36) / 88.9% (32/36) | +11pp |  | 87.1s / 293.4s | 30.5k / 28.5k |

## Notes

### Iteration 1
**First run, single sample.** Skill's win: kept speaker name "Jia Wen" verbatim where
baseline rendered 嘉文. Real-talk excerpts non-discriminating (both perfect); synthetic
carries all signal. Both miss 巴仙 — eval didn't stage the project vocab reference doc
(fixed in iter 2). With-skill tokens/time inflated by a two-pass OpenCC redo after a
mid-run parity fix (python3 was denied to background subagents).

### Iteration 2
**Refactor:** skill owns audience→vocabulary know-how; prompts name only the two
audiences (Malaysian→Simplified, Taiwanese→Traditional). Added 2 zh-Hant localism
assertions (34→36); retires iter-1's "stage a vocab doc" plan. Delta widened as predicted
— baseline, given only audience names, now fails 巴仙 and the new zh-Hant localism
(令吉→林吉特). Shared miss: both transliterated speaker name "Jia Wen" (嘉雯/嘉文) —
with-skill regressed there vs iter 1; watch. Clean single-run cost (no redo). Runs via
Agent tool, graded by grade.py, aggregated from grading.json (not the flaky aggregator).

### Iteration 3
**De-hardcode:** skill names the capability ("slide deck's pre-extracted text"),
`slides.txt` only an example; eval rewired to stage `slides.txt` and prompts point at it
(not `slides.pdf`). **No-regression check, not a cost win** — tokens flat vs iter 2
(30.5k vs 30.1k): translate reads the deck only on-demand to confirm a spelling, so format
barely matters (the slides.txt token win lives in polish, not here). Pass ticked 35→36
only because the iter-2 "Jia Wen" transliteration miss (n=1 variance, rule untouched)
didn't recur. Time 87s is executor variance, not a slides.txt effect — read the token
column. `with_skill` only; **baseline carried from iter 2** (28.5k / 293.4s; it never
reads the deck).
