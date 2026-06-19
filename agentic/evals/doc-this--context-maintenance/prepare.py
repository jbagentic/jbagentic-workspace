#!/usr/bin/env python3
"""Stage clean-room work folders for the context-maintenance rule eval.

This eval measures an ALWAYS-ON behavioral rule ("How to Document Context") that
doc-this installs into the top-level CLAUDE.md/AGENTS.md — not an invocable skill.
The A/B is *rule present in the agent's instructions* vs *absent*; the single
controlled variable must be exactly that rule block.

Unlike the discovery eval, maintenance is a WRITE behavior, so each run is an
action: the staged agent makes a real code change and is expected to reconcile the
doc that covers it in the same pass. Two things follow:

  1. The doc-this skill is copied into EVERY clean room (both arms), because the
     rule literally routes doc work to it and in the real world the skill is always
     present. Holding the skill constant across arms keeps the rule block the only
     variable (an isolation spike confirmed a copied skill is discoverable and
     invocable in headless `claude -p`).
  2. The corpus copy is the agent's writable workspace; grade.py reads the mutated
     files back from this $TMPDIR work dir after run.py executes.

As in the discovery eval, each work dir is staged OUTSIDE the repo (under $TMPDIR)
with a root CLAUDE.md identical across arms except the rule block:
  - with_rule    -> CLAUDE.md = preamble + the verbatim "How to Document Context" block
  - without_rule -> CLAUDE.md = preamble only

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
REPO = HERE.parents[2]  # doc-this--context-maintenance -> evals -> agentic -> repo root
CORPUS = HERE / "fixtures" / "corpus"
RULE_REF = REPO / ".agents/skills/doc-this/references/context-maintenance.reference.md"
SKILL_SRC = REPO / "agentic/skills/doc-this"

PREAMBLE = (
    "# Acme Platform\n\n"
    "Internal backend monorepo. Make the requested code changes to the services here.\n"
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
    if "How to Document Context" not in block:
        raise SystemExit(f"extracted block is not the maintenance rule:\n{block}")
    return block


def claude_md_for(config: str, rule_block: str) -> str:
    if config == "with_rule":
        return f"{PREAMBLE}\n{rule_block}\n"
    if config == "without_rule":
        return PREAMBLE
    raise SystemExit(f"unknown config '{config}' (expected with_rule | without_rule)")


def stage_workdir(tmp_root: Path, config: str, rule_block: str) -> Path:
    """One clean room: corpus copy + arm-specific CLAUDE.md + copied doc-this skill."""
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir(parents=True)
    # Corpus contents copied into the work root so corpus/README.md is the project
    # root README the agent lands on, and the tree is the agent's writable workspace.
    for child in CORPUS.iterdir():
        dst = tmp_root / child.name
        if child.is_dir():
            shutil.copytree(child, dst)
        else:
            shutil.copy2(child, dst)
    (tmp_root / "CLAUDE.md").write_text(claude_md_for(config, rule_block), encoding="utf-8")
    # Hermetic copy of the doc-this skill into BOTH arms (held constant; the rule
    # block is the only variable). A copy, not a symlink — a write-enabled agent
    # must not be able to mutate the real skill through the clean room.
    skill_dst = tmp_root / ".claude" / "skills" / "doc-this"
    shutil.copytree(SKILL_SRC, skill_dst)
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
    if not SKILL_SRC.is_dir():
        raise SystemExit(f"doc-this skill source not found: {SKILL_SRC}")

    tmp_base = Path(tempfile.gettempdir()) / "doc-this--context-maintenance" / iteration.name

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
                    "task": case["prompt"],
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
                    "mode": case.get("mode", "change"),
                    "change_file": case.get("change_file"),
                    "change_keywords": case.get("change_keywords", []),
                    "doc_file": case["doc_file"],
                    "doc_must_exist": case["doc_must_exist"],
                    "doc_required": case["doc_required"],
                    "doc_forbidden": case.get("doc_forbidden", []),
                    "also_reconcile": case.get("also_reconcile", []),
                    "secondary_doc": case.get("secondary_doc"),
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
