# Agents Guide

Instructions for agents that apply to this entire workspace.

## Ground Rules

### Context Discovery

Before you read, create, change a file, or explore the workspace, gather context efficiently first using 3 simple steps:

1. Read the nearest `README.md` **first** — check the file's own folder, then parent folders.
2. Use its manifest to load **only** the linked docs your task needs.
3. Still need more? Keep going up to the next `README.md`. Otherwise, stop once you know enough.

Do **not** launch Explore/search subagents or run broad `Grep`/`Glob` sweeps before reading the nearest `README.md` — the manifest usually points you straight to the answer, so a blind search wastes tokens and skips the curated entry point.

If two `README.md` files disagree, follow the nearest one. Ignore folders that aren't relevant.


## Git Workflow

Work directly on `main`. No feature branches, no PRs.

- **Commit early, commit often** — small, focused commits with clear messages.
- **Never force-push** `main`.
- **No branches** unless explicitly asked for a risky/experimental change. If you do branch, merge it back and delete the branch promptly.
- **Commit message style**: imperative mood, one-line summary under 72 chars. Add a body paragraph only when the "why" isn't obvious from the summary.

