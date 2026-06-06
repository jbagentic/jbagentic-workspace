---
name: agentic-workspace
description: >-
  Set up and maintain a cross-agent project knowledge base: a token-efficient,
  file-based convention that any coding agent (Claude Code, Codex, Cursor, Gemini
  CLI, OpenCode) can consume on demand. Use when scaffolding a project, deciding
  where a doc belongs, adding or conforming a knowledge file, choosing concept vs
  reference vs decision, deciding where to store a skill, or regenerating the
  manifest — even without the words "knowledge base" (e.g. "where should this doc
  go", "how do I document this for the agent", "add this to the project knowledge",
  "make our docs work across Cursor and Codex", "set up AGENTS.md").
---

# Agentic Workspace

A project knowledge base that is **read by coding agents on demand**, stays human-reviewable, and works **identically across agent tools** because the source of truth is plain Markdown plus one canonical `AGENTS.md`.

The model in one line:

- **Atomic, typed knowledge files** + a **generated manifest** that dispatches them on demand.
- The **human** owns the knowledge and the review; the **agent** owns the formatting; the **PR** is the trust boundary.
- Optimize the always-in-context surface (the manifest) hard; load everything else only when its trigger fires.

Where things live:

- **Rules** — [`references/conventions.reference.md`](references/conventions.reference.md)
- **Templates** — [`assets/`](assets/)
- This file says **which action to run when**; read the reference for the exact rule a step needs.

## Pick the action

| When | Action |
|---|---|
| First setting up a project | [Scaffold](#scaffold-a-project) |
| Documenting facts/specs to look up | [Add a knowledge atom](#add-or-update-a-knowledge-atom) → `.reference.md` |
| Documenting how/what something works | [Add a knowledge atom](#add-or-update-a-knowledge-atom) → `.concept.md` |
| Recording why we chose X | [Record a decision](#record-a-decision) |
| Adding a procedure to the project | [Place a skill](#place-a-skill) |
| Changed anything under `knowledge/` | [Regenerate the manifest](#regenerate-the-manifest) |

## Scaffold a project

- Create the workspace structure (see [Structure](references/conventions.reference.md#structure--workspace--optional-projects)) — add the optional `projects/` level only if there's more than one context:
  - `AGENTS.md` at the repo **root** — hand-written rules + an empty manifest block. This is the canonical file every agent converges on.
  - `knowledge/` (+ `decisions/`), `skills/`.
- **Make each agent auto-load it at session start** (see [Cross-agent compatibility](references/conventions.reference.md#cross-agent-compatibility)). Each agent auto-loads its *own* root entry file every session, so give each agent in use a root entry that resolves to `AGENTS.md`:
  - **Claude Code** — add a root `CLAUDE.md` containing the single line `@AGENTS.md` (preferred; Claude expands the import and you can add Claude-only lines below). Claude Code does **not** read `AGENTS.md` directly — without this shim it loads zero instructions, silently.
  - **Codex / Cursor / Windsurf / OpenCode** — read root `AGENTS.md` as-is; nothing to do.
  - **Gemini CLI** — add a `GEMINI.md` pointer to `AGENTS.md`.
- Copy from `assets/`.
- Do **not** pre-create empty knowledge files or subject folders — stay flat until a subject earns a folder (see [Filenames & folders](references/conventions.reference.md#filenames--folders)).

## Add or update a knowledge atom

1. **Create vs update** (see [Atomicity](references/conventions.reference.md#atomicity--the-create-vs-update-decision)): same retrieval intent as an existing file → update in place; new independently-loaded topic → new file.
2. **Type + suffix** (see [File types](references/conventions.reference.md#file-types--one-type-per-file)): look-up facts/specs/snippets → `.reference.md`; understand what/how → `.concept.md`.
3. **Write BLUF-first** — answer/rule first, detail below.
4. **One `load_when`** (see [Front-matter](references/conventions.reference.md#front-matter--exactly-one-field)) — a *situation/trigger*, not a topic label. A compound trigger means two files.
5. **Check atomicity** (see [Atomicity](references/conventions.reference.md#atomicity--the-create-vs-update-decision)): one subject, standalone, one trigger — else split.
6. Add the **`## Related`** footer (see [Linking](references/conventions.reference.md#linking)), then [regenerate the manifest](#regenerate-the-manifest).

- Ask when a fact is missing — **never invent.**

## Record a decision

- "Why we chose X" is **append-only**.
- Add a numbered `knowledge/decisions/NNNN-<slug>.md` (template: `assets/decision.template.md`).
- Never rewrite an old decision — supersede it with a new one and link them.
- Decisions carry no `load_when`.

## Place a skill

- This governs **where** procedures live, not how they're written.
- Keep the canonical copy at `skills/<name>/SKILL.md`.
- Make it discoverable by adding a per-agent symlink (`.claude/skills → ../skills`, `.codex/skills → ../skills`, …) for each agent in use (see [Cross-agent compatibility](references/conventions.reference.md#cross-agent-compatibility)) — one canonical folder, N discovery points.
- Skills need no manifest — agents auto-surface their descriptions.
- Keep the skill folder to its **installable surface only** — `SKILL.md` plus genuine runtime resources (`scripts/`, `references/`, `assets/`). Put eval specs in `skill_evals/<name>/` (a sibling of `skills/`), never inside the skill, so they don't ship in the `.skill`. Point skill-creator at that path explicitly when running evals, and direct its run outputs to `skill_evals/<name>/runs/` (gitignored) — otherwise it defaults to a `<name>-workspace/` inside `skills/` and re-pollutes the install surface.

## Regenerate the manifest

- The manifest is **generated, never hand-edited**.
- Glob `knowledge/**/*.md`, read each file's `load_when` + path, group by subject, emit `[load_when](path)` lines (see [The manifest](references/conventions.reference.md#the-manifest)).
- Splice between the `<!-- KNOWLEDGE MANIFEST -->` markers in `AGENTS.md`.
- Do this with file tools — no runtime needed.
- Run it after any knowledge change so the committed manifest never drifts.

## Always true (invariants)

- Every `knowledge/**/*.md` (except `README`/`INDEX` and `decisions/`) has a `load_when` field and a `.concept`/`.reference` suffix.
- One subject, one `load_when`, per file.
- No derivable metadata is stored — no author/date/title/id/scope/keywords (see [Front-matter](references/conventions.reference.md#front-matter--exactly-one-field)).
- The committed manifest equals a fresh regeneration (no drift).
- `AGENTS.md` is the single source of truth; every other entry file points to it, never forks it.
