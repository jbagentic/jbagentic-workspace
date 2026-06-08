# doc-this — benchmark history

One row per eval iteration. The trend is the point: does each change to the skill actually move quality, and at what cost. Full detail per run lives in `iteration-N.md`; raw outputs are in the gitignored `runs/`.

| Iteration | Date | Model | With-skill pass | Baseline pass | Delta | Time (skill) | Tokens (skill) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-08 | claude-opus-4-8 | 100% (24/24) | 92% (21/24) | +0.08 | 57.8s | 23,120 | First run, single sample per case. Only the backup-tool case discriminates (12/12 vs 9/12 — baseline skips typed docs + manifest); readme-only and fold-existing are non-discriminating (both 6/6). |
