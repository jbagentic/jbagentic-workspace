---
name: subtitle-polish
description: Polish SRT subtitles from a recorded talk or other spoken-word video — strip fillers and stutters, fix mis-transcribed terms (product names, file names, acronyms, jargon) against a domain context (slide deck, abstract, README), then minor-edit verify. Use whenever the user mentions cleaning, polishing, fixing, or correcting an SRT, VTT, or subtitle/caption/transcript file — even if they don't name a specific operation. Also use when handed a talk folder containing both a transcript and slides.
---

# Polishing subtitles

## Input
- A raw, unpolished subtitle file (SRT/VTT) for a talk. Default convention: a `*.raw.srt` file; a project may define another via its own reference doc.
- Its domain context (slide-deck PDF, slide PNGs, abstract, README). Discover alongside the subtitle file per the project's layout; ask only if nothing is found.

## Output
- The polished subtitle file, named and placed per the project's subtitle-file convention. Default: a sibling of the input with the `.raw` marker removed from the stem (e.g. `foo.en.raw.srt` → `foo.en.srt`). The original raw file stays untouched.
- Invariants: no empty subtitles, no numbering holes, timestamps and encoding (UTF-8 without BOM) unchanged from the source.

## Workflow

1. **Strip fillers and stutters.** Decide the filler set at runtime for this speaker. Remove standalone filler tokens — `um`, `uh`, and standalone discourse markers (`like`, `you know`, `I mean`) sitting between clauses with no meaning — and collapse consecutive duplicate words. Light touch on the discourse markers: never remove `like` when it carries meaning (verb or preposition — "I like X", "tools like X"). Dedup across the flat token stream — stutters often straddle subtitle boundaries. If a subtitle becomes empty, drop and renumber; leave no holes.

2. **Fix mis-transcribed terms.** Build a glossary from the domain context first — highest-confidence sources are slide bullets (not titles), inline-code spans, filenames with extensions, and the intro slide. The glossary recovers mis-heard *sounds*, not off-slide *word choices*: replace a token only when it is a phonetic mishearing of a glossary entry (same syllable skeleton), preserving the glossary's canonical case. If the speaker clearly said a different real word, keep it — even when a slide names something else for the same concept. For words with legitimate alternate meanings, only replace inside verified phrase contexts — no bare global swaps.

3. **Verify (minor edits only). The speaker's words win.** Supporting materials (slides, abstract, README) exist to recover what the transcriber mangled — not to overrule what the speaker chose to say. A speaker is free to diverge from their own slides during the talk; that divergence is not a transcription error, so when a clearly-said word conflicts with the slide, keep the spoken word. Default to keep. Only fix what has a phonetic path — misheard sound → wrong word → correct glossary term. Don't smooth grammar or off-script content. Loop steps 2–3 until residual issues are stylistic, not transcription errors.

## Conventions

Don't touch:

- Affirmations (`yeah`, `oh`, `okay`).
- Regional syntax, casual contractions, code-switched grammar.
- Mechanically collapsed `had had` / `that that`-type repetitions — don't rephrase to restore grammar.

Discourse particles (`lah`, `la`, `ya`) — **keep as voice, thin redundancy, never to zero.** Subtitles are read, not heard: a particle that's natural in speech becomes visual noise when over-repeated on screen. Keep instances that carry tone (`cannot lah` — emphatic softener) and always leave a representative few. Thin only on objective triggers — drop a trailing particle when a cue exceeds comfortable reading speed (~15–17 chars/sec) or when particles stack redundantly (`okay lah, so lah`). No per-speaker counting, no global strip.
