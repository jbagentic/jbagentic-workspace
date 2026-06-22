# talk-youtube-metadata — benchmark history

One row per iteration; the trend is the point — does each change to the skill move
quality, and at what cost. `w = with_skill`, `wo = without_skill` (baseline). Per-run
and per-dimension detail lives in `iteration-N.md`; raw outputs in the gitignored
`runs/`. `Tools` is blank — tool-call counting isn't wired up for this suite yet.
Format: [history.reference.md](../../docs/history.reference.md).

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [1](#iteration-1) | 2026-06-05 | claude-opus-4-8 (approx, unverified) | 100% (24/24) / 50% (12/24) | +50pp |  | 114.3s / 51.7s | 49.0k / 61.5k |
| [2](#iteration-2) | 2026-06-06 | claude-opus-4-6 | 100% (24/24) / 83% (20/24) | +17pp |  | 92.8s / 62.3s | 73.4k / 70.0k |

## Notes

### Iteration 1
**Single run per case — no variance yet.** Model not captured at source. Baseline is
*dearer* here (61.5k vs 49.0k) — the `srt_digest.py` digest hands the model
pre-structured input, so the skill does less raw-transcript flailing.

### Iteration 2
**Baseline improved** (kowa now passes); skill still 100%, delta narrowed. Tokens now
roughly level (73.4k vs 70.0k) — the it1 token edge reflected a different (approximate)
model, so the two iterations' token numbers aren't directly comparable.
