# subtitle-polish — benchmark history

One row per eval iteration. The trend is the point: does each change to the skill actually move quality, and at what cost. Full detail per run lives in `iteration-N.md`; raw outputs are in the gitignored `runs/`.

| Iteration | Date | Model | With-skill pass | Baseline pass | Delta | Time (skill) | Tokens (skill) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-08 | claude-opus-4-8 | 93.3% (28/30) | 96.7% (29/30) | −0.03 | 245.6s | 50,730 | First run, single sample. Skill trails baseline on raw pass rate but its loss is an over-correction (rewrote spoken "OpenClaw" → slide's "OpenRouter") while baseline's loss is the failure the skill prevents (scrubbed "ya"/"okay" particles). Real 916-cue case non-discriminating (both 10/10); synth cases carry all signal. |
