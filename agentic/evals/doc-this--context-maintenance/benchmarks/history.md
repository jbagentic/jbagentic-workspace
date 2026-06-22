# Context-maintenance rule — benchmark history

One row per iteration. `w = with_rule`, `wo = without_rule` — the "How to Document
Context" block present/absent in a `$TMPDIR` clean-room `CLAUDE.md` is the only variable
(the doc-this skill is copied into both arms). `Pass` blends correctness (change
applied) + reconcile (covering doc kept true) + tool budget; **reconcile** is the
headline dimension and the blended rate understates the rule's effect (correctness and
budget pass nearly always), so the per-dimension breakdown lives in each `iteration-N.md`.
Tokens are cache-read-dominated — directional only; tool calls are the cleaner signal.
Format: [history.reference.md](../../docs/history.reference.md).

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [1](#iteration-1) | 2026-06-20 | claude-opus-4-8 | 100% (30/30) / 93.3% (28/30) | +7pp | 7.0 / 6.4 | 36.3s / 38.5s | 165.6k / 161.4k |
| [2](#iteration-2) | 2026-06-20 | claude-opus-4-8 | 100% (36/36) / 94.4% (34/36) | +6pp | 8.2 / 6.2 | 40s / 36s | 176.2k / 189.3k |
| [3](#iteration-3) | 2026-06-20 | claude-opus-4-8 | 100% (36/36) / 97.2% (35/36) | +3pp | 7.4 / 6.5 | 42.4s / 34.9s | 190.7k / 151.5k |

## Notes

### Iteration 1
**First run, n=2.** Both baseline failures are reconcile omissions on the *additive*
cases (didn't add `push` to the notify README; didn't create the audit README). The
three *stale-value* cases (modify-reference, parent-doc, refactor) the baseline
reconciled 6/6 — net-new docs are easier to forget than a value the task implies. No
suppression from the "use doc-this" wording: `with_rule` reconciled 10/10 and invoked
doc-this 3× on the additive cases. (reconcile 10/10 / 8/10.)

### Iteration 2
**Closed the 4 coverage gaps.** Added an `author`-mode case (Bullet-1 "writing/organizing
docs" trigger, graded on routing through doc-this) and an `AGENTS.md` multi-doc reconcile
on the refactor case. Same two baseline failures as iter 1 (additive omissions). Author
case: both arms routed to doc-this → no delta (an explicit doc task is obviously the
skill's job; the rule's marginal effect is on *change*-triggered omissions). `AGENTS.md`
reconcile is now a hard gate (didn't separate arms at n=2). (reconcile 12/12 / 10/12.)

### Iteration 3
**No-regression check for the rule rewrite** (form-aligned to the discovery rule, ~25%
shorter; reconcile target now stated as "either in the folder or in the nearest parent
folder" rather than "the folder's own README, or the nearest one above"). `with_rule`
held 100% / 12-12 reconcile, unchanged from iter 2. `parent-doc-reconcile` passed both
`with_rule` runs — the softer location-framed wording still reconciled the parent README.
The lone baseline miss is the usual additive omission (`new-module` audit README); the
higher `without_rule` rate is n=2 variance (one omission this round vs two), not a rule
effect. Efficiency is a non-signal (7.4 vs 6.5 tools, all under budget; the baseline's
lower mean partly reflects the failed run doing less work). doc-this calls 4/2,
concentrated in the author case (both arms) + `new-module` (`with_rule` only, where it
reconciled while the baseline failed); other change cases hand-edited in both arms.
(reconcile 12/12 / 11/12.)
