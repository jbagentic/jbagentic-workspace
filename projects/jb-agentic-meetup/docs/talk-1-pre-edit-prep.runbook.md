# Pre-edit prep

Render a talk's slide deck into overlay frames before the video edit. This is the
first phase of the talk-recording pipeline — see the [project README](../README.md)
for the full flow.

**Actor:** agent · **In:** `slides.pdf` · **Out:** `slides/slide-NN.png`

## Prerequisites

- The talk folder exists and is named to convention (`JBAgentic-<YYYYMMDD>-meetup-<N>-<Speaker>-<Topic>`). See [talk-recordings.reference.md](talk-recordings.reference.md).
- `slides.pdf` — the full slide deck — is placed in the talk folder (manual input).

## Steps

1. Confirm `slides.pdf` is in the talk folder.
2. Run `/slides-pdf-to-png` on the talk folder. It renders one HD PNG per page to `slides/slide-NN.png` (1080p, zero-padded, 1-based) and clears any stale `slide-*.png` first.
3. The skill self-verifies that the PNG count equals the PDF page count and the frame numbers are contiguous. Spot-check that the first and last frame look right.

## Handoff

`slides/slide-NN.png` feeds two later phases:

- **Phase 2 — [video edit](talk-2-video-edit.runbook.md):** the editor drops the frames onto the CapCut timeline as slide overlays.
- **Phase 3 — [post-edit processing](talk-3-post-edit-processing.runbook.md):** `/subtitle-polish` reads them as glossary/domain context when fixing mis-transcribed terms.

## Related

- [`/slides-pdf-to-png` SKILL.md](../../../agentic/skills/slides-pdf-to-png/SKILL.md) — the skill this runbook drives.
- [talk-recordings.reference.md](talk-recordings.reference.md) — file names and folder convention.
- [talk-2-video-edit.runbook.md](talk-2-video-edit.runbook.md) — the next phase.
