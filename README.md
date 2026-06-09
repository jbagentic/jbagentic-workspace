# JB Agentic Workspace

- Digital workspace for various projects run by JB Agentic community.

## Workspace Layout

| Folder | What it holds |
|--------|---------------|
| [`agentic/`](agentic/README.md) | Agent capabilities — the skill library (`skills/`) and the evals that measure them. |
| [`projects/`](projects/) | Community projects, one folder per project (see below). |
| [`docs/`](docs/) | Workspace-wide reference docs and architecture decisions. |

### Projects

- [JB Agentic Meetup](projects/jb-agentic-meetup/README.md) — brand facts, past-meetup records, and per-talk recording assets (subtitles, slides, video links, YouTube metadata).

## Common Skills

Common skills we use across projects in this workspace:

- [`doc-this`](agentic/skills/doc-this/SKILL.md) — turn raw materials (notes, transcripts, scattered docs) into structured contextual information and store into a relevant folder. Implements Contextful Folder pattern.

See the [agentic skill catalog](agentic/README.md#skills) for the full list — including the subtitle, slides, and YouTube skills the meetup project relies on.


## Docs Manifest

- [SKILL.md convention in this workspace](docs/skill-convention.reference.md)

