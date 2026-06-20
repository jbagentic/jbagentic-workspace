# Context-discovery rule — benchmark history

One row per iteration. Configs: `with_rule` vs `without_rule` (rule block
present/absent in a `$TMPDIR` clean-room `CLAUDE.md`; that block is the only
variable). Pass rate aggregates correctness + README-first process + tool budget.

| Iteration | Date | Model | with_rule | without_rule | Delta | Tools (w/wo) | Time (w/wo) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-19 | claude-opus-4-8 | 100% (24/24) | 83.3% (20/24) | +0.17 | 3.25 / 4.62 | 16.8s / 26.1s | First run, n=2. Correctness equal (16/16 reached answer); rule wins on process + tool calls, most on the trap (3 vs 7). No-README case costs the rule (4 vs 1.5). Token sum cache-read-dominated, not a clean signal at this corpus size. |
| 2 | 2026-06-20 | claude-opus-4-8 | 100% (24/24) | 77.8% (21/27→ proc 11/24) | +0.22 | 2.88 / 4.5 | — | Rule copy refactored to scannable bulleted form (v6). **Grader corrected**: process now measures the principle (README read before any code/content; globs are navigation), not the strict "first action is a README read". n=6. with_rule 100% on all dims; rule's value sharpens — process 24/24 vs 11/24 (46%), ~36% fewer tool calls. New copy ties old prose on principle (both ~100%) while more compact (~18% fewer words) and equally efficient. |
