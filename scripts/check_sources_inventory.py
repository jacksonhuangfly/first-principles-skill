#!/usr/bin/env python3
"""Validate source-card metadata, nonempty captures, and unique source URLs.

Catalog entries and indexes remain useful references but are counted separately
from captured content. Counts are descriptive, not arbitrary quality thresholds.
This checks structure, not source accuracy, rights, or completeness.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit

KINDS = ("books", "transcripts", "articles")
REQUIRED = ("url", "author", "date", "captured_at", "source_type", "language")


def source_files(path: Path) -> list[Path]:
    return sorted(p for p in path.rglob("*.md")
                  if p.is_file() and not p.name.lower().startswith("readme"))


def metadata(text: str) -> dict[str, str]:
    """Read the simple scalar frontmatter used by cards, without PyYAML."""
    match = re.match(r"\A\ufeff?---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([\w-]+):\s*(.*?)\s*$", line)
        if not field:
            continue
        key, value = field.groups()
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except (ValueError, TypeError):
                value = ""
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        else:
            value = value.split(" #", 1)[0].strip()
        result[key] = value if isinstance(value, str) and value not in {"null", "~"} else ""
    return result


def capture_sections(text: str) -> list[tuple[str, str]]:
    sections = []
    for match in re.finditer(r"^##\s+Captured\s+([^\n]+)\n", text, re.M):
        # Captured articles may contain their own H2 headings. Only card-level
        # metadata sections (or a subsequent capture) terminate the body.
        end = re.search(
            r"^##[ \t]+(?:Source Metadata|Extracted Headings|Traceability|Distillation Note|Captured[ \t]+[^\n]+)[ \t]*$",
            text[match.end():], re.M,
        )
        body = text[match.end():match.end() + end.start()] if end else text[match.end():]
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        body = "\n".join(line for line in body.splitlines() if not line.lstrip().startswith("#"))
        if re.search(r"\w", body):
            sections.append((match.group(1).strip(), body.strip()))
    return sections


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    host = parts.netloc.lower()
    if (parts.scheme.lower() == "https" and host.endswith(":443")) or (
            parts.scheme.lower() == "http" and host.endswith(":80")):
        host = host.rsplit(":", 1)[0]
    return urlunsplit((parts.scheme.lower(), host, parts.path.rstrip("/"), parts.query, ""))


def inspect_card(path: Path) -> tuple[dict[str, str], str, list[str]]:
    text = path.read_text(encoding="utf-8")
    fields = metadata(text)
    errors = [f"missing metadata: {key}" for key in REQUIRED if not fields.get(key, "").strip()]
    url = urlsplit(fields.get("url", ""))
    if fields.get("url") and (url.scheme not in {"http", "https"} or not url.netloc):
        errors.append("url must be an absolute HTTP(S) URL")
    if fields.get("captured_at"):
        try:
            date.fromisoformat(fields["captured_at"])
        except ValueError:
            errors.append("captured_at must be an ISO date (YYYY-MM-DD)")
    sections = capture_sections(text)
    if not sections:
        errors.append("missing nonempty Captured section")
    source_type = fields.get("source_type", "").lower()
    is_index = any(term in source_type for term in ("catalog", "index", "archive_root", "archive_card"))
    is_index = is_index or source_type == "official_site" or any(
        "catalog" in label.lower() or "index" in label.lower() for label, _ in sections)
    category = "index" if is_index else "content"
    if is_index and any(label.lower() == "full text" for label, _ in sections):
        errors.append("catalog/index must use Captured Catalog Entry/Index, not Captured Full Text")
    return fields, category, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    root = repo / "references" / "sources"
    if not repo.is_dir() or not root.is_dir():
        parser.error(f"source directory does not exist: {root}")
    failed = False
    urls = defaultdict(list)
    total = 0
    for kind in KINDS:
        counts = {"content": 0, "index": 0}
        files = source_files(root / kind)
        total += len(files)
        for path in files:
            fields, category, errors = inspect_card(path)
            counts[category] += 1
            if fields.get("url"):
                urls[canonical_url(fields["url"])].append(path)
            for error in errors:
                print(f"FAIL {path.relative_to(repo)}: {error}")
                failed = True
        print(f"{kind}: files={len(files)} content={counts['content']} index={counts['index']}")
    if not total:
        print(f"FAIL: no source cards found under {root}")
        failed = True
    for url, paths in urls.items():
        if len(paths) > 1:
            failed = True
            print(f"FAIL duplicate source URL: {url}")
            for path in paths:
                print(f"  {path.relative_to(repo)}")
    if failed:
        return 1
    print(f"OK: {total} source cards; {len(urls)} unique URLs; metadata and nonempty captures checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
