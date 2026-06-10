#!/usr/bin/env python3
"""Digest a recording folder into the raw material for YouTube metadata.

Usage:
    python srt_digest.py <folder> [--bucket SECONDS]

Prints three blocks:
  1. METADATA  — parsed from the folder name (date, episode #, person, title)
  2. TIMELINE  — the .en.srt collapsed into time-bucketed lines (for chapters)
  3. TRANSCRIPT — the full cleaned transcript (for titles / description)

The skill (series-youtube-metadata) consumes this so it doesn't re-derive
timestamps by hand each run. Deterministic mechanics only — no judgement.
The folder-name METADATA is a locator hint only; the show's episode records
are authoritative for date / number / title / people.

The SRT mechanics are content-agnostic. Only DEFAULT_FOLDER_RE is show-specific:
it matches the example scheme `<Series>-<YYYYMMDD>-meetup-<N>-<Person>-<Title>`.
A project with a different naming scheme swaps that pattern (or has the agent
parse the name per its show profile); everything else stays as-is.
"""
import re
import sys
import glob
import os

# Default folder pattern — the JB Agentic meetup scheme. Swap this for another
# show's convention, or skip it and parse the name per the show profile.
DEFAULT_FOLDER_RE = re.compile(
    r"JBAgentic-(\d{8})-meetup-(\d+)-([A-Za-z0-9]+)-(.+)", re.IGNORECASE
)


def split_camel(token: str) -> str:
    """KhewJiaPeng -> 'Khew Jia Peng'; AIMeetsInfrastructure -> 'AI Meets Infrastructure'."""
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", token)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", s)
    return s.strip()


def parse_folder(folder: str):
    base = os.path.basename(os.path.normpath(folder))
    m = DEFAULT_FOLDER_RE.match(base)
    if not m:
        return {
            "raw": base,
            "date": None,
            "meetup": None,
            "speaker": None,
            "topic": None,
            "warning": "Folder name does not match the default pattern "
            "(<Series>-<YYYYMMDD>-meetup-<N>-<Person>-<Title>). "
            "It is only a locator — identify the episode another way and read "
            "its facts from the show's episode records; if you still can't, "
            "ask the user.",
        }
    date, meetup, speaker, topic = m.groups()
    return {
        "raw": base,
        "date": f"{date[0:4]}-{date[4:6]}-{date[6:8]}",
        "meetup": int(meetup),
        "speaker": split_camel(speaker),
        "topic": split_camel(topic),
    }


def find_en_srt(folder: str):
    cands = glob.glob(os.path.join(folder, "*.en.srt"))
    # Prefer the polished .en.srt over any .en.raw.srt
    non_raw = [c for c in cands if ".raw." not in os.path.basename(c)]
    pool = non_raw or cands
    return sorted(pool)[0] if pool else None


def parse_cues(path: str):
    """Return list of (start_seconds, text)."""
    cues = []
    cur_start = None
    buf = []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip("\n")
            if "-->" in line:
                if cur_start is not None and buf:
                    cues.append((cur_start, " ".join(buf).strip()))
                    buf = []
                ts = line.split("-->")[0].strip()
                hh, mm, rest = ts.split(":")
                ss = rest.replace(",", ".").split(".")[0]
                cur_start = int(hh) * 3600 + int(mm) * 60 + int(ss)
            elif re.fullmatch(r"\d+", line.strip()):
                continue
            elif line.strip() == "":
                continue
            else:
                buf.append(line.strip())
    if cur_start is not None and buf:
        cues.append((cur_start, " ".join(buf).strip()))
    return cues


def fmt_ts(sec: int) -> str:
    return f"{sec // 60}:{sec % 60:02d}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    folder = sys.argv[1]
    bucket = 45
    if "--bucket" in sys.argv:
        bucket = int(sys.argv[sys.argv.index("--bucket") + 1])

    meta = parse_folder(folder)
    srt = find_en_srt(folder)

    print("===== METADATA =====")
    for k in ("raw", "date", "meetup", "speaker", "topic"):
        print(f"{k}: {meta.get(k)}")
    if meta.get("warning"):
        print(f"WARNING: {meta['warning']}")
    print(f"srt: {os.path.basename(srt) if srt else 'NONE FOUND'}")
    print()

    if not srt:
        print("No .en.srt found in folder; cannot produce timeline/transcript.")
        sys.exit(2)

    cues = parse_cues(srt)
    if cues:
        print(f"duration: ~{fmt_ts(cues[-1][0])}")
        print()

    print(f"===== TIMELINE ({bucket}s buckets) =====")
    last_b = None
    buf = []
    for sec, text in cues:
        b = (sec // bucket) * bucket
        if b != last_b:
            if last_b is not None:
                print(f"{fmt_ts(last_b)} | {' '.join(buf)}")
            buf = []
            last_b = b
        buf.append(text)
    if last_b is not None:
        print(f"{fmt_ts(last_b)} | {' '.join(buf)}")
    print()

    print("===== TRANSCRIPT =====")
    print(" ".join(t for _, t in cues))


if __name__ == "__main__":
    main()
