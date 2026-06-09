# Project Guide: JB Agentic Meetup

## About

The project folder for the JB Agentic Meetup — brand facts, past-meetup records, and the assets for each talk recording.

## Structure

| Folder | What it holds |
|--------|---------------|
| [`docs/`](docs/) | Reference docs — brand facts, past-meetup records, and the talk-recording convention (see the manifest below). |
| [`talk-recordings/`](talk-recordings/) | Per-talk recording assets, one folder per talk — subtitles, slides, video link, cover image, and more. |

## Talk recording pipeline

How a recorded talk becomes a published video, in four phases. Each links to its runbook.

1. **[Setup (new meetup)](docs/talk-setup.runbook.md)** — *human, then agent.* Meetup details → updated records + one empty talk folder per talk.
2. **[Pre-edit prep](docs/talk-pre-edit-prep.runbook.md)** — *agent.* `slides.pdf` → `slides/slide-NN.png` overlay frames.
3. **[Video edit (CapCut)](docs/talk-video-edit.runbook.md)** — *human, manual.* Recorded video + overlays → final video + raw English subtitles (`.en.raw.srt`).
4. **[Post-edit processing](docs/talk-post-edit-processing.runbook.md)** — *agent.* `.en.raw.srt` → polished + translated subtitles and `youtube-content.md`, ready to upload.

## Docs Manifest

- [Facts about the meetup brand — facts, links, social, blurbs](docs/meetup-info.reference.md)
- [Details of past meetups — talk titles, speaker names, meetup number, date, time, attendance](docs/meetup-records.reference.md)
- [Talk recording file/folder convention — folder layout, naming, which skill makes each file](docs/talk-recordings.reference.md)
- [Setup runbook — record a new meetup and scaffold its talk folders](docs/talk-setup.runbook.md)
- [Pre-edit prep runbook — render slides.pdf into slide-NN.png overlay frames](docs/talk-pre-edit-prep.runbook.md)
- [Video edit (CapCut) runbook — manual edit handoff: inputs needed and outputs to produce](docs/talk-video-edit.runbook.md)
- [Post-edit processing runbook — polish and translate subtitles, then write YouTube metadata](docs/talk-post-edit-processing.runbook.md)
