# Benchmark — talk-youtube-metadata, iteration 2

- **Date:** 2026-06-06
- **Model:** claude-opus-4-6
- **Cases:** 3 talks (eval-khew-iac, eval-kowa-journey, eval-soh-friction)
- **Runs per case:** 1
- **Baseline:** same prompt with no skill

## Result

| Metric | With skill | Baseline | Delta |
|---|---|---|---|
| Pass rate | 100% (24/24) | 83% (20/24) | **+0.17** |
| Time | 92.8s | 62.3s | +30.5s |
| Tokens | 73,419 | 70,031 | +3,388 |

### Per-case breakdown

| Case | With skill | Baseline | Baseline failures |
|---|---|---|---|
| khew-iac | 8/8 | 7/8 | titles >70 chars (78, 71, 71) |
| kowa-journey | 8/8 | 8/8 | — |
| soh-friction | 8/8 | 5/8 | no series suffix, title >70 chars (77), no Luma link |

## Reading

- **The skill still works** — 100% pass rate, same as iteration 1. The invariants (series suffix, 3 A/B titles ≤70 chars, 0:00 chapters, tags <500, verbatim links, category) are consistently met.
- **Baseline improved** — 83% vs 50% in iteration 1. The baseline now passes kowa-journey fully (was 4/8 in iter 1). This may reflect model improvement (opus-4-6 vs opus-4-8) or run variance — single samples can't distinguish.
- **Baseline still fails on title length and community links** — the two discriminating assertions are "titles ≤70 chars" (baseline overruns by 1–8 chars) and "verbatim Luma link" (baseline omits or rewrites the footer when not prompted). The skill's knowledge-atom reference and explicit char-count instruction fix both.
- **Slower, slightly more tokens** — +30.5s and +3.4k tokens. The skill reads the knowledge atom and verifies invariants, which costs time. Token overhead is smaller than iteration 1's delta (was −12.5k) — the baseline is now more efficient too.

## Comparison to iteration 1

| | Iter 1 | Iter 2 | Change |
|---|---|---|---|
| With-skill pass | 100% | 100% | stable |
| Baseline pass | 50% | 83% | +33pp |
| Delta | +0.50 | +0.17 | narrowed |
| Skill time | 114.3s | 92.8s | −21.5s |
| Skill tokens | 48,992 | 73,419 | +24,427 |

The skill's absolute quality held; the gap narrowed because baselines improved, not because the skill regressed. Token increase likely reflects a different model (opus-4-6 vs prior run's approximate opus-4-8) — the two are not directly comparable.

## Caveats

- **Single run per case.** No variance estimate. Run 3× per case for reliable stddev.
- **Model changed.** Iteration 1 used approximate opus-4-8; this uses opus-4-6. Cross-iteration token/time comparisons are directional, not precise.
