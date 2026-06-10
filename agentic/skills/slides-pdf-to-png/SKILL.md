---
name: slides-pdf-to-png
description: Extract every page of a slide-deck PDF into HD PNG images for use as video overlays. Use whenever the user wants to convert, extract, export, or render slides/a slide deck/a PDF into PNG (or image) frames — including phrasings like "turn these slides into images", "export the deck as PNGs", or when handed a talk folder containing a slides.pdf that needs frames.
---

# Slide PDF → HD PNG frames

## Input
- A slide-deck `.pdf` (e.g. `slides.pdf`). If multiple PDFs are present, ask which one.

## Output
- A subfolder containing one PNG file per page of the slide-deck PDF. By default, name the folder `slides/` and place it under the same folder as the slide-deck PDF.
- PNG file naming: `slide-NN.png`, zero-padded to at least 2 digits, 1-based, in page order (`slide-01.png`, `slide-02.png`, …). Use more digits only if the deck has 100+ pages.
- Invariants: one PNG per page, no gaps in numbering; each frame is HD — rendered at the deck's native aspect ratio scaled so height = 1080 px (a 16:9 deck yields exactly 1920×1080), with no padding, cropping, or letterboxing; `slides/` is emptied of prior `slide-*.png` first so stale frames never linger.

## Workflow

1. **Locate the PDF and prepare the output folder.** Resolve the source PDF, create `slides/` beside it, and clear any existing `slide-*.png` so a re-run is clean.

2. **Render each page to PNG.** Scale so output height = 1080 px (HD), preserving aspect ratio — overlays must match the video frame without distortion. Save zero-padded, 1-based, in page order. (Suggested approach: PyMuPDF — `zoom = 1080 / page.rect.height`, `page.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(...)`.)

3. **Verify.** Page count equals PNG count, names are contiguous with no holes, and the first frame's pixel dimensions are HD (height 1080). Report the count and resolution.

## Conventions
- Don't assume any interpreter already has PyMuPDF. Probe first (`python3 -c "import fitz"`); if it's missing, provision an isolated, throwaway venv (`python3 -m venv` in a temp dir, `pip install pymupdf`) rather than `pip install --break-system-packages` into a system or shared environment. Never assume a project `.venv` exists or contains the dependency — verify before using it.
- Any tool that renders PDF pages at a chosen resolution works (poppler's `pdftoppm -png -r`, ImageMagick); PyMuPDF is just the zero-system-dependency default.
- Don't alter the source PDF, and don't touch non-slide files in `slides/`.
- HD/1080p is the house target because these frames overlay HD video clips — don't downscale below it.
