# Eval: slides-pdf-to-png skill

Dev-time eval for the [`slides-pdf-to-png`](../../skills/slides-pdf-to-png/) skill — does it render
a slide-deck PDF into correctly-sized, contiguously-named PNG frames, clear stale frames on
re-export, and ask which PDF to use when a folder holds several? Shares the
[suite conventions](../README.md).

## What it measures

Configs `with_skill` / `without_skill`. Three cases:
- **happy-path-16x9** — 16:9 deck → `slides/slide-01.png…` at 1080px height (1920×1080), zero-padded, contiguous.
- **rerun-clears-stale** — re-export drops stale frames (4:3 deck → 1440×1080) and leaves non-slide files (e.g. `notes.txt`) untouched.
- **multi-pdf-asks** — a folder with two PDFs → the skill must **ask** which to render, not guess.

Grading is **deterministic, stdlib-only** (zero LLM tokens): PNG dimensions read straight from the
IHDR chunk (no Pillow); source-PDF integrity via sha256 in [fixtures/manifest.json](fixtures/manifest.json)
(no PDF parsing); ask-behavior via `?` + both PDF names in the response.

## Layout
- [evals.json](evals.json) — the 3 cases + assertions.
- [prepare.py](prepare.py) — stages per-run work dirs (3 cases × 2 configs) under `runs/`; seeds stale frames/notes; writes `eval_metadata.json` + resolved prompts.
- [grade.py](grade.py) — deterministic checker.
- [fixtures/](fixtures/) — tiny committed synthetic PDFs + [manifest.json](fixtures/manifest.json); [make_fixtures.py](fixtures/make_fixtures.py) regenerates them (run bare to verify, `--write` to rewrite).
- `benchmarks/` — committed iteration records.
- `runs/` — gitignored scratch; the executor writes `outputs/final-response.md` (the multi-PDF case grades on it) + `timing.json`. (No `run.py` — executors run via the harness.)

## Running
```bash
python3 agentic/evals/slides-pdf-to-png/prepare.py runs/iteration-N
# harness runs each staged work dir; executor writes outputs/final-response.md + timing.json
python3 agentic/evals/slides-pdf-to-png/grade.py runs/iteration-N
```
Then aggregate, guard, and promote per the [suite workflow](../README.md).

## Notes
- Baseline executors must be told to ignore the installed skill (it's present in this workspace).
- The multi-PDF case is the sharp discriminator: the skill asks; the baseline confidently renders the wrong deck.
