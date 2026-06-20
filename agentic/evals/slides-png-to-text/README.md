# Eval: slides-png-to-text skill

Dev-time eval for the [`slides-png-to-text`](../../skills/slides-png-to-text/) skill — does it
transcribe a deck's slide PNGs into a reusable `slides.txt` that follows the `## slide-NN` contract
and preserves exact-casing terms (including text only visible in screenshots)? Shares the
[suite conventions](../README.md).

## What it measures

Configs `with_skill` / `without_skill` (baseline ignores the installed skill). Two real committed decks:
- **kowa** (21 slides) — includes screenshot text (e.g. the `CLAUDE.md` editor view on slide 7) that a PDF text-layer parser misses.
- **khew** (6 slides) — image-only deck (vision-only path).

The discriminator is **output-contract adherence**, not term recall (baselines recover terms fine).
Grading is **deterministic, stdlib-only**: a `slides.txt` beside `slides.pdf` with exactly one
`## slide-NN` section per staged PNG (zero-padded, 1-based, contiguous, no empty bodies, UTF-8 no
BOM), exact-casing presence of curated terms, and source files untouched (sha256).

## Layout
- [evals.json](evals.json) — the 2 cases + assertions.
- [prepare.py](prepare.py) — stages per-run work dirs from real decks: copies a talk's `slides.pdf` + `slides/` PNGs (never the committed `slides.txt`).
- [grade.py](grade.py) — deterministic contract checker.
- `benchmarks/` — committed iteration records.
- `runs/` — gitignored scratch; the harness writes `timing.json`; the skill writes `work/slides.txt`. (No `run.py` — executors run via the harness.)

## Running
```bash
python3 agentic/evals/slides-png-to-text/prepare.py runs/iteration-N
# harness runs each work dir; with_skill transcribes PNGs via the vision model, without_skill ignores the skill
python3 agentic/evals/slides-png-to-text/grade.py runs/iteration-N
```
Then aggregate, guard, and promote per the [suite workflow](../README.md).

## Notes
- Iteration 1 ran under the old name `slides-pdf-to-text` (a hand-rolled PDF text-layer parser); it was lossy on real exports and was retired in iteration 2, which transcribes every slide via vision (one path). The `CLAUDE.md` screenshot term is the grounded trap a text-layer parser can't recover. See [benchmarks/](benchmarks/).
