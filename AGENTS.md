# Agents Guide

Instructions for every agent we collaborate with in this workspace.

## How Agents Work

- **Value simplicity.** Simple words, straight to the point; simplify rigorously.
- **Think in systems.** Improve the whole system, avoid local optimization.
- **Reason from first principles.** Break problems down to fundamentals, then build up.
- **Ask why.** Don't assume — clarify the goal, constraints, and expectations before you start.
- **Say no when no is right.** Push back and voice your concerns.
- **Be resourceful and open-minded.** Get things done, stay open to a better way.
- **Be honest and kind.** Tell the truth; don't lie to please.

## Ground Rules

### How to Discover Context

A folder is a context boundary; its `README.md` is the onboarding guide to what's inside and how to work there. Start from the README nearest your task and follow where it points — linked guides, references, runbooks, and code. Then walk the tree: **up** to a parent for broader context, **down** into a subfolder for specifics. Stop once you know enough.

Use READMEs as a map before any blind `Find`/`Grep`/`Glob` search; search only when the map runs out.

### How to Document Context

Folders follow the **Contextful Folder** convention. Use the `doc-this` skill to write or organize a folder's docs — don't hand-write them free-form; the skill owns the spec and loads it only when needed.

- **Writing or organizing docs** → run `doc-this`.
- **Changing a folder's contents** → update its docs in the same pass, while it's fresh (`doc-this` reconciles). Stale docs mislead whoever comes next.

### Sandbox

**Treat the project folder as your boundary.** Keep files, outputs, and temp work in-project; use only allowlisted network; don't read credential dirs. Reach outside only when the task truly needs it — then surface it, don't route around it.

Concretely: write with the Write/Edit tools at in-project paths; for scratch/temp use the gitignored `tmp/` at the repo root — never system temp (`$TMPDIR`, `/var/folders`, `/tmp`).

**Under Claude Code** this is OS-enforced via `.claude/settings.json` — out-of-box actions prompt (supervised) or auto-deny (unattended); see [`docs/permissions-and-sandbox.guide.md`](docs/permissions-and-sandbox.guide.md). **Other agents** enforce through their own config (e.g. Codex's sandbox/approval policy, OpenCode's permission rules), not this file — honor the norm and set yours to match; don't assume `.claude/settings.json` governs you.

## Git Workflow

Branch-based workflow, no PRs (solo dev).

- **Always work on a branch** — never commit straight to `main`.
- **Branch from `main`** — use short, clear names (e.g. `add-logging`, `fix-parser-crash`).
- **Merge to `main` when done** — keep `main` history clean and well-written (squash messy branches, keep already-clean ones). Delete the branch after merging. Push `main` to the remote after merging.
- **Commit early, commit often** — small, focused commits with clear messages.
- **Never force-push `main`.**
- **Commit message style**: [Conventional Commits](https://www.conventionalcommits.org/) — `type: summary` under 72 chars. Common types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`. Add a body paragraph only when the "why" isn't clear from the summary.
