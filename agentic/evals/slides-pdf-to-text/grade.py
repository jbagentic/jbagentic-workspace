#!/usr/bin/env python3
"""Deterministic grader for the slides-pdf-to-text evals. Stdlib only, zero LLM tokens.

Grades each run IN PLACE against its staged work/ folder (executors write
work/slides.txt; they don't copy outputs). The grader is branch-agnostic: it
checks the OUTPUT CONTRACT the skill promises regardless of whether the text
came from the cheap stdlib extractor (textlayer-kowa) or the vision fallback
(vision-khew):

  - slides.txt exists beside the staged slides.pdf
  - one `## slide-NN` section per slide, count == staged PNG count, zero-padded,
    1-based and contiguous; no empty sections
  - UTF-8 without a BOM
  - per-term verbatim, CASE-SENSITIVE presence (exact casing is the skill's whole
    promise, so 'Vue JS' must not arrive as 'VueJS')
  - source slides.pdf and every slides/ PNG byte-identical to the staged seed

Walks <iteration-dir>/eval-*/<config>/run-*/ and writes per run a grading.json
carrying BOTH shapes the benchmark contract requires (see agentic/evals/README.md):
  expectations[] {text, passed, evidence}   — for the viewer
  summary {pass_rate, passed, failed, total} — for the aggregator

Usage:
  python3 grade.py runs/iteration-1
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SECTION_RE = re.compile(r"^##\s+slide-(\d+)\s*$", re.M)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quoted(text):
    """The single-quoted term inside an assertion, e.g. 'Vue JS'."""
    m = re.search(r"'([^']+)'", text)
    return m.group(1) if m else None


def parse_sections(text):
    """[(header_str, number_int, body_str), ...] in document order."""
    out = []
    matches = list(SECTION_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append((m.group(0).strip(), int(m.group(1)), text[start:end]))
    return out


class Run:
    def __init__(self, case, run_dir):
        self.case = case
        self.run_dir = run_dir
        self.work = run_dir / "work"
        self.seed = json.loads((run_dir / "seed.json").read_text(encoding="utf-8"))
        self.pages = sum(1 for f in self.seed["files"] if f.startswith("slides/slide-"))
        self.txt_path = self.work / "slides.txt"
        self.raw = self.txt_path.read_bytes() if self.txt_path.exists() else None
        self.text = self.raw.decode("utf-8", "replace") if self.raw is not None else None
        self.sections = parse_sections(self.text) if self.text is not None else []


# --- checkers: each returns (passed, evidence) ---------------------------

def check_exists(run):
    ok = run.txt_path.exists()
    return ok, "slides.txt present beside slides.pdf" if ok else "slides.txt missing in work/"


def check_section_count(run):
    if run.text is None:
        return False, "no slides.txt to parse"
    n = len(run.sections)
    ok = n == run.pages
    return ok, f"{n} ## slide-NN sections vs {run.pages} staged PNGs"


def check_contiguous(run):
    if not run.sections:
        return False, "no sections to check"
    headers = [h for h, _, _ in run.sections]
    expected = [f"## slide-{i:02d}" for i in range(1, run.pages + 1)]
    ok = headers == expected
    return ok, "headers zero-padded 1-based contiguous" if ok else f"got {headers}, expected {expected}"


def check_no_empty(run):
    if not run.sections:
        return False, "no sections to check"
    empty = [h for h, _, body in run.sections if not body.strip()]
    return not empty, "all sections non-empty" if not empty else f"empty sections: {empty}"


def check_utf8_no_bom(run):
    if run.raw is None:
        return False, "no slides.txt"
    if run.raw.startswith(b"\xef\xbb\xbf"):
        return False, "file begins with a UTF-8 BOM"
    try:
        run.raw.decode("utf-8")
    except UnicodeDecodeError as e:
        return False, f"not valid UTF-8: {e}"
    return True, "UTF-8, no BOM"


def check_term(run, term):
    if run.text is None:
        return False, "no slides.txt"
    ok = term in run.text  # case-sensitive substring
    return ok, f"'{term}' present verbatim" if ok else f"'{term}' not found with exact casing"


def check_pdf_untouched(run):
    p = run.work / "slides.pdf"
    seed_sha = run.seed["files"].get("slides.pdf")
    if not p.exists():
        return False, "slides.pdf was deleted"
    ok = sha256(p) == seed_sha
    return ok, "slides.pdf byte-identical to staged" if ok else "slides.pdf was modified"


def check_pngs_untouched(run):
    bad = []
    for rel, seed_sha in run.seed["files"].items():
        if not rel.startswith("slides/slide-"):
            continue
        p = run.work / rel
        if not p.exists():
            bad.append(f"{rel} missing")
        elif sha256(p) != seed_sha:
            bad.append(f"{rel} modified")
    return not bad, "all slide PNGs untouched" if not bad else "; ".join(bad)


# Keyword dispatch: first matching pattern wins.
CHECKERS = [
    (r"exists beside the source slides\.pdf", check_exists),
    (r"## slide-NN sections, one per slide", check_section_count),
    (r"zero-padded, 1-based, contiguous", check_contiguous),
    (r"No empty sections", check_no_empty),
    (r"UTF-8 without a BOM", check_utf8_no_bom),
    (r"preserved verbatim", check_term),  # term pulled from the quoted span
    (r"slides\.pdf is byte-identical", check_pdf_untouched),
    (r"slide PNGs under slides/ are untouched", check_pngs_untouched),
]


def grade_run(case, assertions, run_dir):
    run = Run(case, run_dir)
    expectations = []
    for text in assertions:
        for pattern, checker in CHECKERS:
            if re.search(pattern, text):
                if checker is check_term:
                    term = quoted(text)
                    passed, evidence = (
                        check_term(run, term) if term else (False, "no quoted term in assertion")
                    )
                else:
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
    (run_dir / "grading.json").write_text(
        json.dumps(grading, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
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
