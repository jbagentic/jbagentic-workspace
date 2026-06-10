# Talk Recording Assets

How a talk's recording assets are named and laid out under `talk-recordings/`, and which skill produces each file. One folder per talk.

> **Licensing:** these talk assets are speaker-owned — © the respective speakers, all rights reserved, and **not** covered by the repo's MIT license. JB Agentic holds only a limited non-commercial license to publish them on its own channels. See the root [`NOTICE`](../../../NOTICE).

## Folder layout

```
talk-recordings/
└── <talk-slug>/                        # one folder per talk (see "Folder name" below)
    ├── <talk-slug>.en.raw.srt          # raw English subtitles (manual input)
    ├── <talk-slug>.en.srt              # polished English subtitles
    ├── <talk-slug>.zh-Hans.srt         # Simplified Chinese subtitles
    ├── <talk-slug>.zh-Hant.srt         # Traditional Chinese subtitles
    ├── cover.png                       # video cover image (manual)
    ├── slides.pdf                      # full slide deck (manual input)
    ├── slides/slide-NN.png             # one PNG per slide, zero-padded, 1-based
    ├── video-file.html                 # meta-refresh redirect to the Drive video
    └── youtube-content.md              # YouTube titles, description, tags
```

The `.mov` video file is gitignored and not listed here.

## Folder name

The folder name is the talk slug — `JBAgentic-<YYYYMMDD>-meetup-<N>-<Speaker>-<Title>` — e.g. `JBAgentic-20260530-meetup-1-KhewJiaPeng-AIMeetsInfrastructure`:

- `JBAgentic` — brand prefix
- `20260530` — meetup date, `YYYYMMDD`
- `meetup-1` — meetup number in the series
- `KhewJiaPeng` — speaker name, PascalCase, no spaces
- `AIMeetsInfrastructure` — the talk [**title**](#talk-title-and-subtitle) (excluding any subtitle), PascalCase, no spaces

Subtitle files reuse the full slug as their stem (`<talk-slug>.<lang>.srt`). `cover.png`, `slides.pdf`, `video-file.html`, and `youtube-content.md` use fixed names.

## Talk title and subtitle

A talk's name has up to two parts:

- **Title** — the primary name (e.g. *AI For Everyday Friction*).
- **Subtitle** — an optional secondary part (e.g. *Building a personal expense agent with Hermes and MCP*).
- **Full title** — the two joined by a colon, `Title: Subtitle` (e.g. *AI For Everyday Friction: Building a personal expense agent with Hermes and MCP*). With no subtitle, the full title is just the title (e.g. *AI Meets Infrastructure*).

How each is used:

- **Slugs use the title only.** The `<Title>` segment of the folder name is the talk title in PascalCase, with any subtitle dropped — and the subtitle-file stems reuse that segment.
- **Display and records use the full title.** The [meetup records](meetup-records.reference.md) Talks list and the YouTube metadata show the full title.

> A talk's *subtitle* here means the secondary part of its name — not the `.srt` subtitle (caption) files described above, which this doc also calls "subtitle files."

## Files

What you add by hand (**manual input**) vs. what a skill writes (**generated**):

- `<talk-slug>.en.raw.srt` — manual input (raw subtitles)
- `<talk-slug>.en.srt`, `<talk-slug>.zh-Hans.srt`, `<talk-slug>.zh-Hant.srt` — generated subtitles
- `slides.pdf` — manual input
- `slides/slide-NN.png` — generated
- `video-file.html` — generated
- `youtube-content.md` — generated
- `cover.png` — manual

## Preferred Skills

Use these skills when processing a new talk recording:

- `/subtitle-polish`
  - Input
    - raw English subtitles: `<talk-slug>.en.raw.srt`
    - domain context: `slides.pdf`, `slides/slide-NN.png` (siblings)
  - Output
    - polished subtitles: `<talk-slug>.en.srt` (input stem with `.raw` removed; sibling)
- `/subtitle-translate-zh`
  - Input
    - polished English subtitles: `<talk-slug>.en.srt`
  - Output
    - Simplified Chinese: `<talk-slug>.zh-Hans.srt` — audience: Malaysian Chinese readers
    - Traditional Chinese (Taiwan): `<talk-slug>.zh-Hant.srt` — audience: Taiwanese readers
  - The skill owns each audience's vocabulary; we only name the audiences here.
- `/slides-pdf-to-png`
  - Input
    - slide-deck: `slides.pdf`
  - Output
    - `slides/slide-NN.png`
- `/redirect-bookmark`
  - Input
    - target folder: the talk folder
    - external URL: the talk recording's Google Drive share link (`https://drive.google.com/file/d/<FILE_ID>/view?usp=drive_link`)
  - Output
    - `video-file.html` (fixed name) — meta-refresh redirect + a "committee access only" fallback link
  - Why: the multi-GB `.mov` lives in committee-only Drive and is gitignored out of the public GitHub repo; this committed stub is the durable in-repo pointer to it.
- `/series-youtube-metadata`
  - Input
    - polished English subtitles: `<talk-slug>.en.srt`
    - show profile: [meetup-info.reference.md](meetup-info.reference.md) — series identity, title suffix, content type, audience, links, footer
    - episode records: [meetup-records.reference.md](meetup-records.reference.md) — meetup number, date, full title, speaker (authoritative)
    - locator: the [Folder name](#folder-name) above — identifies the talk and where the transcript lives
  - Output
    - YouTube metadata: `youtube-content.md` — 3 A/B titles, description with 0:00 chapters, tags, and a recommended category

## Related

- [Details of past meetups — date, time, number, talks, speakers, attendance](meetup-records.reference.md)
- Pipeline runbooks — the procedures that produce the files above:
  - [Setup](talk-setup.runbook.md) — record meetup & scaffold talk folders
  - [Pre-edit prep](talk-pre-edit-prep.runbook.md) — slides → overlay frames
  - [Video edit (CapCut)](talk-video-edit.runbook.md) — manual edit handoff
  - [Post-edit processing](talk-post-edit-processing.runbook.md) — subtitles & YouTube metadata
