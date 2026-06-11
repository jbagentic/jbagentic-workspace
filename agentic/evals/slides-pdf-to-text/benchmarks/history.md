# slides-pdf-to-text — benchmark history

One row per eval iteration. The trend is the point: does each change to the skill actually move quality, and at what cost. Full detail per run lives in `iteration-N.md`; raw outputs are in the gitignored `runs/`.

| Iteration | Date | Model | With-skill pass | Baseline pass | Delta | Time (skill) | Tokens (skill) | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-11 | claude-opus-4-8 | 100% (28/28) | 78.6% (22/28) | +0.21 | 153.5s | 41,163 | First run, single sample. 2 real decks, one per branch: textlayer-kowa (text layer) + vision-khew (image-only). **Discriminator is the output contract, not terms** — both baselines recovered every term verbatim but wrote `--- Slide N ---`/freeform, not `## slide-NN`, losing the same 3 format assertions. **Cost premise inverted**: with-skill is ~1.8× dearer (41k vs 23k) — on Kowa the skill's sanity-check rightly rejected the lossy stdlib extractor and escalated to vision (58k) while the baseline pulled the text layer cheaply with pypdf (26k). Finding: bundled extract_deck_text.py is lossy on this project's real exports. Known eval gap: pass-rate doesn't catch that lossiness (curated terms survive the script); iter-2 should add trap terms the script drops (CLAUDE.md, E-initial headings). |
