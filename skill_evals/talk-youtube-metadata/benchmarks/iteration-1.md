# Benchmark — talk-youtube-metadata, iteration 1

- **Date:** 2026-06-05
- **Model:** claude-opus-4-8 (session model; subagent model not captured at source — treat as approximate)
- **Cases:** 3 talks (eval-khew-iac, eval-kowa-journey, eval-soh-friction)
- **Runs per case:** 1 (so stddev is not meaningful yet)
- **Baseline:** same prompt with no skill

## Result

| Metric | With skill | Baseline | Delta |
|---|---|---|---|
| Pass rate | 100% | 50% | **+0.50** |
| Time | 114.3s | 51.7s | +62.6s |
| Tokens | 48,992 | 61,471 | **−12,478** |

Per-case pass (of 8 invariants): with-skill 8/8 on all three; baseline 4/8 on all three.

## Reading

- **The skill works** — 100% vs 50% on the invariants (series suffix, 3 A/B titles ≤70 chars, 0:00 chapters, tags <500, verbatim links, category).
- **Slower** (+63s) — the cost of running the digest, reading the knowledge atom, and verifying. Expected.
- **Cheaper** (−12.5k tokens) — the `srt_digest.py` digest hands the model pre-structured input, so it does less raw-transcript flailing than the baseline. More correct *and* fewer tokens.

## Caveats (don't over-read this)

- **Single run per case.** `± 0` means one sample, not rock-solid. Run 3× per case for real variance.
- **Model unverified.** The aggregator has no model field; subagent model wasn't recorded. Fix going forward by writing model into each run's `timing.json`.
- The auto-generated `runs/iteration-1/benchmark.md` is the working copy; this file is the curated, committed record.
