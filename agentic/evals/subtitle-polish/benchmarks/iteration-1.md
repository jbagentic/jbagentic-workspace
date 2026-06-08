# Benchmark — subtitle-polish, iteration 1

- **Date:** 2026-06-08
- **Model:** claude-opus-4-8
- **Cases:** 3 — `real-fulllength-khewjiapeng` (real auto-transcript, 916 cues), `synth-sohjunwei-excerpt` (43-cue dirtied excerpt), `synth-kowajialiang-excerpt` (24-cue dirtied excerpt)
- **Runs per case:** 1
- **Baseline:** same prompt + same files, no skill
- **Raw outputs / viewer:** `runs/iteration-1/` (gitignored) — `review-iteration-1.html`

## Result

| Metric | With skill | Baseline | Delta |
|---|---|---|---|
| Pass rate (assertions) | 93.3% (28/30) | 96.7% (29/30) | **−0.03** |
| Time (mean) | 245.6s | 169.7s | +75.9s |
| Tokens (mean) | 50,730 | 46,118 | +4,612 |

The skill did **not** beat the no-skill baseline on raw assertion pass rate this
iteration, and cost more time and tokens. But the *kind* of failure differs, and
that's the real signal — see below.

## Per-case breakdown

| Case | With skill | Baseline | Discriminating? |
|---|---|---|---|
| real-fulllength-khewjiapeng | 10/10 | 10/10 | No — assertions too coarse |
| synth-sohjunwei-excerpt | 9/10 | 10/10 | Yes — skill over-corrected |
| synth-kowajialiang-excerpt | 9/10 | 9/10 | Yes — failures differ in kind |

## Reading

- **The skill's loss is an over-correction, not a miss.** On SohJunWei the speaker
  says "OpenClaw"; the slides say "OpenRouter". The skill rewrote speech to match
  the slide ("OpenClaw" → "OpenRouter"), which violates its own convention
  ("speakers disagree with their own slides, and that's not a transcription
  error"). The baseline left it as spoken and passed. This is the headline finding
  for the next iteration: the glossary step is reaching past phonetic near-misses
  into off-slide reconciliation. *(Caveat: whether "OpenRouter" is the truer term
  is genuinely debatable — worth a human call before hard-coding a fix.)*
- **The baseline's loss is the exact failure the skill prevents.** On KowaJiaLiang
  the baseline scrubbed the Singlish particle "ya" and the affirmation "okay" as if
  they were filler; the with-skill run preserved both. So the skill's restraint
  guidance demonstrably works — it just isn't enough to offset the points lost
  above.
- **The skill's other loss is a genuine miss:** it left one injected filler
  ("...AI to **like** retrieve...") in the KowaJiaLiang output.
- **The real case is non-discriminating.** Both runs cleared all 10 invariant +
  spot-check assertions (IaC family, Azure, Terraform/Bicep, MCP, file names all
  recovered; timestamps and numbering intact). The assertions aren't fine-grained
  enough to separate two strong-but-different polishes.

## Caveats

- **Single sample per case** — no variance estimate; the −0.03 delta is within noise.
- **Coarse real-case assertions.** The real case grades on invariants + a few
  spot-checked terms, so it can't distinguish quality differences. A future
  iteration could diff against the human `*.en.srt` gold on a sampled cue set.
- **Synthetic fixtures are author-controlled.** Errors were injected from a known
  answer key (`fixtures/*/answer-key.json`), so grading is exact but the error
  distribution is ours, not a real transcriber's.
- The `OpenClaw`/`OpenRouter` assertion encodes a judgment call; revisit it if the
  skill is changed to handle off-slide terms differently.
