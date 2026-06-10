#!/usr/bin/env python3
"""Stage per-run work folders for the slides-pdf-to-png evals.

Unlike subtitle-polish's shared stage/, this stages ONE work dir per
(case x config x run) so concurrent runs never collide — the fixtures are
KB-sized, so copying is free. Everything lands inside the gitignored runs/.

Layout created under <iteration-dir>:
  eval-<name>/
  |- eval_metadata.json          # {eval_id, eval_name, prompt, assertions} per config/run via resolved_prompts
  |- <config>/run-<k>/
     |- work/                    # the executor's task folder (PDFs [+ seeded slides/])
     |- seed.json                # staged-file inventory + sha256s, read by grade.py

Prompts in evals.json carry a {WORK_DIR} placeholder; it is resolved to each
run's absolute work path and printed in the run plan below, so the harness can
paste executor prompts without composing anything.

Idempotent: re-running wipes and re-stages each run dir's work/ and seed.json.

Usage:
  python3 prepare.py runs/iteration-1 [--configs with_skill,without_skill] [--runs 1]
"""
import argparse
import hashlib
import json
import shutil
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"

STALE_FRAMES = 5  # > pages of the 3-page deck, so leftovers are detectable
NOTES_TEXT = "speaker notes - not a slide frame, must be left untouched\n"


def tiny_png():
    """A constant 10x10 gray PNG, built with stdlib only (deterministic bytes)."""
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))

    ihdr = struct.pack(">IIBBBBB", 10, 10, 8, 0, 0, 0, 0)  # 8-bit grayscale
    raw = b"".join(b"\x00" + b"\x80" * 10 for _ in range(10))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_case(case, run_dir):
    work = run_dir / "work"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    work.mkdir(parents=True)

    name = case["name"]
    if name == "happy-path-16x9":
        shutil.copy2(FIXTURES / "deck-3p-16x9.pdf", work / "slides.pdf")
    elif name == "rerun-clears-stale":
        shutil.copy2(FIXTURES / "deck-3p-4x3.pdf", work / "slides.pdf")
        slides = work / "slides"
        slides.mkdir()
        png = tiny_png()
        for i in range(1, STALE_FRAMES + 1):
            (slides / f"slide-{i:02d}.png").write_bytes(png)
        (slides / "notes.txt").write_text(NOTES_TEXT, encoding="utf-8")
    elif name == "multi-pdf-asks":
        shutil.copy2(FIXTURES / "deck-3p-16x9.pdf", work / "slides-talk.pdf")
        shutil.copy2(FIXTURES / "deck-2p-a4.pdf", work / "slides-workshop.pdf")
    else:
        raise SystemExit(f"no staging recipe for case {name!r}")

    seed = {
        "case": name,
        "files": {
            str(p.relative_to(work)): sha256(p)
            for p in sorted(work.rglob("*"))
            if p.is_file()
        },
    }
    (run_dir / "seed.json").write_text(json.dumps(seed, indent=2) + "\n")
    return work


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iteration_dir", help="e.g. runs/iteration-1 (relative to this eval folder, or absolute)")
    ap.add_argument("--configs", default="with_skill,without_skill")
    ap.add_argument("--runs", type=int, default=1)
    args = ap.parse_args()

    iteration = Path(args.iteration_dir)
    if not iteration.is_absolute():
        iteration = HERE / iteration
    configs = [c.strip() for c in args.configs.split(",") if c.strip()]

    spec = json.loads((HERE / "evals.json").read_text(encoding="utf-8"))
    plan = []
    for case in spec["evals"]:
        eval_dir = iteration / f"eval-{case['name']}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        resolved = {}
        for config in configs:
            for k in range(1, args.runs + 1):
                run_dir = eval_dir / config / f"run-{k}"
                work = stage_case(case, run_dir)
                prompt = case["prompt"].replace("{WORK_DIR}", str(work))
                resolved[f"{config}/run-{k}"] = prompt
                plan.append((case["name"], config, k, work, prompt))
        (eval_dir / "eval_metadata.json").write_text(
            json.dumps(
                {
                    "eval_id": case["id"],
                    "eval_name": case["name"],
                    "prompt": case["prompt"],
                    "expected_output": case["expected_output"],
                    "assertions": case["assertions"],
                    "resolved_prompts": resolved,
                },
                indent=2,
            )
            + "\n"
        )

    print(f"staged {len(plan)} runs under {iteration}\n")
    print("RUN PLAN (paste prompts verbatim into executors):")
    for name, config, k, work, prompt in plan:
        print(f"\n- {name} / {config} / run-{k}")
        print(f"  work: {work}")
        print(f"  prompt: {prompt}")


if __name__ == "__main__":
    main()
