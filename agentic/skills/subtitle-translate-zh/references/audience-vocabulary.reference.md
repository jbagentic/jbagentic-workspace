# Audience vocabulary — reference

Reusable know-how for translating subtitles into the right Chinese for a *named* audience. The project's reference doc names which audiences it wants; this file is the skill's expertise on what each implies — output script, locale vocabulary, and idiom. It is the same wherever the skill runs, so it ships with the skill.

## How to use this

1. Read the target audience(s) the project's reference doc names.
2. Look each up in the profile table below for its output script and vocabulary rules.
3. An audience not listed here → produce widely-understood Chinese and ask.

## Audience profiles

| Audience | Output / script | Money & percent | Tech vocabulary & idiom |
|----------|-----------------|-----------------|--------------------------|
| **Malaysian Chinese readers** | `zh-Hans` — Simplified | ringgit → `令吉`; percent → `巴仙` | Mainland-flavored tech terms are the natural written register here. Prefer locally-natural phrasing; avoid mainland-only idioms when a more universal phrasing exists. |
| **Taiwanese readers** | `zh-Hant` — Traditional, Taiwan vocabulary | ringgit → `林吉特`; percent → `百分比` (`百分之N` when numeric) | Taiwan tech forms: `資料庫`, `軟體`, `影片`, `網路`, `資訊`, `程式`. Natural Taiwan Mandarin; no Malaysian localisms. OpenCC `s2twp` supplies the Taiwan tech forms — see below. |

Extend by adding a row with the same columns (e.g. Hong Kong readers, mainland readers): output script, money/percent localisms, and tech-vocabulary + idiom guidance.

## How the two files relate

The Simplified file is translated for Malaysian Chinese readers. The Traditional file is *derived* from it by a deterministic OpenCC `s2twp` conversion, which handles script and mainland→Taiwan tech vocabulary (`数据库→資料庫`, `软件→軟體`, `视频→影片`, `网络→網路`, `信息→資訊`, `程序→程式`).

What OpenCC does **not** touch: loan-word localisms like `令吉` and `巴仙`. These are valid Chinese characters, not mainland tech terms, so `s2twp` carries them through verbatim — which is wrong for Taiwanese readers. Correct them with the map below, after conversion.

## Malaysian → Taiwan localism correction

Apply to the converted Traditional file — the small set OpenCC leaves behind:

| Malaysian (in `zh-Hans`) | OpenCC leaves it as | Taiwan correction (`zh-Hant`) |
|--------------------------|---------------------|-------------------------------|
| `令吉` (ringgit) | `令吉` | `林吉特` |
| `巴仙` (percent) | `巴仙` | `百分比`, or `百分之N` when followed by a number (e.g. "80 percent" → `百分之八十`) |

## What does not belong here

Only reusable locale/audience vocabulary lives here. A project's *own* values — product and coined-term names, speaker names, project glossary, and which audiences the project wants — stay in the project's reference doc.
