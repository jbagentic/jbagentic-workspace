# Agents Guide

## Ground Rules

### Context Discovery

Before you read, create, or change a file, gather context in this order and stop once you know enough:

1. Read the nearest `README.md` — check the file's own folder first, then parent folders.
2. Read any docs it links to that relate to your task.
3. Still need more? Keep going up to the next `README.md` files.

If two `README.md` files disagree, follow the nearest one. Ignore folders that aren't relevant.


## Git Workflow

Work directly on `main`. No feature branches, no PRs.

- **Commit early, commit often** — small, focused commits with clear messages.
- **Never force-push** `main`.
- **No branches** unless explicitly asked for a risky/experimental change. If you do branch, merge it back and delete the branch promptly.
- **Commit message style**: imperative mood, one-line summary under 72 chars. Add a body paragraph only when the "why" isn't obvious from the summary.


## Authoring skills

When creating, editing, or improving any skill in `skills/`:

1. Use the **skill-creator** skill to drive the process (drafting, evals, iteration).
2. Conform the resulting `SKILL.md` to this project's house style in
   [`docs/skill-convention.reference.md`](docs/skill-convention.reference.md) —
   it governs structure and rules; skill-creator governs the workflow. On conflict, follow the reference file for the final shape of the file.

**Skill evals live outside the skill folder**, at `agentic/evals/<skill-name>/` so they never ship in the installed `.skill`. Check `agentic/evals/` for how that folder is organized and the run → promote → history workflow.
