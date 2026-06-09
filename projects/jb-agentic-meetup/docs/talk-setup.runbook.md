# Setup (new meetup)

Bring a new meetup into the pipeline: record it, scaffold a talk-recording folder for
each of its talks, and seed each folder with its slide deck. This is the first phase —
it runs once per meetup and fans out to one folder per talk. See the
[project README](../README.md) for the full flow.

**Actor:** human + agent · **In:** meetup details (date, number, talks) + each talk's `slides.pdf` · **Out:** updated records + one folder per talk, each holding its `slides.pdf`

## Prerequisites

- A confirmed meetup: its date, meetup number `N`, and its list of talks (each talk's full title and speaker).
- Each talk's `slides.pdf` (the full slide deck) — needed for step 3.

## Steps

1. **Record the meetup (human).** Append a new `## JB Agentic Meetup #N — YYYY-MM-DD` section to [meetup-records.reference.md](meetup-records.reference.md) — newest at the top — with the time, location, guest count, and a numbered **Talks** list (each entry `Full Title — Speaker`, where the full title is `Title: Subtitle` and the [talk subtitle](talk-recordings.reference.md#talk-title-and-subtitle) is optional). This record is the source of truth the folder names derive from.
2. **Scaffold the talk folders (agent).** From that record, create one folder per talk under `talk-recordings/`, each named to the slug convention `JBAgentic-<YYYYMMDD>-meetup-<N>-<Speaker>-<Title>` — speaker and the talk [**title**](talk-recordings.reference.md#talk-title-and-subtitle) (the title only, excluding any subtitle) in PascalCase, no spaces. See [talk-recordings.reference.md](talk-recordings.reference.md) for the slug rules. A human reviews the names against the record.
3. **Add each talk's slides (human).** Drop the talk's `slides.pdf` — the full slide deck — into its folder.

## Handoff

Each talk folder now holds its `slides.pdf` and is ready for [pre-edit prep](talk-pre-edit-prep.runbook.md). The remaining files — raw subtitles (from the [video edit](talk-video-edit.runbook.md)), the cover image, and all generated outputs — are added by the later phases.

## Related

- [meetup-records.reference.md](meetup-records.reference.md) — where the meetup and its talks are recorded (step 1).
- [talk-recordings.reference.md](talk-recordings.reference.md) — the folder slug convention step 2 follows.
- [talk-pre-edit-prep.runbook.md](talk-pre-edit-prep.runbook.md) — the next phase.
