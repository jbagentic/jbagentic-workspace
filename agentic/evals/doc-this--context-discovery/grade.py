#!/usr/bin/env python3
"""Deterministic grader for the context-discovery rule eval. Stdlib only, zero LLM tokens.

Reads each run's captured transcript (run.py wrote transcript.jsonl + answer.txt)
and grades three dimensions the rule is supposed to improve:

  1. correctness — the final answer contains the case's answer_keywords
     (AND-of-ORs, case-insensitive) and none of its answer_forbidden phrases.
  2. process     — HOW context was gathered. This measures the PRINCIPLE, not
                   the method: *how* the agent locates a README doesn't matter.
       readme_first  -> a README was read before any code/content access (a
                        non-README Read or a content Grep). Globs only *locate*
                        files (navigation), so they never count against this —
                        globbing **/README.md or **/foo/** to find the entry
                        point is fine, as long as a README is read first.
       fallback_file -> the target file was read directly (correct when the
                        folder has no README — graceful fallback, not paralysis)
  3. efficiency  — total read/search tool calls <= the case's tool_budget.

It also records raw metrics (reads/greps/globs, content accesses before the
first README, readme-first flag, total tool calls) so the iteration write-up can
show the with_rule vs without_rule deltas the aggregator's pass-rate alone can't.

Writes per run a grading.json carrying the benchmark-contract shapes
(expectations[] for the viewer, summary{} for the aggregator) plus
execution_metrics{total_tool_calls} (the aggregator surfaces it as tool_calls).
Timing is intentionally left to the sibling timing.json run.py wrote.

Usage:
  python3 grade.py runs/iteration-1
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTEXT_TOOLS = {"Read", "Grep", "Glob"}


def tool_calls(transcript_path: Path):
    """Ordered list of {name, target} for every context tool_use in the transcript."""
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


def is_readme(target: str) -> bool:
    return target.lower().rstrip("/").endswith("readme.md")


def is_content_access(call) -> bool:
    """Accessing file *contents* without first consulting a README.

    The principle is "use a README as the entry point before diving into code" —
    so what counts is content access, not how the README was located:
      - Grep reads file contents -> content access.
      - Read of a non-README file -> content access.
      - Read of a README -> that IS consulting the map (handled by the caller).
      - Glob only *locates* files (navigation); globbing **/README.md or
        **/foo/** to find the entry point is fine -> never content access.
    """
    if call["name"] == "Grep":
        return True
    if call["name"] == "Read":
        return not is_readme(call["target"])
    return False  # Glob is navigation, not content access


def compute_metrics(calls):
    ctx = [c for c in calls if c["name"] in CONTEXT_TOOLS]
    reads = [c for c in ctx if c["name"] == "Read"]
    greps = [c for c in ctx if c["name"] == "Grep"]
    globs = [c for c in ctx if c["name"] == "Glob"]

    # first README read position among context calls
    first_readme_idx = next(
        (i for i, c in enumerate(ctx) if c["name"] == "Read" and is_readme(c["target"])),
        None,
    )
    before = ctx[:first_readme_idx] if first_readme_idx is not None else ctx
    content_before = sum(1 for c in before if is_content_access(c))
    # README-first = a README was read before any code/content access. Globs that
    # merely locate the README (or a folder) beforehand are navigation, not a
    # violation — only a content Grep or a non-README Read ahead of it counts.
    readme_first = first_readme_idx is not None and content_before == 0

    return {
        "reads": len(reads),
        "greps": len(greps),
        "globs": len(globs),
        "total_context_tools": len(ctx),
        "readme_first": readme_first,
        "content_access_before_readme": content_before,
        "read_paths": [c["target"] for c in reads],
        "all_calls": [f"{c['name']}:{c['target']}" for c in ctx],
    }


def check_correctness(answer: str, keyword_groups, forbidden):
    low = answer.lower()
    missing = [g for g in keyword_groups if not any(alt.lower() in low for alt in g)]
    hit_forbidden = [f for f in forbidden if f.lower() in low]
    if not answer.strip():
        return False, "empty answer"
    if hit_forbidden:
        return False, f"forbidden phrase present: {hit_forbidden}"
    if missing:
        return False, f"missing required keyword group(s): {missing}"
    return True, "answer contains all required keyword groups; no forbidden phrases"


def check_process(meta, metrics):
    process = meta["process"]
    if process == "readme_first":
        ok = metrics["readme_first"]
        ev = (
            "a README was read before any code/content access (globs to locate it are fine)"
            if ok
            else f"code/content was accessed before any README read; content accesses before "
            f"README: {metrics['content_access_before_readme']}; calls: {metrics['all_calls'][:4]}"
        )
        return ok, ev
    if process == "fallback_file":
        target = meta["target_file"]
        ok = any(c.endswith(target) for c in metrics["read_paths"])
        ev = (
            f"read target file {target} directly (no README to lean on)"
            if ok
            else f"did not read {target}; reads: {metrics['read_paths']}"
        )
        return ok, ev
    return False, f"unknown process '{process}'"


def grade_run(meta, run_dir: Path):
    answer = (run_dir / "answer.txt").read_text(encoding="utf-8") if (run_dir / "answer.txt").exists() else ""
    metrics = compute_metrics(tool_calls(run_dir / "transcript.jsonl"))

    c_ok, c_ev = check_correctness(answer, meta["answer_keywords"], meta.get("answer_forbidden", []))
    p_ok, p_ev = check_process(meta, metrics)
    budget = meta["tool_budget"]
    e_ok = metrics["total_context_tools"] <= budget
    e_ev = f"{metrics['total_context_tools']} read/search calls (budget {budget})"

    expectations = [
        {"text": "Reaches the correct answer", "passed": c_ok, "evidence": c_ev},
        {"text": f"Discovery process: {meta['process']}", "passed": p_ok, "evidence": p_ev},
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
        "execution_metrics": {"total_tool_calls": metrics["total_context_tools"], "errors_encountered": 0},
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
                print(
                    f"{meta['eval_name']} / {config_dir.name} / {run_dir.name}: "
                    f"{s['passed']}/{s['total']}  "
                    f"[reads={m['reads']} grep={m['greps']} glob={m['globs']} "
                    f"readme_first={m['readme_first']} content_before={m['content_access_before_readme']}]"
                )
                for e in g["expectations"]:
                    print(f"    [{'PASS' if e['passed'] else 'FAIL'}] {e['text']} — {e['evidence']}")
    if not graded:
        sys.exit("graded 0 runs — wrong iteration dir or run.py not run?")
    print(f"\ngraded {graded} runs")


if __name__ == "__main__":
    main()
