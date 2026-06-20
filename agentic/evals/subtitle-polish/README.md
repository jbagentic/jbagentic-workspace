# Eval: subtitle-polish skill

Dev-time eval for the [`subtitle-polish`](../../skills/subtitle-polish/) skill — does it clean a
raw talk SRT (strip fillers and discourse particles, fix mis-transcribed terms against the deck,
translate code-switched speech to English) **without** breaking SRT invariants or over-correcting
the speaker's own words? Shares the [suite conventions](../README.md).

## What it measures

Configs `with_skill` / `without_skill` (same model; skill guidance is the only variable). Three
real JB Agentic Meetup talks as cases — `khew` (916 cues, Mandarin code-switching + term mangles),
`kowa` (875 cues, phonetic mishears), `soh` (806 cues, mostly-correct terms, a restraint test).

Grading is **stdlib-only** (deterministic assertions, no LLM judge):
- **SRT invariants** — valid SRT, no empty cues, contiguous numbering, timestamps unchanged, UTF-8 without BOM.
- **Filler / particle density** down; non-English speech rendered to English in place.
- **Per-talk term fixes** — slide-canonical (e.g. `cloud`→`Claude`) *and* off-slide field jargon (e.g. `Cortez`→`Codex`).
- **Speaker restraint** — keep the speaker's own word (e.g. `OpenClaw` not rewritten to a slide term).

## Layout
- [evals.json](evals.json) — the 3 cases (prompts, expected output, assertions).
- [prepare.py](prepare.py) — stages each talk's `.en.raw.srt` + deck (`slides/`, `slides.pdf`, `slides.txt`) from `talk-recordings/` into `stage/`.
- [grade.py](grade.py) — runs the per-case assertions over each run's output SRT.
- `stage/` — gitignored staged inputs, one folder per talk.
- `benchmarks/` — committed iteration records ([history.md](benchmarks/history.md)).
- `runs/` — gitignored scratch. (No `run.py` — executors run via the eval harness.)

## Running
```bash
python3 agentic/evals/subtitle-polish/prepare.py            # stage inputs into stage/
# harness runs the skill (with_skill) and baseline (without_skill) per case;
# each writes <slug>.en.srt into its run's outputs/
python3 agentic/evals/subtitle-polish/grade.py runs/iteration-N
```
Then aggregate, guard, and promote per the [suite workflow](../README.md) and
[benchmark contract](../docs/benchmark-contract.reference.md).

## Notes
- The skill prefers the deck's extracted `slides.txt` over reading slide PNGs for its glossary (token saving — see iteration 3).
- On a strong baseline, particle-removal and translation no longer discriminate; the cleanest separators are invariant discipline and off-slide jargon recovery. See [benchmarks/](benchmarks/) for the honest read.
