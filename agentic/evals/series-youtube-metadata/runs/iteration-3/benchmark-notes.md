# series-youtube-metadata — iteration-3 analysis

Companion to the auto-generated `benchmark.md` (stats table) and `benchmark.json`.
Run after the revision that sources episode facts (number, date, full title,
people) from `meetup-records.reference.md` and demotes the folder name to a
locator. 3 evals × {with_skill, without_skill baseline}, outputs under
`eval-*/<cfg>/outputs/` — committed talk folders untouched.

## Headline

| Config | Pass rate | Avg tokens | Avg wall-clock |
|--------|-----------|-----------|----------------|
| with_skill | **94.9%** (mean of 12/13, 12/13, 13/13) | 46.8k | 173s |
| without_skill | 79.5% (10/13, 11/13, 10/13) | 66.1k | 82s |
| delta | **+0.15** | **−19.3k** | +91.5s |

The skill is more compliant **and** ~30% leaner on tokens; slower in wall-clock
because it runs the digest helper and reads the profile + records instead of
free-styling.

## What the skill reliably fixes (discriminating assertions, with vs without /3)

- **Title length ≤72 (~70 target):** 3/3 vs 1/3. Baselines overshoot — khew
  75/77/79, soh 71/76/77. (Strict ≤70: 1/3 vs 0/3 — see residual below.)
- **No reader-facing timestamp caveat:** 3/3 vs 1/3. Two baselines added the
  banned "timestamps assume the video starts…" note.
- **Exact `📍 JB Agentic Meetup #1 — 30 May 2026` line:** 3/3 vs 2/3.

## Non-discriminating (both pass)

full title *with subtitle*, verbatim footer + links, title suffix, chapters at
0:00, ≥3 chapters, tags <500, category. The **full title** passed in both
configs because the baselines, with full repo access, found
`meetup-records.reference.md` on their own. So the records change doesn't beat a
strong repo-aware baseline — its value is making the correct title *reliable and
structured* vs the old folder slug (`AIForEverydayFriction`, subtitle dropped).

## Residual (optional future polish, not a defect)

Even with the skill, *strict* ≤70 is only 1/3 — with-skill titles creep to 71–72
(khew 72, kowa 71). Within the skill's own "≤ ~70" approximate bar, so left as-is.

## Per-eval title lengths (incl. suffix)

| eval | with_skill | without_skill |
|------|-----------|---------------|
| khew-iac | 65 / 69 / 72 | 75 / 77 / 79 |
| kowa-journey | 66 / 67 / 71 | 60 / 67 / 72 |
| soh-friction | 64 / 66 / 69 | 71 / 76 / 77 |

Grading was scripted (objective substring + length checks); see
`grading-summary.txt` for the full per-assertion matrix.
