# Post-edit processing

Turn a freshly edited talk into publish-ready subtitles and YouTube metadata. This
is the last phase of the pipeline. An agent runs all of it. See the
[project README](../README.md) for the full flow.

**Actor:** agent · **In:** `<talk-slug>.en.raw.srt` + `slides/` + `cover.png` · **Out:** polished + translated SRTs, `youtube-content.md`

## Prerequisites

These are ready when this phase starts, from earlier phases and manual assets:

- `<talk-slug>.en.raw.srt` — raw English subtitles from the [video edit](talk-video-edit.runbook.md).
- `slides/slide-NN.png` — from [pre-edit prep](talk-pre-edit-prep.runbook.md), used as glossary context.
- `cover.png` — the thumbnail asset.

## Steps

1. **Polish the English subtitles** — run `/subtitle-polish`. It removes fillers and stutters, fixes mis-transcribed terms against the slides, and writes `<talk-slug>.en.srt` (the input stem with `.raw` removed).
2. **Translate to Chinese** — run `/subtitle-translate-zh`. One run writes `<talk-slug>.zh-Hans.srt` (Simplified, for Malaysian Chinese readers), then converts it to `<talk-slug>.zh-Hant.srt` (Taiwan Traditional) with OpenCC `s2twp`, correcting Malaysian localisms to Taiwan-standard forms for the Taiwanese-reader target.
3. **Write YouTube metadata** — run `/series-youtube-metadata`. It reads `<talk-slug>.en.srt` and writes `youtube-content.md` (A/B titles, description, auto-generated chapters, tags). It reads the show profile in [meetup-info.reference.md](meetup-info.reference.md) for the series suffix, links, and footer (copied verbatim), and needs the meetup number in the folder name.

**Ordering:** Steps 2 and 3 both need only `<talk-slug>.en.srt`. Once step 1 is done, they're independent — run them in parallel if you like. They're listed in order here just for an easy read.

## Gate

Each skill checks its own output (entry counts match the source, timestamps unchanged, UTF-8 without BOM). The phase is done when the talk folder holds all of:

- `<talk-slug>.en.srt`
- `<talk-slug>.zh-Hans.srt`
- `<talk-slug>.zh-Hant.srt`
- `youtube-content.md`
- `cover.png`

Now the talk is ready to upload to YouTube.

## Related

- [`/subtitle-polish` SKILL.md](../../../agentic/skills/subtitle-polish/SKILL.md), [`/subtitle-translate-zh` SKILL.md](../../../agentic/skills/subtitle-translate-zh/SKILL.md), [`/series-youtube-metadata` SKILL.md](../../../agentic/skills/series-youtube-metadata/SKILL.md) — the skills this runbook drives.
- [talk-recordings.reference.md](talk-recordings.reference.md) — file names, folder convention, and the per-skill IO list.
- [meetup-info.reference.md](meetup-info.reference.md) — the show profile (series identity, links, footer) the metadata step reads.
