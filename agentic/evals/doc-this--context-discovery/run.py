#!/usr/bin/env python3
"""Run the context-discovery eval executors headlessly and capture transcripts.

For every staged run dir (prepare.py wrote a seed.json into each), launch one
`claude -p` process with cwd = the run's $TMPDIR clean room, restricted to
READ-ONLY tools (Read, Grep, Glob — no Bash/Edit/Write), and capture the full
stream-json transcript. The transcript is the eval's raw material: it records the
exact tool-call sequence (what the agent read, in what order, and whether it
grepped before reading a README) plus token/duration usage.

Per run it writes, into the repo run dir:
  - transcript.jsonl   — raw stream-json, one event per line (grade.py parses this)
  - answer.txt         — the final answer text, for quick eyeballing
  - timing.json        — {total_tokens, total_duration_seconds} per the benchmark contract

Read-only by construction: only Read/Grep/Glob are whitelisted, so an executor
cannot mutate the staged corpus even if it tried.

Usage:
  python3 run.py runs/iteration-1 [--jobs 4] [--timeout 240] [--model <id>]
"""
import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALLOWED_TOOLS = "Read,Grep,Glob"


def parse_stream(stdout: str):
    """Return (final_answer, total_tokens, duration_s) from a stream-json dump."""
    answer, tokens, duration_s = "", 0, 0.0
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            answer = ev.get("result", "") or ""
            usage = ev.get("usage", {}) or {}
            tokens = sum(
                int(usage.get(k, 0) or 0)
                for k in (
                    "input_tokens",
                    "output_tokens",
                    "cache_creation_input_tokens",
                    "cache_read_input_tokens",
                )
            )
            duration_s = round(int(ev.get("duration_ms", 0) or 0) / 1000, 1)
    return answer, tokens, duration_s


def run_one(run_dir: Path, timeout: int, model: str | None):
    seed = json.loads((run_dir / "seed.json").read_text(encoding="utf-8"))
    work = Path(seed["work_dir"])
    if not work.is_dir():
        return run_dir, False, f"work dir missing ({work}) — re-run prepare.py"

    cmd = [
        "claude", "-p", seed["question"],
        "--output-format", "stream-json",
        "--verbose",
        "--allowedTools", ALLOWED_TOOLS,
        "--max-turns", "30",
    ]
    if model:
        cmd += ["--model", model]

    try:
        proc = subprocess.run(
            cmd, cwd=str(work), capture_output=True, text=True, timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return run_dir, False, f"timed out after {timeout}s"

    (run_dir / "transcript.jsonl").write_text(proc.stdout, encoding="utf-8")
    if proc.returncode != 0:
        (run_dir / "stderr.txt").write_text(proc.stderr, encoding="utf-8")

    answer, tokens, duration_s = parse_stream(proc.stdout)
    (run_dir / "answer.txt").write_text(answer + "\n", encoding="utf-8")
    (run_dir / "timing.json").write_text(
        json.dumps({"total_tokens": tokens, "total_duration_seconds": duration_s}) + "\n",
        encoding="utf-8",
    )
    ok = bool(answer) and proc.returncode == 0
    detail = f"{tokens} tok, {duration_s}s" if ok else f"rc={proc.returncode}, empty/err answer"
    return run_dir, ok, detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iteration_dir", help="e.g. runs/iteration-1 (relative to this eval folder, or absolute)")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--model", default=None, help="optional model id override")
    args = ap.parse_args()

    iteration = Path(args.iteration_dir)
    if not iteration.is_absolute():
        iteration = HERE / iteration
    if not iteration.is_dir():
        sys.exit(f"no such iteration dir: {iteration} — run prepare.py first")

    run_dirs = sorted(p.parent for p in iteration.glob("eval-*/*/run-*/seed.json"))
    if not run_dirs:
        sys.exit(f"no staged runs under {iteration} — run prepare.py first")

    print(f"running {len(run_dirs)} executors (jobs={args.jobs}, timeout={args.timeout}s)\n")
    failures = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(run_one, rd, args.timeout, args.model): rd for rd in run_dirs}
        for fut in as_completed(futs):
            run_dir, ok, detail = fut.result()
            rel = run_dir.relative_to(iteration)
            mark = "ok " if ok else "ERR"
            if not ok:
                failures += 1
            print(f"[{mark}] {rel}  ({detail})")

    print(f"\ndone — {len(run_dirs) - failures}/{len(run_dirs)} ok")
    if failures:
        print("some runs failed; inspect stderr.txt / transcript.jsonl in those run dirs")
    print(f"next: python3 {HERE.name}/grade.py {args.iteration_dir}")


if __name__ == "__main__":
    main()
