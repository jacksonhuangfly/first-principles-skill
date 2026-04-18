#!/usr/bin/env python3
"""Find repeated prose blocks and three-line spans within/across Markdown files.

Ignores frontmatter, headings, fenced code, HTML comments, and link-only indexes.
Only blocks with at least 120 non-space characters (or 40 CJK characters) count;
short repeated labels and ordinary source lists are outside this check's scope.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re


def normalize(line: str) -> str:
    return " ".join(line.split())


def substantial(text: str) -> bool:
    return len(re.sub(r"\s", "", text)) >= 120 or len(re.findall(r"[\u3400-\u9fff]", text)) >= 40


def link_only(line: str) -> bool:
    if re.match(r"^\s{0,3}\[[^\]]+\]:", line):
        return True
    stripped = re.sub(r"!?\[[^\]]*\]\([^)]*\)", "", line)
    stripped = re.sub(r"<?https?://\S+>?", "", stripped)
    return not re.sub(r"[\W_]+", "", stripped)


def prose_lines(path: Path) -> list[tuple[int, str]]:
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group().count("\n"),
                  path.read_text(encoding="utf-8"), flags=re.S)
    output = []
    frontmatter = False
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        if number == 1 and line.lstrip("\ufeff").strip() == "---":
            frontmatter = True
            continue
        if frontmatter:
            if line.strip() == "---":
                frontmatter = False
            continue
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            output.append((number, "\0"))
            continue
        if fence:
            continue
        if re.match(r"^\s{0,3}#{1,6}\s", line) or (line.strip() and link_only(line)):
            output.append((number, "\0"))  # barrier: do not join unrelated sections
        else:
            output.append((number, normalize(line)))
    return output


def candidates(path: Path):
    paragraph = []
    span = []
    emitted = set()

    def emit(parts):
        if not parts:
            return None
        text = normalize(" ".join(line for _, line in parts))
        location = parts[0][0]
        key = (text, location)
        if substantial(text) and key not in emitted:
            emitted.add(key)
            return text, location
        return None

    for number, line in prose_lines(path) + [(0, "\0")]:
        if not line or line == "\0":
            result = emit(paragraph)
            if result:
                yield result
            paragraph = []
            if line == "\0":
                span = []
            continue
        paragraph.append((number, line))
        span.append((number, line))
        span = span[-3:]
        if len(span) == 3:
            result = emit(span)
            if result:
                yield result


def scan_files(paths: list[Path]):
    buckets = defaultdict(set)
    for path in paths:
        for text, line in candidates(path):
            buckets[text].add((path, line))
    return {text: sorted(locations, key=lambda item: (str(item[0]), item[1]))
            for text, locations in buckets.items() if len(locations) > 1}


def scan(path: Path):
    return {text: [line for _, line in locations]
            for text, locations in scan_files([path]).items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.exists():
        parser.error(f"input does not exist: {target}")
    files = [target] if target.is_file() else sorted(target.rglob("*.md"))
    if not files:
        parser.error(f"no Markdown files found: {target}")
    dupes = scan_files(files)
    if dupes:
        for text, locations in list(dupes.items())[:20]:
            print(f"REPEATED PROSE: {text[:100]}...")
            for path, line in locations:
                print(f"  {path}:{line}")
        print(f"FAIL: {len(dupes)} repeated passages in {len(files)} files")
        return 1
    print(f"OK: checked prose blocks and three-line spans across {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
