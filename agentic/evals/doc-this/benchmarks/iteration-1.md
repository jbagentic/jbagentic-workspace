# Benchmark — doc-this, iteration 1

- **Date:** 2026-06-08
- **Model:** claude-opus-4-8 (executor subagents; main loop opus-4-8 [1m])
- **Cases:** 3 (eval-backup-tool, eval-readme-only, eval-fold-existing)
- **Runs per case:** 1 (no variance estimate yet)
- **Baseline:** same prompt with no skill
- **Assertions:** 24 total (12 + 6 + 6)

## Result

| Metric | With skill | Baseline | Delta |
|---|---|---|---|
| Pass rate (mean of cases) | 100% | 91.7% | **+0.08** |
| Pass rate (assertions) | 24/24 | 21/24 | +3 |
| Time | 57.8s | 37.7s | +20.1s |
| Tokens | 23,120 | 15,736 | +7,384 |

## Per-case breakdown

| Case | With skill | Baseline | Baseline failures |
|---|---|---|---|
| backup-tool (full folder) | 12/12 | 9/12 | no docs manifest; no `*.guide.md`; no `*.reference.md` |
| readme-only (restraint) | 6/6 | 6/6 | — |
| fold-existing (idempotent edit) | 6/6 | 6/6 | — |

## Reading

- **The skill works and the one discriminating case proves it.** `backup-tool` is the case with
  enough raw material to demand real structure, and that's exactly where the gap opens: the skill
  routed content into a `*.guide.md` (incremental-chain concept), a `*.reference.md` (env vars +
  command table), and a `*.runbook.md` (restore procedure), with a true README manifest linking all
  three. The baseline consolidated everything into one long README — no typed docs, no manifest —
  so it missed 3 of 12 assertions. The split is precisely the Contextful Folder value the skill encodes.
- **The two easy cases don't discriminate — and that's the right outcome.** For `readme-only` (one
  5-line script) and `fold-existing` (add one spec fact), the natural answer already matches the skill:
  both configs produced a single README / a single surgical edit to the correct `*.reference.md`,
  no over-splitting, no duplication, manifest intact, no frontmatter. The skill earns its keep by not
  *regressing* restraint here, not by beating the baseline.
- **Cost.** +20.1s and +7.4k tokens with-skill — the overhead of reading the skill + its two
  references and verifying invariants. Reasonable for the routing quality gained on substantive inputs.

## Discrimination note

Only `backup-tool` separates skill from baseline; the other two are non-discriminating (both 6/6).
That's expected for thin/idempotent inputs, but it means iteration-1's signal rests on a single case.
To harden the eval, consider adding a second "enough material to split" case (so routing is tested
more than once) and a near-miss case that *tempts* over-splitting of thin material (to test restraint
adversarially rather than only confirming it).

## Caveats

- **Single run per case.** No stddev; per-config variance is unknown. Run 3× per case for reliable
  variance before trusting the delta's magnitude.
- **Grading was inline** (main agent against the drafted assertions + direct file inspection), not a
  separate grader subagent. Assertions are objective (file presence, naming, frontmatter, manifest
  link resolution, fixture-diff), so this is low-risk, but a blind grader would be more rigorous.
- **`runs/benchmark.json` metadata** reports `runs_per_configuration: 3` and `<model-name>` —
  those are aggregator defaults, not real; the accurate values are recorded here (1 run, opus-4-8).
