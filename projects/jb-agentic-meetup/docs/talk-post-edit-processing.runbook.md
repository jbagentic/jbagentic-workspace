# Post-edit processing

Turn a freshly edited talk into publish-ready subtitles and YouTube metadata. This
is the final phase of the talk-recording pipeline, all agent-run; see the
[project README](../README.md) for the full flow.

**Actor:** agent · **In:** `<talk-slug>.en.raw.srt` + `slides/` + `cover.png` · **Out:** polished + translated SRTs, `youtube-content.md`

## Prerequisites

Available when this phase starts (from earlier phases and manual assets):

- `<talk-slug>.en.raw.srt` — raw English subtitles from the [video edit](talk-video-edit.runbook.md).
- `slides/slide-NN.png` — from [pre-edit prep](talk-pre-edit-prep.runbook.md), used as glossary context.
- `cover.png` — the thumbnail asset.

## Steps

1. **Polish the English subtitles** — run `/subtitle-polish`. Strips fillers and stutters and fixes mis-transcribed terms against the slides, writing `<talk-slug>.en.srt` (the input stem with `.raw` removed).
2. **Translate to Chinese** — run `/subtitle-translate-zh`. One run produces `<talk-slug>.zh-Hans.srt` (Simplified) and then, by deterministic OpenCC `s2twp` conversion, `<talk-slug>.zh-Hant.srt` (Taiwan Traditional).
3. **Write YouTube metadata** — run `/talk-youtube-metadata`. Reads `<talk-slug>.en.srt` and writes `youtube-content.md` (A/B titles, description, auto-generated chapters, tags). Needs `meetup-<N>` in the folder name, and copies links/footer verbatim from [meetup-info.reference.md](meetup-info.reference.md).

**Ordering:** steps 2 and 3 each need only `<talk-slug>.en.srt`, so once step 1 is done they're independent and can run in parallel — they're listed in sequence here just for a clean read.

## Gate

Each skill self-verifies its own output (entry counts match the source, timestamps preserved byte-for-byte, UTF-8 without BOM). The phase is done when the talk folder holds all of:

- `<talk-slug>.en.srt`
- `<talk-slug>.zh-Hans.srt`
- `<talk-slug>.zh-Hant.srt`
- `youtube-content.md`
- `cover.png`

At that point the talk is ready to upload to YouTube.

## Related

- [`/subtitle-polish` SKILL.md](../../../agentic/skills/subtitle-polish/SKILL.md), [`/subtitle-translate-zh` SKILL.md](../../../agentic/skills/subtitle-translate-zh/SKILL.md), [`/talk-youtube-metadata` SKILL.md](../../../agentic/skills/talk-youtube-metadata/SKILL.md) — the skills this runbook drives.
- [talk-recordings.reference.md](talk-recordings.reference.md) — file names, folder convention, and the per-skill IO list.
- [meetup-info.reference.md](meetup-info.reference.md) — links and description footer the metadata step copies verbatim.
