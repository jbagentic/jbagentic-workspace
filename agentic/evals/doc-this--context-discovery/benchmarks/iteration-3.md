# Iteration 3 — extend the rule to the nearest `AGENTS.md`

- **Date:** 2026-06-20
- **Model:** claude-opus-4-8 (default headless `claude -p`)
- **Configs:** `with_rule` vs `without_rule` (rule block present/absent in the staged `CLAUDE.md`)
- **Runs:** 2 per (case × config) → 28 executors, all read-only (`Read,Grep,Glob`)
- **What changed since iteration 2:**
  1. The rule now tells agents to read the nearest **`AGENTS.md`** (per-folder
     instructions they must follow) in addition to the nearest `README.md`. This
     closes a real harness gap: neither Claude Code nor Codex reliably auto-loads
     a *subfolder's* `AGENTS.md`, so the agent must read it itself.
  2. Three new cases + fixtures exercise that behavior (see below).
  3. The grader gained an independent **`agents_first`** track and `process` can
     now be a list of checks (all must pass). `AGENTS.md` is treated as a
     discovery doc like `README.md` in `is_content_access()`.

## Headline

| metric | with_rule | without_rule | delta |
|--------|-----------|--------------|-------|
| pass rate (3 dims/case, 7 cases) | **100.0% (42/42)** | 76.2% (32/42) | **+0.24** |
| correctness | 14/14 | 14/14 | 0 |
| process (docs as entry point) | **14/14 (100%)** | 6/14 (43%) | **+57pp** |
| within tool budget | 14/14 | 12/14 | +2 |
| mean wall-clock / task (directional) | 20.2s | 25.9s | −5.7s |

### The new `AGENTS.md` cases (the point of this iteration)

| metric (3 new cases) | with_rule | without_rule | delta |
|----------------------|-----------|--------------|-------|
| correctness | 6/6 | 6/6 | 0 |
| process (`agents_first` ± `readme_first`) | **6/6 (100%)** | **1/6 (17%)** | **+83pp** |
| within tool budget | 6/6 | 5/6 | +1 |
| mean tool calls / task | 4.67 | 5.33 | −0.66 |

The rule's marginal value is exactly where the harness gap is: without it, agents
discover the nearest `AGENTS.md` correctly only **1 time in 6**; with it, **every
time**. The four README-only cases show no regression (`with_rule` 8/8 all dims;
unchanged from iterations 1–2).

## The three new cases

| case | fixture shape | what it proves |
|------|---------------|----------------|
| `subfolder-agents-no-readme` | `services/auth/` has an `AGENTS.md` but **no** README | the two artifacts resolve independently — agent reads the subfolder `AGENTS.md` **and** walks up to the parent README (`process: [agents_first, readme_first]`) |
| `payments-refund-constraint` | `services/payments/` has **both** a README and an `AGENTS.md`; the binding rule is only in the `AGENTS.md` | agent reads the `AGENTS.md` even when a README is present (the Claude Code failure mode) |
| `auth-handlers-agents-walkup` | `services/auth/handlers/` has no docs of its own | agent walks **up** to the nearest parent `AGENTS.md` — the mirror of README walk-up |

### How `without_rule` fails each (process)

- **no-readme:** agents land in `services/auth/`, read its `AGENTS.md` (the
  question names the folder), but never walk up to the parent README — so the
  composite `agents_first + readme_first` fails (read content before any README).
- **walkup:** agents read `handlers/refresh.py` and grep/read the token files
  directly, never walking up to `services/auth/AGENTS.md` — `agents_first` fails.
- **readme-present:** one run read the `AGENTS.md` before content (passed), the
  other read the README + code first and reached the `AGENTS.md` only after —
  `agents_first` fails. The rule makes this reliable.

## Honest caveats

- **Small corpus, correctness saturates.** All arms answer correctly — the answer
  files (`token_types.yaml`, `gen_tokens.py`, `refunds.py`) are findable by grep,
  so a `without_rule` agent can stumble onto the right answer without reading the
  `AGENTS.md`. The discriminating signal is **process** (did it consult the
  mandatory instructions doc) + tool budget, as designed. In the wild, an
  `AGENTS.md` rule the agent never reads is silently violated even when the
  "answer" looks right — which is exactly what the process metric captures.
- **Two-doc cases cost more reads.** A rule-following agent reads both the nearest
  README and `AGENTS.md`; `subfolder-agents-no-readme`'s budget is 7 (vs 6
  elsewhere) to reflect that. Still cheaper on average than `without_rule`'s blind
  searching (4.67 vs 5.33 mean calls on the new cases).
- **Tokens** remain cache-read-dominated and are not a clean efficiency signal at
  this corpus size; tool-call count is the cleaner one.
- **Time is directional.** 20.2s vs 25.9s tracks the tool-call gap but is
  executor/environment-variance-prone at n=2; reported for completeness, don't
  over-read it — tool calls are the cleaner efficiency signal.
- **n=2.** Smaller than iteration 2's n=6; the process gap is large enough
  (+83pp on the new cases) to read clearly, but treat the exact rates as
  indicative.

## Verdict

Extending the rule to the nearest `AGENTS.md` ships with **no regression** on the
README cases and a **large, clean gain** on the new ones: `with_rule` consults the
mandatory per-folder instructions **100%** of the time vs **17%** without. The
grader now measures each discovery artifact on its own track, so the eval
faithfully reflects what the extended rule asks for.
