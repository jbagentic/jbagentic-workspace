# agentic

The agent capabilities for this workspace: the **skills** agents invoke, and the **evals**
that measure those skills. If you want to know what an agent can do here, or how we track
its quality over time, this is the folder.

## Structure

| Folder | What it holds |
|--------|---------------|
| [`skills/`](skills/) | The reusable capabilities an agent loads and runs — one self-contained folder per skill, each with a `SKILL.md` (plus optional `references/` or `scripts/`) that says when to use it and how to run it. Canonical location: the repo's `.claude/skills` is a symlink to here, so installed skills and their source are the same files. |
| [`evals/`](evals/) | Dev-time test suites that run each skill against fixtures and record how it performs across iterations — for building and improving skills, not run at agent time. One folder per skill under test; see [`evals/README.md`](evals/README.md) for the layout and the run → promote → history workflow. |

## Skills

The library in [`skills/`](skills/) — one folder per skill, each documented by its own `SKILL.md`:

- [`doc-this`](skills/doc-this/SKILL.md) — turn raw materials (notes, transcripts, scattered docs) into Contextful Folder documentation.
- [`redirect-bookmark`](skills/redirect-bookmark/SKILL.md) — committed HTML meta-refresh stub that bookmarks an external/Drive URL in the repo.
- [`slides-pdf-to-png`](skills/slides-pdf-to-png/SKILL.md) — extract every page of a slide-deck PDF into HD PNG frames.
- [`subtitle-polish`](skills/subtitle-polish/SKILL.md) — clean raw SRT subtitles and fix mis-transcribed terms against slide context.
- [`subtitle-translate-zh`](skills/subtitle-translate-zh/SKILL.md) — translate an English SRT into Simplified and Taiwan-flavored Traditional Chinese.
- [`youtube-metadata`](skills/youtube-metadata/SKILL.md) — generate YouTube titles, description, chapters, and tags for a recorded talk, podcast, or other long-form video, driven by the project's show profile.

## Authoring

Skills are written with the **skill-creator** skill and follow the workspace house
style. See [`docs/skill-convention.reference.md`](../docs/skill-convention.reference.md) for the conventions.
