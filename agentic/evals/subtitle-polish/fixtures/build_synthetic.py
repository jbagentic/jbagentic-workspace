#!/usr/bin/env python3
"""Build synthetic subtitle-polish fixtures from real polished talk SRTs.

For each synthetic case we:
  1. Take a contiguous cue range from a talk's polished `.en.srt` -> the GOLD
     (renumbered to start at 1). This is "what good output looks like".
  2. Derive a dirtied `.raw.srt` INPUT by applying a documented edit list:
       - inject standalone filler tokens (um/uh/you know/like ...)
       - inject duplicate-word stutters (the the / I I ...), some across cue boundaries
       - swap slide-backed canonical terms for phonetic near-misses
     Timestamps and cue count are preserved; only cue TEXT changes.
  3. Emit an answer-key JSON recording every injected error so assertions
     (and the grader) can check the polished output removed/corrected each one.

The polished talk SRTs already contain Singlish particles (ya/lah/mah) and
affirmations (yeah/okay) that the skill must PRESERVE -- those are recorded as
`restraint_keep` so grading can verify the skill didn't over-correct them.

Run from the fixtures/ dir:  python3 build_synthetic.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TALKS = HERE.parent.parent.parent.parent / "projects/jb-agentic-meetup/talk-recordings"


def parse_srt(text):
    """Return list of (index, timing, text) cues."""
    blocks = re.split(r"\n\s*\n", text.strip())
    cues = []
    for b in blocks:
        lines = b.splitlines()
        if len(lines) < 3:
            continue
        idx, timing, body = lines[0], lines[1], "\n".join(lines[2:])
        cues.append([idx.strip(), timing.strip(), body])
    return cues


def slice_renumber(cues, start, end):
    """Take cues whose original index in [start, end], renumber from 1."""
    out = []
    for idx, timing, body in cues:
        if start <= int(idx) <= end:
            out.append([str(len(out) + 1), timing, body])
    return out


def write_srt(cues, path):
    blocks = [f"{i}\n{t}\n{b}" for i, t, b in cues]
    # SRT convention: trailing newline, UTF-8 no BOM, CRLF-free
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def apply_edits(cues, edits):
    """edits: list of dicts {cue:int(1-based), find:str, replace:str}.
    Applies to a deep copy; returns (new_cues, applied_count)."""
    new = [[i, t, b] for i, t, b in cues]
    applied = 0
    for e in edits:
        c = e["cue"] - 1
        body = new[c][2]
        if e["find"] not in body:
            raise SystemExit(f"FIND MISS cue {e['cue']}: {e['find']!r} not in {body!r}")
        new[c][2] = body.replace(e["find"], e["replace"], 1)
        applied += 1
    return new, applied


def load_talk(folder, name):
    f = TALKS / folder / f"{name}.en.srt"
    return parse_srt(f.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# CASE A: SohJunWei -- AI for Everyday Friction. Gold = polished cues 117-159.
# Slide-backed canonical terms (slide-06 "What Is Behind It?"):
#   Telegram, MCP (Expense Assistant MCP Server), Hermes Agent, dashboard, database
# ---------------------------------------------------------------------------
soh_src = load_talk(
    "JBAgentic-20260530-meetup-1-SohJunWei-AIForEverydayFriction",
    "JBAgentic-20260530-meetup-1-SohJunWei-AIForEverydayFriction",
)
soh_gold = slice_renumber(soh_src, 117, 159)

# Edits applied to GOLD text to produce the dirtied RAW input.
# Cue numbers are 1-based within the renumbered gold (117 -> cue 1).
soh_term_edits = [
    {"cue": 7, "find": "the Hermes agent", "replace": "the Herpes agent", "wrong": "Herpes agent", "term": "Hermes agent"},
    {"cue": 14, "find": "the Hermes agent", "replace": "the Herpes agent", "wrong": "Herpes agent", "term": "Hermes agent"},
    {"cue": 16, "find": "the Telegram", "replace": "the telegraph", "wrong": "telegraph", "term": "Telegram"},
    {"cue": 36, "find": "the Telegram", "replace": "the telegraph", "wrong": "telegraph", "term": "Telegram"},
    {"cue": 31, "find": "MCP which", "replace": "the EMCP which", "wrong": "EMCP", "term": "MCP"},
    {"cue": 43, "find": "using the MCP", "replace": "using the EMCP", "wrong": "EMCP", "term": "MCP"},
]
soh_filler_edits = [
    {"cue": 2, "find": "so it basically", "replace": "so it basically um", "kind": "filler"},
    {"cue": 9, "find": "trying to explore", "replace": "trying to uh explore", "kind": "filler"},
    {"cue": 20, "find": "the AI will basically", "replace": "the AI will uh basically", "kind": "filler"},
    {"cue": 32, "find": "I will quickly demo", "replace": "I will you know quickly demo", "kind": "filler"},
]
soh_stutter_edits = [
    {"cue": 1, "find": "so more specific", "replace": "so so more specific", "kind": "stutter"},
    {"cue": 24, "find": "saved to the database", "replace": "saved to the the database", "kind": "stutter"},
    {"cue": 29, "find": "the use of tools", "replace": "the use of of tools", "kind": "stutter"},
]

# ---------------------------------------------------------------------------
# CASE B: KowaJiaLiang -- Our AI Journey. Gold = polished cues 424-447.
# Slide-backed canonical terms (slide-06 "Automate processes with Claude Code"):
#   Claude / Claude Code, MCP, JSON, API
# ---------------------------------------------------------------------------
kowa_src = load_talk(
    "JBAgentic-20260530-meetup-1-KowaJiaLiang-OurAIJourney",
    "JBAgentic-20260530-meetup-1-KowaJiaLiang-OurAIJourney",
)
kowa_gold = slice_renumber(kowa_src, 424, 447)

kowa_term_edits = [
    {"cue": 2, "find": "MCP is a standardized", "replace": "the NCP is a standardized", "wrong": "NCP", "term": "MCP"},
    {"cue": 7, "find": "the old way before MCP", "replace": "the old way before NCP", "wrong": "NCP", "term": "MCP"},
    {"cue": 18, "find": "inside Claude", "replace": "inside cloud", "wrong": "cloud", "term": "Claude"},
    {"cue": 19, "find": "so Claude can", "replace": "so cloud can", "wrong": "cloud", "term": "Claude"},
    {"cue": 24, "find": "set up through JSON", "replace": "set up through Jason", "wrong": "Jason", "term": "JSON"},
]
kowa_filler_edits = [
    {"cue": 1, "find": "so let me go next", "replace": "so um let me go next", "kind": "filler"},
    {"cue": 6, "find": "enabling the AI to retrieve", "replace": "enabling the AI to like retrieve", "kind": "filler"},
    {"cue": 15, "find": "this is very hard", "replace": "this is uh very hard", "kind": "filler"},
]
kowa_stutter_edits = [
    {"cue": 2, "find": "for AI agent", "replace": "for AI AI agent", "kind": "stutter"},
    {"cue": 9, "find": "for every external", "replace": "for for every external", "kind": "stutter"},
]


def build(name, gold, term_edits, filler_edits, stutter_edits, restraint_keep, source):
    out_dir = HERE / name
    gold_path = out_dir / f"{name}.en.srt.gold"
    raw_path = out_dir / f"{name}.en.raw.srt"
    write_srt(gold, gold_path)

    all_edits = term_edits + filler_edits + stutter_edits
    raw, n = apply_edits(gold, all_edits)
    write_srt(raw, raw_path)

    key = {
        "case": name,
        "source": source,
        "gold": gold_path.name,
        "raw": raw_path.name,
        "cue_count": len(gold),
        "term_corrections": [
            {"cue": e["cue"], "wrong": e["wrong"], "should_become": e["term"]} for e in term_edits
        ],
        "term_targets": sorted({e["term"] for e in term_edits}),
        "injected_fillers": [{"cue": e["cue"], "added": e["replace"]} for e in filler_edits],
        "injected_stutters": [{"cue": e["cue"], "added": e["replace"]} for e in stutter_edits],
        "restraint_keep": restraint_keep,
        "total_injected_errors": n,
    }
    (out_dir / "answer-key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    print(f"{name}: {len(gold)} cues, {len(term_edits)} term errors, "
          f"{len(filler_edits)} fillers, {len(stutter_edits)} stutters -> {n} total")
    return key


build(
    "sohjunwei-synth", soh_gold, soh_term_edits, soh_filler_edits, soh_stutter_edits,
    # "OpenClaw" is the speaker's own word; the slides say "OpenRouter". It is NOT
    # a phonetic transcription error, so the skill must leave it alone (don't
    # reconcile speech to slides). Good over-correction guard.
    restraint_keep=["OpenClaw"],
    source="JBAgentic-20260530-meetup-1-SohJunWei-AIForEverydayFriction .en.srt cues 117-159",
)
build(
    "kowajialiang-synth", kowa_gold, kowa_term_edits, kowa_filler_edits, kowa_stutter_edits,
    restraint_keep=["ya", "okay"],  # Singlish particle + affirmation must survive
    source="JBAgentic-20260530-meetup-1-KowaJiaLiang-OurAIJourney .en.srt cues 424-447",
)
print("done")
