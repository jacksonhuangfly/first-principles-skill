#!/usr/bin/env python3
"""Check local file targets in Markdown links throughout a file or directory.

Supports inline/image links, reference definitions, URL-encoded paths, titles,
and fragments. Fenced/inline code and HTML comments are ignored. Fragment names
and remote URLs are not validated. Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def prose_only(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return re.sub(r"(`+)(.*?)\1", "", "\n".join(lines), flags=re.S)


def destination(text: str, start: int) -> str | None:
    """Read a Markdown destination without its optional title or closing )."""
    i = start
    while i < len(text) and text[i].isspace():
        i += 1
    if i >= len(text):
        return None
    if text[i] == "<":
        end = i + 1
        while end < len(text):
            if text[end] == "\\":
                end += 2
                continue
            if text[end] == ">":
                return text[i + 1:end]
            end += 1
        return None
    begin = i
    depth = 0
    while i < len(text):
        char = text[i]
        if char == "\\":
            i += 2
            continue
        if char.isspace():
            break
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                break
            depth -= 1
        i += 1
    return text[begin:i]


def links(text: str):
    text = prose_only(text)
    # Definitions cover full, collapsed, and shortcut reference links without
    # mistaking ordinary [bracketed prose] for a link.
    for match in re.finditer(r"^\s{0,3}\[[^\]\n]+\]:\s*", text, re.M):
        link = destination(text, match.end())
        if link is not None:
            yield link
    for match in re.finditer(r"(?<!\\)\]\(", text):
        link = destination(text, match.end())
        if link is not None:
            yield link


def check_file(path: Path) -> list[str]:
    bad = []
    for raw in links(path.read_text(encoding="utf-8")):
        link = html.unescape(re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", raw))
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = path.parent / unquote(parsed.path)
        if not target.exists() and raw not in bad:
            bad.append(raw)
    return bad


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Markdown file or directory")
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.exists():
        parser.error(f"input does not exist: {target}")
    files = [target] if target.is_file() else sorted(target.rglob("*.md"))
    if not files:
        parser.error(f"no Markdown files found: {target}")
    failed = False
    for file in files:
        bad = check_file(file)
        if bad:
            failed = True
            print(f"BROKEN LINKS: {file}")
            for link in bad:
                print(f"  {link}")
    if failed:
        return 1
    print(f"OK: checked local file targets in {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
