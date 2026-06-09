# Video edit (CapCut)

Assemble the final talk video. This phase is **fully manual** — a human edits in
CapCut, outside this workspace. It sits between [pre-edit prep](pre-edit-prep.runbook.md)
and [post-edit processing](post-edit-processing.runbook.md); see the
[project README](../README.md) for the full pipeline.

**Actor:** human editor · **In:** recorded video + slide overlays · **Out:** final video + `<talk-slug>.en.raw.srt`

> Nothing here is automated. This runbook documents the **handoff** — what the
> editor needs going in and what must come out — so the agent-run phases on either
> side line up. The CapCut steps themselves are the editor's own process.

## Inputs the editor needs

- The recorded talk video (screen capture and/or camera).
- `slides/slide-NN.png` — slide overlay frames from [pre-edit prep](pre-edit-prep.runbook.md).
- `cover.png` — if used as an intro/outro card or thumbnail (manual asset).

## Steps (manual — fill in)

> TODO: document the CapCut editing process here — timeline setup, how slide
> overlays are placed, transitions, audio cleanup, caption/auto-transcript export,
> and final export settings.

## Required outputs

These are the contract into [post-edit processing](post-edit-processing.runbook.md):

- **Final exported video** — uploaded to the committee Google Drive, then bookmarked in-repo with `/redirect-bookmark` → `video-file.html`. (The multi-GB `.mov` is gitignored out of the public repo; the stub is the durable in-repo pointer.)
- **`<talk-slug>.en.raw.srt`** — the raw English subtitles (auto-transcript) exported from the edited video. This is the manual input Phase 3 starts from.
- **`cover.png`** present in the talk folder for the YouTube thumbnail.

## Related

- [talk-recordings.reference.md](talk-recordings.reference.md) — file names and folder convention.
- [`/redirect-bookmark` SKILL.md](../../../agentic/skills/redirect-bookmark/SKILL.md) — bookmarks the Drive video as `video-file.html`.
- [post-edit-processing.runbook.md](post-edit-processing.runbook.md) — the next phase.
