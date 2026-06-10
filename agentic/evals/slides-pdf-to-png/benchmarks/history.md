# slides-pdf-to-png — benchmark history

One row per eval iteration. The trend is the point: does each change to the skill actually move quality, and at what cost. Full detail per run lives in `iteration-N.md`; raw outputs are in the gitignored `runs/`.

| Iteration | Date | Model | With-skill pass | Baseline pass | Delta | Time (skill) | Tokens (skill) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-10 | claude-fable-5 | 100% (21/21) | 49% (10/21) | +0.51 | 59.1s | 16,278 | First run, 1 run/config, deterministic grade.py. All 3 cases discriminate: baseline skips `slides/` subfolder (1/8), renders width-pinned 1920×1440 (6/8), and guesses both PDFs instead of asking (3/5). Skill is also cheaper (−4.7k tokens) and faster (−56s) — baseline wastes tokens on tool exploration and visual frame checks. |
