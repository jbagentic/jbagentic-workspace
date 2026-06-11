#!/usr/bin/env python3
"""Stage per-run work folders for the slides-pdf-to-text evals.

Like slides-pdf-to-png, this stages ONE work dir per (case x config x run) so
concurrent runs never collide, all inside the gitignored runs/. Unlike that
eval, the fixtures are the REAL committed talk decks — each case copies a talk
folder's slides.pdf + slides/ PNG folder into work/. It deliberately does NOT
copy the talk's committed slides.txt: that file is the human-verified oracle the
curated term lists were drawn from, and staging it would hand the executor the
answer. grade.py reads it from the talk folder, never from work/.

The vision case's deck (Khew) is image-only — the cheap extractor returns nothing
and the skill must transcribe the slides/ PNGs via vision — so the PNGs are
essential inputs, not just untouched-check bait, and are always staged.

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
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]  # slides-pdf-to-text -> evals -> agentic -> repo root
TALKS = REPO / "projects/jb-agentic-meetup/talk-recordings"

# case name -> talk slug whose slides.pdf + slides/ feed it.
CASE_SLUGS = {
    "textlayer-kowa": "JBAgentic-20260530-meetup-1-KowaJiaLiang-OurAIJourney",
    "vision-khew": "JBAgentic-20260530-meetup-1-KhewJiaPeng-AIMeetsInfrastructure",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_case(case, run_dir):
    slug = CASE_SLUGS[case["name"]]
    src = TALKS / slug
    pdf = src / "slides.pdf"
    pngdir = src / "slides"
    if not pdf.exists():
        raise SystemExit(f"MISSING source deck: {pdf}")
    if not pngdir.is_dir():
        raise SystemExit(f"MISSING rendered PNGs: {pngdir}")

    work = run_dir / "work"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    work.mkdir(parents=True)

    shutil.copy2(pdf, work / "slides.pdf")
    shutil.copytree(pngdir, work / "slides")

    seed = {
        "case": case["name"],
        "talk_slug": slug,
        "files": {
            str(p.relative_to(work)): sha256(p)
            for p in sorted(work.rglob("*"))
            if p.is_file()
        },
    }
    (run_dir / "seed.json").write_text(json.dumps(seed, indent=2) + "\n")
    return work, seed


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
        pages = None
        for config in configs:
            for k in range(1, args.runs + 1):
                run_dir = eval_dir / config / f"run-{k}"
                work, seed = stage_case(case, run_dir)
                pages = sum(1 for f in seed["files"] if f.startswith("slides/slide-"))
                prompt = case["prompt"].replace("{WORK_DIR}", str(work))
                resolved[f"{config}/run-{k}"] = prompt
                plan.append((case["name"], config, k, pages, work, prompt))
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
    for name, config, k, pages, work, prompt in plan:
        print(f"\n- {name} / {config} / run-{k}  ({pages} slides)")
        print(f"  work: {work}")
        print(f"  prompt: {prompt}")


if __name__ == "__main__":
    main()
