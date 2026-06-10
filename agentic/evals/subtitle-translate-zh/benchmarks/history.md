# subtitle-translate-zh — benchmark history

One row per eval iteration. The trend is the point: does each change to the skill actually move quality, and at what cost. Full detail per run lives in `iteration-N.md`; raw outputs are in the gitignored `runs/`.

| Iteration | Date | Model | With-skill pass | Baseline pass | Delta | Time (skill) | Tokens (skill) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-10 | claude-opus-4-8 | 97.2% (33/34) | 94.4% (32/34) | +0.03 | 331.8s | 62,577 | First run, single sample. Skill's win: kept speaker name "Jia Wen" verbatim where baseline rendered 嘉文. Real-talk excerpts non-discriminating (both perfect); synthetic carries all signal. Both miss 巴仙 — eval didn't stage the project vocab reference doc (fix in iter 2). With-skill tokens/time inflated by a two-pass OpenCC redo after a mid-run parity fix (python3 was denied to background subagents). |
