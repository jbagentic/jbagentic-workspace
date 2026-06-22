# slides-png-to-text — benchmark history

> Renamed from `slides-pdf-to-text` after iteration 1: the skill now transcribes the rendered
> slide PNGs with the vision model (one path), dropping the hand-rolled PDF text-layer parser.

One row per iteration; the trend is the point — does each change to the skill move
quality, and at what cost. `w = with_skill`, `wo = without_skill` (baseline). Per-run
and per-dimension detail lives in `iteration-N.md`; raw outputs in the gitignored
`runs/`. `Tools` is blank — tool-call counting isn't wired up for this suite yet.
Format: [history.reference.md](../../docs/history.reference.md).

| Iteration | Date | Model | Pass (w/wo) | Δ | Tools (w/wo) | Time (w/wo) | Tokens (w/wo) |
|---|---|---|---|---|---|---|---|
| [1](#iteration-1) | 2026-06-11 | claude-opus-4-8 | 100% (28/28) / 78.6% (22/28) | +21pp |  | 153.5s / 100.5s | 41.2k / 22.8k |
| [2](#iteration-2) | 2026-06-11 | claude-opus-4-8 | 100% (29/29) / 79.3% (23/29) | +21pp |  | 141.3s / 152.6s | 38.9k / 38.2k |

## Notes

### Iteration 1
**First run, single sample.** 2 real decks, one per branch: textlayer-kowa (text layer)
+ vision-khew (image-only). **Discriminator is the output contract, not terms** — both
baselines recovered every term verbatim but wrote `--- Slide N ---`/freeform, not
`## slide-NN`, losing the same 3 format assertions. **Cost premise inverted**: with-skill
is ~1.8× dearer (41k vs 23k) — on Kowa the skill's sanity-check rightly rejected the
lossy stdlib extractor and escalated to vision (58k) while the baseline pulled the text
layer cheaply with pypdf (26k). Finding: bundled `extract_deck_text.py` is lossy on this
project's real exports. Known eval gap: pass-rate doesn't catch that lossiness (curated
terms survive the script); iter-2 should add trap terms the script drops (CLAUDE.md,
E-initial headings).

### Iteration 2
**Simplified + renamed** `slides-pdf-to-text`→`slides-png-to-text`: deleted the
hand-rolled PDF parser; skill now just transcribes the slide PNGs with vision (one path).
No regression. Added a **grounded screenshot trap** `CLAUDE.md` (slide-07 editor view)
the old text-layer parser couldn't read — `with_skill` recovers it (kowa 16/16); the
committed slides.txt, byte-identical to the old parser output, lacks it. Discriminator
unchanged: the `## slide-NN` contract (baselines wrote `=== Slide N ===`). No cost story
this run — baseline had no pypdf so also used vision (38.2k vs 38.9k); the win is
simplicity + screenshot recovery, not cost. Single sample, both configs.
