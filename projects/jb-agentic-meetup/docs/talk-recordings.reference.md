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

The folder name is the talk slug, e.g. `JBAgentic-20260530-meetup-1-KhewJiaPeng-AIMeetsInfrastructure`:

- `JBAgentic` — brand prefix
- `20260530` — meetup date, `YYYYMMDD`
- `meetup-1` — meetup number in the series
- `KhewJiaPeng` — speaker name, PascalCase, no spaces
- `AIMeetsInfrastructure` — talk title, PascalCase, no spaces

Subtitle files reuse the full slug as their stem (`<talk-slug>.<lang>.srt`). `cover.png`, `slides.pdf`, `video-file.html`, and `youtube-content.md` use fixed names.

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
    - Simplified Chinese: `<talk-slug>.zh-Hans.srt`
    - Traditional Chinese (Taiwan): `<talk-slug>.zh-Hant.srt`
  - Audience: Malaysian Chinese readers — prefer vocabulary they'd naturally use (令吉 for ringgit, 巴仙 for percent); avoid mainland-only idioms when a more universal phrasing exists.
- `/slides-pdf-to-png` — `slides.pdf` → `slides/slide-NN.png`
- `/redirect-bookmark`
  - Input
    - target folder: the talk folder
    - external URL: the talk recording's Google Drive share link (`https://drive.google.com/file/d/<FILE_ID>/view?usp=drive_link`)
  - Output
    - `video-file.html` (fixed name) — meta-refresh redirect + a "committee access only" fallback link
  - Why: the multi-GB `.mov` lives in committee-only Drive and is gitignored out of the public GitHub repo; this committed stub is the durable in-repo pointer to it.
- `/talk-youtube-metadata` — reads `<talk-slug>.en.srt` → writes `youtube-content.md`

## Related

- [Details of past meetups — date, time, number, talks, speakers, attendance](meetup-records.reference.md)
