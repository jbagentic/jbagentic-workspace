---
name: talk-caption-translate-zh
description: Translate an English SRT caption file from a talk, recording, or presentation into Simplified Chinese (zh-Hans) and Taiwan-flavored Traditional Chinese (zh-Hant). Use whenever the user asks to translate, localize, or generate Chinese subtitles/captions/SRT for a talk, video, recording, or slide deck — including when they only point at a `.en.srt` and reference slides or a PDF alongside it.
---

# Translating talk captions to Chinese

## Input
- `<basename>.en.srt` — the polished SRT (output of `/talk-caption-polish`). If the file still looks like raw ASR output (mangled proper nouns, single-letter acronyms, speaker fillers everywhere), suggest running `/talk-caption-polish` first rather than carrying that burden here.
- Companion materials (slides, PDF, README) when present — consulted only to disambiguate terms, not as a default opener.

## Output
- Two siblings, derived by swapping the language tag:
  - `<basename>.zh-Hans.srt` — Simplified Chinese
  - `<basename>.zh-Hant.srt` — Traditional Chinese (Taiwan vocabulary)
- Honor the user if they want only one variant or a different flavor (HK, plain `s2t`, etc.).
- Invariants: same entry count as the source; every cue number and timestamp line preserved byte-for-byte; UTF-8 without BOM.

## Workflow

1. **Translate to Simplified Chinese.** Produce `.zh-Hans.srt` entry by entry. Read companion materials only when you hit a term whose meaning is genuinely ambiguous from the SRT alone.

2. **Convert Simplified → Traditional (Taiwan vocabulary).** This is a deterministic vocabulary/idiom swap (数据库→資料庫, 软件→軟體, 视频→影片, …), so use a conversion tool rather than re-translating. Suggested: OpenCC's `s2twp` profile.

   ```python
   from opencc import OpenCC  # pip install opencc-python-reimplemented
   OpenCC('s2twp').convert(open(src_zh_hans).read())
   ```

3. **Verify.** Entry count, timestamp lines, and encoding all match the source.

## Conventions

- **Audience: Malaysian Chinese readers.** Prefer vocabulary they'd naturally use (e.g. 令吉 for ringgit, 巴仙 for percent); avoid mainland-only idioms when a more universal phrasing exists.
- **Keep proper names and product/tech names in their original form** unless the user says otherwise — people (Hui Ming, Soh Jun Wei, …), products (Claude, MCP, Telegram, GitHub, …), file names (SKILL.md, CLAUDE.md, …).
