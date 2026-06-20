# Eval: the "How to Discover Context" rule

Dev-time eval for the always-on **context-discovery rule** that the
[`doc-this`](../../skills/doc-this/) skill installs into a project's top-level
`AGENTS.md`/`CLAUDE.md` (see the skill's
[context-discovery reference](../../skills/doc-this/references/context-discovery.reference.md)).
This is **not a skill** — it measures a behavioral rule. It sits beside the skill
evals and is named `doc-this--context-discovery` (the `--` marks it a doc-this
sub-suite) so it shares the [eval harness conventions](../README.md) without
being mistaken for a skill of its own.

## What it measures

The rule says: *before working in a folder, read its nearest `README.md` **and**
`AGENTS.md` first, follow their pointers, walk up/down as needed, and use those
docs as a map before any blind `Grep`/`Glob`.* `README.md` is orientation;
`AGENTS.md` is the per-folder instructions an agent must follow, and its
nearest-lookup is independent of the README's. The eval asks whether an agent
that has this rule discovers context **more effectively (correctness) and
efficiently (fewer reads/searches)** than one that doesn't — on read-only
questions.

The A/B is *rule present vs absent in the agent's instructions* — **not**
`with_skill`/`without_skill`. The two configs are `with_rule` and `without_rule`.

## How isolation works (the hard part)

This workspace's own `AGENTS.md` already carries the rule, and any agent run
inside the repo inherits it — so an in-repo baseline is contaminated. An
isolation spike (three `claude -p` runs from `$TMPDIR` clean rooms) confirmed two
facts the harness relies on:

1. A `claude -p` run from a `$TMPDIR` cwd does **not** inherit the workspace
   `AGENTS.md` — no rule leaks in.
2. Headless `claude` loads a local **`CLAUDE.md`** but **not** a bare `AGENTS.md`
   (in the real workspace the rule loads only because `CLAUDE.md` does
   `@AGENTS.md`).

So each run is staged in its own clean room **outside the repo** (under
`$TMPDIR`) with a root `CLAUDE.md` that is byte-identical across arms **except**
the rule block:

- `with_rule` → `CLAUDE.md` = neutral preamble + the verbatim rule block.
- `without_rule` → `CLAUDE.md` = the same preamble only.

The rule block is the single controlled variable. A `without_rule` agent that
reads a README by its own default habit is the honest baseline — the metric
captures the rule's *marginal* effect over default behavior.

## Layout

- `evals.json` — 7 read-only cases. Each carries `answer_keywords` (AND-of-ORs),
  optional `answer_forbidden`, a `process` expectation (one check or a list of
  checks that must all pass — `readme_first` | `agents_first` | `fallback_file`),
  a `target_file`, and a `tool_budget`. `agents_first` asserts the nearest
  `AGENTS.md` (= `target_file`) was read before any content access.
- `fixtures/corpus/` — a small committed contextful tree (services + ops) with a
  README map, a **decoy** (`legacy_config.py`, stale retry value the README flags
  as deprecated), a **no-README** folder (`ops/scripts/`), and two `AGENTS.md`
  fixtures: `services/auth/` (an `AGENTS.md` but **no** README — a generated-file
  rule, with `tokens.py`/`token_types.yaml`/`gen_tokens.py` and a docs-free
  `handlers/` subfolder for the walk-up case) and `services/payments/` (**both** a
  README and an `AGENTS.md`, where the binding refund rule lives only in the
  `AGENTS.md`).
- `prepare.py` / `run.py` / `grade.py` — stage, execute, grade (below).
- `benchmarks/` — committed durable record (`iteration-N.md`, `history.md`).
- `runs/` — gitignored scratch (transcripts, per-run grading/timing).

The seven cases, by what they stress:

| case | type | what it probes |
|------|------|----------------|
| `retry-policy-value` | efficiency + trap | answer in nearest README; blind grep also hits the stale decoy |
| `notify-naming-convention` | navigation-up | convention defined in the *parent* README; must walk up |
| `billing-source-of-truth` | correctness-trap | README names the canonical file and flags the decoy as dead |
| `ops-script-purpose` | no-README fallback | folder has no README → must fall back to reading the file |
| `subfolder-agents-no-readme` | AGENTS.md, no README | subfolder has an `AGENTS.md` but no README → read the subfolder `AGENTS.md` *and* walk up to the parent README |
| `payments-refund-constraint` | AGENTS.md trap (README present) | the binding rule lives in `AGENTS.md` even though the folder also has a README |
| `auth-handlers-agents-walkup` | AGENTS.md navigation-up | deeper folder has no `AGENTS.md` → walk up to the nearest parent `AGENTS.md` |

## Running

```bash
# from the repo root
EVAL=agentic/evals/doc-this--context-discovery
python3 $EVAL/prepare.py runs/iteration-1 --runs 2     # stage clean rooms in $TMPDIR
python3 $EVAL/run.py     runs/iteration-1 --jobs 4     # headless read-only executors, capture transcripts
python3 $EVAL/grade.py   runs/iteration-1              # deterministic grading.json + (run.py wrote) timing.json

# aggregate + guard (reuses the shared infra)
AGG=~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py
python3 "$AGG" $EVAL/runs/iteration-1 --skill-name doc-this--context-discovery
python3 agentic/evals/check_benchmark.py $EVAL/runs/iteration-1
```

`run.py` whitelists only `Read,Grep,Glob` — read-only by construction. It captures
each executor's stream-json transcript (the tool-call sequence is the eval's raw
material) and writes a sibling `timing.json`. `grade.py` re-reads those
transcripts, so you can re-grade without re-running executors after a metric
change.

## What the numbers mean

Correctness alone barely separates the arms on a 10-file corpus — both usually
answer right. The rule's measurable effect is in the **process** and
**tool-call count**, plus **correctness on the trap**, where blind grep can latch
onto the stale decoy.

The **process** metric measures the *principle*, not the method: does the agent
**read the folder's docs (the nearest README and, where present, the nearest
`AGENTS.md`) as the entry point before accessing any code/content** (a content
`Grep` or a Read of a non-doc file)? *How* it locates those docs is irrelevant —
globbing `**/README.md` or `**/foo/**` to find the entry point is navigation, not
a violation. README and `AGENTS.md` are measured on independent tracks
(`readme_first`, `agents_first`), so a case can require either or both. (Earlier
iterations used a stricter check that counted any non-README glob as a "blind
search"; that penalized benign glob-then-read navigation and was corrected — see
`benchmarks/iteration-2.md`.)
See [`benchmarks/`](benchmarks/) for results and honest caveats — notably that on
the no-README folder the rule costs *more* (it globs for a map that isn't there),
and that the token sum is cache-read-dominated, so it is not a clean efficiency
signal at this corpus size. Every iteration writeup reports the full metric set for
both arms (pass rate, process, tool calls, and mean time) per the [reporting
contract](../docs/benchmark-contract.reference.md) (§3) — a noisy metric like time
is flagged *directional*, never dropped.
