#!/usr/bin/env python3
"""Generate (or verify) the synthetic fixture PDFs for the slides-pdf-to-png evals.

The PDFs are hand-rolled with the stdlib (no PyMuPDF/reportlab on this machine)
and byte-deterministic: no /CreationDate, no IDs, fixed object ordering. They are
generated ONCE with --write and committed, together with manifest.json recording
each fixture's page count, page size in points, sha256, and the frame width
expected at the skill's 1080px target height. Eval runs never regenerate them;
grade.py reads manifest.json instead of parsing PDFs.

Each page is visually non-blank: a full-page colored rectangle (distinct per
page), a large page number, and a footer line.

Usage:
  python3 make_fixtures.py          # verify committed PDFs match manifest.json
  python3 make_fixtures.py --write  # regenerate PDFs + manifest.json
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# name -> (width_pt, height_pt, pages)
FIXTURES = {
    "deck-3p-16x9.pdf": (720, 405, 3),   # 16:9 -> 1920x1080 frames
    "deck-3p-4x3.pdf": (640, 480, 3),    # 4:3  -> 1440x1080 frames
    "deck-2p-a4.pdf": (595, 842, 2),     # A4 portrait decoy for the multi-PDF case
}

# Distinct full-page background color per page index (RGB, 0..1)
PAGE_COLORS = ["0.85 0.30 0.25", "0.25 0.55 0.85", "0.30 0.70 0.40"]


def page_content(w, h, page_no):
    color = PAGE_COLORS[(page_no - 1) % len(PAGE_COLORS)]
    return (
        f"{color} rg 0 0 {w} {h} re f\n"
        f"BT 1 1 1 rg /F1 144 Tf {w * 0.4:.0f} {h * 0.4:.0f} Td ({page_no}) Tj ET\n"
        f"BT 1 1 1 rg /F1 12 Tf 20 20 Td (slides-pdf-to-png eval fixture - page {page_no}) Tj ET\n"
    ).encode("ascii")


def build_pdf(w, h, pages):
    # Objects: 1 catalog, 2 pages, 3 font, then per page: page obj + content obj.
    objects = {}
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(pages))
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[2] = (
        f"<< /Type /Pages /Kids [{kids}] /Count {pages} >>".encode("ascii")
    )
    objects[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    for i in range(pages):
        page_num, content_num = 4 + 2 * i, 5 + 2 * i
        objects[page_num] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {w} {h}] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_num} 0 R >>"
        ).encode("ascii")
        stream = page_content(w, h, i + 1)
        objects[content_num] = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"endstream"
        )

    out = bytearray(b"%PDF-1.4\n")
    offsets = {}
    for num in sorted(objects):
        offsets[num] = len(out)
        out += f"{num} 0 obj\n".encode("ascii") + objects[num] + b"\nendobj\n"
    xref_pos = len(out)
    count = len(objects) + 1
    out += f"xref\n0 {count}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for num in sorted(objects):
        out += f"{offsets[num]:010d} 00000 n \n".encode("ascii")
    out += (
        f"trailer\n<< /Size {count} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n"
    ).encode("ascii")
    return bytes(out)


def main():
    write = "--write" in sys.argv[1:]
    manifest = {}
    failures = []
    for name, (w, h, pages) in FIXTURES.items():
        data = build_pdf(w, h, pages)
        entry = {
            "pages": pages,
            "page_width_pt": w,
            "page_height_pt": h,
            "sha256": hashlib.sha256(data).hexdigest(),
            "expected_frame_width_at_1080": round(1080 * w / h),
            "expected_frame_height": 1080,
        }
        manifest[name] = entry
        path = HERE / name
        if write:
            path.write_bytes(data)
            print(f"wrote {name}: {pages} pages, {w}x{h} pt, {len(data)} bytes")
        else:
            if not path.exists():
                failures.append(f"{name}: missing (run with --write)")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
                failures.append(f"{name}: sha256 mismatch vs generator")
            else:
                print(f"ok {name}")

    if write:
        (HERE / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        print("wrote manifest.json")
    else:
        committed = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
        if committed != manifest:
            failures.append("manifest.json: does not match generator output")
        if failures:
            sys.exit("FAIL:\n  " + "\n  ".join(failures))
        print("all fixtures match manifest.json")


if __name__ == "__main__":
    main()
