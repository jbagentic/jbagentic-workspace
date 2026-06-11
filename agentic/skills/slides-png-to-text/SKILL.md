---
name: slides-png-to-text
description: Extract a slide deck's text into a reusable plain-text file (`slides.txt`) by transcribing the deck's rendered slide images, so later steps build a term glossary from cheap text instead of re-reading the images. Use whenever the user wants the text/wording/contents of a slide deck pulled out, asks to make a deck searchable or to produce a glossary/term list from slides, or hands over a talk folder whose slides downstream subtitle/metadata work will need the deck wording from. Not for rendering slides into PNG frames (use slides-pdf-to-png).
---

# Slides PNG → text

Turn a talk's rendered slides into one reusable text file. Downstream skills
(`subtitle-polish`, `subtitle-translate-zh`) read this for their term glossary —
recovering the exact spelling of product names, file names, and jargon — instead
of reading the slide images themselves, which is far more expensive and is paid
again on every run. Extract once here; every later run and skill reads the text.

## Input
- The rendered slide images (`slides/slide-NN.png`), produced upstream by
  `slides-pdf-to-png`. This skill *reads* the images; it does not render them — if
  the `slides/` PNGs are not there yet, run `slides-pdf-to-png` first.

## Output
- The slide deck's text as a committed `slides.txt` — default name; a project's layout
  may define another. One section per slide in document order, each headed `## slide-NN`,
  holding the slide's text — title, bullets, inline code, file names, product/tool names,
  URLs. It captures *glossary text, not layout*. Preserve the exact casing and spelling of
  technical terms (e.g. `IaC`, `CLAUDE.md`, `OpenRouter`, `Next.js`) — that exactness is the
  whole point.

## Workflow

1. **Transcribe each slide image.** Read the `slides/` PNGs in order and write each slide's
   text into a `## slide-NN` section. Transcribe what is *written* on the slide — exact
   spelling and casing — including text inside screenshots and diagrams. Do not invent terms
   that aren't shown, and do not "correct" a coined or unusual term to what you expect (keep
   e.g. `OpenClaw` exactly as written).

2. **Sanity-check.** Confirm one `## slide-NN` section per slide image and that the
   high-value terms (product/tool names, file names, code) came through with their exact
   spelling.

## Notes
- Leave the slide images and the source PDF untouched; this step only adds `slides.txt`.
- Reading the rendered images is deliberate: the model recovers exact tech-term casing and
  text baked into screenshots/diagrams that a PDF text-layer extractor silently mangles or
  misses, and it keeps speaker-owned slides in-house (no third-party OCR service).
