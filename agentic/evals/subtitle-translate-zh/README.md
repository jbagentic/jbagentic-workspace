# Eval: subtitle-translate-zh skill

Dev-time eval for the [`subtitle-translate-zh`](../../skills/subtitle-translate-zh/) skill — does it
translate an English talk SRT into Simplified (zh-Hans) and Taiwan-flavored Traditional (zh-Hant)
Chinese with correct script purity, Taiwan vocabulary, regional localization, and preserved proper
nouns + SRT structure? Shares the [suite conventions](../README.md).

## What it measures

Configs `with_skill` / `without_skill`. Three cases:
- **excerpt-khew**, **excerpt-soh** — minimal real-talk excerpts (the cue range covering each talk's signature terms, e.g. Bicep / Telegram / ringgit); regression guards (both arms pass on structure + proper nouns).
- **synthetic-vocab-traps** — the high-signal case: controlled traps for Taiwan vs. Malaysian terms (令吉→林吉特, 巴仙→百分比), script divergence (数据库 vs. 資料庫), and proper-noun restraint (speaker name "Jia Wen" left untranslated).

Grading is **stdlib-only** and re-derives sources from the committed talks/fixtures (never the
gitignored `stage/`): both output files exist; cue numbers/timestamps preserved byte-for-byte; UTF-8
no BOM; CJK density; **script purity** (no Hant markers in Hans and vice versa); Taiwan vocab
conversion; Malaysia→Taiwan localism; Latin proper nouns preserved.

## Layout
- [evals.json](evals.json) — the 3 cases + assertions + reference files.
- [prepare.py](prepare.py) — stages talk excerpts + the synthetic fixture into `stage/`; guards the OpenCC prerequisite.
- [grade.py](grade.py) — stdlib-only grader (no OpenCC needed to grade).
- [fixtures/](fixtures/) — `synthetic-vocab-traps.en.srt` (committed).
- `stage/` — gitignored staged inputs.
- `benchmarks/` — committed iteration records; `runs/` — gitignored scratch. (No `run.py` — executors run via the harness.)

## Running
```bash
python3 agentic/evals/subtitle-translate-zh/prepare.py     # stage excerpts + fixture; checks OpenCC
# harness runs the skill; it writes .zh-Hans.srt / .zh-Hant.srt siblings
python3 agentic/evals/subtitle-translate-zh/grade.py runs/iteration-N
```
Then aggregate, guard, and promote per the [suite workflow](../README.md).

## Notes
- **OpenCC prerequisite.** The skill's real Hans→Hant step uses OpenCC (`s2twp`). It must be importable by plain `python3`, or `with_skill` runs silently fall back to a manual conversion and measure the wrong workflow. `prepare.py` guards this — see [environment parity](../docs/environment-parity.reference.md) for the install command and rationale.
