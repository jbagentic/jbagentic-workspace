---
name: slides-pdf-to-text
description: Extract a slide deck's text into a reusable plain-text file (`slides.txt`) so later steps build a term glossary from cheap text instead of reading slide images. Use whenever the user wants the text/wording/contents of a slide deck pulled out of a PDF, asks to make a deck searchable or to produce a glossary/term list from slides, or hands over a talk folder with a `slides.pdf` that downstream subtitle/metadata work will need the deck wording from. Not for rendering slides into PNG frames (use slides-pdf-to-png).
---

# Slides PDF → text

Turn a talk's slide deck into one reusable text file. Downstream skills
(`subtitle-polish`, `subtitle-translate-zh`) read this for their term glossary —
recovering the exact spelling of product names, file names, and jargon — instead
of reading the slide PNGs as vision input, which is far more expensive and is paid
again on every run. Extract once here; every later run and skill reads the text.

## Input
- A slide-deck PDF (default `slides.pdf` in the talk folder).
- The rendered slide PNGs (`slides/slide-NN.png`) as a fallback source — needed
  only when the PDF has no text layer (see step 2).

## Output
- The slide deck's text as a committed sibling of the PDF — default name `slides.txt`; a project's layout may define another. One section per slide in
  document order, each headed `## slide-NN`, holding the slide's text — title,
  bullets, inline code, file names, product/tool names, URLs. It captures
  *glossary text, not layout*. Preserve the exact casing and spelling of technical
  terms (e.g. `IaC`, `CLAUDE.md`, `OpenRouter`, `Next.js`) — that exactness is the
  whole point.

## Workflow

1. **Try the text layer first (cheap, deterministic).** Run
   `scripts/extract_deck_text.py slides.pdf`. Most slide exports (Google Slides,
   Keynote, PowerPoint) carry a real text layer, and the script recovers it with
   no dependencies — decoding subsetted-font glyphs through the PDF's `/ToUnicode`
   map. If it prints substantial text (exit 0), that is `slides.txt`; save it.

2. **Fall back to vision for image-only decks.** If the script exits non-zero or
   prints little (a "print to PDF" or scanned deck with no text layer), read the
   `slides/` PNGs once and transcribe each slide's text into the same
   `## slide-NN` format. This is a one-time vision cost, amortized across every
   later run and consumer. Transcribe what is *written* on the slide — exact
   spelling and casing — and do not invent terms that aren't shown.

3. **Sanity-check.** Confirm one `## slide-NN` section per slide and that the
   high-value terms (product/tool names, file names, code) came through with their
   exact spelling. Note that screenshots/diagrams may hold text the deck author
   never typed; the vision fallback can capture it, the text-layer path cannot.

## Notes
- `extract_deck_text.py` is stdlib-only (`zlib` + regex); it needs no PDF library
  and no network. It is best-effort: it returns nothing for a deck with no text
  layer, which is the signal to use step 2 — not an error.
- Leave the slide PNGs and the PDF untouched; this step only adds `slides.txt`.
