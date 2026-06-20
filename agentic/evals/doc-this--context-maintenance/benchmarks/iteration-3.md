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
| `with_rule` | **100%** (36/36) | **12/12** | 12/12 | 12/12 | 7.4 | 4 |
| `without_rule` | 97.2% (35/36) | 11/12 | 12/12 | 12/12 | 6.5 | 2 |

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
- **Efficiency is a non-signal, and the baseline's lower count is partly an artifact.**
  Mean action tools: `with_rule` 7.4 vs `without_rule` 6.5 — the rule arm runs slightly
  *heavier*, same direction as every prior iteration (it does the additive reconcile work
  the baseline sometimes skips). Every run is well under budget (max 11 vs budgets of
  15–20), so efficiency doesn't separate the arms. Don't read the baseline's lower mean as
  thrift: `new-module` `without_rule` was `[4, 11]`, and the 4-tool run is the one that
  *failed* to create the audit README — fewer tools because it did less, not because it was
  efficient. A text rewrite shouldn't move tool efficiency anyway; it changes what the
  agent reads, not what it does.
- **doc-this usage: 4 `with_rule` / 2 `without_rule`, concentrated in two cases.** The
  author case (`document-undocumented-folder`) routed through doc-this in *both* arms (2
  each) — an explicit doc task is obviously the skill's job, so the rule adds no delta
  there. The only *change*-case routing was `new-module`, where `with_rule` invoked
  doc-this (2) and reconciled both runs, while `without_rule` didn't invoke it and one run
  failed to create the README. Every other change case (`modify-reference`, `parent-doc`,
  `refactor`, `add-function`) hand-edited in both arms — confirming the trimmed rule (which
  no longer says "`doc-this` reconciles" on the change bullet) still gets docs reconciled
  by hand, while doc-this remains the path the rule reaches for on net-new docs.
- **Small sample (n=2).** The reconcile signal still rests on a single baseline failure.
  Widen with `--runs 4+` and weight the additive cases to firm it up.
