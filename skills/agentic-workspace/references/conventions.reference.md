# Agentic Workspace — Conventions Reference

The exact rules behind the `agentic-workspace` skill. Each section is BLUF: the rule first, the rationale after. This is the standard a knowledge file is checked against.

---

## Structure — workspace + optional projects

```
<workspace>/                        # LEVEL 1 — shared, project-agnostic truth
├── AGENTS.md                       # canonical agent entry: hand-written rules + generated manifest
├── CLAUDE.md                       # pointer → AGENTS.md (Claude Code reads this)
├── GEMINI.md                       # pointer → AGENTS.md (Gemini CLI reads this)
├── knowledge/                      # Concept + Reference atoms (read to UNDERSTAND / LOOK UP)
│   └── decisions/                  # Explanation / ADRs (append-only "why")
├── skills/                         # How-to / task procedures (canonical home)
│   └── <name>/SKILL.md
├── skill_evals/                    # dev-time eval specs, one folder per skill
│   └── <name>/
│       ├── evals.json              # test cases — kept OUT of skills/ so it never ships in the .skill
│       ├── benchmarks/             # committed: iteration-N.md summaries + history.md trend
│       └── runs/                   # skill-creator run outputs (gitignored scratch)
├── .claude/skills/  → ../skills    # per-agent discovery pointer (symlink)
└── projects/                       # LEVEL 2 — optional; one folder per project (client, product, module)
    └── <project>/
        ├── AGENTS.md               # "read workspace AGENTS.md first; here's what's specific"
        ├── CLAUDE.md               # pointer → this project's AGENTS.md
        └── knowledge/              # this project's atoms (+ decisions/)
```

- A project agent reads the **workspace** `AGENTS.md` first, then the **project** one.
- `projects/<project>/knowledge/` is **additive** — this project's facts only. Its `skills/` (if any) holds **overrides** (same name wins) or net-new project procedures.
- **Scope is encoded by location**, never by a `scope:` field.
- **Level 2 is optional.** A workspace with a single context skips `projects/` entirely and keeps everything at level 1. The split exists for reuse across projects, not ceremony.
- A "project" is any distinct context that inherits the shared truth and specializes it — a client engagement, a product line, a module.
- **Skill evals live in `skill_evals/<name>/`, not in `skills/<name>/`.** A skill folder is the installable surface — everything inside it ships in the `.skill`. Eval specs are dev-time only (read by skill-creator, never by the skill at runtime), so they sit in a sibling `skill_evals/` tree keyed by skill name. The trade: a clean install surface in exchange for losing skill-creator's default auto-discovery, so the eval path is passed explicitly when iterating. Run outputs go to `skill_evals/<name>/runs/` (skill-creator otherwise defaults to a `<name>-workspace/` *inside* `skills/`, which re-pollutes the install surface) — keep specs and their results together, and gitignore `runs/` since it's disposable scratch. For the `aggregate_benchmark` script to read a run, lay each iteration out as `runs/iteration-N/eval-<id>/<config>/run-<k>/{grading.json,timing.json}` — the `run-<k>` tier is mandatory (it's how variance across repeated runs is measured), and `grading.json` must carry a `summary` block (`pass_rate`, `passed`, `failed`, `total`) alongside its `expectations`. Without that tier and block the aggregator silently emits an all-zero benchmark. The `runs/` tree is disposable; **promote** a curated, accurate summary per iteration to the committed `skill_evals/<name>/benchmarks/iteration-N.md` and keep a `benchmarks/history.md` trend table — that's the quality-over-time record, separate from the ignored scratch (the split avoids gitignore-negation, which can't re-include a file under an ignored parent dir).

---

## File types — one type per file

Four reader intents (Diátaxis minus Tutorial — an agent is always *working*, never *learning*):

| Type | Reader intent | Lives in | Marker |
|---|---|---|---|
| **Reference** | look up exact facts / specs / snippets | `knowledge/*.reference.md` | `.reference` suffix |
| **Concept** | understand what / how something works | `knowledge/*.concept.md` | `.concept` suffix |
| **How-to / Task** | execute a procedure | `skills/<name>/SKILL.md` | folder + `SKILL.md` |
| **Explanation / Decision** | why we chose X (append-only) | `knowledge/decisions/NNNN-*.md` | numbered, in `decisions/` |

- **Rule: never mix types in one file.** A file needing two load reasons is two files.
- Type is declared in the **filename suffix**, not a folder and not a front-matter field — so it is visible in the editor tree and greppable.
- **Why suffix, not folder:** subject and type are *orthogonal* facets; a directory tree encodes only one. The suffix lets storage stay grouped by subject while type stays greppable.

---

## Front-matter — exactly one field

```yaml
---
load_when: "choosing a token type, or checking whether a request is authenticated"
---
```

- `load_when` is the **only** required field.
- It is a **situation/trigger**, not a topic label — write it as the condition under which an agent should pull the file.
- It drives both the manifest and the agent's load decision.

Everything else is **derivable and must NOT be stored**:

| Tempting field | Where it actually lives |
|---|---|
| author / created / history | `git log`, `git blame` |
| last-edited / "reviewed" date | master = reviewed (PR gate); freshness = git commit date |
| title | the `# H1` |
| id / slug | the filename |
| scope | the directory |
| keywords | full-text grep — add a synonym to the body only if it is a *true* synonym absent from the text |

- **Why:** storing derivable metadata creates a second source of truth that rots — git history and the filesystem already hold it.

---

## Filenames & folders

- **kebab-case nouns, subject-prefixed:** `auth-flow.concept.md`, `auth-tokens.reference.md`, `api-errors.reference.md`.
- **No dates or versions in names** — freshness is git's job.
- **Flat by subject inside `knowledge/`.** Do not create type folders (type is the suffix) and do not pre-create subject folders.
- **Promotion trigger:** fold a subject into `knowledge/<subject>/` only once it crosses ~8–10 files that are mostly linked to each other (high intra-subject coupling). Until then, flat.
- **Decisions** are numbered for stable ordering and reference: `decisions/0003-session-tokens.md`.
- **Why flat:** premature folders impose a tree (one facet) on data with two facets (subject × type). Get *grouping* from the manifest instead — it regroups freely without moving files.

---

## Atomicity & the create-vs-update decision

A file is **atomic** when all three hold:

1. **One subject** — nameable in a sentence with no "and" joining unrelated things.
2. **Standalone** — understandable without inlining another file.
3. **One `load_when`** — a single trigger pulls it. A compound trigger ("A; also unrelated B") means two files.

Decision table:

| Situation | Action |
|---|---|
| Same retrieval intent as an existing file | **Update in place** — knowledge files hold current truth; rewrite freely |
| New nameable topic, loaded independently | **New file** |
| One file serving 2+ unrelated intents | **Split** |
| Two files always loaded together | **Merge** |
| A fact appearing in two files | It has no home — keep one home + **link** (DRY) |
| "Why we chose X" | **Append** to `decisions/`, never rewrite |

**Content ordering: BLUF.** Lead every file and every section with the answer/rule; supporting detail below. Both AI extraction and human review read top-first.

---

## The manifest

- The single **always-in-context** surface. **Generated, never hand-maintained.**
- Lives inline in `AGENTS.md` between markers — the cross-agent-safe choice, since every tool reads plain Markdown.
- An `@import` of a generated `INDEX.md` is cleaner but Claude-Code-only, so prefer inline for portability.
- Token-efficient format: **link text = the `load_when`, link target = the path, grouped by subject header.**

```markdown
<!-- KNOWLEDGE MANIFEST (generated) — load a file when its line matches your task -->

**auth**
- [token type choice, request-auth check](knowledge/auth-flow.concept.md)
- [token formats, header examples](knowledge/auth-tokens.reference.md)

**api**
- [error codes and retry rules](knowledge/api-errors.reference.md)

<!-- END KNOWLEDGE MANIFEST -->
```

- Each entry reduces to two irreducible parts: *what to load it for* (the trigger) + *where it is* (the path). Subject is factored to the group header; type rides in the path suffix; "load when" is stated once. ~20–25 tokens per entry.
- **Regeneration (agent-run, no runtime needed):** glob `knowledge/**/*.md`, read each file's `load_when` and path, group by subject prefix, emit the lines above, splice between the markers.
- Always regenerate after a knowledge change so the committed manifest never drifts from the files.

---

## Linking

- **Relative `.md` paths** so editors (VS Code) resolve Cmd/Ctrl+Click; `#heading-slug` jumps to a section.
- Each file ends with a **`## Related`** footer using a small typed vocabulary: **Reference · How-to · Why · Related concept · Up**.

```markdown
## Related
- **Reference** — [auth-tokens](./auth-tokens.reference.md)
- **How-to** — [rotate-keys skill](../skills/rotate-keys/SKILL.md)
- **Why** — [0003 · Session tokens over JWT](./decisions/0003-session-tokens.md)
- **Up** — [workspace: auth flow](../../../knowledge/auth-flow.concept.md)
```

- Use real `##` headings (not custom anchors) so the editor Outline and anchor links work.
- Enable `markdown.updateLinksOnFileMove.enabled` so VS Code rewrites inbound links on rename/move.
- VS Code has no automatic backlinks — the `## Related` footer is the hand/agent-maintained backlink layer.

---

## Capture & human ↔ agent collaboration

**Division of labor:**

- **Human** = knowledge source + final reviewer.
- **Agent** = scribe + conformance layer.
- The **PR** is the seam: merge = approval = reviewed knowledge.

New knowledge atom:

1. **Human supplies raw** — chat dump, voice, rough bullets, or a pasted source. Zero format burden. An optional one-line hint ("this is auth" / "update the api-errors file") sharpens create-vs-update.
2. **Agent conforms it** — decides create-vs-update, splits for atomicity, picks type + suffix, writes BLUF-first, adds `load_when`, fixes links, regenerates the manifest. **Asks when a fact is missing — never invents.**
3. **Human reviews for truth, not format** — the agent already handled format.

- Trivial edits (a typo, a value bump, a broken link) go direct — size the ceremony to the change.

---

## Cross-agent compatibility

**One canonical entry + one canonical skills folder, with thin per-agent discovery pointers.** Different tools look in different places; the convention converges them on `AGENTS.md` and `skills/` rather than forking content.

- `AGENTS.md` is the source of truth and lives at the **repo root**.

### Always loaded at session start

- The "always loaded" guarantee is built in: **each agent auto-loads its own root entry file at the start of every session.** So the rule is simply — give each agent in use a *root* entry file it auto-loads, resolving to `AGENTS.md`.
- Agents that read a different filename than `AGENTS.md` get a **pointer**: a symlink on macOS/Linux, or (Windows / sync-tool-safe) a stub that imports or links `AGENTS.md`.

| Agent | Auto-loads at session start | Set up |
|---|---|---|
| Codex CLI, Cursor, Windsurf, Amp, OpenCode | `AGENTS.md` | nothing — they read the canonical file directly |
| Claude Code | `CLAUDE.md` — does **not** read `AGENTS.md` | root `CLAUDE.md` that imports it: a single line `@AGENTS.md` (preferred — lets you add Claude-only lines below), or `ln -s AGENTS.md CLAUDE.md` |
| Gemini CLI | `GEMINI.md` (also reads `AGENTS.md`) | optional `GEMINI.md` pointer → `AGENTS.md`; if both exist, `GEMINI.md` wins, so keep it a thin pointer |

- **Claude import detail:** Claude Code expands `@AGENTS.md` at load time (nested imports supported), so the shared standard plus any Claude-only lines all land in context. A bare `AGENTS.md` with **no** `CLAUDE.md` loads **zero** instructions in Claude Code, and fails silently — so the shim is required, not optional.
- **Root-only auto-load:** only root (and `.claude/`) entry files load at session start. A `projects/<project>/` entry file is picked up when the agent works inside that folder (Claude walks up from the cwd collecting `CLAUDE.md`), so start the session in the project dir to load both levels. The workspace manifest stays in context; project knowledge loads on demand via the manifest.
- `AGENTS.md` is the emerging cross-tool standard (OpenAI origin, now under the Linux Foundation's Agentic AI Foundation) — deliberately plain Markdown, no required schema. Keep the hand-written rules minimal; let the generated manifest carry the dispatch.

### Skills discovery

- Each agent auto-discovers project skills from **its own** folder; none reads a foreign agent's folder — except **OpenCode**, which reads `.claude/skills/`.
- Keep the canonical procedures in `./skills/<name>/SKILL.md` and add a discovery **symlink per agent as you adopt it**:

| Agent | Skills discovery path | Pointer |
|---|---|---|
| Claude Code, OpenCode | `.claude/skills/` | `.claude/skills → ../skills` |
| Codex CLI | `.codex/skills/` | `.codex/skills → ../skills` |
| Cursor | `.cursor/skills/` | `.cursor/skills → ../skills` |
| Gemini CLI | `.gemini/skills/` | `.gemini/skills → ../skills` |

- One canonical folder, N discovery points. Add only the pointers for agents actually in use.
- **Why skills need no manifest but knowledge does:** agents auto-surface `SKILL.md` *descriptions* and load bodies on demand. Plain `knowledge/*.md` is not an auto-loaded type, so the manifest is its dispatch layer.

### Portability notes

- **Symlinks** are clean in git on macOS/Linux but break on native Windows checkouts and some sync tools (iCloud/Dropbox). When portability matters, use stub files instead of symlinks for entry pointers, and document the skills-folder mapping for adopters to wire per platform.
- Keep `AGENTS.md` free of tool-specific syntax (no `@imports` in the canonical file) so every tool parses it identically. Put tool-specific niceties only in that tool's own pointer file.

---

## Related
- **How-to** — [agentic-workspace skill](../SKILL.md)
- **Templates** — [assets/](../assets/)
