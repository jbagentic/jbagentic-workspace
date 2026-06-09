#!/usr/bin/env python3
"""Grade subtitle-polish eval outputs against the per-case assertions.

For each run dir (with_skill / without_skill) under runs/iteration-N/eval-*/,
this finds the produced .srt in outputs/, evaluates every assertion from the
case's eval_metadata.json, and writes grading.json with the exact fields the
eval viewer needs: {text, passed, evidence}.

All three cases are real talks: the input is the talk's genuine auto-transcript,
and grading is invariants + filler-density drop + per-talk term spot-checks
against the slide-canonical forms (the speaker's own polish legitimately differs
from the skill's, so we don't diff against a gold). The raw input is read from
the committed talk folder under talk-recordings/.

Usage:
  python3 grade.py runs/iteration-1
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]  # subtitle-polish -> evals -> agentic -> repo root
TALKS = REPO / "projects/jb-agentic-meetup/talk-recordings"

# eval-name keyword -> (talk slug, restraint tokens that must survive)
CASES = {
    "khew": ("JBAgentic-20260530-meetup-1-KhewJiaPeng-AIMeetsInfrastructure", ["lah", "ya"]),
    "kowa": ("JBAgentic-20260530-meetup-1-KowaJiaLiang-OurAIJourney", ["ya", "okay", "lah"]),
    "soh":  ("JBAgentic-20260530-meetup-1-SohJunWei-AIForEverydayFriction", ["ya", "lah", "ah"]),
}


# ------------------------------ SRT parsing --------------------------------
def parse(path_or_text, is_text=False):
    text = path_or_text if is_text else Path(path_or_text).read_text(encoding="utf-8", errors="replace")
    cues = []
    for b in re.split(r"\n\s*\n", text.strip()):
        lines = b.splitlines()
        if not lines:
            continue
        idx = lines[0].strip()
        timing = lines[1].strip() if len(lines) > 1 else ""
        body = "\n".join(lines[2:]).strip() if len(lines) > 2 else ""
        cues.append({"idx": idx, "timing": timing, "body": body})
    return cues


def find_output_srt(run_dir):
    out = Path(run_dir) / "outputs"
    srts = [p for p in out.rglob("*.srt")]
    nonraw = [p for p in srts if ".raw." not in p.name]
    pick = (nonraw or srts)
    return pick[0] if pick else None


# ------------------------------ generic checks -----------------------------
def chk_exists_nonraw(ctx):
    p = ctx["out_path"]
    if p is None:
        return False, "No .srt produced in outputs/"
    ok = ".raw." not in p.name
    return ok, f"Output {p.name} ({'no' if ok else 'still has'} .raw marker)"


def chk_valid_srt(ctx):
    c = ctx["out"]
    bad = [x["idx"] for x in c if not x["timing"] or "-->" not in x["timing"]]
    return (not bad and len(c) > 0), f"{len(c)} cues parsed; {len(bad)} malformed"


def chk_no_empty(ctx):
    empties = [x["idx"] for x in ctx["out"] if not x["body"]]
    return (not empties), ("no empty cues" if not empties else f"empty cues at {empties[:5]}")


def chk_contiguous(ctx):
    nums = [int(x["idx"]) for x in ctx["out"] if x["idx"].isdigit()]
    ok = nums == list(range(1, len(nums) + 1))
    return ok, ("contiguous 1.." + str(len(nums)) if ok else f"non-contiguous: {nums[:8]}...")


def chk_no_bom(ctx):
    bom = ctx["out_bytes"][:3] == b"\xef\xbb\xbf"
    return (not bom), ("UTF-8 without BOM" if not bom else "BOM present")


def chk_timestamps_subset(ctx):
    raw_t = {x["timing"] for x in ctx["raw"]}
    missing = [x["timing"] for x in ctx["out"] if x["timing"] not in raw_t]
    ok = not missing
    return ok, ("all output timestamps exist in the raw input" if ok else f"{len(missing)} invented/shifted, e.g. {missing[:3]}")


def body_text(ctx):
    return "\n".join(x["body"] for x in ctx["out"])


# ------------------------------ term checks --------------------------------
def chk_present(ctx, term):
    ok = re.search(r"\b" + re.escape(term) + r"\b", body_text(ctx), re.I) is not None
    return ok, f"'{term}' {'present' if ok else 'MISSING'}"


def chk_keep(ctx, tokens):
    t = body_text(ctx)
    missing = [w for w in tokens if re.search(r"\b" + re.escape(w) + r"\b", t) is None]
    ok = not missing
    return ok, ("preserved: " + ", ".join(tokens) if ok else f"wrongly removed: {missing}")


def term_gone_canonical(ctx, wrong, canon, tol=0):
    """Wrong form appears <= tol times (word-boundary, case-insensitive) and the
    canonical form is present. tol gives slack for terms whose mis-hearing is also
    a real English word (e.g. 'cloud')."""
    t = body_text(ctx)
    wrong_n = len(re.findall(r"\b" + re.escape(wrong) + r"\b", t, re.I))
    canon_present = re.search(r"\b" + re.escape(canon) + r"\b", t, re.I) is not None
    ok = wrong_n <= tol and canon_present
    return ok, f"'{wrong}' x{wrong_n} (tol {tol}); '{canon}' {'present' if canon_present else 'MISSING'}"


# ------------------------------ Khew specials ------------------------------
FILLER_RE = re.compile(r"\b(um|uh|uhh|umm|erm)\b", re.I)
IAC_BAD = re.compile(r"\b(IAC|ISC|ISA|ICNA|I a C|I C|ICA)\b")


def chk_iac(ctx):
    txt = body_text(ctx)
    bad = IAC_BAD.findall(txt)
    has_canon = "IaC" in txt
    ok = has_canon and len(bad) <= 2  # canonical must dominate; allow a couple stray
    return ok, f"'IaC' present={has_canon}; bad-variants={len(bad)} (e.g. {bad[:4]})"


def chk_azure(ctx):
    txt = body_text(ctx)
    if "Asia bottle" in txt:
        return False, "'Asia bottle' still present"
    ok = "Azure portal" in txt or "Azure" in txt
    return ok, ("'Azure portal'/'Azure' present" if ok else "no Azure recovery")


# ------------------------------ assertion wiring ---------------------------
def quoted(a):
    return re.findall(r"'([^']+)'", a)


def eval_assertions(ctx, assertions, keeps):
    out = []
    raw_txt = "\n".join(x["body"] for x in ctx["raw"])
    txt = body_text(ctx)
    for a in assertions:
        al = a.lower()
        q = quoted(a)
        if "raw marker removed" in al:
            p, e = chk_exists_nonraw(ctx)
        elif "parses as valid" in al or "valid srt" in al:
            p, e = chk_valid_srt(ctx)
        elif "no empty" in al:
            p, e = chk_no_empty(ctx)
        elif "contiguous" in al:
            p, e = chk_contiguous(ctx)
        elif "timestamp" in al:
            p, e = chk_timestamps_subset(ctx)
        elif "bom" in al:
            p, e = chk_no_bom(ctx)
        elif "filler density" in al:
            raw_n = len(FILLER_RE.findall(raw_txt))
            out_n = len(FILLER_RE.findall(txt))
            p = out_n < raw_n
            e = f"standalone um/uh: raw={raw_n} -> output={out_n}"
        elif "iac" in al:
            p, e = chk_iac(ctx)
        elif "azure" in al:
            p, e = chk_azure(ctx)
        elif "corrected to" in al and len(q) >= 2:
            tol = 3 if "stray" in al else 0
            p, e = term_gone_canonical(ctx, q[0], q[1], tol)
        elif "restraint" in al:
            keep = [q[0]] if q else keeps  # preserve the first quoted token (not rewrite it)
            p, e = chk_keep(ctx, keep)
        elif "preserved" in al or "particle" in al:
            keep = q if q else keeps
            p, e = chk_keep(ctx, keep)
        elif ("appears" in al or "present" in al) and q:
            p, e = chk_present(ctx, q[0])
        else:
            p, e = False, "NO CHECKER MATCHED"
        out.append({"text": a, "passed": bool(p), "evidence": e})
    return out


# ------------------------------ driver -------------------------------------
def case_key(name):
    for k in CASES:
        if k in name.lower():
            return k
    return None


def grade_run(eval_dir, cfg):
    meta = json.loads((eval_dir / "eval_metadata.json").read_text())
    name = meta["eval_name"]
    assertions = meta["assertions"]
    run_dir = eval_dir / cfg
    out_path = find_output_srt(run_dir)
    if out_path is None:
        expectations = [{"text": a, "passed": False, "evidence": "No output SRT produced"} for a in assertions]
        (run_dir / "grading.json").write_text(json.dumps({"expectations": expectations}, indent=2))
        return name, cfg, 0, len(assertions)

    key = case_key(name)
    if key is None:
        raise SystemExit(f"unknown talk for eval '{name}' (expected one of {list(CASES)})")
    slug, keeps = CASES[key]
    raw_path = TALKS / slug / f"{slug}.en.raw.srt"

    ctx = {
        "out_path": out_path,
        "out_bytes": out_path.read_bytes(),
        "out": parse(out_path),
        "raw": parse(raw_path),
    }
    expectations = eval_assertions(ctx, assertions, keeps)
    (run_dir / "grading.json").write_text(json.dumps({"expectations": expectations}, indent=2))
    passed = sum(1 for x in expectations if x["passed"])
    return name, cfg, passed, len(expectations)


def main():
    itr = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "runs/iteration-1"
    itr = itr if itr.is_absolute() else ROOT / itr
    for eval_dir in sorted(itr.glob("eval-*")):
        for cfg in ("with_skill", "without_skill"):
            if (eval_dir / cfg).exists():
                name, c, p, n = grade_run(eval_dir, cfg)
                print(f"{name:24s} {c:14s} {p}/{n}")


if __name__ == "__main__":
    main()
