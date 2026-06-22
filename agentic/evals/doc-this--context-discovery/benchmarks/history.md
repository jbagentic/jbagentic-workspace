# Context-discovery rule — benchmark history

One row per iteration. `w = with_rule`, `wo = without_rule` — the rule block
present/absent in a `$TMPDIR` clean-room `CLAUDE.md` is the only variable. `Pass` blends
correctness + discovery process (README/`AGENTS.md` as entry point) + tool budget; the
per-dimension breakdown lives in each `iteration-N.md`. Tokens are cache-read-dominated —
directional only (and often favor `wo`); tool calls are the cleaner efficiency signal.
Format: [history.reference.md](../../docs/history.reference.md).

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [1](#iteration-1) | 2026-06-19 | claude-opus-4-8 | 100% (24/24) / 83.3% (20/24) | +17pp | 3.25 / 4.62 | 16.8s / 26.1s | 98.6k / 57.4k |
| [2](#iteration-2) | 2026-06-20 | claude-opus-4-8 | 100% (72/72) / 77.8% (56/72) | +22pp | 2.88 / 4.5 | 15.7s / 19.4s | 89.2k / 65.9k |
| [3](#iteration-3) | 2026-06-20 | claude-opus-4-8 | 100% (42/42) / 76.2% (32/42) | +24pp | 3.71 / 5.36 | 20.2s / 25.9s | 85.6k / 67.7k |

## Notes

### Iteration 1
**First run, n=2.** Correctness equal (16/16 reached answer); the rule wins on process
+ tool calls, most on the trap (3 vs 7). The no-README case costs the rule (4 vs 1.5).
Token sum is cache-read-dominated — not a clean signal at this corpus size.

### Iteration 2
**Rule copy refactored to scannable bulleted form (v6); grader corrected.** Process now
measures the principle (README read before any code/content; globs are navigation), not
the strict "first action is a README read". n=6. `with_rule` 100% on all dims; the
rule's value sharpens — process 24/24 vs 11/24 (46%), ~36% fewer tool calls. The new
copy ties the old prose on principle (both ~100%) while more compact (~18% fewer words)
and equally efficient.

### Iteration 3
**Rule extended to the nearest `AGENTS.md`** (mandatory per-folder instructions),
closing the harness gap where a subfolder `AGENTS.md` isn't auto-loaded. 3 new cases +
fixtures (no-README subfolder, README+AGENTS both present, AGENTS walk-up). Grader gains
an independent `agents_first` track; `process` can be a list. n=2. On the 3 new cases:
process **6/6 vs 1/6 (+83pp)** — without the rule, agents read the nearest `AGENTS.md`
only 1 time in 6. No regression on the 4 README cases (`with_rule` 8/8).
