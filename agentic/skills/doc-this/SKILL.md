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
  documentation, standardize how a directory is documented, keep a folder's docs in
  sync after a change ("we changed X, fold it in"), or just says "doc this"
  / "document this folder" — even if they don't name the file types. Not for polishing
  an existing doc's prose in place (just edit it), but do use it to reconcile a
  folder's docs after its files or behavior change; not for authoring context-discovery
  rules as a standalone task.
---

# Doc This

Take raw input materials — or a change that just happened in a folder — and produce or update that folder's documentation so it conforms to the Contextful Folder pattern: a small, predictable file vocabulary so humans and agents always know where information lives. The routing quick-reference under *Conventions* covers the common case inline; the authoritative spec travels with this skill at [`references/contextful-folder.reference.md`](references/contextful-folder.reference.md), one file away.

## Input

- **A source — what to document.** Either *raw materials* the user hands over (loose notes, a transcript, a description, a feature brief, scattered/half-written docs) **or** *a change that just happened* in an already-documented folder (files added, removed, renamed, or behavior changed) — then the change is the material and the job is to bring the folder's docs back in sync. **Required** — if neither was given (e.g. the skill was invoked bare), ask what to document first, before anything else. Don't scan the repo to invent a subject; but a change the user states or points you to is a legitimate subject.
- **A home folder** (the directory the docs describe). If the user named one, use it. When you're reconciling a change, it's the folder whose contents changed — the nearest Contextful Folder — so there's nothing to approve. Otherwise infer it *from the raw material* and propose it with a reason for approval before writing — never assumed silently or guessed by walking the tree.
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

1. **Get the source first — don't go fishing.** This skill runs on what the user gives you: raw materials, or a change they've described or pointed you to. If neither was given (e.g. the skill was invoked bare), ask what to document and stop. Don't glob the tree or read unrelated files to invent a subject — that produces docs nobody asked for. A stated change is the exception: it names the subject, so reading the changed files and the folder's existing docs to sync them is the job, not fishing.

2. **Settle the home folder.** Decide the single directory the docs describe *and the right level for it* — attach to the nearest specific existing folder, or create one when none fits. Don't park docs too high (a parent that owns more than this material) or too low (a leaf that's really part of a larger unit). Everything downstream anchors to this folder layer. If the user already named a target folder, that's your answer — use it. If they didn't, infer the best fit *from the raw material*, tell the user your choice and why, and wait for their approval before writing — placement is the user's final call, so don't create a folder and dump docs into it unprompted. When you're reconciling a change, the home folder is already settled — it's the folder whose contents changed, which already has docs — so skip the placement question and go straight to updating it.

3. **Classify each piece of raw material by intent.** For every chunk of input, ask which one job it does: *orientation* → README; *agent instruction/constraint* → AGENTS; *concept/explanation* → guide; *fact/spec* → reference; *procedure/recurring task* → runbook. One chunk, one home — if a note mixes intents, split it into atoms first. This routing is the heart of the skill.

4. **Write or update the files.** Produce the README (with a manifest that links each deeper doc and a one-line hook), then any AGENTS and typed docs the material warranted. When updating an existing folder, fold new material into the right existing file instead of creating a parallel one; replace stale content rather than appending duplicates. **Whenever you add, remove, or rename a `docs/` file**, update the README manifest in the same pass so it lists every current doc and no stale ones. Keep each file to one topic and link across them.

5. **Verify before reporting done.** Confirm: a README exists; only approved file types/names are present; the manifest and `docs/` are in sync — every `docs/*` file has a manifest entry and every manifest link resolves; content is routed to the correct type; nothing is duplicated across files. Fix anything that fails.

6. **Offer to install the always-on conventions (first time only).** The docs you just wrote only pay off if agents are told to *navigate* by them and to *keep them current*. Both rules are always-on behavior, so they belong in your **always-on agent instructions** — the top-level `AGENTS.md` or `CLAUDE.md` that's loaded on every task and applies to every folder, not the local `AGENTS.md` of the folder you just documented, and not this skill's on-demand scope. Check that file for each convention — **context-discovery** ([`references/context-discovery.reference.md`](references/context-discovery.reference.md)) and **context-maintenance** ([`references/context-maintenance.reference.md`](references/context-maintenance.reference.md)). For whichever is **absent**, offer to add its block and **ask the user before writing** — confirm where it should go, since both apply above the folder you're documenting. If they decline, point them to the atoms so they can copy them in themselves.

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
- **Context-discovery convention (bundled)** — [context-discovery.reference.md](references/context-discovery.reference.md) — the always-on navigation rule to install into your top-level `AGENTS.md`/`CLAUDE.md` (the always-on instructions), so agents read the docs this skill writes.
- **Context-maintenance convention (bundled)** — [context-maintenance.reference.md](references/context-maintenance.reference.md) — the always-on rule to install alongside discovery, so agents keep these docs current when a folder's contents change.

