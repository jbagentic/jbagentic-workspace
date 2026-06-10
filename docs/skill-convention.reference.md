# SKILL.md Convention

The standard structure for every `SKILL.md` in this project. Goal: consistent, scannable, and reusable across projects and teams.

## Structure

```
---
name: <kebab-case>
description: <what it does + every trigger phrase/context>
---

# <Human-readable title>

## Input
- <file/shape> + when to defer to another skill
- Project-specific facts a skill needs → an **input contract**: describe the expected file/path convention in prose, with a sensible default. (See *Context-agnostic by design*.)

## Output
- <file/shape> + naming rule
- Invariants: <what must hold true of the output>

## Workflow
1. **<Step goal>.** What it achieves + constraints. (Suggested approach: …)
2. ...
3. **Verify.** What to check before done.

## Conventions
- Durable, capability-level rules only (e.g. "keep proper names in their original form"); defer project values — glossary, audience, locale — to the reference doc.
```

Heading order is fixed: Title → Input → Output → Workflow → Conventions.

## Rules

- **Context-agnostic by design.** Design each skill as a reusable *capability*, not a project task. Keep project-specific facts out of the body — paths, filenames, glossaries, target audience, naming schemes. Declare them as an **input contract** (describe the shape, give a sensible default) and let whoever installs the skill satisfy it from their own reference doc. This is what lets one skill serve many projects and teams. When a skill is irreducibly project-specific, that's fine — but externalize whatever *can* be.
- **Frontmatter: `name` + `description` by default.** These two carry every skill; all other fields are optional — add `allowed-tools` to scope tools, or `model`/`effort` to tune cost, only when the skill genuinely needs them. Avoid `paths`: it pins a project's file layout into the skill (see *Context-agnostic by design*). Keep every trigger phrase in `description` — the one field every runtime reads — not in a separate field or the body. Lean slightly pushy on triggers (skills under-fire) and phrase them around the capability, not one project's filenames.
- **Invariants go under Output**, since they're properties of the output (e.g. "same entry count", "no numbering holes", "UTF-8 without BOM").
- **Pin the contract, free the method.** Input/output/invariants are strict — a more capable future model must still honor them. *How* a step is achieved stays open: name a tool only as a *suggestion* so a smarter model can override it, since implementation knowledge improves faster than this file does.
- **Imperative voice.** Explain *why* a constraint matters instead of stacking MUSTs.
- **One heading, one concept.** Keep it scannable. Push depth into a `references/` file only if the body outgrows a quick read.
- **Self-contained.** No hyperlinks out of the skill folder — it may be extracted and shipped on its own. State external needs as input contracts (see *Context-agnostic by design*).

## Reference implementations

`skills/subtitle-polish/`, `skills/subtitle-translate-zh/`, `skills/redirect-bookmark/`, and `skills/talk-youtube-metadata/` follow this standard.
