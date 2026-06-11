# Post-edit processing

Turn a freshly edited talk into publish-ready subtitles and YouTube metadata. This
is the last phase of the pipeline. An agent runs all of it. See the
[project README](../README.md) for the full flow.

**Actor:** agent · **In:** `<talk-slug>.en.raw.srt` · `slides.txt` · the Drive video link · **Out:** polished + translated SRTs, `youtube-content.md`, `video-file.html`

## Prerequisites

These are ready when this phase starts, from earlier phases and manual assets:

- `<talk-slug>.en.raw.srt` — raw English subtitles from the [video edit](talk-video-edit.runbook.md).
- `slides.txt` — from [pre-edit prep](talk-pre-edit-prep.runbook.md), the deck's extracted text used as glossary context (cheaper than reading the slide PNGs).
- `cover.png` — the thumbnail asset.
- The **final exported video file** — handed off from the [video edit](talk-video-edit.runbook.md). It gets uploaded to Drive in this phase (step 1); the upload is *not* done yet when the phase starts.

## Steps

1. **Request the video upload (non-blocking).** Ask the user to upload the final exported video to the **JB Agentic committee shared Drive** folder (committee access only: `https://drive.google.com/drive/u/0/folders/1TctQRwKEBbdHkSNOevNMRzBxtMluMUwR`) and to send back the video's share link. That link is a **required input** for step 5 — but don't wait on it. Kick this off, then start steps 2–4 while the user uploads.
2. **Polish the English subtitles** — run `/subtitle-polish`. Writes the polished file with `.raw` dropped from the stem.
   - In: `<talk-slug>.en.raw.srt` (source) · `slides.txt` (glossary context)
   - Out: `<talk-slug>.en.srt` (polished)
3. **Translate to Chinese** — run `/subtitle-translate-zh`. One run writes both files.
   - In: `<talk-slug>.en.srt` (source) · `slides.txt` (glossary context, on demand) · audiences: Malaysian Chinese readers, Taiwanese readers
   - Out: `<talk-slug>.zh-Hans.srt` (Simplified, for Malaysian Chinese readers) · `<talk-slug>.zh-Hant.srt` (Taiwan Traditional, for Taiwanese readers)
4. **Write YouTube metadata** — run `/series-youtube-metadata`.
   - In: `<talk-slug>.en.srt` (transcript source) · brand identity (series suffix, links, footer) → [meetup-info.reference.md](meetup-info.reference.md) · this talk's facts (number, date, full title, speaker) → [meetup-records.reference.md](meetup-records.reference.md) · folder name = locator only (match talk → record)
   - Out: `youtube-content.md`
5. **Bookmark the video** — once the user sends the Drive link, run `/redirect-bookmark` on the talk folder. The multi-GB video stays out of the public repo; this committed stub is the durable in-repo pointer to it.
   - In: talk folder (write destination) · the Drive video link (redirect target) · fallback link text "committee access only"
   - Out: `video-file.html`

**Ordering:**

- Step 1 — fired first, but blocks nothing; only step 5 needs its result.
- Step 2 — gates steps 3 and 4 (both need `<talk-slug>.en.srt`).
- Steps 3 & 4 — independent of each other; run them in parallel if you like.
- Step 5 — runs whenever the Drive link arrives, by the end of the phase.

## Gate

Each skill verifies its own output. The phase is done when the talk folder holds all of:

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
- [meetup-records.reference.md](meetup-records.reference.md) — the episode records (number, date, full title, speaker) the metadata step reads.
