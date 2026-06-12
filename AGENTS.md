# Agents Guide

Instructions for every agent we collaborate with in this workspace.

## How We Work

- **Value simplicity.** Simple words, short sentences, reason from first principles.
- **Think in systems.** Improve the whole system, not just one part.
- **Be honest and kind.** Tell the truth; don't lie to please people.
- **Be resourceful and open-minded.** Get things done, and stay open to a better way.
- **Be a good storyteller.** Make your thinking easy to follow.
- **Say no when no is right.** Don't agree just to agree.
- **Ask why.** Learn the goals, intent, constraints, and expectations before you start.

## Ground Rules

### Context Discovery Rule

A folder is a context boundary, and its `README.md` is the front door that tells you what's inside. When you need context, start from the README closest to your task and follow where it points — not just other READMEs, but anything it links: reference docs, skill files, code.

From there, follow the context instead of searching:

- Need **broader** context? Go *up* to the parent folders.
- Need **more specific** context? Go *down* into the subfolders.
- Stop once you know enough.

READMEs are the map, so use them before a blind `Find`/`Grep`/`Glob` sweep — searching first wastes tokens and skips the map. If the trail doesn't cover what you need, then search.

### Documenting a Folder

Use the `doc-this` skill for a folder's docs — don't hand-write them.

- **Creating or organizing docs** — turning notes, a brain-dump, or scattered materials into a `README.md` / `AGENTS.md` / typed `docs/*.{guide|reference|runbook}.md`, or a brief aside like "doc this" / "document the references" / "write this up" → run `doc-this`.
- **Keeping docs current** — when you change what's in a Contextful Folder, update its docs in the same pass: the nearest folder with a `README.md`. If you're unsure what to change, ask `doc-this` to reconcile them.
- **Why** — the next agent or person works from these docs and can't ask you later; stale or missing docs make them get it wrong.

### Write Files In-Project

Create and edit files with the **Write/Edit tools** at **in-project paths** — not shell heredocs into system temp (`$TMPDIR`, `/var/folders`).

- **Why** — Write-tool output is reviewable and diffable, and in-project paths stay inside the sandbox, so unattended runs don't stall on an approval prompt (or silently auto-deny). See [`docs/permissions-and-sandbox.guide.md`](docs/permissions-and-sandbox.guide.md).
- Use shell or temp files only for genuine throwaway scratch, never for a deliverable.

## Git Workflow

Branch-based workflow, no PRs (solo dev).

- **Always work on a branch** — never commit straight to `main`.
- **Branch from `main`** — use short, clear names (e.g. `add-logging`, `fix-parser-crash`).
- **Merge to `main` when done** — keep `main` history clean and well-written (squash messy branches, keep already-clean ones). Delete the branch after merging. Push `main` to the remote after merging.
- **Commit early, commit often** — small, focused commits with clear messages.
- **Never force-push `main`.**
- **Commit message style**: [Conventional Commits](https://www.conventionalcommits.org/) — `type: summary` under 72 chars. Common types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`. Add a body paragraph only when the "why" isn't clear from the summary.
