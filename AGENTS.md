# Agents Guide

Instructions for agents that apply to this entire workspace.

## Ground Rules

### Efficient Context Discovery

A folder is a context boundary, and its `README.md` is the entry point that orients you to what's inside. When you need context, start from the README nearest your task and let it point you to what's worth reading — not just other READMEs, but whatever it links: reference docs, skill files, code.

From there, navigate by context rather than by search:

- Need **broader** context? Go *up* the parent folders.
- Need **more specific** context? Go *down* into subfolders.
- Stop once you know enough.

READMEs are the curated map, so reach for them before a blind `Find`/`Grep`/`Glob` sweep — searching first wastes tokens and skips the map. If the trail doesn't cover what you need, then search.

### Keeping Context Current

When you change what's in a Contextful Folder, update its docs at the same time — a default you apply with judgment, not a hard rule.

- **Why** — the next agent or person relies on those docs and can't ask you later; if the docs are out of date, they get it wrong.
- **Which docs** — the nearest Contextful Folder's: the nearest folder with a `README.md`, which is your file's own folder or, more often, a parent.
- **If you're unsure what to change** — ask the `doc-this` skill to update the docs for you.


## Git Workflow

Work directly on `main`. No feature branches, no PRs.

- **Commit early, commit often** — small, focused commits with clear messages.
- **Never force-push** `main`.
- **No branches** unless explicitly asked for a risky/experimental change. If you do branch, merge it back and delete the branch promptly.
- **Commit message style**: imperative mood, one-line summary under 72 chars. Add a body paragraph only when the "why" isn't obvious from the summary.

