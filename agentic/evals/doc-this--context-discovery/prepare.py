#!/usr/bin/env python3
"""Stage clean-room work folders for the context-discovery rule eval.

This eval measures an ALWAYS-ON behavioral rule ("How to Discover Context") that
doc-this installs into the top-level CLAUDE.md/AGENTS.md — not an invocable skill.
The A/B is therefore *rule present in the agent's instructions* vs *absent*, and
the single controlled variable must be exactly that.

The trap: this workspace's own AGENTS.md already carries the rule, and any agent
run inside the repo inherits it — so an in-repo baseline is contaminated. The
isolation spike (see README.md) confirmed two facts this staging relies on:
  1. a `claude -p` run from a $TMPDIR cwd does NOT inherit the workspace AGENTS.md
     (no rule leaks in), and
  2. headless claude loads a local CLAUDE.md but NOT a bare AGENTS.md.

So each work dir is staged OUTSIDE the repo (under $TMPDIR) and carries a root
CLAUDE.md that is identical across arms except for the rule block:
  - with_rule    -> CLAUDE.md = preamble + the verbatim "How to Discover Context" block
  - without_rule -> CLAUDE.md = preamble only

The corpus (fixtures/corpus/) is copied in beside CLAUDE.md so the project root
README is the agent's entry point. Durable artifacts (seed.json, eval_metadata,
and later transcripts/grading) live under this eval's runs/ inside the repo; the
ephemeral clean rooms live in $TMPDIR.

Idempotent: re-running wipes and re-stages each run's $TMPDIR work dir.

Usage:
  python3 prepare.py runs/iteration-1 [--configs with_rule,without_rule] [--runs 2]
"""
import argparse
import json
import shutil
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]  # doc-this--context-discovery -> evals -> agentic -> repo root
CORPUS = HERE / "fixtures" / "corpus"
RULE_REF = REPO / ".agents/skills/doc-this/references/context-discovery.reference.md"

PREAMBLE = (
    "# Acme Platform\n\n"
    "Internal backend monorepo. Answer questions about the code and services here.\n"
)


def extract_rule_block() -> str:
    """Pull the verbatim rule block from the doc-this reference's first ```md fence."""
    text = RULE_REF.read_text(encoding="utf-8")
    marker = "```md"
    start = text.find(marker)
    if start == -1:
        raise SystemExit(f"could not find a ```md fence in {RULE_REF}")
    start += len(marker)
    end = text.find("```", start)
    if end == -1:
        raise SystemExit(f"unterminated ```md fence in {RULE_REF}")
    block = text[start:end].strip("\n")
    if "How to Discover Context" not in block:
        raise SystemExit(f"extracted block is not the discovery rule:\n{block}")
    return block


def claude_md_for(config: str, rule_block: str) -> str:
    if config == "with_rule":
        return f"{PREAMBLE}\n{rule_block}\n"
    if config == "without_rule":
        return PREAMBLE
    raise SystemExit(f"unknown config '{config}' (expected with_rule | without_rule)")


def stage_workdir(tmp_root: Path, config: str, rule_block: str) -> Path:
    """Create one clean-room work dir: corpus copy + arm-specific CLAUDE.md."""
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir(parents=True)
    # Copy corpus contents directly into the work root so corpus/README.md is the
    # project root README the agent lands on.
    for child in CORPUS.iterdir():
        dst = tmp_root / child.name
        if child.is_dir():
            shutil.copytree(child, dst)
        else:
            shutil.copy2(child, dst)
    (tmp_root / "CLAUDE.md").write_text(claude_md_for(config, rule_block), encoding="utf-8")
    return tmp_root


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iteration_dir", help="e.g. runs/iteration-1 (relative to this eval folder, or absolute)")
    ap.add_argument("--configs", default="with_rule,without_rule")
    ap.add_argument("--runs", type=int, default=2)
    args = ap.parse_args()

    iteration = Path(args.iteration_dir)
    if not iteration.is_absolute():
        iteration = HERE / iteration
    configs = [c.strip() for c in args.configs.split(",") if c.strip()]
    rule_block = extract_rule_block()

    tmp_base = Path(tempfile.gettempdir()) / "doc-this--context-discovery" / iteration.name

    spec = json.loads((HERE / "evals.json").read_text(encoding="utf-8"))
    plan = []
    for case in spec["evals"]:
        eval_dir = iteration / f"eval-{case['name']}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        for config in configs:
            for k in range(1, args.runs + 1):
                run_dir = eval_dir / config / f"run-{k}"
                run_dir.mkdir(parents=True, exist_ok=True)
                work = stage_workdir(tmp_base / f"eval-{case['name']}" / config / f"run-{k}",
                                     config, rule_block)
                seed = {
                    "case": case["name"],
                    "config": config,
                    "run": k,
                    "arm_has_rule": config == "with_rule",
                    "work_dir": str(work),
                    "question": case["prompt"],
                }
                (run_dir / "seed.json").write_text(json.dumps(seed, indent=2) + "\n", encoding="utf-8")
                plan.append((case["name"], config, k, work))
        (eval_dir / "eval_metadata.json").write_text(
            json.dumps(
                {
                    "eval_id": case["id"],
                    "eval_name": case["name"],
                    "type": case["type"],
                    "prompt": case["prompt"],
                    "expected_output": case["expected_output"],
                    "answer_keywords": case["answer_keywords"],
                    "answer_forbidden": case.get("answer_forbidden", []),
                    "process": case["process"],
                    "target_file": case["target_file"],
                    "tool_budget": case["tool_budget"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    print(f"staged {len(plan)} clean rooms under {tmp_base}")
    print(f"artifacts will land under {iteration}\n")
    print("next:")
    print(f"  python3 {HERE.name}/run.py {args.iteration_dir}")
    print("then:")
    print(f"  python3 {HERE.name}/grade.py {args.iteration_dir}")


if __name__ == "__main__":
    main()
