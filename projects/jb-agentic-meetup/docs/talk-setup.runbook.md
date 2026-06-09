# Setup (new meetup)

Bring a new meetup into the pipeline: record it, then scaffold a talk-recording
folder for each of its talks. This is the first phase — it runs once per meetup and
fans out to one folder per talk. See the [project README](../README.md) for the full flow.

**Actor:** human, then agent · **In:** meetup details (date, number, talks) · **Out:** updated records + one empty folder per talk

## Prerequisites

- A confirmed meetup: its date, meetup number `N`, and the list of talks (each talk's title and speaker).

## Steps

1. **Record the meetup (human).** Append a new `## JB Agentic Meetup #N — YYYY-MM-DD` section to [meetup-records.reference.md](meetup-records.reference.md) — newest at the top — with the time, location, guest count, and a numbered **Talks** list (each entry `Full Title — Speaker`, where the full title is `Title: Subtitle` and the [talk subtitle](talk-recordings.reference.md#talk-title-and-subtitle) is optional). This record is the source of truth the folder names derive from.
2. **Scaffold the talk folders (agent).** From that record, create one folder per talk under `talk-recordings/`, each named to the slug convention `JBAgentic-<YYYYMMDD>-meetup-<N>-<Speaker>-<Title>` — speaker and the talk [**title**](talk-recordings.reference.md#talk-title-and-subtitle) (the title only, excluding any subtitle) in PascalCase, no spaces. See [talk-recordings.reference.md](talk-recordings.reference.md) for the slug rules. The folders start empty; a human reviews the names against the record.

## Handoff

Each empty talk folder is ready for [pre-edit prep](talk-pre-edit-prep.runbook.md): a human drops `slides.pdf` into it (and, after the edit, the `<talk-slug>.en.raw.srt`), and the per-talk phases take over from there.

## Related

- [meetup-records.reference.md](meetup-records.reference.md) — where the meetup and its talks are recorded (step 1).
- [talk-recordings.reference.md](talk-recordings.reference.md) — the folder slug convention step 2 follows.
- [talk-pre-edit-prep.runbook.md](talk-pre-edit-prep.runbook.md) — the next phase.
