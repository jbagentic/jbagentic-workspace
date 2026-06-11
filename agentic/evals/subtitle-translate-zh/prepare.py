#!/usr/bin/env python3
"""Stage the inputs for the subtitle-translate-zh evals.

The eval runs the skill against throwaway copies — never the committed talk
folders, because the skill writes its outputs as siblings of the input
(`<slug>.en.srt` -> `<slug>.zh-Hans.srt` / `<slug>.zh-Hant.srt`), which would
clobber the talks' committed translations.

Two real cases are excerpts, not full talks: the first N cues of each talk's
polished `.en.srt`, cut to the minimal range that covers the talk's signature
terms (full ~850-cue talks cost 5x+ more to translate and full real
transcripts proved non-discriminating in the subtitle-polish eval). Cue
numbering and timestamps are kept byte-for-byte so the skill's invariants are
checkable against the staged file. The synthetic case is copied from the
committed fixtures/.

Idempotent. Run before grading/iterating the subtitle-translate-zh skill:
  python3 agentic/evals/subtitle-translate-zh/prepare.py
"""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]  # subtitle-translate-zh -> evals -> agentic -> repo root
TALKS = REPO / "projects/jb-agentic-meetup/talk-recordings"
STAGE = HERE / "stage"

# talk slug -> last cue to keep (1-based, inclusive). Ranges chosen so each
# talk's trap terms all appear: Khew's Bicep last hits cue 127; Soh's Telegram
# first appears at cue 132 and ringgit at cues 86/92.
EXCERPTS = {
    "JBAgentic-20260530-meetup-1-KhewJiaPeng-AIMeetsInfrastructure": 130,
    "JBAgentic-20260530-meetup-1-SohJunWei-AIForEverydayFriction": 140,
}


def excerpt(src_srt, last_cue):
    """First `last_cue` cues, numbering and timestamps untouched."""
    text = src_srt.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", text.strip())
    if len(blocks) < last_cue:
        sys.exit(f"{src_srt.name} has only {len(blocks)} cues, need {last_cue}")
    return "\n\n".join(blocks[:last_cue]) + "\n"


def stage_talk(slug, last_cue):
    src = TALKS / slug
    en = src / f"{slug}.en.srt"
    if not en.exists():
        sys.exit(f"MISSING polished transcript: {en}")
    dst = STAGE / slug
    dst.mkdir(parents=True, exist_ok=True)
    (dst / en.name).write_text(excerpt(en, last_cue), encoding="utf-8")
    pdf = src / "slides.pdf"
    if pdf.exists():
        shutil.copy2(pdf, dst / "slides.pdf")
    txt = src / "slides.txt"
    if txt.exists():
        shutil.copy2(txt, dst / "slides.txt")
    extras = "".join(s for s, p in ((" + slides.pdf", pdf), (" + slides.txt", txt)) if p.exists())
    print(f"staged {slug}: cues 1-{last_cue}{extras}")


def stage_synthetic():
    fixture = HERE / "fixtures/synthetic-vocab-traps.en.srt"
    dst = STAGE / "synthetic-vocab-traps"
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fixture, dst / fixture.name)
    print(f"staged synthetic-vocab-traps: {fixture.name}")


def check_opencc():
    """Parity guard: the skill's real workflow converts Hans -> Hant with
    OpenCC s2twp. Eval subagents can't pip-install (sandboxed, no network),
    so OpenCC must already be importable — otherwise runs silently exercise
    a manual-conversion fallback instead of the workflow being measured.
    Fix: pip3 install --user --break-system-packages opencc-python-reimplemented
    """
    try:
        from opencc import OpenCC  # noqa: F401
    except ImportError:
        sys.exit(
            "MISSING opencc: eval runs would fall back to manual Hans->Hant\n"
            "conversion instead of the skill's real OpenCC step. Install it:\n"
            "  pip3 install --user --break-system-packages opencc-python-reimplemented"
        )


def main():
    check_opencc()
    for slug, last_cue in EXCERPTS.items():
        stage_talk(slug, last_cue)
    stage_synthetic()
    print(f"done -> {STAGE.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
