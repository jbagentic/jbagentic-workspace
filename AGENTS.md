# Agents Guide

Welcome to JB Agentic's digital workspace. 

JB Agentic is a volunteer-led community that runs regular meetups for tech practitioners to meet and share best practices on using AI agentic tools in software work.

This workspace contains the necessary knowledge and skills to produce digital deliverables to support JB Agentic activities, such as video recordings, official website, etc.


## Knowledge

Load a file below only when its line matches your task. The manifest is **generated** —
do not hand-edit between the markers; regenerate after any change to `knowledge/` (see the [agentic-workspace skill](skills/agentic-workspace/SKILL.md)).

<!-- KNOWLEDGE MANIFEST (generated) — load a file when its line matches your task -->

**community**
- [describing JB Agentic in audience-facing copy — descriptions, website, social, slides; facts, links, blurbs](knowledge/jb-agentic-meetup.reference.md)
- [looking up facts about a past meetup — date, time, number, talks, speakers, attendance](knowledge/meetup-log.reference.md)

**authoring**
- [creating or conforming a SKILL.md — structure, headings, front-matter](knowledge/skill-convention.reference.md)

<!-- END KNOWLEDGE MANIFEST -->


## Boundaries & linking

`knowledge/` and `skills/` are **independently extractable units** — any skill may later be lifted into its own repo and installed system-wide, and `knowledge/` may be repackaged on its own.

1. **Hyperlinks point only *within* a unit.** A `knowledge/` file links to other `knowledge/` files; a skill links only inside itself. Never link `knowledge/ ↔ skills/` in either direction.
2. **Express cross-unit needs as contracts, not links.** When a skill needs project knowledge, it *describes* the expected input — e.g. a file/path convention — in prose. No hyperlink required; whoever installs the skill satisfies the contract.
3. **Duplication is the price of decoupling.** When a unit needs a durable fact from another, copy it in rather than link out.

`AGENTS.md` is exempt: it's the root index, not a shippable unit, so it may link into both folders.

## Authoring skills

When creating, editing, or improving any skill in `skills/`:

1. Use the **skill-creator** skill to drive the process (drafting, evals, iteration).
2. Conform the resulting `SKILL.md` to this project's house style in
   [`knowledge/skill-convention.reference.md`](knowledge/skill-convention.reference.md) —
   it governs structure and rules; skill-creator governs the workflow. On conflict, follow the reference file for the final shape of the file.

**Skill evals live outside the skill folder**, at `skill_evals/<skill-name>/` (e.g. `skill_evals/talk-youtube-metadata/evals.json`) — not inside `skills/<name>/`, so they never ship in the installed `.skill`. They are dev-time specs read by skill-creator, never by the skill at runtime. Auto-discovery doesn't reach this path, so point skill-creator at it explicitly when running or iterating evals. Direct skill-creator's run outputs to `skill_evals/<skill-name>/runs/` (specs and their results stay together); that `runs/` scratch is gitignored. After aggregating a run, **promote** a curated summary to the committed `skill_evals/<skill-name>/benchmarks/iteration-N.md` and append a row to `benchmarks/history.md` — that's the durable quality-over-time record; `runs/` is disposable.
