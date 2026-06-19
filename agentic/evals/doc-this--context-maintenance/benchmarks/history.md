# Context-maintenance rule — benchmark history

One row per iteration. Configs: `with_rule` vs `without_rule` (the "How to Document
Context" block present/absent in a `$TMPDIR` clean-room `CLAUDE.md`; that block is
the only variable — the doc-this skill is copied into both arms). Pass rate
aggregates correctness (change applied) + reconcile (covering doc kept true) + tool
budget. **Reconcile** is the headline dimension; the blended rate understates the
rule's effect because correctness and budget pass nearly always.

| Iteration | Date | Model | with_rule | without_rule | Delta | Reconcile (w/wo) | Tools (w/wo) | Time (w/wo) | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-20 | claude-opus-4-8 | 100% (30/30) | 93.3% (28/30) | +0.07 | 10/10 / 8/10 | 7.0 / 6.4 | 36.3s / 38.5s | First run, n=2. Both baseline failures are reconcile omissions on the *additive* cases (didn't add `push` to the notify README; didn't create the audit README). The three *stale-value* cases (modify-reference, parent-doc, refactor) the baseline reconciled 6/6 — net-new docs are easier to forget than a value the task implies. No suppression from the "use doc-this" wording: with_rule reconciled 10/10 and invoked doc-this 3× on the additive cases. |
| 2 | 2026-06-20 | claude-opus-4-8 | 100% (36/36) | 94.4% (34/36) | +0.06 | 12/12 / 10/12 | 8.2 / 6.2 | 40s / 36s | Closed the 4 coverage gaps: added an `author`-mode case (Bullet-1 "writing/organizing docs" trigger, graded on routing through doc-this) and an `AGENTS.md` multi-doc reconcile on the refactor case. Same two baseline failures as iter 1 (additive omissions). Author case: both arms routed to doc-this → no delta (an explicit doc task is obviously the skill's job; the rule's marginal effect is on *change*-triggered omissions). AGENTS.md reconcile is now a hard gate (didn't separate arms at n=2). |
