# Agents Guide

## Ground Rules

### Context Discovery

Before you read, create, or change a file, gather context in this order and stop once you know enough:

1. Read the nearest `README.md` — check the file's own folder first, then parent folders.
2. Read any docs it links to that relate to your task.
3. Still need more? Keep going up to the next `README.md` files.

If two `README.md` files disagree, follow the nearest one. Ignore folders that aren't relevant.


## Authoring skills

When creating, editing, or improving any skill in `skills/`:

1. Use the **skill-creator** skill to drive the process (drafting, evals, iteration).
2. Conform the resulting `SKILL.md` to this project's house style in
   [`docs/skill-convention.reference.md`](docs/skill-convention.reference.md) —
   it governs structure and rules; skill-creator governs the workflow. On conflict, follow the reference file for the final shape of the file.

**Skill evals live outside the skill folder**, at `agentic/evals/<skill-name>/` so they never ship in the installed `.skill`. Check `agentic/evals/` for how that folder is organized and the run → promote → history workflow.
