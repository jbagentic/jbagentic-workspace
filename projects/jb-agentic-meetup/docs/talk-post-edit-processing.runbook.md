# Post-edit processing

Turn a freshly edited talk into publish-ready subtitles and YouTube metadata. This
is the last phase of the pipeline. An agent runs all of it. See the
[project README](../README.md) for the full flow.

**Actor:** agent · **In:** `<talk-slug>.en.raw.srt` + `slides/` + `cover.png` + the Drive video link · **Out:** polished + translated SRTs, `youtube-content.md`, `video-file.html`

## Prerequisites

These are ready when this phase starts, from earlier phases and manual assets:

- `<talk-slug>.en.raw.srt` — raw English subtitles from the [video edit](talk-video-edit.runbook.md).
- `slides/slide-NN.png` — from [pre-edit prep](talk-pre-edit-prep.runbook.md), used as glossary context.
- `cover.png` — the thumbnail asset.
- The **final exported video file** — handed off from the [video edit](talk-video-edit.runbook.md). It gets uploaded to Drive in this phase (step 1); the upload is *not* done yet when the phase starts.

## Steps

1. **Request the video upload (non-blocking).** Ask the user to upload the final exported video to the **JB Agentic private shared Drive** folder (`https://drive.google.com/drive/u/0/folders/1TctQRwKEBbdHkSNOevNMRzBxtMluMUwR`) and to send back the video's private share link. That link is a **required input** for step 5 — but don't wait on it. Kick this off, then start steps 2–4 while the user uploads.
2. **Polish the English subtitles** — run `/subtitle-polish`. It removes fillers and stutters, fixes mis-transcribed terms against the slides, and writes `<talk-slug>.en.srt` (the input stem with `.raw` removed).
3. **Translate to Chinese** — run `/subtitle-translate-zh`. One run writes `<talk-slug>.zh-Hans.srt` (Simplified, for Malaysian Chinese readers), then converts it to `<talk-slug>.zh-Hant.srt` (Taiwan Traditional) with OpenCC `s2twp`, correcting Malaysian localisms to Taiwan-standard forms for the Taiwanese-reader target.
4. **Write YouTube metadata** — run `/series-youtube-metadata`. It reads `<talk-slug>.en.srt` and writes `youtube-content.md` (A/B titles, description, auto-generated chapters, tags). It reads the show profile in [meetup-info.reference.md](meetup-info.reference.md) for the series suffix, links, and footer (copied verbatim), and needs the meetup number in the folder name.
5. **Bookmark the video** — once the user sends the Drive link, run `/redirect-bookmark` on the talk folder with that link. It writes `video-file.html` (fixed name) — a meta-refresh redirect plus a "committee access only" fallback link. The URL is used **byte-identical** to what the user supplied (don't rewrite the `?usp=` form). The multi-GB video stays out of the public repo; this committed stub is the durable in-repo pointer to it.

**Ordering:** Step 1 is fired first but blocks nothing — only step 5 needs its result. Steps 2–4 are the subtitle/metadata track: step 2 gates 3 and 4 (both need `<talk-slug>.en.srt`), and 3 and 4 are independent of each other (run them in parallel if you like). Step 5 runs whenever the Drive link arrives, by the end of the phase.

## Gate

Each skill checks its own output (entry counts match the source, timestamps unchanged, UTF-8 without BOM). The phase is done when the talk folder holds all of:

- `<talk-slug>.en.srt`
- `<talk-slug>.zh-Hans.srt`
- `<talk-slug>.zh-Hant.srt`
- `youtube-content.md`
- `video-file.html`
- `cover.png`

Now the talk is ready to upload to YouTube.

## Related

- [`/subtitle-polish` SKILL.md](../../../agentic/skills/subtitle-polish/SKILL.md), [`/subtitle-translate-zh` SKILL.md](../../../agentic/skills/subtitle-translate-zh/SKILL.md), [`/series-youtube-metadata` SKILL.md](../../../agentic/skills/series-youtube-metadata/SKILL.md), [`/redirect-bookmark` SKILL.md](../../../agentic/skills/redirect-bookmark/SKILL.md) — the skills this runbook drives.
- [talk-recordings.reference.md](talk-recordings.reference.md) — file names and folder convention.
- [meetup-info.reference.md](meetup-info.reference.md) — the show profile (series identity, links, footer) the metadata step reads.
