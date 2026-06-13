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
## How to Discover Context

A `README.md` marks a context boundary; it's the onboarding guide to what's inside and how to
work there. Not every folder has one — a folder without a README is covered by the nearest
README above it. Start from the README nearest your task and follow where it points — linked
guides, references, runbooks, and code. Then walk the tree: **up** to a parent for broader
context, **down** to the next folder that has its own README for specifics. Stop once you know
enough.

Use READMEs as a map before any blind `Find`/`Grep`/`Glob` search; search only when the map
runs out.
```

Adjust the heading level (`##` vs `###`) to fit the host file's structure; keep the
"How to Discover Context" heading so it's easy to detect on re-install.

## Why

Producing contextful folders only pays off if agents navigate by them. Without this rule an
agent falls back to blind `Grep`/`Glob` sweeps — loading too much or missing what's there — and
the READMEs-as-map investment is wasted. See [the guide](contextful-folder.guide.md)
("Why folders?" / selective loading) for the rationale behind up/down progressive disclosure.

## Related

- [Contextful Folder guide](contextful-folder.guide.md) — why the pattern works.
- [Contextful Folder reference](contextful-folder.reference.md) — how to produce contextful folders.
