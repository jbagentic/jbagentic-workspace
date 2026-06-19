# Iteration 2 — context-maintenance rule (coverage gaps closed)

- **Date:** 2026-06-20
- **Model:** claude-opus-4-8 (`claude -p` default)
- **Setup:** 6 cases × 2 configs × 2 runs = 24 runs. Adds an `author`-mode case (the
  "writing or organizing docs" trigger) and an `AGENTS.md` multi-doc reconcile on the
  refactor case. Closes the 4 coverage gaps found analysing iteration 1.

## Result

| Config | Blended pass | Reconcile | Dim-1 (change / means) | Within budget | Tools | Time | doc-this calls |
|---|---|---|---|---|---|---|---|
| `with_rule` | **100%** (36/36) | **12/12** | 12/12 | 12/12 | 8.2 | 40s | 6 |
| `without_rule` | 94.4% (34/36) | **10/12** | 12/12 | 12/12 | 6.2 | 36s | 2 |

Blended delta **+0.06**; the meaningful **reconcile delta is +0.17** (12/12 vs 10/12).
Both `without_rule` failures are the same omission pattern as iteration 1 — additive
cases where the doc is net-new: `add-function` (didn't add "push" to the notify
README) and `new-module` (didn't create the audit README). The stale-value and
multi-doc cases reconciled in both arms.

## What the new coverage showed

- **Bullet-1 trigger (`document-undocumented-folder`) — covered, but no delta.**
  Both arms routed the "document this folder" task through doc-this (dim-1 "routed to
  doc-this" passed 4/4; `without_rule` made exactly its 2 doc-this calls here). The
  honest reading: for an *explicit* doc-authoring task the skill is so obviously
  applicable that the baseline reaches for it without the rule — the rule's marginal
  effect on this trigger is ~0 in this setup. The value of the case is **coverage**
  (the trigger and the "use doc-this" means are now exercised), not a delta. Where the
  rule actually pays off remains the *change*-triggered omissions.
- **AGENTS.md multi-doc reconcile — now a hard gate.** The refactor case requires both
  `auth/README.md` (file manifest) and `auth/AGENTS.md` (convention) to reconcile.
  Spot-checked: agents rewrote the AGENTS.md convention to name `access_tokens.py` /
  `refresh_tokens.py` and drop `session_tokens.py`. All 4 runs passed at n=2 (it didn't
  separate the arms this round), but the second doc is now a real failure surface.

## Notes / caveats

- **doc-this usage rose with the rule on the *change* cases** (6 calls vs 2), but it
  didn't change outcomes — hand-edits reconcile just as well, which is why reconcile is
  graded outcome-based. The means is only graded on the author case (the Gap-2 proxy).
- **Tool count:** `with_rule` higher (8.2 vs 6.2), driven by the extra doc-this
  invocations; all within budget. Not a separating signal (budgets are generous).
- **Refactor fidelity:** some runs reconciled the docs correctly but left the old
  `session_tokens.py` file on disk (the docs no longer reference it). The eval grades
  doc maintenance, not refactor completeness, so this passes — worth knowing the cases
  don't assert full code cleanup.
- **Small sample (n=2).** The reconcile delta still rests on 2 baseline failures.
  Widen with `--runs 4+` and weight the additive cases, which are where the signal lives.
