---
name: subtitle-polish
description: Polish SRT subtitles from a recorded talk or other spoken-word video — strip fillers and stutters, fix mis-transcribed terms (product names, file names, acronyms, jargon) against a domain context (slide deck, abstract, README), then minor-edit verify. Use whenever the user mentions cleaning, polishing, fixing, or correcting an SRT, VTT, or subtitle/caption/transcript file — even if they don't name a specific operation. Also use when handed a talk folder containing both a transcript and slides.
---

# Polishing subtitles

## Input
- A raw, unpolished subtitle file (SRT/VTT) for a talk. Default convention: a `*.raw.srt` file; a project may define another via its own reference doc.
- Its domain context for the glossary. Prefer the slide deck's pre-extracted text when the project provides one (e.g. `slides.txt` — cheap to read); otherwise fall back to the slide-deck PDF, slide PNGs, abstract, or README. Discover alongside the subtitle file per the project's layout; ask only if nothing is found.

## Output
- The polished subtitle file, named and placed per the project's subtitle-file convention. Default: a sibling of the input with the `.raw` marker removed from the stem (e.g. `foo.en.raw.srt` → `foo.en.srt`). The original raw file stays untouched.
- Invariants: no empty subtitles, no numbering holes, timestamps and encoding (UTF-8 without BOM) unchanged from the source.

## Workflow

Run these four steps in order, once each. The pass is linear — do the fix right the first time (step 3) so verify (step 4) is a single light pass, not a correction loop.

1. **Strip fillers and stutters.** Decide the filler set at runtime for this speaker. Remove standalone filler tokens — `um`, `uh`, and standalone discourse markers (`like`, `you know`, `I mean`) sitting between clauses with no meaning — and collapse consecutive duplicate words. Light touch on the discourse markers: never remove `like` when it carries meaning (verb or preposition — "I like X", "tools like X"). Dedup across the flat token stream — stutters often straddle subtitle boundaries. If a subtitle becomes empty, drop and renumber; leave no holes.

2. **Build a glossary.** Read the domain context to assemble the canonical terms. Prefer the project's pre-extracted slide-deck text if present (e.g. `slides.txt`, the cheapest source); otherwise the slide PNGs/PDF, abstract, or README. Highest-confidence entries are slide bullets (not titles), inline-code spans, filenames with extensions, and the intro slide. Record each term in its canonical case — that's the spelling you'll restore in step 3.

3. **Fix mis-transcribed terms — the speaker's words win.** Apply the glossary to recover mis-heard *sounds*, not off-slide *word choices*: replace a token only when it is a phonetic mishearing of a glossary entry (same syllable skeleton), preserving the glossary's canonical case. **Default to keep.** Supporting materials exist to recover what the transcriber mangled — not to overrule what the speaker chose to say. A speaker is free to diverge from their own slides during the talk; that divergence is not a transcription error, so when a clearly-said word conflicts with the slide, keep the spoken word. Only fix what has a phonetic path — misheard sound → wrong word → correct glossary term. Don't smooth grammar or off-script content. For words with legitimate alternate meanings, only replace inside verified phrase contexts — no bare global swaps.

4. **Verify + minor edits (single pass).** One light pass over the result for residual transcription errors only — no loop. Confirm the output invariants hold: no empty subtitles, no numbering holes, timestamps and encoding unchanged from the source. Leave stylistic and off-script content alone.

## Conventions

Don't touch:

- Affirmations (`yeah`, `oh`, `okay`).
- Regional syntax, casual contractions, code-switched grammar.
- Mechanically collapsed `had had` / `that that`-type repetitions — don't rephrase to restore grammar.

Discourse particles (`lah`, `la`, `ya`) — **keep as voice, thin redundancy, never to zero.** Subtitles are read, not heard: a particle that's natural in speech becomes visual noise when over-repeated on screen. Keep the ones that end a sentence or carry tone (`cannot lah` — emphatic softener); drop the ones doing no work — a reflexive mid-clause filler, a repeat within or across adjacent cues, or one trailing on a cue already at reading speed (~15–17 chars/sec). When a speaker leans on a particle heavily (many a minute), thinning matters most: expect to remove a clear share of them so the result reads cleanly but still sounds like the speaker. Never strip to zero, and never count per speaker — judge each instance by whether it earns its place on screen.
