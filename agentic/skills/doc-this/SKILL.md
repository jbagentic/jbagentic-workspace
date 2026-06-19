---
name: doc-this
description: >-
  Turn raw materials — loose notes, a transcript, a brain-dump, or scattered
  half-written docs — into clean, standardized documentation for a folder:
  a README.md plus, as needed, an AGENTS.md and typed docs/*.{guide|reference|runbook}.md.
  Also reconciles a folder's existing docs after its contents change — keeping them
  in sync with what was added, removed, renamed, or changed in behavior.
  Use whenever the user wants to document a folder or project, write or clean up
  a README, organize messy/scattered docs, turn notes or a transcript into proper
  documentation, add a doc / guide / reference to a folder or the workspace,
  standardize how a directory is documented, keep a folder's docs in sync after a
  change ("we changed X, fold it in"), or just drops a brief aside — "doc this"
  / "document this folder" / "document the references / sources / notes for X"
  / "write this up" / "structure the docs" — even if they don't name the file types
  or the request is terse and mid-task. Not for polishing an existing doc's prose in
  place (just edit it), nor for bookmarking a single external URL / Drive link (that's
  the redirect-bookmark skill); but do use it to reconcile a folder's docs after its
  files or behavior change; not for authoring context-discovery rules as a standalone task.
---

# Doc This

Take raw input materials — or a change that just happened in a folder — and produce or update that folder's documentation so it conforms to the Contextful Folder pattern: a small, predictable file vocabulary so humans and agents always know where information lives. The routing quick-reference under *Conventions* covers the common case inline; the authoritative spec travels with this skill at [`references/contextful-folder.reference.md`](references/contextful-folder.reference.md), one file away.

## Input

- **A source — what to document.** *Required.* Either *raw materials* the user hands over (notes, a transcript, a description, a brief, scattered/half-written docs) **or** *a change that just happened* in an already-documented folder (files added, removed, renamed, or behavior changed) — then the change is the material and the job is to sync the folder's docs.
- **A home folder** — the single directory the docs describe. Named by the user, the folder you're reconciling, or inferred from the material with approval (settled in step 2).
- **The Contextful Folder spec** — at [`references/contextful-folder.reference.md`](references/contextful-folder.reference.md). Read it for the authoritative spec; the *Conventions* section below is a routing quick-reference.

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

1. **Get the source — don't go fishing.**
   - Work only from what the user gives: raw materials, or a change they've described or pointed you to.
   - **Neither given?** Ask what to document, then stop.
   - **Don't** glob the tree or read unrelated files to invent a subject — that produces docs nobody asked for.
   - **A stated change is the subject:** read the changed files and the folder's existing docs, then sync them — that's the job, not fishing.

2. **Settle the home folder** — the single directory the docs describe, at the right level.
   - **User named one?** Use it. **Reconciling a change?** It's the changed folder (already documented) — skip placement.
   - **Otherwise:** infer the best fit *from the material* (not by walking the tree), then tell the user your choice and why and wait for approval — placement is their call; don't create a folder and dump docs in unprompted.
   - **Right level:** the nearest specific existing folder, or a new one if none fits — not too high (a parent owning more than this material), nor too low (a leaf that's part of a larger unit).
   - **Small, simple subfolder:** cover it from the parent (cover-by-parent); give it its own README only when it [earns one](references/contextful-folder.reference.md#when-a-subfolder-needs-its-own-readme).

   Everything downstream anchors to this layer.

3. **Classify each chunk by intent** — this routing is the heart of the skill.
   - Ask the one job each chunk does — *orientation*, *agent instruction/constraint*, *concept*, *fact*, or *procedure* — and route it per the routing table below.
   - One chunk, one home — split a note that mixes intents into atoms first.

4. **Write or update the files.**
   - Write the `README.md` first (with its manifest), then any `AGENTS.md` and typed docs the material warrants.
   - Updating an existing folder: fold new material into the right existing file — don't spawn a parallel one; replace stale content, don't append duplicates.
   - Add, remove, or rename a `docs/` file → update the README manifest in the **same pass**.
   - One topic per file; link across them.

5. **Verify before reporting done** — fix anything that fails:
   - A `README.md` exists.
   - Only approved file types/names are present.
   - Manifest and `docs/` in sync — every `docs/*` has a manifest entry, every manifest link resolves.
   - Content routed to the correct type.
   - No duplication across files.

6. **Offer the always-on agent rules (first run only).** Docs pay off only when agents are told to use them. Add to the **top-level `AGENTS.md`/`CLAUDE.md`** (loaded on every task) whichever of these is absent — ask first and confirm where it goes:
   - **`How to Discover Context`** — makes agents read contextual docs first ([reference copy](references/context-discovery.reference.md)).
   - **`How to Document Context`** — routes documentation work to this skill and keeps docs current ([reference copy](references/context-maintenance.reference.md)).

   If the user declines, point them to the reference file to copy manually.

## Conventions

[`references/contextful-folder.reference.md`](references/contextful-folder.reference.md) is the **authoritative** spec — file vocabulary, naming, structure, and the rest. Read it for anything beyond the routing table below. The routing table is the one piece mirrored here because it's needed on nearly every classification decision.

**Routing — pick by the job the content does:**

| Content | Goes in |
|---------|---------|
| Directory purpose and navigation | `README.md` |
| Agent instructions and constraints | `AGENTS.md` |
| Concepts and explanations | `docs/*.guide.md` |
| Facts and specifications | `docs/*.reference.md` |
| Procedures and recurring tasks | `docs/*.runbook.md` |
| Design decisions and tradeoffs | `docs/decisions/YYYYMMDD-*.md` |

**Don't:** invent facts the materials don't support (ask if a key detail is missing); duplicate a fact across files; create file shapes outside the vocabulary.

## Related

- **Reference** — [Contextful Folder reference](references/contextful-folder.reference.md) — the authority this skill enforces.
- **Guide** — [Contextful Folder guide](references/contextful-folder.guide.md) — optional: the *why* behind the pattern, not needed to apply the spec; read only for rationale.
- **Context discovery rule** — [context-discovery.reference.md](references/context-discovery.reference.md) — the always-on navigation rule to install into your top-level `AGENTS.md`/`CLAUDE.md` (the always-on instructions), so agents read the docs this skill writes.
- **Context documentation rule** — [context-maintenance.reference.md](references/context-maintenance.reference.md) — the always-on rule to install alongside discovery, so agents route documentation work to this skill and keep these docs current when a folder's contents change.

