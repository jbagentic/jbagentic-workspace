# Skill evals

Dev-time evaluation specs and durable benchmark records for the skills in [`../skills/`](../skills/).
Everything here is **dev-time only** — it is read by skill-creator while building and iterating skills,
never by a skill at runtime, and it lives **outside the skill folders so it never ships in the installed
`.skill`**.

## Structure

One folder per skill being evaluated, named to match the skill (e.g. `doc-this/`,
`talk-youtube-metadata/`). Each holds:

- `evals.json` — the eval spec (test cases: id, prompt, expected output, fixtures).
- `fixtures/` — input materials the cases run against.
- `benchmarks/` — **committed**, the durable quality-over-time record:
  - `iteration-N.md` — curated summary of one run.
  - `history.md` — one row per iteration (pass rates, deltas).
- `runs/` — **gitignored** scratch; raw per-run outputs, disposable.

## Running and promoting evals

- Auto-discovery does not reach this path, so **point skill-creator at the eval folder explicitly**
  when running or iterating.
- Direct run outputs to `agentic/evals/<skill-name>/runs/` so specs and their results stay together;
  `runs/` is gitignored and disposable.
- After aggregating a run, **promote** a curated summary to the committed
  `agentic/evals/<skill-name>/benchmarks/iteration-N.md` and append a row to `benchmarks/history.md` —
  that's the durable record; the `runs/` scratch can be thrown away.
