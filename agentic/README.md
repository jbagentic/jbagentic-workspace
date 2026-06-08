# agentic

The agent capabilities for this workspace: the **skills** agents invoke, and the **evals**
that measure those skills. If you're looking for what an agent can do here, or how its
quality is tracked over time, this is the folder.

## What's here

- **Skills** are the reusable capabilities an agent loads and runs — each is a self-contained
  folder describing when to trigger it and how to carry it out.
- **Evals** are dev-time test suites that exercise a skill against fixtures and record how it
  performs across iterations. They're for building and improving skills, not run at agent time.

## Structure

| Folder | What it holds |
|--------|---------------|
| [`skills/`](skills/) | The skill library — one folder per skill, each with a `SKILL.md` (plus optional `references/` or `scripts/`). This is the canonical location; the repo's `.claude/skills` is a symlink to here, so installed skills and their source are the same files. |
| [`evals/`](evals/) | Dev-time eval specs and committed benchmarks, one folder per skill under test. See [`evals/README.md`](evals/README.md) for the layout and the run → promote → history workflow. |

## Authoring

Skills are authored with the **skill-creator** skill and conformed to the workspace house
style. See the root [`AGENTS.md`](../AGENTS.md) and
[`docs/skill-convention.reference.md`](../docs/skill-convention.reference.md) for the rules.
