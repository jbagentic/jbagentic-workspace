# Iteration 3 — context-maintenance rule (rewrite, no-regression check)

- **Date:** 2026-06-20
- **Model:** claude-opus-4-8 (`claude -p` default)
- **Setup:** 6 cases × 2 configs × 2 runs = 24 runs. Same fixtures and grader as
  iteration 2 — no eval changes. This run guards a **rewrite of the rule text**, not a
  coverage change.

## Why this iteration

The "How to Document Context" block was rewritten to match the sibling "How to Discover
Context" rule's silhouette (bold opener → condition→action bullets → closing one-liner)
and trim ~25% of the words. The new body states *where covering docs live* ("either in
the folder or in the nearest parent folder with README") instead of ordering "update the
folder's own README, or the nearest one above it if it has none." The question was
whether that softer, location-framed wording would regress reconcile — especially the
`parent-doc-reconcile` case (change in `billing/capture/` with no local README → must
update the parent `services/billing/README.md`).

## Result

| Config | Blended pass | Reconcile | Dim-1 (change / means) | Within budget | Tools | doc-this calls |
|---|---|---|---|---|---|---|
| `with_rule` | **100%** (36/36) | **12/12** | 12/12 | 12/12 | 7.4 | 0 |
| `without_rule` | 97.2% (35/36) | 11/12 | 12/12 | 12/12 | 6.5 | 0 |

**No regression.** `with_rule` holds 100% and reconcile 12/12 — identical to iteration 2.
The one `without_rule` miss is the familiar additive omission (`new-module`: didn't create
`services/audit/README.md`), the same pattern as iterations 1–2. `parent-doc-reconcile`
passed both `with_rule` runs — the location-framed wording reconciled the parent README
without the explicit "nearest one above" directive, so the flagged risk did not
materialise.

## Notes / caveats

- **`without_rule` rose to 97.2%** (from 94.4% in iter 2) because only one additive case
  missed this round instead of two — baseline run variance at n=2, not an effect of the
  rule (the rewrite touches only the `with_rule` arm). The headline is `with_rule` holding
  100% / 12-12, not the shrunken blended delta (+0.03).
- **doc-this calls dropped to 0 in both arms** this round (iter 2 had 6 `with_rule` / 2
  `without_rule`). Agents hand-edited the covering docs throughout. Reconcile is graded
  outcome-based, so this passes — and it confirms the trimmed rule (which no longer says
  "`doc-this` reconciles" on the change bullet) still gets the docs reconciled by hand.
  The author-mode routing means (`document-undocumented-folder`) still passed.
- **Small sample (n=2).** The reconcile signal still rests on a single baseline failure.
  Widen with `--runs 4+` and weight the additive cases to firm it up.
