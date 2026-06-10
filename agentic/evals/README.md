# Skill evals

Dev-time evaluation specs and durable benchmark records for the skills in [`../skills/`](../skills/).
Everything here is **dev-time only** — skill-creator reads it while building and improving skills,
never a skill at runtime, and it lives **outside the skill folders so it never ships in the installed
`.skill`**.

## Structure

One folder per skill being evaluated, named to match the skill (e.g. `doc-this/`,
`youtube-metadata/`). Each holds:

- `evals.json` — the eval spec (test cases: id, prompt, expected output, fixtures).
- `fixtures/` — input materials the cases run against.
- `benchmarks/` — **committed**, the durable quality-over-time record:
  - `iteration-N.md` — curated summary of one run.
  - `history.md` — one row per iteration (pass rates, deltas).
- `runs/` — **gitignored** scratch; raw per-run outputs, disposable.

## Running and promoting evals

- Auto-discovery does not reach this path, so **point skill-creator at the eval folder explicitly**
  when running or improving a skill.
- **`subtitle-polish` stages its inputs first.** Run `python3 subtitle-polish/prepare.py` to
  materialize each talk's real `.en.raw.srt` + slide deck into `subtitle-polish/stage/`
  (gitignored) from `talk-recordings/`. The skill runs against that throwaway copy so its
  sibling output (`<slug>.en.srt`) never overwrites the committed talk folder. The decks and
  transcripts live once, in `talk-recordings/` — they are not copied into the eval.
- Direct run outputs to `agentic/evals/<skill-name>/runs/` so specs and their results stay together;
  `runs/` is gitignored and disposable.
- After aggregating a run, **promote** a curated summary to the committed
  `agentic/evals/<skill-name>/benchmarks/iteration-N.md` and append a row to `benchmarks/history.md` —
  that's the durable record; the `runs/` scratch can be thrown away.
