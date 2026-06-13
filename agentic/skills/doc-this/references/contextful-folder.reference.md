# Contextful Folder — reference

The authoritative reference on how to build **a "contextful" folder**: how to organize the files within it, what each is for, and how they're named. For the *why* behind this vocabulary, see the [Contextful Folder guide](contextful-folder.guide.md).

## Where these files live

The documentation files are **co-located in the folder itself**: `README.md` and `AGENTS.md` sit directly in it, and `docs/` is a subfolder inside it. The folder can also hold other subfolders — code, assets, nested modules — and these docs describe those too.

```
my-folder/
├── README.md                 # required — orients the whole folder
├── AGENTS.md                 # optional — agent instructions
├── docs/                     # optional — deeper typed docs
│   ├── api.reference.md
│   ├── release.runbook.md
│   └── decisions/
│       └── 20260608-use-dita-topic-types.md
├── src/                      # subfolders covered by this README — no README of their own
└── scripts/
```

`src/` and `scripts/` here have no README of their own — they're **covered by** the parent's README. A subfolder gets its own README only when it earns one (see [When a subfolder needs its own README](#when-a-subfolder-needs-its-own-readme)).

## File vocabulary

A contextful folder holds these documentation files, co-located in the folder itself — and only these:

| File | Required? | Purpose |
|------|-----------|---------|
| `README.md` | **Required** | Orientation for the directory: purpose, scope, structure, key workflows, links to deeper docs. The entry point. |
| `AGENTS.md` | Optional | How agents should behave in this directory: constraints, approval rules, output requirements, working conventions. Instructions, not knowledge. |
| `docs/*.{type}.md` | Optional | Deeper documentation, one topic per file, typed by intent (see below). |
| `docs/decisions/YYYYMMDD-*.md` | Optional | Timestamped design decisions — append-only, never edited after writing. |

`type` is one of:

| Type | Use for | Holds |
|------|---------|-------|
| `guide` | Concepts and explanations | Understanding — how/why something works |
| `reference` | Facts and specifications | Authoritative, look-up-able detail |
| `runbook` | Procedures and recurring tasks | Step-by-step operational instructions |

## Naming

Deeper docs are named `{topic}.{type}.md` — a kebab-case topic, then the type, then `.md`:

- `contextful-folder.reference.md`
- `talk-recordings.reference.md`
- `release.runbook.md`

Decision records are named `YYYYMMDD-{topic}.md` inside `docs/decisions/`:

- `docs/decisions/20260608-use-dita-topic-types.md`

`README.md` and `AGENTS.md` use those exact fixed names.

## Rule of thumb

| Content | Goes in |
|---------|---------|
| Directory purpose and navigation | `README.md` |
| Agent instructions and constraints | `AGENTS.md` |
| Concepts and explanations | `docs/*.guide.md` |
| Facts and specifications | `docs/*.reference.md` |
| Procedures and workflows | `docs/*.runbook.md` |
| Design decisions and tradeoffs | `docs/decisions/YYYYMMDD-*.md` |

## Keep it small

`README.md` and `AGENTS.md` are orientation and instruction, not encyclopedias. Push depth into a typed doc and **link** to it rather than duplicating. One file, one topic. When the same fact would appear twice, keep it in one place and link.

## When a subfolder needs its own README

Not every folder has a README. A README marks a context boundary; a small subfolder without one is **covered by** the nearest README above it — named there in the structure section with a one-line hook. The default is **cover-by-parent**: don't give a subfolder its own README until it earns one.

**Promote** a subfolder to its own Contextful Folder (give it a README) when **any** of these clearly holds:

| Signal | Promote when… |
|--------|---------------|
| Bloats the parent | Documenting it inline would crowd the parent's README — it needs more than a hook. |
| Worked in on its own | People or agents land and work here directly, without going through the parent — an independent entry point. |
| Needs its own deeper docs | It warrants its own `AGENTS.md`, typed `docs/`, or decision records. |
| Distinct purpose/audience | Its purpose, conventions, or audience differ enough that mixing would confuse readers. |

When none holds, leave it covered by the parent.

## Presenting structure

The README's structure coverage — the part that lists what the folder contains — should follow a **consistent, scannable convention** so any folder can be eyeballed the same way. Give it a labeled section, and make each entry pair a linked path with a one-line description of what it holds. Keep the shape uniform within a folder, and ideally across the repo.

The *exact* shape is the repo's house style, not something this spec fixes: a heading word (`Structure`, `Layout`, …) and a table or a bullet list — pick what reads best for the content (a flat set of folders suits a table; entries that nest suit a list). Consistency is the requirement; the template is not.

## Finding more context

Need broader context? Read the nearest `README.md` above you. Need something more specific? Read the `README.md` in a nested folder that has one — a subfolder without a README is covered by the README above it, so there's nothing deeper to open.

## Related

- [Contextful Folder guide](contextful-folder.guide.md) — the pattern and the topic-atom model behind this vocabulary.
