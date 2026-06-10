#!/usr/bin/env python3
"""Grade subtitle-translate-zh eval outputs against the per-case assertions.

For each config dir (with_skill / without_skill) under runs/iteration-N/eval-*/,
this finds the produced .zh-Hans.srt and .zh-Hant.srt in outputs/, evaluates
every assertion from the case's eval_metadata.json, and writes grading.json
with BOTH shapes the benchmark contract needs (see ../README.md):
  - summary       {pass_rate, passed, failed, total} — read by the aggregator
  - expectations  [{text, passed, evidence}]         — read by the viewer

The source SRT each case ran against is re-derived here (talk excerpt from the
committed talk folder, synthetic from fixtures/) so grading never depends on
the gitignored stage/. All checks are stdlib-only — no OpenCC: script and
Taiwan-vocabulary correctness are checked against curated character/term
lists, since legitimate translations differ and only the traps are graded.

Usage:
  python3 grade.py runs/iteration-1
"""
import json
import re
import sys
from pathlib import Path

import prepare  # sibling module: excerpt() + EXCERPTS

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]  # subtitle-translate-zh -> evals -> agentic -> repo root
TALKS = REPO / "projects/jb-agentic-meetup/talk-recordings"

# eval-name keyword -> talk slug (None = synthetic fixture)
CASES = {
    "khew": "JBAgentic-20260530-meetup-1-KhewJiaPeng-AIMeetsInfrastructure",
    "soh": "JBAgentic-20260530-meetup-1-SohJunWei-AIForEverydayFriction",
    "synthetic": None,
}

# Unambiguous simplified/traditional character pairs — each side occurs only
# in its own script, so presence of the wrong side flags a script error.
SCRIPT_PAIRS = [
    ("个", "個"), ("这", "這"), ("说", "說"), ("时", "時"), ("会", "會"),
    ("为", "為"), ("们", "們"), ("来", "來"), ("对", "對"), ("后", "後"),
    ("应", "應"), ("还", "還"), ("没", "沒"), ("让", "讓"), ("见", "見"),
    ("东", "東"), ("写", "寫"), ("体", "體"), ("点", "點"), ("几", "幾"),
    ("务", "務"), ("发", "發"), ("经", "經"), ("过", "過"), ("开", "開"),
    ("关", "關"), ("实", "實"), ("现", "現"), ("样", "樣"), ("当", "當"),
    ("单", "單"), ("与", "與"), ("问", "問"), ("题", "題"), ("错", "錯"),
    ("长", "長"), ("间", "間"), ("钱", "錢"), ("记", "記"), ("录", "錄"),
    ("数", "數"), ("据", "據"), ("网", "網"), ("视", "視"), ("软", "軟"),
    ("资", "資"), ("库", "庫"),
]
SIMP_MARKERS = "".join(s for s, _ in SCRIPT_PAIRS)
TRAD_MARKERS = "".join(t for _, t in SCRIPT_PAIRS)

# (mainland term in Hans, Taiwan term expected in Hant, naive char-conversion
# that s2twp would have replaced). Checked only when the Hans term occurs.
TW_VOCAB = [
    ("数据库", "資料庫", "數據庫"),
    ("软件", "軟體", "軟件"),
    ("视频", "影片", "視頻"),
    ("网络", "網路", "網絡"),
    ("信息", "資訊", "信息"),
    ("程序", "程式", "程序"),
]

CJK_RE = re.compile(r"[一-鿿]")


# ------------------------------ SRT parsing --------------------------------
def parse(text):
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


def source_text(case_key):
    """Re-derive the staged source SRT content for a case."""
    slug = CASES[case_key]
    if slug is None:
        return (ROOT / "fixtures/synthetic-vocab-traps.en.srt").read_text(encoding="utf-8")
    return prepare.excerpt(TALKS / slug / f"{slug}.en.srt", prepare.EXCERPTS[slug])


def find_outputs(run_dir):
    out = Path(run_dir) / "outputs"
    if not out.exists():  # run-k/ holds grading artifacts; outputs/ sits at config level
        out = Path(run_dir).parent / "outputs"
    hans = sorted(out.rglob("*.zh-Hans.srt")) if out.exists() else []
    hant = sorted(out.rglob("*.zh-Hant.srt")) if out.exists() else []
    return (hans[0] if hans else None), (hant[0] if hant else None)


def bodies(cues):
    return "\n".join(c["body"] for c in cues)


# ------------------------------ checks --------------------------------------
def chk_exist(ctx):
    missing = [tag for tag, p in (("zh-Hans", ctx["hans_path"]), ("zh-Hant", ctx["hant_path"])) if p is None]
    return (not missing), ("both outputs present" if not missing else f"missing: {missing}")


def per_file(ctx, fn):
    """Run fn(cues, tag) over both outputs, AND the results."""
    results = [fn(ctx[tag], tag) for tag in ("hans", "hant")]
    ok = all(r[0] for r in results)
    return ok, "; ".join(r[1] for r in results)


def chk_count(ctx):
    n = len(ctx["src"])
    return per_file(ctx, lambda c, tag: (len(c) == n, f"{tag}: {len(c)}/{n} cues"))


def chk_headers(ctx):
    def one(cues, tag):
        src = ctx["src"]
        if len(cues) != len(src):
            return False, f"{tag}: cue count differs"
        bad = [i for i, (a, b) in enumerate(zip(src, cues), 1)
               if a["idx"] != b["idx"] or a["timing"] != b["timing"]]
        return (not bad), (f"{tag}: all numbers+timestamps preserved" if not bad
                           else f"{tag}: mismatch at cues {bad[:5]}")
    return per_file(ctx, lambda c, tag: one(c, tag))


def chk_bom(ctx):
    def one(tag):
        p = ctx[f"{tag}_path"]
        has = p.read_bytes()[:3] == b"\xef\xbb\xbf"
        return (not has), f"{tag}: {'BOM present' if has else 'no BOM'}"
    results = [one(t) for t in ("hans", "hant")]
    return all(r[0] for r in results), "; ".join(r[1] for r in results)


def chk_empty(ctx):
    return per_file(ctx, lambda c, tag: (
        not [x["idx"] for x in c if not x["body"]],
        f"{tag}: " + ("no empty cues" if not [x for x in c if not x["body"]]
                      else f"empty at {[x['idx'] for x in c if not x['body']][:5]}")))


def chk_cjk(ctx):
    def one(cues, tag):
        if not cues:
            return False, f"{tag}: no cues"
        n = sum(1 for c in cues if CJK_RE.search(c["body"]))
        return n / len(cues) > 0.5, f"{tag}: {n}/{len(cues)} cues contain CJK"
    return per_file(ctx, one)


def script_check(text, forbidden, label):
    found = sorted({ch for ch in forbidden if ch in text})
    return (not found), (f"no {label}-marker chars" if not found
                         else f"{label}-marker chars present: {''.join(found[:8])}")


def chk_hans_script(ctx):
    ok, e = script_check(bodies(ctx["hans"]), TRAD_MARKERS, "traditional")
    return ok, f"hans: {e}"


def chk_hant_script(ctx):
    ok, e = script_check(bodies(ctx["hant"]), SIMP_MARKERS, "simplified")
    return ok, f"hant: {e}"


def chk_tw_vocab(ctx):
    hans, hant = bodies(ctx["hans"]), bodies(ctx["hant"])
    notes, ok = [], True
    for cn, tw, naive in TW_VOCAB:
        if cn not in hans:
            continue
        good = tw in hant and (naive == cn or naive not in hant)
        ok &= good
        notes.append(f"{cn}->{tw} {'OK' if good else 'FAIL (naive ' + naive + ' or missing)'}")
    return ok, ("; ".join(notes) if notes else "no mainland trap terms used in hans (vacuous pass)")


def chk_nouns(ctx, nouns):
    missing = [(n, tag) for n in nouns for tag in ("hans", "hant") if n not in bodies(ctx[tag])]
    return (not missing), ("all preserved: " + ", ".join(nouns) if not missing
                           else f"missing: {missing[:6]}")


def chk_hans_term(ctx, term):
    ok = term in bodies(ctx["hans"])
    return ok, f"'{term}' {'present' if ok else 'MISSING'} in hans"


# ------------------------------ assertion wiring ---------------------------
def quoted(a):
    return re.findall(r"'([^']+)'", a)


def eval_assertions(ctx, assertions):
    out = []
    for a in assertions:
        al = a.lower()
        if ctx["hans"] is None or ctx["hant"] is None:
            ok, e = chk_exist(ctx)
            if not ok and "exist" not in al:
                out.append({"text": a, "passed": False, "evidence": "output file(s) missing"})
                continue
        if "exist" in al:
            p, e = chk_exist(ctx)
        elif "cue count" in al:
            p, e = chk_count(ctx)
        elif "byte-for-byte" in al or "timestamp" in al:
            p, e = chk_headers(ctx)
        elif "bom" in al:
            p, e = chk_bom(ctx)
        elif "empty" in al:
            p, e = chk_empty(ctx)
        elif "cjk" in al or "chinese" in al:
            p, e = chk_cjk(ctx)
        elif "simplified script" in al:
            p, e = chk_hans_script(ctx)
        elif "traditional script" in al:
            p, e = chk_hant_script(ctx)
        elif "taiwan vocabulary" in al:
            p, e = chk_tw_vocab(ctx)
        elif "proper nouns" in al or "restraint" in al:
            p, e = chk_nouns(ctx, quoted(a))
        elif "令吉" in a:
            p, e = chk_hans_term(ctx, "令吉")
        elif "巴仙" in a:
            p, e = chk_hans_term(ctx, "巴仙")
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


def write_grading(run_dir, expectations):
    passed = sum(1 for x in expectations if x["passed"])
    total = len(expectations)
    grading = {
        "expectations": expectations,
        "summary": {
            "pass_rate": round(passed / total, 4) if total else 0.0,
            "passed": passed,
            "failed": total - passed,
            "total": total,
        },
    }
    (run_dir / "grading.json").write_text(json.dumps(grading, indent=2, ensure_ascii=False))
    return passed, total


def grade_run(eval_dir, run_dir):
    meta = json.loads((eval_dir / "eval_metadata.json").read_text())
    name = meta["eval_name"]
    key = case_key(name)
    if key is None:
        raise SystemExit(f"unknown case for eval '{name}' (expected one of {list(CASES)})")
    hans_path, hant_path = find_outputs(run_dir)
    src = parse(source_text(key))
    ctx = {
        "src": src,
        "hans_path": hans_path,
        "hant_path": hant_path,
        "hans": parse(hans_path.read_text(encoding="utf-8", errors="replace")) if hans_path else None,
        "hant": parse(hant_path.read_text(encoding="utf-8", errors="replace")) if hant_path else None,
    }
    expectations = eval_assertions(ctx, meta["assertions"])
    return (name,) + write_grading(run_dir, expectations)


def run_dirs(cfg_dir):
    """grading.json goes next to outputs/: run-k/ subdirs if present, else cfg_dir."""
    runs = sorted(d for d in cfg_dir.glob("run-*") if d.is_dir())
    return runs or [cfg_dir]


def main():
    itr = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "runs/iteration-1"
    itr = itr if itr.is_absolute() else ROOT / itr
    for eval_dir in sorted(itr.glob("eval-*")):
        for cfg in ("with_skill", "without_skill"):
            if not (eval_dir / cfg).exists():
                continue
            for rd in run_dirs(eval_dir / cfg):
                name, p, n = grade_run(eval_dir, rd)
                print(f"{name:24s} {cfg:14s} {rd.name if rd.name.startswith('run-') else '-':8s} {p}/{n}")


if __name__ == "__main__":
    main()
