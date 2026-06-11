#!/usr/bin/env python3
"""Extract a slide deck's text layer to plain text — stdlib only, zero deps.

Many slide decks (Google Slides / Keynote / PowerPoint exports) carry a real PDF
text layer. This pulls that text out without any PDF library, so a downstream
skill can build a term glossary from cheap text instead of reading slide PNGs as
(expensive) vision input.

How:
  1. Walk the PDF's `stream … endstream` objects and FlateDecode (`zlib`) them.
  2. Build a glyph→Unicode map from every `/ToUnicode` CMap (`beginbfchar` /
     `beginbfrange`) — subsetted fonts remap character codes, so the raw glyph
     bytes are gibberish until you apply this map.
  3. Read the text-showing operators (`(...) Tj`, `[...] TJ`) out of each
     `BT … ET` block, decode through the map, and collapse the per-glyph spacing
     that TJ kerning leaves behind.

One content stream ≈ one slide for typical exports, so output is grouped as
`## slide-NN` sections in document order. This is best-effort and deterministic —
it recovers glossary text (titles, bullets, code, filenames), NOT faithful
layout. It prints nothing usable for an image-only / "print to PDF" deck with no
text layer; that empty result is the signal to fall back to a one-time vision
pass over the slide PNGs.

Usage:
  python3 extract_deck_text.py slides.pdf        # -> stdout
Exit status: 0 if substantial text was recovered, 1 if the deck looks image-only.
"""
import re
import sys
import zlib
from pathlib import Path

_STR = re.compile(rb"\(((?:[^()\\]|\\.)*)\)", re.S)
_TEXT_OP = re.compile(rb"(\[[^\]]*\]\s*TJ|\([^()]*\)\s*Tj)", re.S)
_BT_ET = re.compile(rb"BT(.*?)ET", re.S)
_BFCHAR = re.compile(rb"beginbfchar(.*?)endbfchar", re.S)
_BFRANGE = re.compile(rb"beginbfrange(.*?)endbfrange", re.S)
_CSR = re.compile(rb"begincodespacerange(.*?)endcodespacerange", re.S)
_PAIR = re.compile(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>")
_TRIPLE = re.compile(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>")
_ESC = {b"n": 10, b"r": 13, b"t": 9, b"b": 8, b"f": 12, b"(": 40, b")": 41, b"\\": 92}


def _decompress_streams(pdf: bytes):
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", pdf, re.S):
        raw = m.group(1)
        for wbits in (15, -15):
            try:
                yield zlib.decompress(raw, wbits)
                break
            except zlib.error:
                continue


def _build_cmap(streams):
    """Merge all ToUnicode CMaps in the doc. Returns (code->unicode, code_width)
    where code_width is bytes per glyph code (2 for Identity/CID fonts, else 1)."""
    cmap = {}
    width = 1
    for d in streams:
        for blk in _CSR.findall(d):
            m = re.search(rb"<([0-9A-Fa-f]+)>", blk)
            if m and len(m.group(1)) // 2 > width:
                width = len(m.group(1)) // 2
        for blk in _BFCHAR.findall(d):
            for src, dst in _PAIR.findall(blk):
                cmap[int(src, 16)] = bytes.fromhex(dst.decode()).decode("utf-16-be", "replace")
        for blk in _BFRANGE.findall(d):
            for lo, hi, dst in _TRIPLE.findall(blk):
                lo_i, hi_i, base = int(lo, 16), int(hi, 16), int(dst, 16)
                for k in range(hi_i - lo_i + 1):
                    cmap[lo_i + k] = chr(base + k)
    return cmap, width


def _unescape(s: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == 0x5C and i + 1 < len(s):
            nxt = s[i + 1:i + 2]
            if nxt in _ESC:
                out.append(_ESC[nxt]); i += 2; continue
            mo = re.match(rb"[0-7]{1,3}", s[i + 1:i + 4])
            if mo:
                out.append(int(mo.group(), 8) & 0xFF); i += 1 + len(mo.group()); continue
            i += 1; continue
        out.append(c); i += 1
    return bytes(out)


def _despace(line: str) -> str:
    """TJ kerning emits each glyph separately, leaving a space between letters and
    a wider gap between words. Collapse: 2+ spaces -> word break, single space ->
    nothing. Only fire when the line is clearly letter-spaced (mostly singletons)."""
    runs = [r for r in re.split(r"\s+", line) if r]
    if len(runs) >= 6 and sum(len(r) == 1 for r in runs) / len(runs) > 0.6:
        line = re.sub(r" {2,}", "\x00", line)
        line = line.replace(" ", "")
        return line.replace("\x00", " ").strip()
    return line.strip()


def _decoder(cmap, width):
    def decode(b: bytes) -> str:
        if not cmap:  # non-subsetted font: bytes are (near-)Latin-1 text
            return b.decode("latin-1", "replace")
        if width == 2:
            codes = (int.from_bytes(b[i:i + 2], "big") for i in range(0, len(b) - 1, 2))
        else:
            codes = b
        return "".join(cmap.get(c, "") for c in codes)
    return decode


def extract(path: str) -> str:
    streams = list(_decompress_streams(Path(path).read_bytes()))
    cmap, width = _build_cmap(streams)
    decode = _decoder(cmap, width)
    sections = []
    n = 0
    for d in streams:
        if b"BT" not in d:
            continue
        lines = []
        for blk in _BT_ET.findall(d):
            buf = []
            for op in _TEXT_OP.findall(blk):
                for s in _STR.findall(op):
                    buf.append(decode(_unescape(s)))
            text = "".join(buf)
            for ln in text.splitlines():
                ln = _despace(ln)
                if ln:
                    lines.append(ln)
        if lines:
            n += 1
            sections.append(f"## slide-{n:02d}\n" + "\n".join(lines))
    return "\n\n".join(sections)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: extract_deck_text.py slides.pdf")
    out = extract(sys.argv[1])
    sys.stdout.write(out + ("\n" if out else ""))
    sys.exit(0 if len(out) >= 200 else 1)


if __name__ == "__main__":
    main()
