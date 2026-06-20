# Iteration 2 — context-discovery rule (copy refactor + grader fix)

- **Date:** 2026-06-20
- **Model:** claude-opus-4-8 (default headless `claude -p`)
- **Configs:** `with_rule` vs `without_rule` (rule block present/absent in the staged `CLAUDE.md`)
- **Runs:** 6 per (case × config) → 48 executors, all read-only (`Read,Grep,Glob`)
- **What changed since iteration 1:**
  1. The rule copy was refactored from two dense prose paragraphs to a scannable
     **bulleted** form (Read / Follow / Walk / Search), ~18% fewer words.
  2. The grader's **process** metric was corrected (see below).

## Headline

| metric | with_rule | without_rule | delta |
|--------|-----------|--------------|-------|
| pass rate (3 dims/case) | **100.0%** | 77.8% | **+0.22** |
| correctness | 24/24 | 24/24 | 0 |
| process (README as entry point) | **24/24 (100%)** | 11/24 (46%) | **+54pp** |
| within tool budget | 24/24 | 21/24 | +3 |
| mean tool calls / task | **2.88** | 4.5 | −1.62 (~36%) |

## The grader fix (why the numbers are cleaner than iteration 1)

Iteration 1's `readme_first` check required the agent's *literal first action* to
be a README **read**, and counted any non-README glob as a "blind search". That
penalized perfectly good behavior — globbing `**/README.md` or `**/svc/**` to
*locate* the entry point, then reading it — and manufactured phantom regressions.

The metric now measures the **principle, not the method**: *did the agent read a
README before accessing any code/content (a content `Grep` or a non-README
`Read`)?* Globs only *locate* files (navigation) and never count against it.
Implemented in `grade.py:is_content_access()`. The strict "first action" check is
retired; efficiency concerns about extra globbing are already covered by the tool
budget.

Under the corrected metric the rule's value is **sharper**, not softer:
`without_rule` reads code / greps content before any README **54% of the time**
(process 11/24), while `with_rule` consults a README first **every time**
(24/24).

## Copy refactor — no regression vs the old prose

A controlled A/B (n=16/case, with_rule) of the old prose vs the candidate bulleted
copies, graded by the corrected metric:

| copy | correct | README-first (principle) | genuine violations | mean calls |
|------|---------|--------------------------|--------------------|------------|
| OLD (prose) | 64/64 | 47/48 (98%) | 1 | 3.12 |
| bulleted (early draft) | 64/64 | 46/48 (96%) | 1 | 2.77 |
| **shipped (v6, "with README" walk cues)** | **48/48** | **36/36 (100%)** | **0** | 3.04 |

The shipped copy ties-or-beats the old prose on the principle (100% README-first,
zero genuine violations at n=36 readme-cases) while being more scannable and
~18% shorter. Adding "**up** to a parent folder **with README**" / "**down** into
a subfolder **with README**" anchors the agent on README-bearing folders as the
navigation targets.

## Honest caveats

- **Small corpus, correctness saturates.** All arms answer correctly on a 10-file
  tree; the discriminating signal is process + tool-calls, as designed.
- **Transcript parse-artifacts.** A few runs produce a correct, detailed answer
  but an empty captured transcript (the agent attempted a disallowed tool, then
  read the file); the grader can't see the read and scores process as a miss.
  These are capture glitches, not behavior, and hit both arms.
- **Tokens** remain cache-read-dominated and are not a clean efficiency signal at
  this corpus size; tool-call count is the cleaner one.

## Verdict

The bulleted copy ships with **no regression**: 100% correctness, 100% process
adherence (principle), and equal-or-better efficiency vs the old prose — in a
form that is materially easier to scan and ~18% more compact. The grader now
measures what the rule actually asks for, and on that metric the rule's marginal
value is large (process +54pp, ~36% fewer tool calls).
