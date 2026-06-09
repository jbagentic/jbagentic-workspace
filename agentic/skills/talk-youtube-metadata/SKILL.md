---
name: talk-youtube-metadata
description: >-
  Generate YouTube publishing metadata for a recorded JB Agentic talk — three
  A/B-test titles, a description with auto-generated chapters, tags, and a
  category — written to `youtube-content.md` in the talk's own folder. Use
  whenever the user wants YouTube titles, descriptions, chapters, tags, or
  "youtube content/metadata" for a talk or recording, hands over a talk folder to
  publish, or asks to prepare a meetup talk for upload — even if they don't name
  the file. Not for cleaning or polishing subtitles (use subtitle-polish) or
  translating subtitles (use subtitle-translate-zh).
---

# Generating YouTube metadata for a talk

Turn a recorded talk into upload-ready YouTube metadata. The talk already happened; everything you need is in its folder (the transcript) and in the community knowledge atom (links, blurbs, series number). The job is to package it for discovery, not to invent anything.

## Input

- A talk folder named `JBAgentic-<YYYYMMDD>-meetup-<N>-<Speaker>-<Title>/` containing the English transcript `*.en.srt`. The folder name encodes the date, meetup number, speaker, and title (the talk title, excluding any subtitle). If `meetup-<N>` is missing from the name, ask for the number rather than guessing — it drives the title suffix and can't be derived from the transcript.
- Community facts, canonical links, and ready-made blurbs — the **knowledge atom**. This is the single source of truth for the series suffix, the Luma/YouTube links, and the short/long blurbs. Copy them verbatim — don't paraphrase. The installing project supplies it (e.g. its own meetup reference doc); if it isn't provided, ask for it rather than inventing links or blurbs.
- Suggested helper: `scripts/srt_digest.py <talk-folder>` prints the parsed folder metadata, the cleaned transcript, and a timestamp-bucketed timeline in one pass — the raw material for titles and chapters. Use it so you're not re-deriving timestamps by hand each run.

## Output

- `youtube-content.md` written **inside the talk folder** (sibling to the SRTs). Sections, in order: original talk title → 3 A/B-test titles → description (copy-paste ready) → tags → category.
- Invariants (these are what make the output usable on YouTube):
  - Exactly **3 titles**, each ≤ ~70 characters *including* the ` | JB Agentic Meetup #N` suffix, with the searchable keyword ahead of the suffix so it survives the ~60-char search truncation. The 3 test **different angles** (e.g. keyword / curiosity / benefit), not reworded twins — otherwise the A/B test teaches nothing.
  - **Chapters** begin at `0:00`, have ≥3 markers spaced ≥10s apart, and are derived from the `.en.srt` timestamps.
  - **Description** follows the fixed shape: one short hook paragraph → `🎤 Talk: "<title>" by <Speaker>` → `📍 JB Agentic Meetup #<N> — <D Mon YYYY>` → *What's covered* → *Chapters* → the `📅`/`👉` footer → hashtags. No reader-facing timestamp caveat.
  - **Tags** are comma-separated and total < 500 characters (YouTube's limit).
  - Links and blurbs are byte-identical to the knowledge atom.
  - **Category** defaults to `Science & Technology`.

## Workflow

1. **Digest the folder.** Run `scripts/srt_digest.py <folder>` (suggested) to parse the name into date / meetup # / speaker / title and to get the cleaned transcript plus a bucketed timeline. If the name lacks `meetup-<N>`, ask before continuing.

2. **Understand the talk.** From the transcript, pin down what was actually demoed/argued, the speaker's own working title (often stated in the first minute), and the terms a Malaysian/Singaporean software practitioner would actually search. Discovery comes from matching real search language, so prefer the audience's words over the speaker's slide wording.

3. **Write 3 A/B titles as 3 hypotheses.** Front-load the keyword, append ` | JB Agentic Meetup #N`. Make each variant test a genuinely different bet — a keyword/SEO framing, a curiosity hook, and a concrete-benefit/outcome framing — because YouTube's Test & Compare promotes a winner by watch time, and you only learn something if the variants differ in kind. Keep the searchable part before ~60 characters.

4. **Build chapters from the timeline.** Segment the bucketed timeline at topic shifts into ~8–13 chapters that span both the talk and the Q&A; the first must be `0:00`. Anchor each timestamp to a real cue in the `.en.srt`, not the 45s bucket boundary, and keep titles short and scannable. Don't add a reader-facing caveat about timestamps assuming where the cut starts — it's noise to a viewer.

5. **Write the description in this exact shape.** Lead with **one short hook paragraph** (2–3 sentences) that front-loads the searchable keyword and lands the talk's core idea or tension — this is the slice YouTube indexes and shows before "…more", so no greeting and no preamble, just the hook. Then the structured block below. Pull the `📅`/`👉` footer **verbatim from the knowledge atom's "YouTube description footer" blurb** — never retype the links from memory. Close with 3–5 hashtags, most important first; never a number-only hashtag like `#1` (YouTube won't linkify it).

   ```
   <one short hook paragraph — keyword-forward, lands the talk's core idea>

   🎤 Talk: "<original talk title>" by <Speaker Name>
   📍 JB Agentic Meetup #<N> — <D Mon YYYY>

   What's covered:
   • <5–7 concrete bullets drawn from the talk>

   Chapters:
   0:00 <…>
   <…>

   📅 JB Agentic is a friendly community in Johor Bahru for people building software with AI. We meet on the 4th Saturday of every month. Join the next one: https://lu.ma/jbagentic

   👉 Subscribe for more talks: https://www.youtube.com/@jbagentic

   #Tag #Tag #Tag #Tag #Tag
   ```

   The `🎤`/`📍` lines come from the parsed folder + transcript: the speaker's *original* talk title in quotes, the meetup number, and the date formatted as `D Mon YYYY` (e.g. `30 May 2026`). A `Tech stack: …` line between *What's covered* and *Chapters* is optional — add it only when the talk leans on a specific stack worth surfacing.

6. **Write tags.** 12–15 tags mixing broad reach terms with specific ones lifted from the transcript (tools, techniques, frameworks named in the talk). Keep the total under 500 characters.

7. **Write `youtube-content.md` and verify.** Save into the talk folder, then check the invariants: count titles and their character lengths, confirm tag total < 500, and confirm chapters start at 0:00 and are ordered. Fix anything that fails before reporting done.

## Conventions

- The series suffix, links, and blurbs live in the knowledge atom, not here — pull them each run so a change there propagates. If you find yourself typing a Luma URL or a blurb from memory, stop and read the atom.
- `#N` in a title is a literal label ("number N"), not a hashtag.
- English only. The Chinese SRTs in the folder are out of scope for this skill.
- Don't invent talk facts. If the original title or the speaker's name can't be read confidently from the folder name or transcript, ask.
