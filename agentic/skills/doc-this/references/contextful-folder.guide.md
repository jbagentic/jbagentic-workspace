# Contextful Folder — guide

A folder is **contextful** when a human or agent reading it gets **just enough** context to do their job well — sufficient but bounded.

This guide explains the pattern, why it works, and how to apply it. For the exact file vocabulary and naming rules, see the [Contextful Folder reference](contextful-folder.reference.md).

## The problems

### Problem 1: Written context is now mandatory

Context has always been critical for people to do good work. Language-model agents force you to **write that context down** — they can't tap someone on the shoulder or rely on tribal knowledge.

This raises a new challenge:

- You need to get the information written down in the first place.
- You need to maintain it from now on.

### Problem 2: Loading too much or too little hurts the work

Getting the right amount of context for a task is hard. Two things go wrong:

- **Too much, and you pay to distill it back down.** The context loaded is more than the task needs — too broad, too much information. Agents burn far more tokens than necessary. Humans waste attention on what doesn't matter. Both spend effort distilling instead of doing.

- **Too little, and the work comes out wrong.** The knowledge exists somewhere, but the reader can't find it or doesn't know it's there. Agents do the task in ways nobody intended. Humans miss constraints or requirements. Output quality degrades. In the worst case, the work gets redone.

## The idea

### The folder as context boundary

When you do digital work, you naturally gather inputs into a folder, run tools to transform or summarize them, and write the results back to the same folder. It's already where the work happens — so the context for that work, what you need to know and how it's done, can live there too.

That turns the folder into a natural contextual boundary for work:

**Working in a folder, most of what you need to know is already in it.** You can still look elsewhere when you have to, but usually you won't need to — no scanning the whole repo, no guessing where the knowledge lives.

**When your work changes the folder, you record it in the same folder.** The docs to update sit right next to the files you touched, so you fix them in the same motion.

You're already in the folder, doing the work. Reading its context and keeping it current is just staying where you are — and that's what makes context cheap to get and cheap to keep.

### The test

Drop a human or agent into the folder cold — no prior conversation, no external briefing. Can they read the local docs and answer:

1. What is this folder for?
2. What lives here?
3. How do I work here?
4. Where do I look for more detail?

If yes, the folder is contextful. If no, something is missing or misrouted.

### Why folders?

Folders are already how people organize information everywhere — codebases, documents, shared drives. They're a tool everyone already knows. Nobody needs to learn a new system.

More importantly, folders are **hierarchical**. That gives you context that unfolds as you need it, for free:

- **Need broader context?** Look up to the parent folder.
- **Need more specific context?** Look into a nested folder.

Each level is self-contained at its scope. Parents handle the bigger picture. Children handle specifics. No single folder explains the whole world — it handles its layer and links up or down when you need to zoom.

This nesting lets the pattern scale from a single utility folder to an entire monorepo.

## Making a folder contextful

The boundary is only half the answer — it bounds what you load and what you maintain, but it can't write the context down for you. That's the other half of the pattern: a structured method for filling the folder, so writing isn't a blank-page chore.

A folder isn't contextful by default. You make it so.

### README.md — always present, always the entry point

Every contextful folder starts with a **README**. It does two jobs:

1. **Orient** — what is this folder, what lives here, what's the scope.
2. **Manifest** — list each deeper doc with a one-line hook, so a reader sees what's available without loading everything.

The manifest enables **selective loading**. You see the menu before you order. Without a README, you'd have to scan all files to know what's there — the folder isn't contextful.

### Topic atoms — deeper knowledge, selectively loaded

Deeper knowledge lives in typed files, sliced into small self-contained **topic atoms**. Each atom answers one question. You reach them through the manifest, loading only the atom relevant to your task.

Break knowledge into atoms, each typed by purpose, instead of stitching everything into one long document. That's the core idea of **topic-based authoring**, from the **DITA** framework (Darwin Information Typing Architecture).

DITA's three topic types map onto our file vocabulary:

| DITA topic type | Our file type | Answers |
|-----------------|---------------|---------|
| Concept | Guide | "Help me understand it." |
| Task | Runbook | "Walk me through the steps." |
| Reference | Reference | "Tell me the exact fact." |

One question, one file. Load only what you need. Link between atoms instead of repeating — a runbook links to its conceptual guide rather than re-explaining inline. That keeps atoms reusable and context windows compact.

### AGENTS.md — optional

When present, it holds instructions and constraints for agents, not knowledge.

### Decision records — optional, append-only

Sometimes the important context isn't *how things work now* but *why a choice was made then*. Decision records capture that reasoning — the tradeoffs considered, the alternatives rejected, and why the final call was made.

Topic atoms are living documents that get updated as things change. Decision records are different — you never edit an old record, you write a new one instead. This makes them a historical trail, not current-state knowledge.

Use them when design choices would otherwise be lost in PRs, Slack, or conversation — and future contributors will need that reasoning without asking the original author. They live in their own subfolder, separate from topic atoms.

## A side benefit: context-agnostic skills

The pattern also makes skills more reusable. Keep the skill and its context apart, and a job's inputs — paths, conventions, facts — live in the context, not in the skill. The skill holds only the steps, and takes its inputs from whatever context it runs in. So the same skill works in many contexts — projects, teams, organizations — instead of being tied to one.

## Related

- [Contextful Folder reference](contextful-folder.reference.md) — the file vocabulary, naming, and rule-of-thumb table.
