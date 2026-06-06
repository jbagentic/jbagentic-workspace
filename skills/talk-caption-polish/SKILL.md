---
name: talk-caption-polish
description: Polish SRT captions from recorded talks — strip fillers and stutters, fix mis-transcribed terms (product names, file names, acronyms, jargon) against a domain context (slide deck, abstract, README), then minor-edit verify. Use whenever the user mentions cleaning, polishing, fixing, or correcting an SRT, VTT, or caption/transcript file — even if they don't name a specific operation. Also use when handed a talk folder containing both a transcript and slides.
---

# Polishing talk captions

## Input
- Original `<name>.raw.srt`.
- Domain context (PDF, slide PNGs, abstract, README). Auto-discover in the SRT's parent folder; ask only if nothing found.

## Output
- Sibling `<name>.srt` — input filename with `.raw` stripped (e.g. `foo.en.raw.srt` → `foo.en.srt`). The original `.raw.srt` stays untouched.
- Invariants: no empty subtitles, no numbering holes, timestamps and encoding (UTF-8 without BOM) unchanged from the source.

## Workflow

1. **Strip fillers and stutters.** Decide the filler set at runtime for this speaker. Remove standalone filler tokens and collapse consecutive duplicate words. Dedup across the flat token stream — stutters often straddle subtitle boundaries. If a subtitle becomes empty, drop and renumber; leave no holes.

2. **Fix mis-transcribed terms.** Build a glossary from the domain context first — highest-confidence sources are slide bullets (not titles), inline-code spans, filenames with extensions, and the intro slide. Scan the cleaned SRT for tokens phonetically close to glossary entries but not matching, and replace them, preserving the glossary's canonical case. For words with legitimate alternate meanings, only replace inside verified phrase contexts — no bare global swaps.

3. **Verify (minor edits only).** Default to keep. Only fix what has a phonetic path — misheard sound → wrong word → correct glossary term. Don't smooth grammar or off-script content; speakers disagree with their own slides, and that's not a transcription error. Loop steps 2–3 until residual issues are stylistic, not transcription errors.

## Conventions

Don't touch:

- Affirmations (`yeah`, `oh`, `okay`).
- Regional syntax, casual contractions, code-switched grammar.
- Mechanically collapsed `had had` / `that that`-type repetitions — don't rephrase to restore grammar.
