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

Not every folder has a README. A README marks a context boundary; a small subfolder without one is **covered by** the nearest README above it. The default is **cover-by-parent**: don't give a subfolder its own README until it earns one.

**Promote** a subfolder to its own Contextful Folder (give it a README) when **any** of these clearly holds:

| Signal | Promote when… |
|--------|---------------|
| Independent entry point | People or agents land and work here directly, without going through the parent — an independent entry point. |
| Needs deeper docs | It warrants its own `AGENTS.md`, several typed `docs/`, or decision records. |
| Distinct purpose | Its purpose, conventions, or work differ enough that mixing would confuse users. |

When none holds, leave it covered by the parent.

## Consistent content structure

The content of READMEs should follow a **consistent, uniform convention** so any folder can be easily scanned and eyeballed.

For example, when documenting what's in the folder, give the section a consistent title, and describe each file (or file pattern) and subfolder with a linked path and a one-line description. Keep the shape uniform across READMEs.

## Finding more context

Need broader context? Read the nearest `README.md` above you. Need something more specific? Read the `README.md` in a nested folder that has one — a subfolder without a README is covered by the README above it.

## Related

- [Contextful Folder guide](contextful-folder.guide.md) — the pattern and the topic-atom model behind this vocabulary.
