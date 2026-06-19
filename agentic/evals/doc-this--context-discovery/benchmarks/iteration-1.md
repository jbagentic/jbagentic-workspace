# Iteration 1 — context-discovery rule

- **Date:** 2026-06-19
- **Model:** claude-opus-4-8 (default headless `claude -p`)
- **Configs:** `with_rule` vs `without_rule` (rule block present/absent in the staged `CLAUDE.md`)
- **Runs:** 2 per (case × config) → 16 executors, all read-only (`Read,Grep,Glob`)
- **Isolation:** each run staged in its own `$TMPDIR` clean room; rule block is the only variable.

## Headline

| metric | with_rule | without_rule | delta |
|--------|-----------|--------------|-------|
| pass rate (3 dims/case) | **100.0%** | 83.3% | **+0.17** |
| mean tool calls / task | **3.25** | 4.62 | −1.37 |
| mean wall-clock / task | 16.8s | 26.1s | −9.3s (variance-prone) |
| mean tokens / task | 98.6k | 57.4k | **+41k** (see caveat) |

Pass rate aggregates three per-case dimensions: **correctness**, **process**
(README-first or graceful fallback), and **within tool budget**.

## What actually separated the arms

**Not correctness.** All 16 runs reached the correct answer — a 10-file corpus is
answerable by blind search too. Correctness was equal; the rule's value showed
elsewhere.

**Process + efficiency.** `without_rule` repeatedly grepped *before* consulting
the README map, which (a) failed the README-first expectation and (b) cost more
calls. Mean tool calls per task, with / without:

| case | with_rule | without_rule |
|------|-----------|--------------|
| retry-policy-value | 3.0 | 5.0 |
| notify-naming-convention | 3.0 | 5.0 |
| billing-source-of-truth (trap) | **3.0** | **7.0** |
| ops-script-purpose (no README) | 4.0 | **1.5** |

**The trap bit once.** `without_rule` billing-source-of-truth run-2 grepped, glob'd,
and scored 1/3 — the only run that missed process *and* budget. `with_rule` read
`billing/README.md`, which names `settings.py` as canonical and flags
`legacy_config.py` as dead, every time.

## Honest caveats

- **No-README case favors `without_rule`.** On `ops/scripts/` (no README), the
  rule made the agent glob for a map that doesn't exist (4 calls) while the
  baseline read the script directly (1.5). The rule degrades *gracefully* (it
  still answered correctly) but it is **not free** when there's no map. This is a
  real cost, not noise.
- **Tokens are not a clean efficiency signal here.** `with_rule`'s higher token
  sum is dominated by `cache_read_input_tokens`: reading the README chain adds
  context that is re-read (cached) across turns. On a tiny corpus, blind grep is
  cheap, so the rule's at-scale benefit (not loading too much, not missing what's
  there) is *understated*. Tool-call count is the cleaner signal at this size.
- **Time is directional.** 16.8s vs 26.1s tracks the tool-call gap but is
  executor/environment-variance-prone at n=2; don't over-read it.
- **Small n, small corpus.** Single small fixture, 2 runs/config. Treat deltas as
  directional. The design's discriminating power lives in the trap and the
  no-README case; a larger/deeper corpus would widen the tool-call gap.

## Verdict

The rule holds correctness, cuts tool calls on README-covered tasks (most on the
trap, 3 vs 7), and degrades gracefully where no README exists — at a real cost on
that no-README path. Process adherence (README-first) is the cleanest separator;
token cost is not a win at this corpus size and is reported as such.
