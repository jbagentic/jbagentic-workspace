# Benchmark — doc-this, iteration 2

- **Date:** 2026-06-08
- **Model:** claude-opus-4-8 (executor subagents; main loop opus-4-8 [1m])
- **Change under test:** two-gate input handling — (1) bare/no-material invocation asks for the source material instead of scanning the repo; (2) when no folder is named, propose a home folder with a reason and wait for approval before writing. When a folder *is* named, proceed directly (no over-asking).
- **Cases run:** 2 new (case 3, case 4) with both configs + case 0 with-skill as a regression check. Cases 1–2 not re-run — the change doesn't touch their path (explicit folder + thin/idempotent material; iteration-1 had both at 6/6).
- **Runs per case:** 1.
- **Method note:** run manually via executor subagents in the live repo (no external aggregator). The first baseline pass auto-fired the *installed* `doc-this` skill and was discarded; baselines were re-run with the skill explicitly suppressed to get a true no-skill comparison.

## Result — the two new gate cases

| Case | With skill | Baseline (skill suppressed) | Discriminates? |
|---|---|---|---|
| 3 — no input → ask for material | **PASS** — asked for the source material, read only SKILL.md, wrote nothing, did not scan | **FAIL** — interpreted "doc this" as "document the cwd", ran `ls`/`find`/multiple reads, wrote a README unprompted | ✅ yes |
| 4 — material, no folder → propose + await approval | **PASS** — proposed `tools/backup-tool/` with a reason, listed the planned files, waited for approval, wrote nothing | **FAIL** — picked a location itself and wrote without asking for placement approval | ✅ yes |

Case 3's baseline behavior is exactly the reported problem: with no input, a generic assistant scans files and invents a subject. The skill converts that into an upfront ask.

## Regression check — explicit folder given (case 0)

| Case | With skill | Outcome |
|---|---|---|
| 0 — backup-tool, folder named `tools/backup-tool/` | **PASS** | Proceeded directly to writing — did **not** stop to ask for approval (folder was named). Produced the full conformant set: README + manifest, AGENTS (two hard rules), `cli.reference.md`, `incremental-snapshots.guide.md`, `restore.runbook.md`; correct routing, no duplication. |

This is the key non-regression: the new approval gate fires **only** when the folder is unspecified, so the normal flow with a named folder is unchanged from iteration-1.

## Reading

- **The change does what it set out to.** Both new gates pass with-skill and both discriminate cleanly against a true baseline — and the case-3 baseline reproduces the original complaint verbatim (scans a lot of files).
- **No over-asking regression.** With the folder named, the skill skips the approval round-trip and writes immediately, matching iteration-1's output quality.

## Caveats

- **Single run per case; manual harness.** No variance estimate, and grading was by direct inspection of executor transcripts + outputs rather than a separate grader subagent. The gate assertions are behavioral and objective (asked vs. scanned; wrote vs. waited), so this is low-risk.
- **Cases 1–2 not re-run this iteration** — unchanged code path. If a future change touches classification/writing, re-run the full set.
- **Baseline contamination is a standing hazard** when running evals inside a repo where the skill is installed — baselines must explicitly suppress the Skill tool.
