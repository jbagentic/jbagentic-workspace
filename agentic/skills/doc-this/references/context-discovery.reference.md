# Context discovery — reference

The **navigation half** of the Contextful Folder pattern: how an agent should *read*
contextful folders to gather context efficiently — pulling the nearest `README.md` (orientation)
**and** the nearest `AGENTS.md` (instructions it must follow) before working in any folder. The
[guide](contextful-folder.guide.md) and [reference](contextful-folder.reference.md) cover how to
*produce* such folders; this covers how to *consume* them.

This rule is **always-on behavior** — it shapes how an agent gathers context on every task,
not just when documenting. So it belongs in your **always-on agent instructions** — the
top-level `AGENTS.md` or `CLAUDE.md` loaded on every task, the one that applies to every folder
— not in an on-demand skill, and not in any single folder's local `AGENTS.md`. Install the
block below there once.

## The rule (install this)

```md
## How to Discover Context

**Before working in any folder, ALWAYS read its nearest `README.md` and `AGENTS.md` first — read
them to onboard yourself, DO NOT delegate.** Each is either in the folder or in the nearest parent
folder that has one.

- **Read** the README as the onboarding guide to know the context, and the AGENTS.md for the
  instructions you **must** follow while working in the folder.
- **Follow** links in README, if relevant, to read more guides, references, runbooks, or files.
- **Walk** the folder tree to adjust the context boundary — **up** to a parent folder with
  README for broader context, **down** into a subfolder with README for specific context.
- **(Optional) Search** with `Find`/`Grep`/`Glob` or `Explore` agents as a fallback option.

Stop once you know enough context.
```

Adjust the heading level (`##` vs `###`) to fit the host file's structure; keep the
"How to Discover Context" heading so it's easy to detect on re-install.

## Why

Producing contextful folders only pays off if agents navigate by them. Without this rule an
agent falls back to blind `Grep`/`Glob` sweeps — loading too much or missing what's there — and
the READMEs-as-map investment is wasted. See [the guide](contextful-folder.guide.md)
("Why folders?" / selective loading) for the rationale behind up/down progressive disclosure.

The rule says read them *yourself* because delegating the onboarding read to a subagent fails
quietly: the subagent reads the docs and reports a summary back, but the deciding agent never
grounds itself in the folder's own map — it acts on a second-hand digest, and any per-folder
`AGENTS.md` instruction the summary glossed over is silently skipped. A search or `Explore` agent
is a fallback you may reach for after orienting — never the onboarding read itself. (This is
distinct from the `AGENTS.md` auto-load gap below — that one is about the harness not loading the
file at all.)

The rule also covers `AGENTS.md`, not just `README.md`, because no harness reliably auto-loads a
*subfolder's* `AGENTS.md` when an agent touches a file there: Claude Code auto-loads `CLAUDE.md`
(not `AGENTS.md`), and Codex loads a subfolder's `AGENTS.md` only when it is the current working
directory. Only the top-level `AGENTS.md` is dependably in context. So the agent must read the
nearest `AGENTS.md` itself — otherwise the mandatory per-folder instructions it carries are
silently skipped.

## Related

- [Contextful Folder guide](contextful-folder.guide.md) — why the pattern works.
- [Contextful Folder reference](contextful-folder.reference.md) — how to produce contextful folders.
