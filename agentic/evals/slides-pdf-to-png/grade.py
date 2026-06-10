#!/usr/bin/env python3
"""Deterministic grader for the slides-pdf-to-png evals. Stdlib only, zero LLM tokens.

Grades each run IN PLACE against its staged work/ folder (executors don't copy
outputs). PDF facts (page counts, geometry, checksums) come from
fixtures/manifest.json — written by make_fixtures.py — so no PDF is ever parsed
here; PNG dimensions are read straight from the IHDR chunk, no Pillow.

Walks <iteration-dir>/eval-*/<config>/run-*/ and writes per run a grading.json
carrying BOTH shapes the benchmark contract requires (see agentic/evals/README.md):
  expectations[] {text, passed, evidence}   — for the viewer
  summary {pass_rate, passed, failed, total} — for the aggregator

The multi-pdf-asks response assertions read <run-dir>/outputs/final-response.md;
if the harness didn't save it, those assertions fail with self-explaining
evidence rather than silently.

Usage:
  python3 grade.py runs/iteration-1
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / "fixtures/manifest.json").read_text(encoding="utf-8"))

# case -> {staged pdf name in work/: fixture name in manifest}
CASE_PDFS = {
    "happy-path-16x9": {"slides.pdf": "deck-3p-16x9.pdf"},
    "rerun-clears-stale": {"slides.pdf": "deck-3p-4x3.pdf"},
    "multi-pdf-asks": {
        "slides-talk.pdf": "deck-3p-16x9.pdf",
        "slides-workshop.pdf": "deck-2p-a4.pdf",
    },
}
WIDTH_TOLERANCE_PX = 1  # renderers round 1080*w/h either way


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(path):
    """(width, height) from the IHDR chunk, or None if not a valid PNG."""
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def frames(work):
    return sorted((work / "slides").glob("slide-*.png")) if (work / "slides").is_dir() else []


def deck(case):
    """Manifest entry of the case's primary deck (the one meant to be rendered)."""
    return MANIFEST[CASE_PDFS[case]["slides.pdf"]]


class Run:
    def __init__(self, case, run_dir):
        self.case = case
        self.run_dir = run_dir
        self.work = run_dir / "work"
        self.seed = json.loads((run_dir / "seed.json").read_text(encoding="utf-8"))
        resp = run_dir / "outputs" / "final-response.md"
        self.response = resp.read_text(encoding="utf-8") if resp.exists() else None


# --- checkers ------------------------------------------------------------
# Each returns (passed, evidence).

def check_slides_folder(run):
    ok = (run.work / "slides").is_dir()
    return ok, "slides/ exists" if ok else "slides/ folder missing"


def check_frame_count(run):
    expected = deck(run.case)["pages"]
    names = [f.name for f in frames(run.work)]
    ok = len(names) == expected
    return ok, f"expected {expected} frames, found {len(names)}: {names}"


def check_contiguous_names(run):
    expected = [f"slide-{i:02d}.png" for i in range(1, deck(run.case)["pages"] + 1)]
    names = [f.name for f in frames(run.work)]
    ok = names == expected
    return ok, f"names {names}" + ("" if ok else f", expected {expected}")


def check_valid_png(run):
    fs = frames(run.work)
    if not fs:
        return False, "no frames to check"
    bad = [f.name for f in fs if png_size(f) is None]
    return not bad, "all frames parse as PNG" if not bad else f"invalid PNG: {bad}"


def check_height(run):
    fs = frames(run.work)
    if not fs:
        return False, "no frames to check"
    sizes = {f.name: png_size(f) for f in fs}
    bad = {n: s for n, s in sizes.items() if s is None or s[1] != 1080}
    return not bad, "all frames 1080 px high" if not bad else f"wrong height: {bad}"


def check_width(run):
    expected = deck(run.case)["expected_frame_width_at_1080"]
    fs = frames(run.work)
    if not fs:
        return False, "no frames to check"
    sizes = {f.name: png_size(f) for f in fs}
    bad = {
        n: s
        for n, s in sizes.items()
        if s is None or abs(s[0] - expected) > WIDTH_TOLERANCE_PX
    }
    return (
        not bad,
        f"all frames {expected}±{WIDTH_TOLERANCE_PX} px wide"
        if not bad
        else f"expected width {expected}±{WIDTH_TOLERANCE_PX}, got {bad}",
    )


def check_pdfs_untouched(run):
    bad = []
    for staged, fixture in CASE_PDFS[run.case].items():
        p = run.work / staged
        if not p.exists():
            bad.append(f"{staged} missing")
        elif sha256(p) != MANIFEST[fixture]["sha256"]:
            bad.append(f"{staged} modified")
    return not bad, "source PDF(s) byte-identical to fixtures" if not bad else "; ".join(bad)


def check_frame_size(run):
    fs = frames(run.work)
    if not fs:
        return False, "no frames to check"
    bad = {f.name: f.stat().st_size for f in fs if f.stat().st_size < 1024}
    return not bad, "all frames >= 1 KB" if not bad else f"stub-sized frames: {bad}"


def check_fresh_not_stale(run):
    fs = frames(run.work)
    if not fs:
        return False, "no frames to check"
    stale_shas = {
        sha for name, sha in run.seed["files"].items()
        if re.fullmatch(r"slides/slide-\d+\.png", name)
    }
    stale = [f.name for f in fs if sha256(f) in stale_shas]
    return not stale, "no frame matches a stale seed" if not stale else f"still the stale seeds: {stale}"


def check_notes_untouched(run):
    p = run.work / "slides/notes.txt"
    seed_sha = run.seed["files"].get("slides/notes.txt")
    if not p.exists():
        return False, "slides/notes.txt was deleted"
    ok = sha256(p) == seed_sha
    return ok, "notes.txt present and unchanged" if ok else "notes.txt was modified"


def check_no_pngs(run):
    found = [str(p.relative_to(run.work)) for p in run.work.rglob("slide-*.png")]
    return not found, "no slide-*.png anywhere" if not found else f"frames were rendered: {found}"


def check_no_new_files(run):
    now = {str(p.relative_to(run.work)) for p in run.work.rglob("*") if p.is_file()}
    extra = sorted(now - set(run.seed["files"]))
    return not extra, "work folder matches staged inventory" if not extra else f"new files: {extra}"


def check_valid_png_and_size(run):
    ok1, ev1 = check_valid_png(run)
    ok2, ev2 = check_frame_size(run)
    return ok1 and ok2, f"{ev1}; {ev2}"


def _need_response(run):
    if run.response is None:
        return False, "outputs/final-response.md missing — harness must save the executor's final reply"
    return True, None


def check_asks_question(run):
    ok, evidence = _need_response(run)
    if not ok:
        return False, evidence
    asked = "?" in run.response
    return asked, "response contains a question" if asked else "response contains no '?'"


def check_names_both_pdfs(run):
    ok, evidence = _need_response(run)
    if not ok:
        return False, evidence
    text = run.response.lower()
    missing = [stem for stem in ("slides-talk", "slides-workshop") if stem not in text]
    return not missing, "response names both PDFs" if not missing else f"response does not mention: {missing}"


# Keyword dispatch: first matching pattern wins.
CHECKERS = [
    (r"slides/ folder exists", check_slides_folder),
    (r"No slide-\*\.png was created", check_no_pngs),
    (r"No new files", check_no_new_files),
    (r"Exactly \d+ slide-\*\.png frames", check_frame_count),
    (r"zero-padded, 1-based, contiguous", check_contiguous_names),
    (r"fresh renders, not the stale", check_fresh_not_stale),
    (r"valid PNG of non-trivial size", check_valid_png_and_size),
    (r"valid PNG", check_valid_png),
    (r"height is exactly 1080", check_height),
    (r"width is \d+ px", check_width),
    (r"notes\.txt is untouched", check_notes_untouched),
    (r"byte-identical to (the|their) fixture", check_pdfs_untouched),
    (r"non-trivial in size|non-trivial size", check_frame_size),
    (r"asks the user a question", check_asks_question),
    (r"names both candidate PDFs", check_names_both_pdfs),
]


def grade_run(case, assertions, run_dir):
    run = Run(case, run_dir)
    expectations = []
    for text in assertions:
        for pattern, checker in CHECKERS:
            if re.search(pattern, text):
                passed, evidence = checker(run)
                break
        else:
            passed, evidence = False, "NO CHECKER MATCHED — fix grade.py dispatch"
        expectations.append({"text": text, "passed": passed, "evidence": evidence})

    passed = sum(1 for e in expectations if e["passed"])
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
    (run_dir / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")
    return grading


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    iteration = Path(sys.argv[1])
    if not iteration.is_absolute():
        iteration = HERE / iteration
    if not iteration.is_dir():
        sys.exit(f"no such iteration dir: {iteration}")

    graded = 0
    for eval_dir in sorted(iteration.glob("eval-*")):
        meta = json.loads((eval_dir / "eval_metadata.json").read_text(encoding="utf-8"))
        case, assertions = meta["eval_name"], meta["assertions"]
        for config_dir in sorted(p for p in eval_dir.iterdir() if p.is_dir()):
            run_dirs = sorted(config_dir.glob("run-*")) or [config_dir]
            for run_dir in run_dirs:
                if not (run_dir / "seed.json").exists():
                    print(f"SKIP {run_dir} (no seed.json — not a staged run)")
                    continue
                g = grade_run(case, assertions, run_dir)
                s = g["summary"]
                graded += 1
                print(f"{case} / {config_dir.name} / {run_dir.name}: {s['passed']}/{s['total']}")
                for e in g["expectations"]:
                    mark = "PASS" if e["passed"] else "FAIL"
                    print(f"  [{mark}] {e['text']}\n         {e['evidence']}")
    if not graded:
        sys.exit("graded 0 runs — wrong iteration dir or prepare.py not run?")
    print(f"\ngraded {graded} runs")


if __name__ == "__main__":
    main()
