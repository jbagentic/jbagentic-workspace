# Benchmark — slides-pdf-to-png, iteration 1

- **Date:** 2026-06-10
- **Model:** claude-fable-5 (executor subagents; main-loop harness fable-5 [1m])
- **Cases:** 3 (happy-path-16x9, rerun-clears-stale, multi-pdf-asks)
- **Runs per case:** 1 per config (no variance estimate yet)
- **Baseline:** same prompt, skill explicitly suppressed
- **Assertions:** 21 total (8 + 8 + 5), all graded deterministically by `grade.py` (zero LLM grading tokens)

## Result

| Metric | With skill | Baseline | Delta |
|---|---|---|---|
| Pass rate (mean of cases) | 100% | 49.2% | **+0.51** |
| Pass rate (assertions) | 21/21 | 10/21 | +11 |
| Time (mean) | 59.1s | 115.6s | **−56.4s** |
| Tokens (mean) | 16,278 | 21,010 | **−4,732** |

## Per-case breakdown

| Case | With skill | Baseline | Baseline failures |
|---|---|---|---|
| happy-path-16x9 | 8/8 | 1/8 | wrote frames into the work folder root, no `slides/` subfolder — 7 assertions cascade |
| rerun-clears-stale | 8/8 | 6/8 | rendered 1920×1440 (width-pinned via a hand-built CoreGraphics/Swift renderer) instead of height-1080 → wrong height and width |
| multi-pdf-asks | 5/5 | 3/5 | guessed instead of asking: rendered **both** PDFs at 200 DPI with its own naming (`slides-talk-page-01.png`, 2000×1125) |

## Reading

- **Every case discriminates, each on a different invariant.** The baseline can render PDFs fine —
  what it can't know are the conventions the skill encodes: the `slides/` output folder, the
  height-1080 HD target, and the ask-when-ambiguous gate. All three baseline runs produced
  confident "Done." replies whose outputs violate the contract the downstream video workflow needs.
- **The skill is cheaper AND faster, not just better.** −4.7k tokens and −56s per run on average.
  Two reasons visible in the transcripts: (1) the skill hands over the exact recipe (PyMuPDF,
  zoom = 1080/page height, naming), so the baseline's tool-exploration and a from-scratch Swift
  renderer build don't happen; (2) both failing baselines "verified" by reading frames back
  **visually** — vision tokens the skill's scripted verification avoids. The usual skill-overhead
  cost story is inverted here.
- **The ask-gate works.** With-skill stopped at a clarifying question naming both PDFs in 30s /
  15.2k tokens — the cheapest run of the six. The baseline spent 97s rendering both decks wrong.

## Caveats

- **Single run per case.** No per-config variance; the pass_rate stddev (0.33 baseline) in
  benchmark.json is across *cases*, not runs. Run 2–3× per case before trusting the delta's
  magnitude — though the failure modes are categorical (conventions unknown to the baseline),
  so they are unlikely to be run-to-run noise.
- **`benchmark.json` metadata defaults:** `executor_model: <model-name>` and
  `runs_per_configuration: 3` are aggregator defaults, not real; accurate values are recorded here
  (fable-5, 1 run per config).
- **Question-detection is a heuristic** (`?` + both PDF basenames in the final response). It worked
  cleanly this iteration; the filesystem assertions carry the discriminating signal regardless.
