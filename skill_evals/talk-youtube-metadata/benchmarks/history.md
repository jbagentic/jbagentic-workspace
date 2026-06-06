# talk-youtube-metadata — benchmark history

One row per eval iteration. The trend is the point: does each change to the skill actually move quality, and at what cost. Full detail per run lives in `iteration-N.md`; raw outputs are in the gitignored `runs/`.

| Iteration | Date | Model | With-skill pass | Baseline pass | Delta | Time (skill) | Tokens (skill) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-05 | claude-opus-4-8 (approx, unverified) | 100% (3×8/8) | 50% (3×4/8) | +0.50 | 114.3s | 48,992 | Single run per case — no variance yet. Model not captured at source. |
| 2 | 2026-06-06 | claude-opus-4-6 | 100% (3×8/8) | 83% (20/24) | +0.17 | 92.8s | 73,419 | Baseline improved (kowa now passes); skill still 100%. Delta narrowed. |
