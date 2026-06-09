# Benchmark — doc-this, iteration 3

- **Date:** 2026-06-09
- **Model:** claude-opus-4-8 (executor subagents; main loop opus-4-8 [1m])
- **Change under test:** widen what counts as the skill's *source* so it also supports change-driven (reconcile) use — a stated change in an already-documented folder is now a valid source, the folder is its home (no approval round-trip), and only what changed is reconciled. Description broadened to advertise change-driven triggering; Step 6 now offers both the context-discovery and the new context-maintenance convention.
- **Cases run:** 1 new (case 5) with both configs (new skill + old-skill snapshot baseline) + cases 3 and 4 with-skill as gate-regression checks. Cases 0–2 not re-run — their path is unchanged.
- **Runs per case:** 1.
- **Method note:** run manually via executor subagents on **copies** of the fixtures under the gitignored `runs/iteration-3/` (the committed `fixtures/existing-widget/` is never mutated). The old-skill baseline uses a snapshot whose `SKILL.md` is the pre-change version (commit `e9693a4`).

## Result — new change-driven case

| Case | With skill (new) | Baseline (old skill) | Discriminates? |
|---|---|---|---|
| 5 — reconcile after stated change (drop SVG), folder named | **PASS** — no material-ask, no approval round-trip; removed both SVG mentions (README summary + `format` row), manifest intact, no new file, idempotent | **PASS** — same edits; old skill also reconciled in place | ❌ no (execution) |

The baseline **not** discriminating is the honest, expected result: the prompt names the folder and states the change, so even the old skill's "fold into the existing folder" path handles it once invoked (consistent with case 2). The change's real value is **triggering** — the old description never advertised change-driven use, so the skill would not reliably *fire* on "keep the docs in sync after a change" — and making the reconcile path explicit instead of dependent on the model overriding the old "don't scan" / approval gates by judgment. Triggering is a description-level property this execution harness does not measure (see Follow-up).

## Gate-regression checks — the widened source must not break the input gates

| Case | With skill (new) | Outcome |
|---|---|---|
| 3 — bare "doc this", no material | **PASS** | Asked what to document, read only SKILL.md, scanned nothing, wrote nothing. (Its ask now also mentions the change-driven option, reflecting the widened source.) |
| 4 — material, no folder named | **PASS** | Proposed a home folder with a reason, listed the planned files, waited for approval, wrote nothing. (Now also notes it would offer both conventions at Step 6.) |

This is the key non-regression: widening the source did **not** weaken the bare→ask or author→await-approval gates. Both still fire on authoring-from-scratch; only a *stated change in a named/documented folder* bypasses them.

## Reading

- **The reconcile path works and stays gate-free** — case 5 reconciles minimally and idempotently with no material-ask and no approval round-trip.
- **No gate regression** — cases 3 and 4 behave exactly as in iteration-2.
- **Execution was already reachable on the old skill once invoked** — so the win is triggering + reliability, not new execution capability. Reported honestly rather than claiming a false delta.

## Follow-up (not run this iteration)

- **Description-triggering test.** The discriminating win (does the broadened description fire on change-driven phrasings without over-triggering near-misses?) is best measured by skill-creator's description-optimization loop (`run_loop.py`) over a should-trigger / should-not-trigger query set. Deferred to keep this iteration light; recommended before relying on auto-fire.

## Caveats

- **Single run per case; manual harness.** Behavioral, objective assertions (asked vs. scanned; wrote vs. waited; SVG removed vs. not), graded by inspecting executor reports + resulting files.
- **Cases 0–2 not re-run** — unchanged path. Re-run the full set if a future change touches classification/writing.
- **Baseline contamination hazard** stands — baselines must point at the old-skill snapshot, not the installed skill.
