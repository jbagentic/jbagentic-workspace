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

Whoever changes what's in a Contextful Folder should update its contextual information, so its docs stay accurate. This is a default you apply with judgment, not a hard rule — skip it when it doesn't fit (a throwaway experiment, or docs deliberately left for someone else).

When you add, remove, rename, or change files, the docs that describe them live in the **nearest Contextful Folder** — the nearest enclosing folder with a `README.md`. That may be the file's own folder or a parent, since not every folder has its own docs and some are left to a parent on purpose. After a change, find that folder and update its `README.md` (and any `AGENTS.md` or `docs/*`) in the same pass:

- **New entry the README should list** → add it with a one-line description.
- **Removed or renamed entry** → drop or fix its line in the README.
- **Changed behavior** → update the doc that describes it.

Keep it **just enough** — update only what your change affected. Don't over-document, and don't add a README to a folder that's meant to rely on its parent. For a bigger reorganization, or a folder with no docs yet, use the `doc-this` skill instead of editing by hand.


## Git Workflow

Work directly on `main`. No feature branches, no PRs.

- **Commit early, commit often** — small, focused commits with clear messages.
- **Never force-push** `main`.
- **No branches** unless explicitly asked for a risky/experimental change. If you do branch, merge it back and delete the branch promptly.
- **Commit message style**: imperative mood, one-line summary under 72 chars. Add a body paragraph only when the "why" isn't obvious from the summary.

