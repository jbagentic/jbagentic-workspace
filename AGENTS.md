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


## Git Workflow

Work directly on `main`. No feature branches, no PRs.

- **Commit early, commit often** — small, focused commits with clear messages.
- **Never force-push** `main`.
- **No branches** unless explicitly asked for a risky/experimental change. If you do branch, merge it back and delete the branch promptly.
- **Commit message style**: imperative mood, one-line summary under 72 chars. Add a body paragraph only when the "why" isn't obvious from the summary.

