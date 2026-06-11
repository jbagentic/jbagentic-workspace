# subtitle-polish — benchmark history

One row per eval iteration. The trend is the point: does each change to the skill actually move quality, and at what cost. Full detail per run lives in `iteration-N.md`; raw outputs are in the gitignored `runs/`.

| Iteration | Date | Model | With-skill pass | Baseline pass | Delta | Time (skill) | Tokens (skill) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-08 | claude-opus-4-8 | 93.3% (28/30) | 96.7% (29/30) | −0.03 | 245.6s | 50,730 | First run, single sample. Skill trails baseline on raw pass rate but its loss is an over-correction (rewrote spoken "OpenClaw" → slide's "OpenRouter") while baseline's loss is the failure the skill prevents (scrubbed "ya"/"okay" particles). Real 916-cue case non-discriminating (both 10/10); synth cases carry all signal. |
| 2 | 2026-06-11 | claude-opus-4-8 | 97.1% (33/34) | 97.1% (33/34) | 0.00 | 662.5s | 109,841 | Skill rewrite: principle-based restraint + phonetic-only term gate + particle "thin, never to zero". All-real eval (34 assertions, not like-for-like with iter 1). **Iter-1 over-correction fixed** — skill kept spoken "Open Claw" (≠ slide "OpenRouter"). Fixed a grader brittleness (`\bOpenClaw\b` couldn't match the spaced form: 32→33). Skill's only booked miss ("Jason B"→`jsonb`, the truer answer) is an expected-answer artifact left unscored — credit it and delta is +0.03; baseline's miss is a real "ah" particle scrub. Single sample. |
