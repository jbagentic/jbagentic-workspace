# slides-pdf-to-png — benchmark history

One row per iteration; the trend is the point — does each change to the skill move
quality, and at what cost. `w = with_skill`, `wo = without_skill` (baseline). Per-run
and per-dimension detail lives in `iteration-N.md`; raw outputs in the gitignored
`runs/`. `Tools` is blank — tool-call counting isn't wired up for this suite yet.
Format: [history.reference.md](../../docs/history.reference.md).

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [1](#iteration-1) | 2026-06-10 | claude-fable-5 | 100% (21/21) / 49.2% (10/21) | +51pp |  | 59.1s / 115.6s | 16.3k / 21.0k |

## Notes

### Iteration 1
**First run, 1 run/config, deterministic `grade.py`.** All 3 cases discriminate: baseline
skips the `slides/` subfolder (1/8), renders width-pinned 1920×1440 (6/8), and guesses
both PDFs instead of asking (3/5). The skill is also cheaper (−4.7k tokens) and faster
(−56s) — the baseline wastes tokens on tool exploration and visual frame checks.
