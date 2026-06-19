#!/usr/bin/env python3
"""Deterministic grader for the context-maintenance rule eval. Stdlib only, zero LLM tokens.

Maintenance is a WRITE behavior, so — unlike the discovery grader — this one reads
the MUTATED files back from each run's $TMPDIR clean room (seed.json records the
work_dir) and grades three dimensions the rule is supposed to improve:

  1. dimension 1 depends on the case mode:
       change (default) — the requested code change actually landed:
         work_dir/<change_file> exists and contains all change_keywords.
       author           — the rule's OTHER trigger ("writing or organizing docs ->
         run doc-this"): the agent routed the doc work through doc-this (a Skill
         tool_use for doc-this). This is the one place we grade the MEANS, not just
         the outcome.
  2. reconcile   — every doc that COVERS the change was kept true (the rule's core
     behavior): the primary doc_file plus any also_reconcile entry each exists
     (always, or newly — doc_must_exist/must_exist), contains all required groups,
     and contains NONE of forbidden (the stale fact is gone). Outcome-based: grades
     the same whether the agent hand-edited, created the file, or invoked doc-this.
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
            target = inp.get("file_path") or inp.get("path") or inp.get("pattern") or inp.get("skill") or ""
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


def check_one_doc(work: Path, rel: str, must_exist: bool, required, forbidden):
    """Reconcile a single covering doc: exists (if required), has required, lacks forbidden."""
    p = work / rel
    if not p.exists():
        return False, (f"{rel} was not created" if must_exist else f"{rel} missing")
    text = p.read_text(encoding="utf-8", errors="replace")
    hit = present_forbidden(text, forbidden)
    if hit:
        return False, f"stale fact still in {rel}: {hit}"
    miss = missing_groups(text, required)
    if miss:
        return False, f"{rel} not reconciled — missing: {miss}"
    return True, f"{rel} reconciled"


def check_reconcile(work: Path, meta):
    """Every covering doc — the primary doc_file plus any also_reconcile — must reconcile."""
    targets = [(meta["doc_file"], meta["doc_must_exist"], meta["doc_required"], meta.get("doc_forbidden", []))]
    for extra in meta.get("also_reconcile", []) or []:
        targets.append((extra["file"], extra.get("must_exist", True),
                        extra.get("required", []), extra.get("forbidden", [])))
    evidence = []
    all_ok = True
    for rel, must, req, forb in targets:
        ok, ev = check_one_doc(work, rel, must, req, forb)
        all_ok = all_ok and ok
        evidence.append(ev)
    return all_ok, "; ".join(evidence)


def doc_this_invoked(calls) -> bool:
    """True iff the transcript shows a Skill tool_use routing to the doc-this skill."""
    return any(c["name"] == "Skill" and "doc-this" in c["target"].lower() for c in calls)


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

    mode = meta.get("mode", "change")
    if mode == "author":
        # Dimension 1 = the MEANS directive: route doc work through doc-this.
        d1_text = "Routed doc work to doc-this"
        d1_ok = doc_this_invoked(calls)
        d1_ev = "invoked the doc-this skill" if d1_ok else "did not invoke doc-this (hand-wrote / other)"
    else:
        d1_text = "Change applied to code"
        d1_ok, d1_ev = (False, f"work dir missing ({work}) — re-run prepare.py/run.py") \
            if not work.is_dir() else check_correctness(work, meta)

    if not work.is_dir():
        r_ok, r_ev = False, "work dir missing"
    else:
        r_ok, r_ev = check_reconcile(work, meta)

    budget = meta["tool_budget"]
    e_ok = metrics["total_action_tools"] <= budget
    e_ev = f"{metrics['total_action_tools']} action tool calls (budget {budget})"

    expectations = [
        {"text": d1_text, "passed": d1_ok, "evidence": d1_ev},
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
