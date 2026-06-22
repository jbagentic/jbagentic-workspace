# doc-this — benchmark history

One row per iteration; the trend is the point — does each change to the skill move
quality, and at what cost. `w = with_skill`, `wo = without_skill` (baseline). Per-run
and per-dimension detail lives in `iteration-N.md`; raw outputs in the gitignored
`runs/`. `Tools` is blank — tool-call counting isn't wired up for this suite yet.
Format: [history.reference.md](../../docs/history.reference.md).

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [1](#iteration-1) | 2026-06-08 | claude-opus-4-8 | 100% (24/24) / 91.7% (21/24) | +8pp |  | 57.8s / 38s | 23.1k / 15.7k |
| [2](#iteration-2) | 2026-06-08 | claude-opus-4-8 | 2/2 gates / 0/2 gates | — |  | — / — | — / — |
| [3](#iteration-3) | 2026-06-09 | claude-opus-4-8 | case 5 ✓ (+3,4 hold) / case 5 ✓ (old skill) | — |  | — / — | — / — |

## Notes

### Iteration 1
**First run, single sample per case.** Only the backup-tool case discriminates (12/12
vs 9/12 — baseline skips typed docs + manifest); readme-only and fold-existing are
non-discriminating (both 6/6).

### Iteration 2
**Added two-gate input handling** — qualitative gate check, no blended pass rate.
New cases 3 (no input → ask, don't scan) and 4 (no folder → propose + await approval)
both PASS with-skill, both FAIL the true (skill-suppressed) baseline — case-3 baseline
reproduces the "scans a lot of files" complaint. Case 0 (folder named) still writes
directly, no over-ask. Cases 1–2 not re-run (unchanged path). Manual harness, 1 run/case
→ no captured time/tokens (`—`).

### Iteration 3
**Widened the source to support change-driven reconcile** — qualitative check. New case
5 (reconcile after a stated change, folder named) PASSes with-skill — no material-ask, no
approval round-trip, minimal/idempotent. Old-skill baseline also reconciles once invoked,
so case 5 does **not** discriminate on execution; the win is triggering (description),
tested separately. Gate cases 3 & 4 still PASS — widening the source didn't break the
input gates. Manual harness, 1 run/case → no captured time/tokens (`—`).
