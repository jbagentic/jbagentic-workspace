---
name: series-youtube-metadata
description: >-
  Generate YouTube publishing metadata for a recorded long-form spoken-word
  video — a talk, podcast episode, demo, story, or knowledge video — from its
  transcript and the project's show profile: three A/B-test titles, a
  description with auto-generated chapters, tags, and a category, written to
  `youtube-content.md` in the recording's own folder. Use whenever the user
  wants YouTube titles, descriptions, chapters, tags, or "youtube
  content/metadata" for a talk, episode, or recording, hands over a recording
  folder to publish, or asks to prepare a meetup talk or podcast episode for
  upload — even if they don't name the file. Not for cleaning or polishing
  subtitles (use subtitle-polish) or translating subtitles (use
  subtitle-translate-zh).
---

# Generating YouTube metadata for a recorded video

Turn a recorded video into upload-ready YouTube metadata. The recording already happened; everything you need is in its folder (the transcript), the show's **episode records** (this episode's facts), and the project's **show profile** (brand identity, audience, links). The job is to package it for discovery, not to invent anything.

## Input

- **Recording folder** — holds the English transcript `*.en.srt`. Its name is a **locator**, not the source of truth: it identifies which episode this is (so you can find its record) and where the transcript lives.
  - Default naming scheme: `<Series>-<YYYYMMDD>-<NN>-<Person>-<Title>/`; the project defines its own in the show profile.
  - The title segment is usually abbreviated (subtitle dropped, PascalCase) — take the accurate, full title from the episode records, never the folder slug.
- **Episode records** — the show's per-episode log (a reference doc the project supplies), the source of truth for this episode's facts: its **number**, **date**, **full title** (with any subtitle), and **people** (speaker / host / guest), correctly spelled and cased. Match the recording to its record using the folder's locator, then read these facts from there. If you can't identify the record — or the show numbers episodes and the number is missing — ask rather than guess.
- **Show profile** — the project's reference doc(s), the single source of truth for anything brand-specific. The installing project supplies it (e.g. its own meetup or show reference doc); if it's missing, ask rather than invent. It provides:
  - **Series identity** — name, episode-number scheme, and the **title suffix** to append.
  - **Content type & role vocabulary** — e.g. talk → "Speaker"; podcast → "Host" / "Guest".
  - **Audience** — who searches for this, so titles and tags match their words.
  - **Links & footer** — canonical URLs and the verbatim description footer. Copy byte-for-byte; don't paraphrase.
- **Helper (suggested)** — `scripts/srt_digest.py <folder>` prints the cleaned transcript and a timestamp-bucketed timeline in one pass — the raw material for titles and chapters. It also parses the folder name as a locator hint, but the episode records stay authoritative for the facts.

## Output

- **Output file** — written inside the recording folder (sibling to the SRTs); default name `youtube-content.md`, or whatever the show profile sets. Sections, in order: full title → 3 A/B-test titles → description (copy-paste ready) → tags → category.
- Invariants (these are what make the output usable on YouTube):
  - Exactly **3 titles**, each ≤ ~70 characters *including* the show profile's title suffix, with the searchable keyword ahead of the suffix so it survives the ~60-char search truncation. The 3 test **different angles** (e.g. keyword / curiosity / benefit), not reworded twins — otherwise the A/B test teaches nothing.
  - **Chapters** begin at `0:00`, have ≥3 markers spaced ≥10s apart, and are derived from the `.en.srt` timestamps.
  - **Description** follows the fixed shape: one short hook paragraph → the content-type lead line (`<emoji> <Type>: "<title>" by <Role>`) → the series identity line (`📍 <series + number> — <date>`) → *What's covered* → *Chapters* → the footer (verbatim from the profile) → hashtags. No reader-facing timestamp caveat.
  - **Tags** are comma-separated and total < 500 characters (YouTube's limit).
  - Title suffix, links, and footer are byte-identical to the show profile.
  - **Category** is the single most fitting YouTube category, chosen by the skill from the content — the skill's own recommendation, not a project input or a fixed default.

## Workflow

1. **Digest the folder.** Run `scripts/srt_digest.py <folder>` (suggested) for the cleaned transcript and a bucketed timeline. Treat the folder name as a locator — it tells you which episode this is, not the facts about it.

2. **Get the facts, understand the content.** Read this episode's **number, date, full title, and people** from the show's episode records — authoritative, not the folder slug (which drops the subtitle and abbreviates). Then from the transcript, pin down what was actually demoed/argued/told and the terms the profile's audience would actually search. Discovery comes from matching real search language, so prefer the audience's words over the speaker's slide wording.

3. **Write 3 A/B titles as 3 hypotheses.** Front-load the keyword, append the show profile's title suffix. Make each variant test a genuinely different bet — a keyword/SEO framing, a curiosity hook, and a concrete-benefit/outcome framing — because YouTube's Test & Compare promotes a winner by watch time, and you only learn something if the variants differ in kind. Keep the searchable part before ~60 characters.

4. **Build chapters from the timeline.** Segment the bucketed timeline at topic shifts into ~8–13 chapters that span both the main content and any Q&A; the first must be `0:00`. Anchor each timestamp to a real cue in the `.en.srt`, not the 45s bucket boundary, and keep titles short and scannable. Don't add a reader-facing caveat about timestamps assuming where the cut starts — it's noise to a viewer.

5. **Write the description in this exact shape.** Lead with **one short hook paragraph** (2–3 sentences) that front-loads the searchable keyword and lands the core idea or tension — this is the slice YouTube indexes and shows before "…more", so no greeting and no preamble, just the hook. Then the structured block below. Pull the footer **verbatim from the show profile's footer blurb** — never retype the links from memory. Close with 3–5 hashtags, most important first; never a number-only hashtag like `#1` (YouTube won't linkify it).

   ```
   <one short hook paragraph — keyword-forward, lands the core idea>

   <emoji> <Type>: "<full title>" by <Role(s)>
   📍 <series name> #<N> — <D Mon YYYY>

   What's covered:
   • <5–7 concrete bullets drawn from the content>

   Chapters:
   0:00 <…>
   <…>

   <footer — verbatim from the show profile>

   #Tag #Tag #Tag #Tag #Tag
   ```

   The lead line and series line draw from the episode records and the show profile: the **full title** and **people** come from the records; the content-type label and role vocabulary (e.g. `🎤 Talk: "<title>" by <Speaker>`, or `🎙️ Podcast: "<title>" with <Host> & <Guest>`) and the series name come from the profile; the number comes from the records; format the date as `D Mon YYYY` (e.g. `30 May 2026`). A `Tech stack: …` line between *What's covered* and *Chapters* is optional — add it only when the content leans on a specific stack worth surfacing.

6. **Write tags.** 12–15 tags mixing broad reach terms with specific ones lifted from the transcript (tools, techniques, frameworks named in the content). Keep the total under 500 characters.

7. **Choose the category, write the output, and verify.** Pick the single most fitting YouTube category for the content — your call as the YouTube expert, not a project input. Save the output into the recording folder (default name `youtube-content.md`), then check the invariants: count titles and their character lengths, confirm tag total < 500, and confirm chapters start at 0:00 and are ordered. Fix anything that fails before reporting done.

## Conventions

- The series suffix, identity, links, footer, and audience live in the show profile, not here — pull them each run so a change there propagates. If you find yourself typing a URL, a suffix, or a blurb from memory, stop and read the profile.
- Per-episode facts — number, date, full title, people — come from the show's episode records, not the folder slug (it drops the subtitle and abbreviates). The folder name only locates the episode.
- An episode number in a title (e.g. `#N`) is a literal label, not a hashtag.
- English only. Any non-English SRTs in the folder are out of scope for this skill.
- Don't invent facts. If you can't match the recording to its record, or a needed fact is missing there, ask.
