# Iteration 4 — require the onboarding read be done by the agent, not delegated

- **Date:** 2026-06-24
- **Model:** claude-opus-4-8 (default headless `claude -p`)
- **Configs:** `with_rule` vs `without_rule` (rule block present/absent in the staged `CLAUDE.md`)
- **Runs:** 2 per (case × config) → 28 executors, all read-only (`Read,Grep,Glob`)
- **What changed since iteration 3:** wording only — no new cases or fixtures.
  1. The rule lead-in now says to read the nearest `README.md`/`AGENTS.md` **yourself**
     to onboard — *"ALWAYS … DO NOT delegate"* — closing the gap where an agent
     dispatched a subagent/search to gather the context for it and acted on the
     second-hand digest instead of grounding in the folder's own map.
  2. The fallback bullet now reads *"(Optional) Search with `Find`/`Grep`/`Glob` or
     `Explore` agents as a fallback option"* — filing `Explore` agents explicitly into
     the post-onboarding fallback tier, not the onboarding read.

## Headline

| metric | with_rule | without_rule | delta |
|--------|-----------|--------------|-------|
| pass rate (3 dims/case, 7 cases) | **100.0% (42/42)** | 69.0% (29/42) | **+0.31** |
| correctness | 14/14 | 14/14 | 0 |
| process (docs as entry point) | **14/14 (100%)** | 4/14 (29%) | **+71pp** |
| within tool budget | 14/14 | 11/14 | +3 |
| mean tool calls / task | 3.93 | 5.57 | −1.64 |
| mean wall-clock / task (directional) | 22.5s | 28.3s | −5.8s |
| mean tokens / task (directional, cache-read-dominated) | 94.9k | 67.3k | +27.6k |

The wording change is **measurement-neutral on the grader** by construction — the
new clauses concern delegating to a subagent/`Explore`, and the eval's executor
whitelist is `Read,Grep,Glob` only (no subagent tool), so the delegation behavior
is not exercised here. What this run confirms is the **inverse**: the added wording
does **not** regress the behavior the eval *does* measure. `with_rule` holds at
**100% across all three dimensions** (correctness, process, tool budget), with mean
tool calls (3.93) statistically indistinguishable from iteration 3 (3.71).

## Versus iteration 3 (same fixtures, same n)

| metric (with_rule) | iter-3 | iter-4 | read |
|--------------------|--------|--------|------|
| pass rate | 100% (42/42) | 100% (42/42) | no regression |
| process | 14/14 | 14/14 | no regression |
| mean tool calls | 3.71 | 3.93 | +0.22 — noise at n=2 |
| delta vs baseline | +24pp | +31pp | baseline noisier this run |

The widened delta (+31pp vs +24pp) is **baseline drift, not a rule gain**:
`without_rule` fell to 69.0% from iteration 3's 76.2% on identical fixtures — the
unguided arm is inherently variable run-to-run. The stable signal is `with_rule`
process + correctness holding at 100%.

## Honest caveats

- **The change is untested-by-construction here.** The delegation clause cannot be
  exercised by a `Read,Grep,Glob`-only executor. This run is a **regression check on
  the existing measured behavior**, not validation of the new clause. Coverage for
  "agent declines to delegate the onboarding read" would need a new arm that grants a
  subagent tool and asserts a self-read first — a separate follow-up.
- **Small corpus, correctness saturates.** All arms answer correctly; the
  discriminating signal is **process** + tool budget, as in prior iterations.
- **Tokens** remain cache-read-dominated — directional only; tool calls are the
  cleaner efficiency signal.
- **Time is directional** (high variance at n=2; `without_rule` stddev 16.5s).
  Reported for completeness per the [benchmark contract](../../docs/benchmark-contract.reference.md) §3.
- **n=2.** Treat exact rates as indicative; the headline is "no regression," which the
  100%/100%/100% `with_rule` breakdown supports cleanly.

## Verdict

The wording refinement — *read the docs yourself, do not delegate the onboarding
read; `Explore` is a fallback, not the entry point* — ships with **no regression** on
the behavior this eval measures: `with_rule` stays at **100%** on all three
dimensions with unchanged tool efficiency. The new clause's own behavior (declining
to delegate) is outside this read-only harness's reach and remains an open coverage
item.
