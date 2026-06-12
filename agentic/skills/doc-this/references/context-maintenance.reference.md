# Documenting a folder — reference

The **documenting half** of the Contextful Folder pattern: route a folder's documentation work to
the `doc-this` skill, and keep that documentation current as the folder changes. The
[guide](contextful-folder.guide.md) and [reference](contextful-folder.reference.md) cover the file
vocabulary a documented folder uses; [context-discovery](context-discovery.reference.md) covers how
to *read* such folders; this covers how to *write them and keep them true*.

This rule is **always-on behavior** — it shapes what an agent does whenever it documents a folder or
changes one's contents on any task, not only on an explicit documentation request. So it belongs in
your **always-on agent instructions** — the top-level `AGENTS.md` or `CLAUDE.md` loaded on every
task, the one that applies to every folder — not in an on-demand skill, and not in any single
folder's local `AGENTS.md`. Install the block below there once.

## The rule (install this)

```md
## Documenting a Folder

Use the `doc-this` skill for a folder's docs — don't hand-write them.

- **Creating or organizing docs** — turning notes, a brain-dump, or scattered materials into a `README.md` / `AGENTS.md` / typed `docs/*.{guide|reference|runbook}.md`, or a brief aside like "doc this" / "document the references" / "write this up" → run `doc-this`.
- **Keeping docs current** — when you change what's in a Contextful Folder, update its docs in the same pass: the nearest folder with a `README.md`. If you're unsure what to change, ask `doc-this` to reconcile them.
- **Why** — the next agent or person works from these docs and can't ask you later; stale or missing docs make them get it wrong.
```

Adjust the heading level (`##` vs `###`) to fit the host file's structure; keep the
"Documenting a Folder" heading so it's easy to detect on re-install.

## Why

Producing contextful folders only pays off when the docs are written well and stay true — and both
halves route through one skill. Sending documentation work to `doc-this` keeps every folder on the
same small file vocabulary instead of ad-hoc, hand-written docs that drift from the pattern. And when
a folder's contents change but its docs don't, the next reader works from wrong context — agents do
the task in ways that weren't intended, humans miss constraints, and in the worst case the work has
to be redone. See [the guide](contextful-folder.guide.md) ("Too little context") for the cost of
stale or missing context. Documenting in the same pass as the change is how the producing investment
keeps paying off instead of decaying.

## Related

- [Contextful Folder guide](contextful-folder.guide.md) — why the pattern works.
- [Contextful Folder reference](contextful-folder.reference.md) — how to produce contextful folders.
- [Context discovery reference](context-discovery.reference.md) — the navigation half: how to read contextful folders.
</content>
</invoke>
