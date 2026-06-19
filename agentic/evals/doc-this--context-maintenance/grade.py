#!/usr/bin/env python3
"""Deterministic grader for the context-maintenance rule eval. Stdlib only, zero LLM tokens.

Maintenance is a WRITE behavior, so — unlike the discovery grader — this one reads
the MUTATED files back from each run's $TMPDIR clean room (seed.json records the
work_dir) and grades three dimensions the rule is supposed to improve:

  1. correctness — the requested code change actually landed: work_dir/<change_file>
     exists and contains all change_keywords (AND-of-ORs, case-insensitive).
  2. reconcile   — the doc that COVERS the change was kept true (the rule's core
     behavior): work_dir/<doc_file> exists (always, or newly — doc_must_exist),
     contains all doc_required groups, and contains NONE of doc_forbidden (the
     stale fact is gone). This is the headline metric, the analog of the discovery
     grader's "process": it grades the outcome whether the agent hand-edited,
     created the file, or invoked doc-this.
  3. efficiency  — total read/search/edit tool calls <= the case's tool_budget.

It also records raw metrics (which docs were edited/created, read/edit/write counts,
and an optional secondary_doc check) so the iteration write-up can show the
with_rule vs without_rule deltas the aggregator's pass-rate alone can't.

Writes per run a grading.json carrying the benchmark-contract shapes
(expectations[] for the viewer, summary{} for the aggregator) plus
execution_metrics{total_tool_calls}.

Usage:
  python3 grade.py runs/iteration-1
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACTION_TOOLS = {"Read", "Grep", "Glob", "Edit", "Write", "Skill"}
EDIT_TOOLS = {"Edit", "Write"}


def tool_calls(transcript_path: Path):
    """Ordered list of {name, target} for every tool_use in the transcript."""
    calls = []
    if not transcript_path.exists():
        return calls
    for line in transcript_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") != "assistant":
            continue
        for block in ev.get("message", {}).get("content", []) or []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            name = block.get("name", "")
            inp = block.get("input", {}) or {}
            target = inp.get("file_path") or inp.get("path") or inp.get("pattern") or ""
            calls.append({"name": name, "target": str(target)})
    return calls


def has_all_groups(text: str, groups) -> bool:
    low = text.lower()
    return all(any(alt.lower() in low for alt in group) for group in groups)


def missing_groups(text: str, groups):
    low = text.lower()
    return [g for g in groups if not any(alt.lower() in low for alt in g)]


def present_forbidden(text: str, forbidden):
    low = text.lower()
    return [f for f in forbidden if f.lower() in low]


def check_correctness(work: Path, meta):
    cf = work / meta["change_file"]
    if not cf.exists():
        return False, f"change_file {meta['change_file']} does not exist after run"
    text = cf.read_text(encoding="utf-8", errors="replace")
    miss = missing_groups(text, meta["change_keywords"])
    if miss:
        return False, f"change not applied — missing keyword group(s) in {meta['change_file']}: {miss}"
    return True, f"change applied in {meta['change_file']}"


def check_reconcile(work: Path, meta):
    df = work / meta["doc_file"]
    if not df.exists():
        if meta["doc_must_exist"]:
            return False, f"doc {meta['doc_file']} was not created"
        return False, f"doc {meta['doc_file']} missing"
    text = df.read_text(encoding="utf-8", errors="replace")
    miss = missing_groups(text, meta["doc_required"])
    hit = present_forbidden(text, meta.get("doc_forbidden", []))
    if hit:
        return False, f"stale fact still in {meta['doc_file']}: {hit}"
    if miss:
        return False, f"doc not reconciled — missing in {meta['doc_file']}: {miss}"
    return True, f"{meta['doc_file']} reconciled (new fact present, stale gone)"


def check_secondary(work: Path, meta):
    """Optional, recorded as a metric (not pass/fail)."""
    sec = meta.get("secondary_doc")
    if not sec:
        return None
    kind = sec.get("kind")
    if kind == "dir_has_md":
        d = work / sec["path"]
        done = d.is_dir() and any(d.glob("**/*.md"))
        return {"kind": kind, "path": sec["path"], "done": bool(done)}
    if kind == "contains":
        p = work / sec["path"]
        done = p.exists() and sec["value"].lower() in p.read_text(encoding="utf-8", errors="replace").lower()
        return {"kind": kind, "path": sec["path"], "value": sec["value"], "done": bool(done)}
    return {"kind": kind, "done": None}


def compute_metrics(work: Path, meta, calls):
    action = [c for c in calls if c["name"] in ACTION_TOOLS]
    edits = [c for c in action if c["name"] in EDIT_TOOLS]
    doc_file = meta["doc_file"]
    edited_doc = any(c["target"].endswith(doc_file) for c in edits)
    edited_other_md = sorted({
        c["target"] for c in edits
        if c["target"].lower().endswith(".md") and not c["target"].endswith(doc_file)
    })
    return {
        "reads": sum(1 for c in action if c["name"] == "Read"),
        "edits": len(edits),
        "skills": sum(1 for c in action if c["name"] == "Skill"),
        "total_action_tools": len(action),
        "edited_covering_doc": edited_doc,
        "other_docs_touched": edited_other_md,
        "secondary_doc": check_secondary(work, meta),
        "all_calls": [f"{c['name']}:{c['target']}" for c in action],
    }


def grade_run(meta, run_dir: Path):
    seed = json.loads((run_dir / "seed.json").read_text(encoding="utf-8"))
    work = Path(seed["work_dir"])
    calls = tool_calls(run_dir / "transcript.jsonl")
    metrics = compute_metrics(work, meta, calls)

    if not work.is_dir():
        c_ok, c_ev = False, f"work dir missing ({work}) — re-run prepare.py/run.py"
        r_ok, r_ev = False, "work dir missing"
    else:
        c_ok, c_ev = check_correctness(work, meta)
        r_ok, r_ev = check_reconcile(work, meta)

    budget = meta["tool_budget"]
    e_ok = metrics["total_action_tools"] <= budget
    e_ev = f"{metrics['total_action_tools']} action tool calls (budget {budget})"

    expectations = [
        {"text": "Change applied to code", "passed": c_ok, "evidence": c_ev},
        {"text": "Covering doc reconciled", "passed": r_ok, "evidence": r_ev},
        {"text": f"Within tool budget ({budget})", "passed": e_ok, "evidence": e_ev},
    ]
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
        "execution_metrics": {"total_tool_calls": metrics["total_action_tools"], "errors_encountered": 0},
        "metrics": metrics,
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
        for config_dir in sorted(p for p in eval_dir.iterdir() if p.is_dir()):
            for run_dir in sorted(config_dir.glob("run-*")):
                if not (run_dir / "seed.json").exists():
                    continue
                g = grade_run(meta, run_dir)
                s, m = g["summary"], g["metrics"]
                graded += 1
                sec = m["secondary_doc"]
                sec_s = f" sec={sec['done']}" if sec else ""
                print(
                    f"{meta['eval_name']} / {config_dir.name} / {run_dir.name}: "
                    f"{s['passed']}/{s['total']}  "
                    f"[reads={m['reads']} edits={m['edits']} skill={m['skills']} "
                    f"edited_doc={m['edited_covering_doc']}{sec_s}]"
                )
                for e in g["expectations"]:
                    print(f"    [{'PASS' if e['passed'] else 'FAIL'}] {e['text']} — {e['evidence']}")
    if not graded:
        sys.exit("graded 0 runs — wrong iteration dir or run.py not run?")
    print(f"\ngraded {graded} runs")


if __name__ == "__main__":
    main()
