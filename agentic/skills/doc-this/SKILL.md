---
name: doc-this
description: >-
  Turn raw materials — loose notes, a transcript, a brain-dump, or scattered
  half-written docs — into clean, standardized documentation for a folder:
  a README.md plus, as needed, an AGENTS.md and typed docs/*.{guide|reference|runbook}.md.
  Use whenever the user wants to document a folder or project, write or clean up
  a README, organize messy/scattered docs, turn notes or a transcript into proper
  documentation, standardize how a directory is documented, or just says "doc this"
  / "document this folder" — even if they don't name the file types. Not for editing
  a single existing doc's prose in place (just edit it) and not for authoring
  context-discovery rules as a standalone task.
---

# Doc This

Take raw input materials and produce documentation for a folder that conforms to Contextful Folder pattern — a small, predictable file vocabulary so humans and agents always know where information lives. The routing quick-reference under *Conventions* covers the common case inline; the authoritative spec travels with this skill at [`references/contextful-folder.reference.md`](references/contextful-folder.reference.md), one file away.

## Input

- **Raw materials**: loose notes, a transcript, a description, a feature brief, or existing scattered/half-written docs. Whatever the user hands over as the source of truth for *what* to document. **Required** — if none were handed over (e.g. the skill was invoked bare), ask the user for the source material first, before anything else. Never scan the repo to invent a subject.
- **A home folder** (the directory the docs will describe). Use it if the user named one; otherwise infer it *from the raw material* and propose it with a reason for approval before writing — never assumed silently and never guessed by walking the tree.
- **The Contextful Folder spec** — bundled with this skill at [`references/contextful-folder.reference.md`](references/contextful-folder.reference.md) and its [guide](references/contextful-folder.guide.md). These travel inside the skill, so the contract is satisfied in any repo without external files. Read the reference for the authoritative spec; the *Conventions* section below is a routing quick-reference.

## Output

Files written **into the home folder**, drawn only from this vocabulary:

- `README.md` — always. Orientation: purpose, scope, structure, key workflows, and a manifest linking each deeper doc with a one-line hook.
- `AGENTS.md` — only if there are agent *instructions* (constraints, approval rules, conventions) to record.
- `docs/<topic>.<type>.md` — only as needed, where `<type>` is `guide` (concepts), `reference` (facts), or `runbook` (procedures), and `<topic>` is kebab-case.
- `docs/decisions/YYYYMMDD-<topic>.md` — only when the folder has non-obvious design decisions worth preserving. Append-only, never edited after writing.

Invariants (what makes the output conform):

- **README always present.** It's the entry point; a documented folder without one is incomplete.
- **Only the approved vocabulary** — `README.md`, optional `AGENTS.md`, optional `docs/*.{guide|reference|runbook}.md`, optional `docs/decisions/YYYYMMDD-*.md`. No other doc file shapes.
- **Correct routing** — each piece of content sits in the type that matches its intent (see the routing table under *Conventions*). Instructions never land in a knowledge doc; facts never get buried in a guide.
- **`{topic}.{type}.md` naming**, kebab-case topic; `README.md` / `AGENTS.md` use their fixed names.
- **No duplication** — a fact lives in one place; everything else links to it.
- **Small and scannable** — README/AGENTS orient and instruct; depth is pushed into typed docs and linked, not inlined.
- **Manifest in sync** — the README manifest lists every current `docs/*` file and no stale ones; it's updated in the same pass as any `docs/` change.

## Workflow

1. **Get the raw material first — don't scan.** This skill runs on material the user provides, not on a repo scan. If no material was handed over (e.g. the skill was invoked bare), ask the user what to document and stop. Don't glob the tree, read unrelated files, or infer a subject — that produces docs nobody asked for.

2. **Settle the home folder.** Decide the single directory the docs describe *and the right level for it* — attach to the nearest specific existing folder, or create one when none fits. Don't park docs too high (a parent that owns more than this material) or too low (a leaf that's really part of a larger unit). Everything downstream anchors to this folder layer. If the user already named a target folder, that's your answer — use it. If they didn't, infer the best fit *from the raw material*, tell the user your choice and why, and wait for their approval before writing — placement is the user's final call, so don't create a folder and dump docs into it unprompted.

3. **Classify each piece of raw material by intent.** For every chunk of input, ask which one job it does: *orientation* → README; *agent instruction/constraint* → AGENTS; *concept/explanation* → guide; *fact/spec* → reference; *procedure/recurring task* → runbook. One chunk, one home — if a note mixes intents, split it into atoms first. This routing is the heart of the skill.

4. **Write or update the files.** Produce the README (with a manifest that links each deeper doc and a one-line hook), then any AGENTS and typed docs the material warranted. When updating an existing folder, fold new material into the right existing file instead of creating a parallel one; replace stale content rather than appending duplicates. **Whenever you add, remove, or rename a `docs/` file**, update the README manifest in the same pass so it lists every current doc and no stale ones. Keep each file to one topic and link across them.

5. **Verify before reporting done.** Confirm: a README exists; only approved file types/names are present; the manifest and `docs/` are in sync — every `docs/*` file has a manifest entry and every manifest link resolves; content is routed to the correct type; nothing is duplicated across files. Fix anything that fails.

6. **Offer to install the navigation convention (first time only).** The docs you just wrote are a map; agents only benefit if they're told to *navigate* by it. That navigation rule is always-on behavior, so it belongs in the repo's root agent instructions — not in this skill's on-demand scope. Check the repo's root `AGENTS.md` (or `CLAUDE.md`, if that's what it loads as always-on instructions) for the context-discovery convention. If it's **already present**, do nothing. If it's **absent**, offer to add the block from [`references/context-discovery.reference.md`](references/context-discovery.reference.md) and **ask the user before writing** — it's a root file outside the folder you're documenting. If they decline, point them to that atom so they can copy it in themselves.

## Conventions

The bundled [`references/contextful-folder.reference.md`](references/contextful-folder.reference.md) (with its [guide](references/contextful-folder.guide.md)) is the **authoritative** spec — file vocabulary, naming, structure, and the rest. It ships inside this skill, so it's always available; read it for anything beyond the routing table below. The routing table is the one piece mirrored here because it's needed on nearly every classification decision.

**Routing — pick by the job the content does:**

| Content | Goes in |
|---------|---------|
| Directory purpose and navigation | `README.md` |
| Agent instructions and constraints | `AGENTS.md` |
| Concepts and explanations | `docs/*.guide.md` |
| Facts and specifications | `docs/*.reference.md` |
| Procedures and recurring tasks | `*.runbook.md` |
| Design decisions and tradeoffs | `docs/decisions/YYYYMMDD-*.md` |

**Don't:** invent facts the materials don't support (ask if a key detail is missing); duplicate a fact across files; create file shapes outside the vocabulary.

## Related

- **Reference (bundled)** — [Contextful Folder reference](references/contextful-folder.reference.md) and its [guide](references/contextful-folder.guide.md) — the authority this skill enforces, shipped inside the skill.
- **Context-discovery convention (bundled)** — [context-discovery.reference.md](references/context-discovery.reference.md) — the always-on navigation rule to install into a repo's `AGENTS.md`/`CLAUDE.md`, so agents read the docs this skill writes.

