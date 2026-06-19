# Iteration 1 — context-maintenance rule

- **Date:** 2026-06-20
- **Model:** claude-opus-4-8 (`claude -p` default)
- **Setup:** 5 cases × 2 configs (`with_rule` / `without_rule`) × 2 runs = 20 runs.
  Write-enabled headless executors in `$TMPDIR` clean rooms; doc-this skill copied
  into both arms; rule block the only variable.

## Result

| Config | Blended pass | Reconcile | Change applied | Within budget | Tools (mean) | Time (mean) | doc-this invoked |
|---|---|---|---|---|---|---|---|
| `with_rule` | **100%** (30/30) | **10/10** | 10/10 | 10/10 | 7.0 | 36.3s | 3 |
| `without_rule` | 93.3% (28/30) | **8/10** | 10/10 | 10/10 | 6.4 | 38.5s | 0 |

Blended delta **+0.07**; the meaningful **reconcile delta is +0.20** (100% vs 80%).
The blend dilutes it because *change applied* and *within budget* pass on every run
in both arms — exactly as in the discovery eval, where correctness barely separated
the arms and the signal lived in the secondary dimension.

## What separated the arms

Both `without_rule` failures were **reconcile omissions on the additive cases**:

- `add-function-update-readme` / run-2 — added `send_push()` to the code but left
  the notify README's channel list unchanged (no "push").
- `new-module-create-readme` / run-2 — wrote `audit/audit.py` but never created
  `audit/README.md` for the new module.

The three **stale-value** cases — `modify-reference-in-doc` (a `docs/*` reference),
`parent-doc-reconcile` (parent README), `refactor-update-manifest` (README file
manifest) — the baseline reconciled **6/6**. Reading: updating a doc whose value the
task directly contradicts is hard to skip; **documenting something net-new**
(a new channel, a new module) is the omission the rule actually prevents. That this
is where the rule pays off is the useful finding, and it argues the additive cases
are the ones worth weighting in future iterations.

## Notes / caveats

- **No suppression from the "use doc-this, don't hand-write" wording.** The concern
  was that, with the skill present, a `with_rule` agent might defer to doc-this and
  skip a hand-edit. It didn't: `with_rule` reconciled 10/10 and invoked doc-this 3×
  (on the two additive cases) — the rest it reconciled by hand. The skill-present
  design is sound.
- **The skill's presence did not move the baseline to invoke it** (0 invocations) —
  yet the baseline still reconciled 8/10 by default habit. So the +0.20 is the
  rule's marginal effect *over a strong default*, consistent with the harness's
  baseline philosophy.
- **Tool count:** `with_rule` slightly higher (7.0 vs 6.4), driven by the 3 doc-this
  invocations; all runs stayed well within budget, so efficiency was not a
  separating signal (budgets are deliberately generous because a skill invocation
  inflates inline tool calls). Token sums are close (166k / 161k) and
  cache-dominated — not a clean efficiency signal at this corpus size.
- **Small sample (n=2).** The delta rests on 2 baseline failures; widen with
  `--runs 4+` and consider adding more additive cases before drawing strong
  conclusions.
