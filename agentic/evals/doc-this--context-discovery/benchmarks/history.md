# Context-discovery rule — benchmark history

One row per iteration. Configs: `with_rule` vs `without_rule` (rule block
present/absent in a `$TMPDIR` clean-room `CLAUDE.md`; that block is the only
variable). Pass rate aggregates correctness + discovery process (README/`AGENTS.md`
as entry point) + tool budget.

| Iteration | Date | Model | with_rule | without_rule | Delta | Tools (w/wo) | Time (w/wo) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-19 | claude-opus-4-8 | 100% (24/24) | 83.3% (20/24) | +0.17 | 3.25 / 4.62 | 16.8s / 26.1s | First run, n=2. Correctness equal (16/16 reached answer); rule wins on process + tool calls, most on the trap (3 vs 7). No-README case costs the rule (4 vs 1.5). Token sum cache-read-dominated, not a clean signal at this corpus size. |
| 2 | 2026-06-20 | claude-opus-4-8 | 100% (24/24) | 77.8% (21/27→ proc 11/24) | +0.22 | 2.88 / 4.5 | 15.7s / 19.4s | Rule copy refactored to scannable bulleted form (v6). **Grader corrected**: process now measures the principle (README read before any code/content; globs are navigation), not the strict "first action is a README read". n=6. with_rule 100% on all dims; rule's value sharpens — process 24/24 vs 11/24 (46%), ~36% fewer tool calls. New copy ties old prose on principle (both ~100%) while more compact (~18% fewer words) and equally efficient. |
| 3 | 2026-06-20 | claude-opus-4-8 | 100% (42/42) | 76.2% (32/42) | +0.24 | 3.71 / 5.36 | 20.2s / 25.9s | **Rule extended to the nearest `AGENTS.md`** (mandatory per-folder instructions), closing the harness gap where a subfolder `AGENTS.md` isn't auto-loaded. 3 new cases + fixtures (no-README subfolder, README+AGENTS both present, AGENTS walk-up). Grader gains an independent `agents_first` track; `process` can be a list. n=2. On the 3 new cases: process **6/6 vs 1/6 (+83pp)** — without the rule, agents read the nearest `AGENTS.md` only 1 time in 6. No regression on the 4 README cases (with_rule 8/8). |
