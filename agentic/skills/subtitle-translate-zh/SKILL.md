---
name: subtitle-translate-zh
description: Translate an English SRT subtitle file from a talk, recording, or presentation into Simplified Chinese (zh-Hans) and Taiwan-flavored Traditional Chinese (zh-Hant). Use whenever the user asks to translate, localize, or generate Chinese subtitles/captions/SRT for a talk, video, recording, or slide deck — including when they only point at a `.en.srt` and reference slides or a PDF alongside it.
---

# Translating subtitles to Chinese

## Input
- A polished English subtitle file (SRT/VTT) — typically the output of `/subtitle-polish`. Default convention: `<basename>.en.srt`; a project may define another via its own reference doc. If the file still looks like raw ASR output (mangled proper nouns, single-letter acronyms, speaker fillers everywhere), suggest running `/subtitle-polish` first rather than carrying that burden here.
- Companion materials (slides, PDF, README) when present — consulted only to disambiguate terms, not as a default opener.
- Target audience(s) — named by whatever context invokes the skill (a runbook, README, reference doc, or the prompt itself), e.g. "Malaysian Chinese readers", "Taiwanese readers". The project names the audience; this skill owns what each implies for output script and vocabulary — see [`references/audience-vocabulary.reference.md`](references/audience-vocabulary.reference.md). Absent a named audience, produce widely-understood Chinese and ask if unsure.

## Output
- Two Chinese subtitle files, named and placed per the project's subtitle-file convention. Default: siblings of the input with the language tag swapped:
  - `<basename>.zh-Hans.srt` — Simplified Chinese
  - `<basename>.zh-Hant.srt` — Traditional Chinese (Taiwan vocabulary)
- Honor the user if they want only one variant or a different flavor (HK, plain `s2t`, etc.).
- Invariants: same entry count as the source; every cue number and timestamp line preserved byte-for-byte; UTF-8 without BOM.

## Workflow

1. **Translate to Simplified Chinese.** Produce `.zh-Hans.srt` entry by entry, in the vocabulary the target audience would naturally use. Read companion materials only when you hit a term whose meaning is genuinely ambiguous from the SRT alone.

2. **Convert Simplified → Traditional (Taiwan vocabulary).** Script and tech vocabulary (数据库→資料庫, 软件→軟體, 视频→影片, …) are a deterministic swap, so use a conversion tool rather than re-translating. Suggested: OpenCC's `s2twp` profile.

   ```python
   from opencc import OpenCC  # pip install opencc-python-reimplemented
   OpenCC('s2twp').convert(open(src_zh_hans).read())
   ```

3. **Correct regional localisms.** `s2twp` converts script and mainland→Taiwan tech vocabulary, but it leaves Malaysian loan-word localisms untouched (令吉, 巴仙 are valid characters, not mainland tech terms), so they survive into the Traditional file verbatim. For a Taiwanese-reader target, apply the Malaysian→Taiwan correction map in [`references/audience-vocabulary.reference.md`](references/audience-vocabulary.reference.md) to the converted file (令吉→林吉特, 巴仙→百分比/百分之). Only this small regional set needs correcting — OpenCC does the bulk.

4. **Verify.** Entry count, timestamp lines, and encoding all match the source.

## Conventions

- **Match each named audience's vocabulary.** The project names the audience; this skill knows what each implies. Quick reference: Malaysian Chinese readers → Simplified, 令吉/巴仙; Taiwanese readers → Traditional (Taiwan), 林吉特/百分比. Full profiles and the Malaysian→Taiwan correction map: [`references/audience-vocabulary.reference.md`](references/audience-vocabulary.reference.md). Absent a named audience, prefer widely-understood phrasing over region-specific idioms.
- **Keep proper names and product/tech names in their original form** unless the user says otherwise — people's names, products (Claude, MCP, Telegram, GitHub, …), file names (SKILL.md, CLAUDE.md, …).
