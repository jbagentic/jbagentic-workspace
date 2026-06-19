# Eval: the "How to Document Context" rule

Dev-time eval for the always-on **context-maintenance rule** that the
[`doc-this`](../../skills/doc-this/) skill installs into a project's top-level
`AGENTS.md`/`CLAUDE.md` (see the skill's
[context-maintenance reference](../../skills/doc-this/references/context-maintenance.reference.md)).
This is **not a skill** — it measures a behavioral rule. It sits beside the skill
evals and is named `doc-this--context-maintenance` (the `--` marks it a doc-this
sub-suite) so it shares the [eval harness conventions](../README.md) without being
mistaken for a skill of its own. It is the write-side companion to
[`doc-this--context-discovery`](../doc-this--context-discovery/) (the read side).

## What it measures

The rule says: *changing a folder's contents → update the docs that cover it in the
same pass — the folder's own README, or the nearest one above if it has none.* Its
real failure mode is **omission under task focus**: the agent makes the code change
and forgets the doc. So this eval is **action-based** — each case asks the agent to
make a real code change, and grading inspects whether it **also reconciled the
covering doc**. The question is whether an agent that has this rule keeps docs true
after a change more reliably than one that doesn't.

The A/B is *rule present vs absent in the agent's instructions* — **not**
`with_skill`/`without_skill`. The two configs are `with_rule` and `without_rule`.

## Why this isn't read-only (and why the skill is in the room)

Discovery is a read behavior, so its eval is read-only and grades an answer string.
Maintenance is a **write** behavior, so two things differ:

1. **Write-enabled executors.** `run.py` whitelists `Read,Edit,Write,Grep,Glob,Skill`
   (and `--disallowedTools Bash`). The agent mutates the staged corpus; `grade.py`
   reads the mutated files back from the clean room. Mutations are contained — each
   room is a throwaway `$TMPDIR` copy.
2. **doc-this is copied into BOTH arms.** The rule literally routes doc work to
   doc-this, and in the real world the skill is always present. So a hermetic
   **copy** (not a symlink — a write-enabled agent must not reach the real skill)
   is staged at `<room>/.claude/skills/doc-this/` in both arms. The skill is held
   constant; the **rule block is the only variable**. A `without_rule` agent that
   reconciles docs by its own default habit (or nudged by the skill's mere presence)
   is the honest baseline — the metric captures the rule's *marginal* effect.

### Skill-discoverability spike (green)

A copied skill is only useful if headless `claude -p` can find and invoke it. A
spike confirmed it: a `$TMPDIR` room with `.claude/skills/doc-this/` copied in, run
with `--allowedTools "…,Skill"`, produced a real `Skill` → `{"skill":"doc-this"}`
tool_use (returncode 0, no "unknown skill" markers); the agent applied the code
change and reconciled the README, and the "use doc-this, don't hand-write" line did
**not** suppress the reconcile. (A `Bash` tool_use was attempted despite not being
whitelisted — denied/no-op — so `run.py` also passes `--disallowedTools Bash`.)

## Isolation

This workspace's own `AGENTS.md` already carries the rule, so an in-repo run is
contaminated. As in the discovery eval, each run is staged in a clean room
**outside the repo** (`$TMPDIR`) with a root `CLAUDE.md` that is byte-identical
across arms **except** the rule block:

- `with_rule` → `CLAUDE.md` = neutral preamble + the verbatim rule block.
- `without_rule` → `CLAUDE.md` = the same preamble only.

A headless `claude -p` from a `$TMPDIR` cwd does not inherit the workspace
`AGENTS.md`, and loads a local `CLAUDE.md` but not a bare `AGENTS.md`.

## Layout

- `evals.json` — 5 action cases spanning the doc-this file vocabulary. Each carries
  `change_file`/`change_keywords` (the code change landed), `doc_file` (the covering
  doc), `doc_must_exist` (for create-a-doc cases), `doc_required` (AND-of-ORs),
  `doc_forbidden` (stale fact gone), an optional `secondary_doc` (recorded metric),
  and a `tool_budget`.
- `fixtures/corpus/` — a small committed contextful tree (services with READMEs, a
  typed `docs/*.reference.md`, a README file-manifest, and an undocumented
  sub-folder whose behavior is documented in its parent).
- `prepare.py` / `run.py` / `grade.py` — stage (corpus + skill copy + rule block),
  execute (write-enabled), grade (read mutated rooms).
- `benchmarks/` — committed durable record (`iteration-N.md`, `history.md`).
- `runs/` — gitignored scratch (transcripts, per-run grading/timing).

The five cases, by which doc the change makes stale:

| case | type | task → reconcile target |
|------|------|-------------------------|
| `modify-reference-in-doc` | modify feature, ref in `docs/*` | retry 3→5 → update `billing/docs/retry.reference.md` |
| `refactor-update-manifest` | refactor file structure | split a file → update the `## Files` manifest in `auth/README.md` |
| `add-function-update-readme` | add fn under sub-module | add `send_push` → update `notify/README.md` (+ a new `docs/*`, secondary) |
| `new-module-create-readme` | add brand-new module | create `audit/audit.py` → **create** `audit/README.md` (+ parent manifest row, secondary) |
| `parent-doc-reconcile` | change in undocumented sub-folder | capture timeout 10→30 → update the **parent** `billing/README.md` |

## Running

```bash
# from the repo root
EVAL=agentic/evals/doc-this--context-maintenance
python3 $EVAL/prepare.py runs/iteration-1 --runs 2          # stage clean rooms + skill copy in $TMPDIR
python3 $EVAL/run.py     runs/iteration-1 --jobs 5          # write-enabled headless executors
python3 $EVAL/grade.py   runs/iteration-1                   # reads mutated rooms → grading.json

# aggregate + guard (reuses the shared infra)
AGG=~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py
python3 "$AGG" $EVAL/runs/iteration-1 --skill-name doc-this--context-maintenance
python3 agentic/evals/check_benchmark.py $EVAL/runs/iteration-1
```

`grade.py` reads files from each run's `work_dir` (recorded in `seed.json`), so it
can re-grade without re-running executors after a metric change — **as long as the
clean rooms still exist** in `$TMPDIR` (re-run `prepare.py`+`run.py` if they were
cleaned).

## What the numbers mean

The headline dimension is **reconcile** — did the covering doc get kept true in the
same pass. Correctness (did the change land) and efficiency (tool budget) are the
supporting dimensions, parallel to the discovery eval's correctness/process/
efficiency. See [`benchmarks/`](benchmarks/) for results and caveats — including
whether the rule's "use doc-this" wording helped or hurt in the skill-present room,
and that with-skill invocations inflate tool counts (so the efficiency budget is
deliberately generous and not a clean signal).
