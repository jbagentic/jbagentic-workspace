---
name: subtitle-polish
description: Polish SRT subtitles from a recorded talk or other spoken-word video — strip fillers, stutters, starters, and discourse particles (um, uh, like, lah, ya) by default, then fix mis-transcribed terms (product names, file names, acronyms, jargon) against a domain context (slide deck, abstract, README). Works the whole file in one context across multiple review passes — no chunking. Use whenever the user mentions cleaning, polishing, fixing, or correcting an SRT, VTT, or subtitle/caption/transcript file — even if they don't name a specific operation. Also use when handed a talk folder containing both a transcript and slides.
---

# Polishing subtitles

## Input
- A raw, unpolished subtitle file (SRT/VTT) for a talk. Default convention: a `*.raw.srt` file; a project may define another via its own reference doc.
- Its domain context for the glossary — **required, not optional.** It is what makes mis-transcription detection possible. Prefer the slide deck's pre-extracted text when the project provides one (e.g. `slides.txt` — cheap to read); otherwise fall back to the slide-deck PDF, slide PNGs, abstract, or README. Discover alongside the subtitle file per the project's layout; ask only if nothing is found.
- Optional caller directive — **"keep the speaker's voice."** When the caller flags this talk as voice-preserving, retain the discourse particles (still strip um/uh, stutters, and starters). The default, with no such directive, is to remove the particles too.

## Output
- The polished subtitle file, named and placed per the project's subtitle-file convention. Default: a sibling of the input with the `.raw` marker removed from the stem (e.g. `foo.en.raw.srt` → `foo.en.srt`). The original raw file stays untouched.
- Invariants: no empty subtitles, no numbering holes, timestamps and encoding (UTF-8 without BOM) unchanged from the source. Light readability edits move *text* within and across adjacent cues but never change a timestamp; a cue emptied by edits is dropped and the file renumbered.

## Workflow

Work the **whole file in one context**, top to bottom, across **several sequential passes** — never split it into chunks for parallel subagents. Both rules exist for the same reason: the quality lives in cross-cue consistency. A term mis-heard in cue 12 and again in cue 400 must be fixed the same way both times; a stutter straddling a cue boundary needs both cues in view; the same filler missed on one read gets caught on the next. Chunking and one-and-done passes both break that.

1. **Ground in the domain context (first).** Read the domain context — prefer `slides.txt`, else slide PNGs/PDF, abstract, or README — and build a glossary of canonical terms: product/app names, file names, acronyms, jargon, people's names. Record each in its exact case; that's the spelling you'll restore. Highest-confidence sources are slide bullets (not titles), inline-code spans, file names with extensions, and the intro slide. Absorb what the talk is *about* — that topical grounding is what flags a mis-transcription later. This step is mandatory; the fixes in later passes depend on it.

2. **First pass — correct (whole file, top to bottom).** Make every edit in one read:
   - **Strip fillers and starters** — `um`, `uh`, `er`, false starts, restarts, abandoned fragments, and empty discourse markers (`like`, `you know`, `I mean` when they carry no meaning — keep `like` when it's a verb or preposition: "I like X", "tools like X").
   - **Remove discourse particles** — `lah`, `la`, `ya`, `leh`, `lor`, `meh` — by default. (If the caller asked to keep the speaker's voice, leave them.)
   - **Collapse stutters and duplicate words** across the flat token stream — they often straddle subtitle boundaries.
   - **Fix mis-transcribed terms** from the glossary — phonetic mishearings only, the speaker's words win, default to keep (see Conventions).
   - **Light readability** — sentence capitalization, terminal punctuation, and small word shifts across adjacent cues so lines read as clean sentences. Don't restructure timing.
   - Drop any cue emptied by edits and renumber — leave no holes.

3. **Review passes — repeat until clean.** Re-read the whole result fresh and fix residuals: a filler missed the first time, a term corrected in one cue but not another, a stutter across a boundary, an awkward line. Repeat the full-file read each pass and **stop when a pass makes no substantive change** (converged — expect about two to three passes). This loop is the heart of the quality; one pass reliably misses things. Always sequential, in the same context.

4. **Final invariant check (mechanical, last).** Confirm the output invariants hold: no empty subtitles, no numbering holes, timestamps and encoding unchanged from the source.

## Conventions

**Remove by default.** Most speakers here are not professional and lean heavily on these; on a subtitle, which is *read* not heard, they are noise:
- Fillers — `um`, `uh`, `er`.
- Starters, false starts, restarts, abandoned fragments.
- Empty discourse markers — `like`, `you know`, `I mean` — only when meaningless; keep a meaningful `like`.
- **Discourse particles** — `lah`, `la`, `ya`, `leh`, `lor`, `meh`. Speakers from Malaysia and Singapore lean on these, but they're ~99% verbal habit that reading doesn't need. Removed by default.

**Opt-out** — when the caller says to keep the speaker's voice: keep the discourse particles as character, but still strip `um`/`uh`, stutters, false starts, and empty English fillers. The opt-out preserves voice, not noise.

**Keep — don't touch:**
- Affirmations that carry meaning (`yeah`, `oh`, `okay` as real responses).
- Regional syntax, casual contractions, code-switched grammar — how the speaker talks, not errors.
- The speaker's word choices, even when they diverge from the slides. A speaker is free to depart from their own deck; that divergence is not a transcription error. Supporting materials recover what the transcriber mangled — misheard *sounds* — not off-script *choices*.

**Mis-transcription discipline.** Apply the glossary to recover mis-heard sounds, not off-slide word choices. Replace a token only when it is a phonetic mishearing of a glossary entry (same syllable skeleton), restoring the glossary's canonical case. **Default to keep** — only fix what has a path: misheard sound → wrong word → correct glossary term. Don't smooth grammar or off-script content. For words with legitimate alternate meanings, replace only inside a verified phrase context — no bare global swaps.

**Process discipline.** One context, whole file — no chunking, no parallel subagents. Multiple sequential passes, not one — converge.
