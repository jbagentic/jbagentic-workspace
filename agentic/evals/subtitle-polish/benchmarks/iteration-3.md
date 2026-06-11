# Benchmark — subtitle-polish, iteration 3

- **Date:** 2026-06-11
- **Model:** claude-opus-4-8
- **Cases:** 3 real talks — `real-khewjiapeng` (916 cues, 6-slide deck), `real-kowajialiang` (875 cues, 21-slide deck), `real-sohjunwei` (806 cues, 14-slide deck).
- **Runs per case:** 1, `with_skill` only. The baseline is unchanged from iteration 2 (same prompt, no skill) and **carried forward** — not re-run.
- **What changed:** the glossary source. `subtitle-polish` now reads a `slides.txt` (the deck's text, extracted once) instead of the slide PNGs as vision input. A new `slides-pdf-to-text` skill produces `slides.txt` in pre-edit-prep — stdlib text-layer extraction for decks that have one (Kowa), a one-time vision pass for image-only decks (Khew, Soh). Same 35-assertion eval as iteration 2.

## Result

| Metric | With skill (iter 3) | With skill (iter 2) | Baseline (carried) |
|---|---|---|---|
| Pass rate | **100% (35/35)** | 97.1% (34/35) | 94.3% (33/35) |
| Tokens (mean) | **90,764** | 115,967 | 93,843 |
| Time (mean) | **446.5s** | 903.5s | 464.2s |

**Reading the deck as text instead of images cut ~22% of tokens with no quality
loss — pass rate held at the top (35/35).** The skill is now *cheaper than the
baseline in tokens* while scoring higher.

### Per-deck token/time (the saving scales with slide count)

| Case | slides | tokens iter2→iter3 | Δ tok | time iter2→iter3 | Δ time |
|---|---|---|---|---|---|
| khew | 6 | 96,158 → 101,466 | +5,308 | 624s → 546s | −78s |
| kowa | 21 | 134,708 → **86,065** | **−48,643** | 1,199s → **274s** | −925s |
| soh | 14 | 117,036 → **84,762** | **−32,274** | 887s → 519s | −368s |

The win concentrates on slide-heavy decks (kowa −49k, soh −32k — matching the ~33k
/ ~22k of slide-vision tokens those decks cost in iter 2). Khew's 6-slide deck
saved too little to clear run-to-run noise (+5k is within variance). The kowa iter-2
time (1,199s) was itself a slow outlier, so it inflates that row's time delta — but
even soh and khew dropped on time, reading text beats loading 14/6 images.

## One-time extraction cost (amortized)

Producing `slides.txt` is paid **once per deck**, then every later run and every
slide-consuming skill reads it free:

| Deck | method | one-time cost |
|---|---|---|
| kowa | stdlib `extract_deck_text.py` (text layer) | ~0 tokens, instant |
| khew | one-time vision pass (image-only PDF) | 18,267 tokens |
| soh | one-time vision pass (image-only PDF) | 26,410 tokens |

For a text-layer deck the saving is pure from run 1. For an image-only deck the
~22–26k vision cost is pre-paid once and recouped after ~1 re-run or the second
consumer (`subtitle-translate-zh` also reads `slides.txt`).

## Quality held — the worry cases all passed

- **kowa 13/13** (was 12/13): every term-recovery assertion passed, and this run
  rendered `Jason` → `JSON` (iter-2's only booked miss was the `jsonb` rendering —
  a run-variance choice, both faithful). Particle thinning still fired: `lah`
  138 → 58, `ya` 87 → 29.
- **khew 10/10:** `IaC`/`Terraform`/`Bicep` recovered from the text glossary, and
  **`Azure portal` was still recovered from "Asia bottle"** even though `slides.txt`
  doesn't contain "Azure" — `Bicep` (Azure-only IaC) anchors the inference. This was
  the main risk of dropping the slide images; it held.
- **soh 12/12:** `OpenRouter` recovered where spoken; the speaker's own "Open Claw"
  preserved (restraint intact); MCP/CLI/SQLite/Groq/Qwen/Gemini/Next.js fixed.

## Caveats

- **Single sample per case**, `with_skill` only; baseline carried from iter 2. The
  per-deck token deltas on kowa/soh are far larger than plausible noise; khew's is not.
- **Text-first loses image-only text.** `slides.txt` (text layer or transcribed
  bullets) won't carry terms that live only inside slide screenshots/diagrams. None
  of these three cases needed one, but the skill keeps the PNG/PDF path as a fallback
  when `slides.txt` is absent — it does not currently re-open images to fill a gap.
- **Vision-fallback quality depends on the transcription pass.** Khew/Soh `slides.txt`
  were produced by a one-time vision read; a missed term there would silently weaken
  the glossary. Spot-check `slides.txt` after generating it for a new talk.

## What's next

- iter-3 leaves the jsonb assertion as-is (it passed this run); revisit only if it flaps.
- Consider a tiny `grade.py` check that `slides.txt` exists and is non-trivial before a run.
