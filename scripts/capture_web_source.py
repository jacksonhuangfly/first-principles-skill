#!/usr/bin/env python3
"""Capture a web source into a Markdown file with metadata and cleaned text."""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import re
from pathlib import Path
from urllib.parse import urlparse

TODAY = dt.date.today().isoformat()
TIMEOUT = 20
UA = {"User-Agent": "Mozilla/5.0 Codex/1.0"}
SOURCE_NOTICE_RE = re.compile(r"\bcopyright\b|©|\ball rights reserved\b", re.I)
STANDALONE_NOTICE_RE = re.compile(r"^(?:©|\(c\)\s*\d{4}|copyright\s*(?:©|\(c\)|\d{4})|all rights reserved[.!]?\s*$)", re.I)

FULL_TYPES = {
    "public_domain_book",
    "classical_text",
    "classical_text_selection",
    "official_collected_work",
    "official_speech",
    "speech_transcript",
    "public_recipe_page",
}
FULL_DOMAINS = {
    "classics.mit.edu",
    "ctext.org",
    "www.marxists.org",
    "marxists.org",
    "gov.cn",
    "www.gov.cn",
}
INDEX_TYPES = {
    "official_site",
    "index_page",
    "archive_root",
    "archive_index",
    "official_archive_card",
    "official_long_text_index",
    "blog_corpus_index",
    "corpus_reference_page",
}
NAV_WORDS = {
    "home",
    "browse and comment",
    "browse",
    "search",
    "help",
    "buy books and cd-roms",
    "commentary",
    "download",
    "table of contents",
    "language",
    "rss",
    "newsletters",
    "follow us",
    "sign in",
    "sign out",
    "your account",
    "share",
    "copied",
    "choose your language",
    "radio",
    "tv",
    "live",
    "opinions",
    "video",
    "home >",
    "home >>",
    "首页",
    "简",
    "繁",
    "en",
    "打开app",
    "用app打开",
    "app中查看更多做法",
    "follow cgtn on:",
    "we are china",
    "archive",
    "archives",
    "home page",
    "recently viewed",
    "you may also like",
    "notify me",
}


def yaml_quote(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def source_notice_lines(text: str) -> list[str]:
    """Preserve explicit notice text without interpreting its legal meaning."""
    return [line.strip() for line in text.splitlines() if SOURCE_NOTICE_RE.search(line)]


def request_url(url: str):
    import requests

    response = requests.get(url, headers=UA, timeout=TIMEOUT)
    response.raise_for_status()
    return response


def fetch_via_jina(url: str) -> dict:
    wrapped = f"https://r.jina.ai/{url}"
    response = request_url(wrapped)
    text = response.text.replace("\r\n", "\n")
    final_url = url
    match = re.search(r"^URL Source:\s*(.+)$", text, re.M)
    if match:
        final_url = match.group(1).strip()
    markdown = text.split("Markdown Content:\n", 1)[1] if "Markdown Content:\n" in text else text
    return {
        "status": response.status_code,
        "final_url": final_url,
        "content_type": response.headers.get("content-type", "text/plain"),
        "text": markdown.strip(),
    }


def fetch_direct_html(url: str) -> dict:
    from bs4 import BeautifulSoup, Comment, Doctype, NavigableString

    response = request_url(url)
    response.encoding = response.apparent_encoding or response.encoding or "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    for tag in soup(["script", "style", "noscript", "svg", "path", "form", "button"]):
        tag.decompose()
    # Footers can carry attribution and reuse notices outside the article root.
    # Keep footer text outside the body so body limits cannot remove it.
    footer_texts = [tag.get_text(" ", strip=True) for tag in soup.find_all("footer")]
    for tag in soup.find_all(["header", "footer", "nav", "aside"]):
        tag.decompose()
    root = soup.find("main") or soup.body or soup
    articles = root.find_all("article")
    if articles:
        # Keep one article focused, but include every article when a source
        # divides its chapters/sections between sibling article elements.
        root = articles[0]
        for article in articles[1:]:
            ancestors = list(article.parents)
            while not any(root is ancestor for ancestor in ancestors):
                root = root.parent
    lines = []
    if title:
        lines.append(f"# {title}")
    chunks = []
    block_tags = {
        "address", "article", "blockquote", "caption", "dd", "details", "div", "dl", "dt",
        "fieldset", "figcaption", "figure", "h1", "h2", "h3", "h4", "h5", "h6", "hr",
        "li", "main", "ol", "p", "pre", "section", "summary", "table", "tbody", "td",
        "tfoot", "th", "thead", "tr", "ul",
    }

    def flush():
        text = re.sub(r"\s+", " ", "".join(chunks)).strip()
        if text:
            lines.append(text)
        chunks.clear()

    def walk(element):
        # Visit text nodes once: flattening both a block and its nested blocks
        # repeats quotations/lists, while selecting only p/li misses div prose.
        if isinstance(element, (Comment, Doctype)):
            return
        if isinstance(element, NavigableString):
            chunks.append(str(element))
            return
        if element.name in {"head", "title"}:
            return
        if element.name == "br":
            flush()
            return
        block = element.name in block_tags
        if block:
            flush()
        if re.fullmatch(r"h[1-6]", element.name or ""):
            chunks.append("#" * int(element.name[1]) + " ")
        for child in element.children:
            walk(child)
        if block:
            flush()

    walk(root)
    flush()
    return {
        "status": response.status_code,
        "final_url": response.url,
        "content_type": response.headers.get("content-type", "text/html"),
        "text": "\n".join(lines),
        "footer_texts": [text for text in footer_texts if text],
    }


def fetch_pdf(url: str) -> dict:
    from pypdf import PdfReader

    response = request_url(url)
    reader = PdfReader(io.BytesIO(response.content))
    parts = []
    extraction_notes = []
    for number, page in enumerate(reader.pages, 1):
        try:
            text = page.extract_text() or ""
        except Exception:
            extraction_notes.append(f"Page {number}: text extraction failed.")
            continue
        if not text.strip():
            extraction_notes.append(f"Page {number}: no extractable text; may be blank or require OCR.")
            continue
        parts.append(text)
    return {
        "status": response.status_code,
        "final_url": response.url,
        "content_type": response.headers.get("content-type", "application/pdf"),
        "text": "\n\n".join(parts).strip(),
        "extraction_notes": extraction_notes,
    }


def fetch_url(url: str) -> dict:
    if urlparse(url).path.lower().endswith(".pdf"):
        return fetch_pdf(url)
    try:
        return fetch_via_jina(url)
    except Exception:
        return fetch_direct_html(url)


def choose_mode(source_type: str, url: str) -> str:
    domain = urlparse(url).netloc.lower()
    if "catalog" in source_type:
        return "catalog"
    if source_type in INDEX_TYPES or "index" in source_type:
        return "index"
    if source_type in FULL_TYPES:
        return "full"
    if domain in FULL_DOMAINS and source_type not in INDEX_TYPES:
        return "full"
    return "extract"


def md_link_text(line: str) -> str:
    """Remove inline link destinations without damaging balanced punctuation."""
    def closing(start, opening, ending):
        depth = 1
        pos = start + 1
        while pos < len(line):
            if line[pos] == "\\":
                pos += 2
                continue
            if line[pos] == opening:
                depth += 1
            elif line[pos] == ending:
                depth -= 1
                if not depth:
                    return pos
            pos += 1
        return None

    def link_end(start):
        pos = start + 1
        while pos < len(line) and line[pos].isspace():
            pos += 1
        if pos < len(line) and line[pos] == "<":
            end = closing(pos, "<", ">")
            if end is None:
                return None
            pos = end + 1
        else:
            while pos < len(line) and not line[pos].isspace() and line[pos] != ")":
                if line[pos] == "\\":
                    pos += 2
                elif line[pos] == "(":
                    end = closing(pos, "(", ")")
                    if end is None:
                        return None
                    pos = end + 1
                else:
                    pos += 1
        while pos < len(line) and line[pos].isspace():
            pos += 1
        if pos < len(line) and line[pos] in {"\"", "'", "("}:
            quote = line[pos]
            pos += 1
            while pos < len(line):
                if line[pos] == "\\":
                    pos += 2
                elif line[pos] == (")" if quote == "(" else quote):
                    pos += 1
                    break
                else:
                    pos += 1
            while pos < len(line) and line[pos].isspace():
                pos += 1
        return pos if pos < len(line) and line[pos] == ")" else None

    output = []
    pos = 0
    while pos < len(line):
        if line[pos] == "\\":
            output.append(line[pos:pos + 2])
            pos += 2
            continue
        image = line.startswith("![", pos)
        start = pos + 1 if image else pos
        if line[start:start + 1] == "[":
            label_end = closing(start, "[", "]")
            if label_end is not None and line[label_end + 1:label_end + 2] == "(":
                end = link_end(label_end + 1)
                if end is not None:
                    if not image:
                        output.append(md_link_text(line[start + 1:label_end]))
                    pos = end + 1
                    continue
        output.append(line[pos])
        pos += 1
    return "".join(output)


def clean_markdown(text: str, mode: str) -> tuple[str, str, list[str]]:
    lines = []
    for raw in text.splitlines():
        line = md_link_text(raw).strip()
        if not line:
            continue
        line = re.sub(r"\s+", " ", line)
        low = line.lower().strip(" -:*_#")
        if low in NAV_WORDS:
            continue
        if re.fullmatch(r"[-*_ ]+", line):
            continue
        if line.startswith("URL Source:") or line.startswith("Published Time:"):
            continue
        if sum(token in low for token in ["asia-pacific", "middle east", "americas", "opinions", "documentary"]) >= 2:
            continue
        if "albanian shqip" in low or "arabic العربية" in low:
            continue
        lines.append(line)
    headings = []
    for line in lines:
        if line.startswith("#"):
            heading = re.sub(r"^#+\s*", "", line).strip()
            if heading and heading not in headings:
                headings.append(heading)
    captured = "\n\n".join(lines).strip()
    if mode == "full":
        limit = 80000
        heading_label = "## Captured Full Text"
    elif mode in {"index", "catalog"}:
        limit = 16000
        heading_label = "## Captured Catalog Entry" if mode == "catalog" else "## Captured Index"
    else:
        limit = 16000
        heading_label = "## Captured Long Extract"
    truncated = len(captured) > limit
    captured = captured[:limit].rstrip()
    if truncated:
        captured += f"\n\n[Truncated after {limit} characters to keep the repo readable.]"
        if mode == "full":
            heading_label = "## Captured Long Extract"
    return heading_label, captured, headings[:20]


def build_markdown(args, fetched: dict) -> str:
    notices = source_notice_lines(fetched["text"])
    notices = list(dict.fromkeys(notices))
    mode = choose_mode(args.source_type, args.url)
    if mode == "full" and fetched.get("extraction_notes"):
        mode = "extract"
    heading_label, captured, headings = clean_markdown(fetched["text"], mode)
    body = "\n".join(line for line in captured.splitlines()
                     if not line.lstrip().startswith("#")
                     and not STANDALONE_NOTICE_RE.search(line.strip(" \t>*_#-")))
    if not re.search(r"\w", body):
        raise ValueError("The source returned no usable captured text")
    if mode == "full" and heading_label == "## Captured Long Extract":
        mode = "extract"
    capture_method = {
        "full": "auto_capture_fulltext", "extract": "auto_capture_long_extract",
        "index": "auto_capture_index", "catalog": "auto_capture_catalog_entry",
    }[mode]
    metadata = {
        "title": args.title,
        "author": args.author,
        "date": args.date,
        "url": args.url,
        "source_type": args.source_type,
        "capture_method": capture_method,
        "language": args.language,
        "rights_note": args.rights_note,
        "captured_at": TODAY,
    }
    frontmatter = "---\n" + "\n".join(f"{key}: {yaml_quote(value)}" for key, value in metadata.items()) + "\n---\n\n"
    sections = [
        f"# {args.title}",
        "## Source Metadata\n"
        f"- Author: {args.author}\n"
        f"- Date: {args.date}\n"
        f"- URL: {args.url}\n"
        f"- Source type: `{args.source_type}`\n"
        f"- Capture method: `{capture_method}`\n"
        f"- Language: `{args.language}`\n"
        f"- Rights note: {args.rights_note}",
        heading_label + "\n\n" + captured,
    ]
    if headings:
        sections.append("## Extracted Headings\n" + "\n".join(f"- {heading}" for heading in headings))
    sections.append(
        "## Traceability\n"
        f"- Original URL: {args.url}\n"
        f"- Final URL: {fetched.get('final_url', args.url)}\n"
        f"- HTTP status: {fetched.get('status', '')}\n"
        f"- Content type: {fetched.get('content_type', '')}\n"
        f"- Capture mode: `{mode}`\n"
        f"- Captured at: {TODAY}"
    )
    if fetched.get("extraction_notes"):
        sections[-1] += "\n- Extraction limitations:\n" + "\n".join(
            f"  - {note}" for note in fetched["extraction_notes"]
        )
    if notices:
        sections[-1] += "\n- Preserved source notices (original text):\n" + "\n".join(
            f"  - {notice}" for notice in notices
        )
    if fetched.get("footer_texts"):
        sections[-1] += "\n- Preserved source footer text (original text):\n" + "\n".join(
            f"  - {text}" for text in fetched["footer_texts"]
        )
    return frontmatter + "\n\n".join(sections).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("output")
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", default="Unknown")
    parser.add_argument("--date", default="Unknown")
    parser.add_argument("--source-type", default="article")
    parser.add_argument(
        "--language", required=True, metavar="TAG",
        help="Original source language metadata (e.g. en, zh-CN, or und if unknown); "
             "does not translate content or change the CLI language",
    )
    parser.add_argument("--rights-note", default="Metadata + cleaned capture")
    args = parser.parse_args()
    args.language = args.language.strip()
    if not args.language:
        parser.error("--language must name the original source language, or und if unknown")

    fetched = fetch_url(args.url)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_markdown(args, fetched), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
