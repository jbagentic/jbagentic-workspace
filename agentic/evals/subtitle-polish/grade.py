#!/usr/bin/env python3
"""Grade subtitle-polish eval outputs against the per-case assertions.

For each run dir (with_skill / without_skill) under runs/iteration-N/eval-*/,
this finds the produced .srt in outputs/, evaluates every assertion from the
case's eval_metadata.json, and writes grading.json with the exact fields the
eval viewer needs: {text, passed, evidence}.

Synthetic cases (sohjunwei / kowajialiang) are checked precisely against their
fixture answer-key.json + gold. The real case (khewjiapeng) is checked on
invariants + filler-density drop + spot-checked term recovery, since the
speaker's own polish legitimately differs from the skill's.

Usage:
  python3 grade.py runs/iteration-1
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIX = ROOT / "fixtures"

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
    # prefer one without a .raw marker
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


def out_timings(ctx):
    return [x["timing"] for x in ctx["out"]]


def chk_timestamps_subset(ctx):
    raw_t = {x["timing"] for x in ctx["raw"]}
    missing = [t for t in out_timings(ctx) if t not in raw_t]
    ok = not missing
    return ok, ("all output timestamps exist in the raw input" if ok else f"{len(missing)} invented/shifted, e.g. {missing[:3]}")


def chk_timestamps_equal(ctx):
    raw_t = [x["timing"] for x in ctx["raw"]]
    out_t = out_timings(ctx)
    ok = raw_t == out_t
    return ok, ("timestamps identical to raw, in order" if ok else f"timestamp list differs ({len(out_t)} vs {len(raw_t)} cues)")


def body_text(ctx):
    return "\n".join(x["body"] for x in ctx["out"])


# ------------------------------ synth checks -------------------------------
def term_gone_canonical(ctx, wrong, canonical):
    t = body_text(ctx)
    # word-boundary check for the wrong token (case-insensitive), canonical present (case-sensitive)
    wrong_present = re.search(r"\b" + re.escape(wrong) + r"\b", t, re.I) is not None
    # canonical presence is case-insensitive: a correct fix that differs only in
    # capitalization (e.g. 'Hermes Agent' vs 'Hermes agent') still counts.
    canon_present = re.search(r"\b" + re.escape(canonical) + r"\b", t, re.I) is not None
    ok = (not wrong_present) and canon_present
    return ok, f"'{wrong}' {'still present' if wrong_present else 'gone'}; '{canonical}' {'present' if canon_present else 'MISSING'}"


def filler_removed(ctx, tokens):
    """tokens: list of standalone filler words that were injected and must be gone
    as standalone words (not as substrings of real words)."""
    t = body_text(ctx)
    still = [w for w in tokens if re.search(r"\b" + re.escape(w) + r"\b", t)]
    # 'like'/'uh'/'um' can legitimately appear; we judge by count drop instead for ambiguous ones.
    return still, t


def chk_no_stutters(ctx, pairs):
    """pairs: list of (word) that were duplicated; ensure no 'word word' dup remains for them."""
    t = body_text(ctx).lower()
    remaining = []
    for w in pairs:
        if re.search(r"\b" + re.escape(w.lower()) + r"\s+" + re.escape(w.lower()) + r"\b", t):
            remaining.append(w)
    ok = not remaining
    return ok, ("all injected stutters collapsed" if ok else f"still duplicated: {remaining}")


def chk_keep(ctx, tokens):
    t = body_text(ctx)
    missing = [w for w in tokens if re.search(r"\b" + re.escape(w) + r"\b", t) is None]
    ok = not missing
    return ok, ("preserved: " + ", ".join(tokens) if ok else f"wrongly removed: {missing}")


# ------------------------------ case wiring --------------------------------
def grade_synth(ctx, key):
    """Return dict assertion_text -> (passed, evidence) for synthetic cases."""
    res = {}
    res["__exists"] = chk_exists_nonraw(ctx)
    res["__contig"] = chk_contiguous(ctx)
    res["__noempty"] = chk_no_empty(ctx)
    res["__bom"] = chk_no_bom(ctx)
    res["__ts"] = chk_timestamps_equal(ctx)
    # term corrections grouped by canonical
    by_canon = {}
    for tc in key["term_corrections"]:
        by_canon.setdefault((tc["wrong"], tc["should_become"]), 0)
        by_canon[(tc["wrong"], tc["should_become"])] += 1
    res["__terms"] = {}
    for (wrong, canon), n in by_canon.items():
        res["__terms"][(wrong, canon)] = term_gone_canonical(ctx, wrong, canon)
    return res


def assertion_eval_synth(ctx, key, assertions):
    """Map each assertion string (in order) to a checker result."""
    out = []
    cnt = body_text(ctx)
    for a in assertions:
        al = a.lower()
        if "raw marker removed" in al:
            p, e = chk_exists_nonraw(ctx)
        elif "contiguous" in al and "cues" in al:
            ok1, e1 = chk_contiguous(ctx)
            ok2, e2 = chk_no_empty(ctx)
            want = key["cue_count"]
            got = len([x for x in ctx["out"] if x["idx"].isdigit()])
            okc = got == want
            p = ok1 and ok2 and okc
            e = f"{e1}; {e2}; count {got}/{want}"
        elif "timestamp" in al:
            p, e = chk_timestamps_equal(ctx)
        elif "bom" in al:
            p, e = chk_no_bom(ctx)
        elif "corrected to" in al:
            # extract 'X' is corrected to 'Y'
            m = re.findall(r"'([^']+)'", a)
            wrong, canon = m[0], m[1]
            p, e = term_gone_canonical(ctx, wrong, canon)
        elif "injected fillers" in al:
            # tokens listed in parens
            toks = re.findall(r"\b(um|uh|you know|like)\b", a)
            # judge: injected fillers gone. We check the specific injected phrases from key.
            still = []
            for f in key["injected_fillers"]:
                # the inserted filler word is the token added relative to gold; check the exact inserted phrase absent
                added = f["added"]
                if added in cnt:
                    still.append(f"cue{f['cue']}:{added!r}")
            p = not still
            e = ("all injected filler phrases gone" if p else f"still present: {still}")
        elif "injected stutters" in al:
            still = []
            for s in key["injected_stutters"]:
                if s["added"] in cnt:
                    still.append(f"cue{s['cue']}:{s['added']!r}")
            p = not still
            e = ("all injected stutters collapsed" if p else f"still present: {still}")
        elif "restraint" in al or "preserved" in al:
            p, e = chk_keep(ctx, key["restraint_keep"])
        elif "valid srt" in al or "parses" in al:
            p, e = chk_valid_srt(ctx)
        elif "no empty" in al:
            p, e = chk_no_empty(ctx)
        else:
            p, e = False, "NO CHECKER MATCHED"
        out.append({"text": a, "passed": bool(p), "evidence": e})
    return out


# ------------------------------ real case ----------------------------------
FILLER_RE = re.compile(r"\b(um|uh|uhh|umm|erm)\b", re.I)
IAC_BAD = re.compile(r"\b(IAC|ISC|ISA|ICNA|I a C|I C|ICA)\b")

def assertion_eval_real(ctx, assertions):
    out = []
    txt = body_text(ctx)
    raw_txt = "\n".join(x["body"] for x in ctx["raw"])
    for a in assertions:
        al = a.lower()
        if "raw marker removed" in al:
            p, e = chk_exists_nonraw(ctx)
        elif "parses as valid" in al:
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
            bad = IAC_BAD.findall(txt)
            has_canon = "IaC" in txt
            p = has_canon and len(bad) <= 2  # allow a couple stray; canonical must dominate
            e = f"'IaC' present={has_canon};残 bad-variants={len(bad)} (e.g. {bad[:4]})"
        elif "azure portal" in al:
            p = "Azure portal" in txt or "Azure" in txt
            e = ("'Azure portal'/'Azure' present" if p else "no Azure recovery")
            if "Asia bottle" in txt:
                p = False
                e = "'Asia bottle' still present"
        elif "particle" in al or "preserved" in al:
            keeps = [w for w in ("lah", "ya") if re.search(r"\b" + w + r"\b", txt)]
            p = len(keeps) > 0
            e = f"particles still present: {keeps}"
        else:
            p, e = False, "NO CHECKER MATCHED"
        out.append({"text": a, "passed": bool(p), "evidence": e})
    return out


# ------------------------------ driver -------------------------------------
def grade_run(eval_dir, cfg):
    meta = json.loads((eval_dir / "eval_metadata.json").read_text())
    name = meta["eval_name"]
    assertions = meta["assertions"]
    run_dir = eval_dir / cfg
    out_path = find_output_srt(run_dir)
    ctx = {"out_path": out_path}
    if out_path is None:
        expectations = [{"text": a, "passed": False, "evidence": "No output SRT produced"} for a in assertions]
        (run_dir / "grading.json").write_text(json.dumps({"expectations": expectations}, indent=2))
        return name, cfg, 0, len(assertions)
    ctx["out_bytes"] = out_path.read_bytes()
    ctx["out"] = parse(out_path)

    if "khewjiapeng" in name:
        ctx["raw"] = parse(FIX / "khewjiapeng-real/khewjiapeng.en.raw.srt")
        expectations = assertion_eval_real(ctx, assertions)
    else:
        slug = "sohjunwei-synth" if "sohjunwei" in name else "kowajialiang-synth"
        ctx["raw"] = parse(FIX / slug / f"{slug}.en.raw.srt")
        key = json.loads((FIX / slug / "answer-key.json").read_text())
        expectations = assertion_eval_synth(ctx, key, assertions)

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
                print(f"{name:38s} {c:14s} {p}/{n}")


if __name__ == "__main__":
    main()
