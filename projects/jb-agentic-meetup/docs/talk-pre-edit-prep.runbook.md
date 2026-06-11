# Pre-edit prep

Render a talk's slide deck into overlay frames, and extract its text once for the
later glossary, before the video edit. This phase follows
[setup](talk-setup.runbook.md) and runs once per talk. See the
[project README](../README.md) for the full flow.

**Actor:** agent · **In:** `slides.pdf` · **Out:** `slides/slide-NN.png`, `slides.txt`

## Prerequisites

- The talk folder exists, created in [setup](talk-setup.runbook.md) and named to the slug convention (`JBAgentic-<YYYYMMDD>-meetup-<N>-<Speaker>-<Title>`; see [talk-recordings.reference.md](talk-recordings.reference.md)).
- `slides.pdf` — the full slide deck — is in the talk folder (dropped during [setup](talk-setup.runbook.md)).

## Steps

1. Confirm `slides.pdf` is in the talk folder.
2. Run `/slides-pdf-to-png` on the talk folder. It writes one HD frame per page to `slides/slide-NN.png`.
3. Run `/slides-png-to-text` on the talk folder. It transcribes the `slides/` PNGs from step 2 with the vision model and writes the deck's text to `slides.txt`.
4. The skills verify their own output. Spot-check that the first and last frame look right and that `slides.txt` captured the key product/tool/file names.

## Handoff

- `slides/slide-NN.png` → **[Video edit](talk-video-edit.runbook.md):** the editor drops the frames onto the CapCut timeline as slide overlays.
- `slides.txt` → **[Post-edit processing](talk-post-edit-processing.runbook.md):** `/subtitle-polish` (and `/subtitle-translate-zh`) read it as the term glossary when fixing mis-transcribed terms — far cheaper than reading the slide PNGs on every run.

## Related

- [`/slides-pdf-to-png` SKILL.md](../../../agentic/skills/slides-pdf-to-png/SKILL.md) and [`/slides-png-to-text` SKILL.md](../../../agentic/skills/slides-png-to-text/SKILL.md) — the skills this runbook drives.
- [talk-recordings.reference.md](talk-recordings.reference.md) — file names and folder convention.
- [talk-video-edit.runbook.md](talk-video-edit.runbook.md) — the next phase.
