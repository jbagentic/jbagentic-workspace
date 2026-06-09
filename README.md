# JB Agentic Workspace

A digital workspace for the projects run by the JB Agentic community.

## Structure

| Folder | What it holds |
|--------|---------------|
| [`agentic/`](agentic/README.md) | Agent capabilities — the skill library (`skills/`) and the evals that measure them. |
| [`projects/`](projects/) | Community projects, one folder per project (see below). |
| [`docs/`](docs/) | Workspace-wide reference docs and architecture decisions. |

### Projects

- [JB Agentic Meetup](projects/jb-agentic-meetup/README.md) — brand facts, past-meetup records, and per-talk recording assets (subtitles, slides, video links, YouTube metadata).

## Common Skills

Skills we use across projects in this workspace:

- [`/doc-this`](agentic/skills/doc-this/SKILL.md) — turn raw materials (notes, transcripts, scattered docs) into structured, contextual docs and save them in the right folder. Implements the [**Contextful Folder**](agentic/skills/doc-this/references/contextful-folder.guide.md) pattern.

For other skills, see the [agentic skill catalog](agentic/README.md#skills) for the full list — including the subtitle, slides, and YouTube skills the meetup project uses.


## Docs Manifest

- [SKILL.md convention in this workspace](docs/skill-convention.reference.md)

## License

This repo holds material under two sets of terms:

- **Community-authored work** (skills, eval harness, docs) — [MIT](LICENSE).
- **Speaker talk material** (slides, transcripts, covers, and assets derived from them) — © the respective speakers, all rights reserved, **not** covered by the MIT license. See [NOTICE](NOTICE).

