# Pre-edit prep

Render a talk's slide deck into overlay frames before the video edit. This phase
follows [setup](talk-setup.runbook.md) and runs once per talk. See the
[project README](../README.md) for the full flow.

**Actor:** agent · **In:** `slides.pdf` · **Out:** `slides/slide-NN.png`

## Prerequisites

- The talk folder exists, created in [setup](talk-setup.runbook.md) and named to the slug convention (`JBAgentic-<YYYYMMDD>-meetup-<N>-<Speaker>-<Title>`; see [talk-recordings.reference.md](talk-recordings.reference.md)).
- `slides.pdf` — the full slide deck — is in the talk folder (dropped during [setup](talk-setup.runbook.md)).

## Steps

1. Confirm `slides.pdf` is in the talk folder.
2. Run `/slides-pdf-to-png` on the talk folder. It writes one HD frame per page to `slides/slide-NN.png`.
3. The skill verifies its own output. Spot-check that the first and last frame look right.

## Handoff

`slides/slide-NN.png` feeds two later phases:

- **[Video edit](talk-video-edit.runbook.md):** the editor drops the frames onto the CapCut timeline as slide overlays.
- **[Post-edit processing](talk-post-edit-processing.runbook.md):** `/subtitle-polish` reads them as glossary and domain context when fixing mis-transcribed terms.

## Related

- [`/slides-pdf-to-png` SKILL.md](../../../agentic/skills/slides-pdf-to-png/SKILL.md) — the skill this runbook drives.
- [talk-recordings.reference.md](talk-recordings.reference.md) — file names and folder convention.
- [talk-video-edit.runbook.md](talk-video-edit.runbook.md) — the next phase.
