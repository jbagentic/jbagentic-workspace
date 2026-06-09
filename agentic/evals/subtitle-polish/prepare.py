#!/usr/bin/env python3
"""Stage the real talk inputs for the subtitle-polish evals.

The eval runs the skill against a throwaway copy of each talk's real auto-transcript
plus its slide deck — never the committed talk folder, because the skill writes its
polished output as a sibling of the input (`<slug>.en.raw.srt` -> `<slug>.en.srt`),
which would clobber the talk's committed polished `.en.srt`.

So we copy, per talk, from
  projects/jb-agentic-meetup/talk-recordings/<slug>/
into the gitignored
  agentic/evals/subtitle-polish/stage/<slug>/
the files the skill needs: the raw SRT, slides/, and slides.pdf. Nothing here is
committed — the slide decks and transcripts live once, in talk-recordings/.

Idempotent. Run before grading/iterating the subtitle-polish skill:
  python3 agentic/evals/subtitle-polish/prepare.py
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]  # subtitle-polish -> evals -> agentic -> repo root
TALKS = REPO / "projects/jb-agentic-meetup/talk-recordings"
STAGE = HERE / "stage"

# One real case per talk. The folder name is the talk slug; the raw SRT reuses it.
TALK_SLUGS = [
    "JBAgentic-20260530-meetup-1-KhewJiaPeng-AIMeetsInfrastructure",
    "JBAgentic-20260530-meetup-1-KowaJiaLiang-OurAIJourney",
    "JBAgentic-20260530-meetup-1-SohJunWei-AIForEverydayFriction",
]


def stage_one(slug):
    src = TALKS / slug
    raw = src / f"{slug}.en.raw.srt"
    if not raw.exists():
        sys.exit(
            f"MISSING raw transcript: {raw}\n"
            f"Add the talk's auto-generated <slug>.en.raw.srt before staging."
        )
    dst = STAGE / slug
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(raw, dst / raw.name)
    shutil.copytree(src / "slides", dst / "slides", dirs_exist_ok=True)
    pdf = src / "slides.pdf"
    if pdf.exists():
        shutil.copy2(pdf, dst / "slides.pdf")
    n = len(list((dst / "slides").glob("*.png")))
    print(f"staged {slug}: {raw.name} + {n} slides" + (" + slides.pdf" if pdf.exists() else ""))


def main():
    for slug in TALK_SLUGS:
        stage_one(slug)
    print(f"done -> {STAGE.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
