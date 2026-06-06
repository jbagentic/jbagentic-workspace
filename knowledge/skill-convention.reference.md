---
load_when: "creating, editing, or conforming a SKILL.md in this project — deciding its structure, headings, or front-matter"
---

# SKILL.md Convention

The standard structure for every `SKILL.md` in this project. Goal: consistent, scannable, no fluff.

## Structure

```
---
name: <kebab-case>
description: <what it does + every trigger phrase/context>
---

# <Human-readable title>

## Input
- <file/shape> + when to defer to another skill
- Project knowledge a skill needs is declared as an **input contract** — describe the expected file/path convention in prose. Never hyperlink out to `knowledge/`; whoever installs the skill satisfies the contract.

## Output
- <file/shape> + naming rule
- Invariants: <what must hold true of the output>

## Workflow
1. **<Step goal>.** What it achieves + constraints. (Suggested approach: …)
2. ...
3. **Verify.** What to check before done.

## Conventions
- Durable domain rules: glossary, audience, "don't touch" list.
```

Heading order is fixed: Title → Input → Output → Workflow → Conventions.

## Rules

- **Frontmatter is `name` + `description` only.** All "when to trigger" lives in the description — none in the body. Lean slightly pushy on triggers; skills tend to under-fire.
- **Invariants go under Output**, since they're properties of the output (e.g. "same entry count", "no numbering holes", "UTF-8 without BOM").
- **Pin the contract, free the method.** Input/output/invariants are strict — a more capable future model must still honor them. *How* a step is achieved stays open.
- **Tools are suggestions, not mandates.** When a specific library/command is the right deterministic choice, mark it "suggested" so a smarter model can override it. Models' implementation knowledge improves faster than this file does.
- **Imperative voice.** Explain *why* a constraint matters instead of stacking MUSTs.
- **One heading, one concept.** Keep it scannable. Push depth into a `references/` file only if the body outgrows a quick read.
- **A SKILL.md is self-contained.** No hyperlinks out to `knowledge/` or other units — they may be extracted separately. State cross-unit needs as input contracts (see *Input*).

## Reference implementations

`skills/talk-caption-polish/` and `skills/talk-caption-translate-zh/` follow this standard.

## Related
- **How-to** — the workspace authoring skill drives drafting, evals, and iteration (referenced by name, not path, to keep this file self-contained per the boundaries rule).
