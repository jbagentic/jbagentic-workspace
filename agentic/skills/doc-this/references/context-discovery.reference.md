# Context discovery — reference

The **navigation half** of the Contextful Folder pattern: how an agent should *read*
contextful folders to gather context efficiently. The [guide](contextful-folder.guide.md) and
[reference](contextful-folder.reference.md) cover how to *produce* such folders; this covers
how to *consume* them.

This rule is **always-on behavior** — it shapes how an agent gathers context on every task,
not just when documenting. So it belongs in your **always-on agent instructions** — the
top-level `AGENTS.md` or `CLAUDE.md` loaded on every task, the one that applies to every folder
— not in an on-demand skill, and not in any single folder's local `AGENTS.md`. Install the
block below there once.

## The rule (install this)

```md
## Context Discovery Rule

A folder is a context boundary, and its `README.md` is the front door that tells you what's
inside. When you need context, start from the README closest to your task and follow where it
points — not just other READMEs, but anything it links: reference docs, skill files, code.

From there, follow the context instead of searching:

- Need **broader** context? Go *up* to the parent folders.
- Need **more specific** context? Go *down* into the subfolders.
- Stop once you know enough.

READMEs are the map, so use them before a blind `Find`/`Grep`/`Glob` sweep — searching first
wastes tokens and skips the map. If the trail doesn't cover what you need, then search.
```

Adjust the heading level (`##` vs `###`) to fit the host file's structure; keep the
"Context Discovery Rule" heading so it's easy to detect on re-install.

## Why

Producing contextful folders only pays off if agents navigate by them. Without this rule an
agent falls back to blind `Grep`/`Glob` sweeps — loading too much or missing what's there — and
the READMEs-as-map investment is wasted. See [the guide](contextful-folder.guide.md)
("Why folders?" / selective loading) for the rationale behind up/down progressive disclosure.

## Related

- [Contextful Folder guide](contextful-folder.guide.md) — why the pattern works.
- [Contextful Folder reference](contextful-folder.reference.md) — how to produce contextful folders.
