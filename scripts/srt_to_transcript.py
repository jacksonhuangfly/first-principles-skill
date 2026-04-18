#!/usr/bin/env python3
"""Convert SRT/WebVTT cues into readable paragraphs with the standard library.

Cue IDs, timestamps, NOTE/STYLE/REGION blocks, and markup are removed. Numeric
dialogue is preserved. Only adjacent duplicate lines/cues are removed; this is
not a speech recognizer or a semantic rewrite of rolling captions.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
import re

STAMP = r"(?:\d{2,}:)?\d{2}:\d{2}[.,]\d{3}"
TIMING = re.compile(rf"^{STAMP}\s+-->\s+{STAMP}(?:\s+.*)?$")


def clean_cues(content: str, *, vtt: bool = False) -> str:
    content = content.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    texts = []
    previous_cue = None
    for block in re.split(r"\n[ \t]*\n", content.strip()):
        lines = [line.strip() for line in block.splitlines()]
        if not lines:
            continue
        if vtt and (re.match(r"^WEBVTT(?:\s|$)", lines[0]) or
                    re.match(r"^NOTE(?:\s|$)", lines[0]) or
                    lines[0] in {"STYLE", "REGION"}):
            continue
        timing = next((i for i, line in enumerate(lines) if TIMING.fullmatch(line)), None)
        if timing is None:
            # Unrecognized blocks are not dialogue; never leak cue metadata.
            continue
        cue = []
        for line in lines[timing + 1:]:
            text = html.unescape(re.sub(r"<[^>]+>", "", line)).strip()
            if text:
                cue.append(text)
        if cue == previous_cue:
            continue
        previous_cue = cue
        for text in cue:
            if not texts or texts[-1] != text:
                texts.append(text)
    paragraphs = []
    current = []
    for text in texts:
        current.append(text)
        if len(" ".join(current)) > 200 or re.search(r"[。！？.!?]$", text):
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs)


def clean_srt(content: str) -> str:
    return clean_cues(content)


def clean_vtt(content: str) -> str:
    return clean_cues(content, vtt=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"input file does not exist: {args.input}")
    content = args.input.read_text(encoding="utf-8-sig")
    is_vtt = args.input.suffix.lower() == ".vtt" or content.startswith("WEBVTT")
    transcript = clean_vtt(content) if is_vtt else clean_srt(content)
    if not transcript:
        parser.error("no dialogue found in valid subtitle cues")
    output = args.output or args.input.with_name(f"{args.input.stem}_transcript.txt")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(transcript + "\n", encoding="utf-8")
    paragraphs = len(transcript.split("\n\n"))
    print(f"Converted: {output}")
    print(f"Characters: {len(transcript)}; paragraphs: {paragraphs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
