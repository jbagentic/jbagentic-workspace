# Context maintenance — reference

The **maintenance half** of the Contextful Folder pattern: how to keep contextful folders
current as their contents change. The [guide](contextful-folder.guide.md) and
[reference](contextful-folder.reference.md) cover how to *produce* such folders;
[context-discovery](context-discovery.reference.md) covers how to *read* them; this covers how
to *keep them true* once they exist.

This rule is **always-on behavior** — it shapes what an agent does after changing files on any
task, not just when documenting. So it belongs in your **always-on agent instructions** — the
top-level `AGENTS.md` or `CLAUDE.md` loaded on every task, the one that applies to every folder
— not in an on-demand skill, and not in any single folder's local `AGENTS.md`. Install the
block below there once.

## The rule (install this)

```md
## Context Maintenance Rule

When you change what's in a Contextful Folder, update its docs at the same time.

- **Why** — the next agent or person depends on those docs and can't ask you later; if the docs are stale, they get it wrong.
- **Which docs** — the nearest Contextful Folder's: the closest folder with a `README.md`, which is your file's own folder or, more often, a parent.
- **If you're unsure what to change** — ask the `doc-this` skill to update the docs for you.
```

Adjust the heading level (`##` vs `###`) to fit the host file's structure; keep the
"Context Maintenance Rule" heading so it's easy to detect on re-install.

## Why

Docs are the context the next reader works from, and they can't tap the author on the shoulder.
When a folder's contents change but its docs don't, the reader works from wrong context — agents
do the task in ways that weren't intended, humans miss constraints, and in the worst case the
work has to be redone. See [the guide](contextful-folder.guide.md) ("Too little context") for
the cost of stale or missing context. Keeping docs current in the same pass as the change is how
the producing investment keeps paying off instead of decaying.

## Related

- [Contextful Folder guide](contextful-folder.guide.md) — why the pattern works.
- [Contextful Folder reference](contextful-folder.reference.md) — how to produce contextful folders.
- [Context discovery reference](context-discovery.reference.md) — the navigation half: how to read contextful folders.
