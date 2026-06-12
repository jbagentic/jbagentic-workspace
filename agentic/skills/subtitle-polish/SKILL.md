---
name: subtitle-polish
description: Polish SRT subtitles from a recorded talk or other spoken-word video — strip fillers, stutters, starters, and discourse particles (um, uh, like, lah, ya) by default, fix mis-transcribed terms (product names, file names, acronyms, jargon) against a domain context (slide deck, abstract, README), and translate any non-English speech into English so the track is fully readable. Works the whole file in one context across multiple review passes — no chunking. Use whenever the user mentions cleaning, polishing, fixing, or correcting an SRT, VTT, or subtitle/caption/transcript file — even if they don't name a specific operation. Also use when handed a talk folder containing both a transcript and slides.
---

# Polishing subtitles

## Input
- A raw, unpolished subtitle file (SRT/VTT) for a talk. Default convention: a `*.raw.srt` file; a project may define another via its own reference doc.
- Its domain context for the glossary — **required, not optional.** It is what makes mis-transcription detection possible. Prefer the slide deck's pre-extracted text when the project provides one (e.g. `slides.txt` — cheap to read); otherwise fall back to the slide-deck PDF, slide PNGs, abstract, or README. Discover alongside the subtitle file per the project's layout; ask only if nothing is found.
- Optional caller directive — **"keep the speaker's voice."** When the caller flags this talk as voice-preserving, retain the discourse particles (still strip um/uh, stutters, and starters). The default, with no such directive, is to remove the particles too.

## Output
- The polished subtitle file, named and placed per the project's subtitle-file convention. Default: a sibling of the input with the `.raw` marker removed from the stem (e.g. `foo.en.raw.srt` → `foo.en.srt`). The original raw file stays untouched.
- Invariants: no empty subtitles, no numbering holes, timestamps and encoding (UTF-8 without BOM) unchanged from the source. Light readability edits move *text* within and across adjacent cues but never change a timestamp; a cue emptied by edits is dropped and the file renumbered.
- **Fully English.** Any non-English speech in the source is rendered in English (see the workflow for why).

## Workflow

Work the **whole file in one context**, top to bottom, across **several sequential passes** — never chunk it across parallel subagents. The quality lives in cross-cue consistency: a term mis-heard in cue 12 and again in cue 400 must be fixed the same way both times, and a stutter straddling a cue boundary needs both cues in view. Chunking and one-and-done passes both break that.

1. **Ground: name the field, then harvest the private terms (first).** Read the domain context — prefer `slides.txt`, else slide PNGs/PDF, abstract, or README — and do two things. First, **name the talk's field** (e.g. AI coding agents, molecular biology, options trading). That unlocks your own knowledge of the field's standard jargon — tools, libraries, acronyms, well-known people — and *that* is your glossary for anything public: you know the canonical spelling, so you can recover a mishearing (`Cortez` → `Codex`) even when it never reaches a slide. Second, harvest from the materials the **private terms you couldn't otherwise know** — the speaker's product and app names, internal tools, file names, their own name — in exact case; for these the materials are authoritative. Highest-confidence sources are slide bullets (not titles), inline-code spans, and file names with extensions. This step is mandatory; the fixes in later passes depend on it.

2. **First pass — correct (whole file, top to bottom).** Make every edit in one read:
   - **Strip fillers and starters** — `um`, `uh`, `er`, false starts, restarts, abandoned fragments, and empty discourse markers (`like`, `you know`, `I mean` when they carry no meaning — keep `like` when it's a verb or preposition: "I like X", "tools like X").
   - **Remove discourse particles** — `lah`, `la`, `ya`, `leh`, `lor`, `meh` — by default. (If the caller asked to keep the speaker's voice, leave them.)
   - **Collapse stutters and duplicate words** across the flat token stream — they often straddle subtitle boundaries.
   - **Fix mis-transcribed terms** from the glossary — phonetic mishearings only, the speaker's words win, default to keep (see Conventions).
   - **Light readability** — sentence capitalization, terminal punctuation, and small word shifts across adjacent cues so lines read as clean sentences. Don't restructure timing.
   - **Translate any non-English speech to English.** When the speaker code-switches into another language (Chinese, Malay, etc.), render its meaning in English in that cue, keeping the timing. *Why:* an English-only viewer turns on this track precisely because they can't follow the other language — leaving the original script on screen fails them at the one moment captions are for. Keep proper nouns and glossary terms canonical.
   - Drop any cue emptied by edits and renumber — leave no holes.

3. **Review passes — repeat until clean.** Re-read the whole result fresh and fix residuals: a filler missed the first time, a term corrected in one cue but not another, a stutter across a boundary, an awkward line. Repeat the full-file read each pass and **stop when a pass makes no substantive change** (expect about two to three passes). This loop is the heart of the quality; one pass reliably misses things.

4. **Final invariant check (mechanical, last).** Confirm the Output invariants all hold.

## Conventions

**Remove by default.** Most speakers here are not professional and lean heavily on these; on a subtitle, which is *read* not heard, they are noise:
- Fillers — `um`, `uh`, `er`.
- Starters, false starts, restarts, abandoned fragments.
- Empty discourse markers — `like`, `you know`, `I mean` — only when meaningless; keep a meaningful `like`.
- **Discourse particles** — `lah`, `la`, `ya`, `leh`, `lor`, `meh`. Speakers from Malaysia and Singapore lean on these, but they're ~99% verbal habit that reading doesn't need. Removed by default.

**Opt-out** — when the caller says to keep the speaker's voice: keep the discourse particles as character, but still strip `um`/`uh`, stutters, false starts, and empty English fillers. The opt-out preserves voice, not noise.

**Keep — don't touch:**
- Affirmations that carry meaning (`yeah`, `oh`, `okay` as real responses).
- Regional syntax, casual contractions, and code-switched *words inside an English sentence* — how the speaker talks, not errors. (A passage spoken *in* another language is the opposite case — translate it; see the workflow.)
- The speaker's word choices, even when they diverge from the slides. A speaker is free to depart from their own deck; that divergence is not a transcription error. Supporting materials recover what the transcriber mangled — misheard *sounds* — not off-script *choices*.

**Mis-transcription discipline.** Apply the glossary to recover mis-heard sounds, not off-slide word choices. Replace a token only when it is a phonetic mishearing (same syllable skeleton) of a private term from the materials or the field's standard jargon you know, restoring the canonical case. **Default to keep** — only fix what has a path: misheard sound → wrong word → correct term. For a term that's *in the materials*, the spelling is authoritative. For a term that's only *field knowledge* (not on the slides), fix it only when the local context confirms the referent — it sits among peers of the same kind, so the sound resolves to one obvious name (e.g. a tool named beside "Claude" and "Cursor" resolves a misheard "Cortez" to "Codex"); an isolated odd word with nothing to confirm it stays put. Don't smooth grammar or off-script content. For words with legitimate alternate meanings, replace only inside a verified phrase context — no bare global swaps.
