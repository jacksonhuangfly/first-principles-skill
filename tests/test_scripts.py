"""Offline regression tests for the repository's maintenance scripts.

Run: python3 -m unittest discover -s tests -v
No network requests or yt-dlp installation required. Core tests use the standard
library; HTML extraction integration tests run when BeautifulSoup is present.
"""
from __future__ import annotations

import json
from contextlib import redirect_stderr
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import capture_web_source as capture
import check_links
import check_research_repetition as repetition
import check_sources_inventory as inventory
import srt_to_transcript as subtitles


def run_script(name, *args, cwd=None, env=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / name), *map(str, args)],
        cwd=cwd, env=env, text=True, capture_output=True,
    )


class TemporaryFiles(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def write(self, name, text):
        path = self.folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


class LinkTests(TemporaryFiles):
    def test_fragments_titles_encoded_and_parenthesized_paths(self):
        for name in ("doc.md", "space name.md", "report(v2).md"):
            self.write(name, "# Section")
        doc = self.write("README.md", """
[a](doc.md#section) [b](doc.md "Title") [c](<space name.md> 'Title')
[d](space%20name.md) [e](report(v2).md) [f](report\\(v2\\).md)
[g](https://example.com) [h](mailto:person@example.com) [i](#local)
""")
        self.assertEqual(check_links.check_file(doc), [])

    def test_reference_links_and_images_are_checked(self):
        self.write("exists.md", "text")
        doc = self.write("README.md", """
[ok][good] [bad][missing] ![image](missing.png)
[good]: <exists.md> "Title"
[missing]: absent.md#section
""")
        self.assertEqual(set(check_links.check_file(doc)), {"absent.md#section", "missing.png"})

    def test_code_and_comments_are_ignored(self):
        doc = self.write("README.md", """
`[example](absent.md)`
```md
[example](absent.md)
```
<!-- [hidden](absent.md) -->
""")
        self.assertEqual(check_links.check_file(doc), [])

    def test_multiline_inline_code_is_ignored(self):
        doc = self.write("README.md", "Text with `inline code\n[example](not-a-file.md)\n` continues.")
        self.assertEqual(check_links.check_file(doc), [])

    def test_all_markdown_including_chinese_readme_and_references(self):
        self.write("README.md", "# English")
        chinese = self.write("README.zh-CN.md", "[broken](absent.md)")
        result = run_script("check_links.py", self.folder)
        self.assertEqual(result.returncode, 1)
        self.assertIn(chinese.name, result.stdout)
        chinese.write_text("# 中文", encoding="utf-8")
        self.write("references/topic.md", "[broken](missing.md)")
        result = run_script("check_links.py", self.folder)
        self.assertEqual(result.returncode, 1)
        self.assertIn("topic.md", result.stdout)

    def test_missing_or_empty_input_fails(self):
        for target in (self.folder / "absent", self.folder):
            with self.subTest(target=target):
                self.assertNotEqual(run_script("check_links.py", target).returncode, 0)


class SourceTests(TemporaryFiles):
    def card(self, name="a.md", *, body="Captured prose.", kind="article",
             label="Long Extract", url="https://example.com/a", language="en", omit=()):
        fields = {"url": url, "author": "Unknown", "date": "Unknown",
                  "captured_at": "2026-10-08", "source_type": kind, "language": language}
        frontmatter = "\n".join(f"{key}: {json.dumps(value)}"
                                for key, value in fields.items() if key not in omit)
        return self.write("references/sources/articles/" + name,
                          f"---\n{frontmatter}\n---\n\n## Captured {label}\n\n{body}\n")

    def test_relative_repo_and_arbitrary_directory_name(self):
        self.card()
        for args in ((), (".",)):
            with self.subTest(args=args):
                result = run_script("check_sources_inventory.py", *args, cwd=self.folder)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("1 source cards", result.stdout)

    def test_empty_heading_and_metadata_do_not_pass(self):
        for body in ("", "<!-- pending capture -->", "### Heading only"):
            with self.subTest(body=body):
                path = self.card(body=body)
                self.assertIn("missing nonempty Captured section", inventory.inspect_card(path)[2])
        path = self.card(omit=("author",))
        self.assertIn("missing metadata: author", inventory.inspect_card(path)[2])

    def test_catalog_and_index_are_counted_separately(self):
        self.card("content.md")
        self.card("catalog.md", kind="bibliographic_catalog_entry",
                  label="Catalog Entry", url="https://example.com/book")
        self.card("index.md", kind="lecture_index", label="Index",
                  url="https://example.com/lectures")
        result = run_script("check_sources_inventory.py", self.folder)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("articles: files=3 content=1 index=2", result.stdout)

    def test_source_language_is_required_but_unknown_is_allowed(self):
        for kwargs in ({"omit": ("language",)}, {"language": ""}, {"language": "   "}):
            with self.subTest(kwargs=kwargs):
                self.assertIn("missing metadata: language", inventory.inspect_card(self.card(**kwargs))[2])
        self.assertEqual(inventory.inspect_card(self.card(language="und"))[2], [])

    def test_source_h2_headings_do_not_hide_captured_body(self):
        path = self.card(body="# An article\n\n## Introduction\n\nRetained evidence.\n\n## Traceability\n- URL")
        self.assertEqual(inventory.inspect_card(path)[2], [])
        self.assertEqual(inventory.capture_sections(path.read_text())[0][1], "Retained evidence.")

    def test_traceability_does_not_count_as_captured_body(self):
        path = self.card(body="# Article title only\n\n## Traceability\n- Original URL: https://example.com")
        self.assertIn("missing nonempty Captured section", inventory.inspect_card(path)[2])

    def test_distillation_note_is_not_captured_source_text(self):
        path = self.card(body="# Article title only\n\n## Distillation Note\nEditorial interpretation, not retained source prose.")
        self.assertIn("missing nonempty Captured section", inventory.inspect_card(path)[2])

    def test_index_cannot_claim_full_text(self):
        path = self.card(kind="lecture_index", label="Full Text")
        self.assertTrue(any("not Captured Full Text" in error
                            for error in inventory.inspect_card(path)[2]))

    def test_duplicate_source_urls_report_both_cards(self):
        self.card("first.md", url="https://EXAMPLE.com:443/a/#first")
        self.card("second.md", url="https://example.com/a#second")
        result = run_script("check_sources_inventory.py", self.folder)
        self.assertEqual(result.returncode, 1)
        for token in ("duplicate source URL", "first.md", "second.md"):
            self.assertIn(token, result.stdout)

    def test_missing_source_tree_fails(self):
        self.assertNotEqual(run_script("check_sources_inventory.py", self.folder).returncode, 0)


class CaptureTests(TemporaryFiles):
    def args(self, source_type="article"):
        return SimpleNamespace(source_type=source_type, url="https://example.com/article",
                               title="Test", author="Unknown", date="Unknown",
                               language="en", rights_note="Test")

    def test_jina_preserves_original_protocol(self):
        response = SimpleNamespace(text="URL Source: https://example.com/article\nMarkdown Content:\nText",
                                   status_code=200, headers={})
        with patch.object(capture, "request_url", return_value=response) as request:
            result = capture.fetch_via_jina("https://example.com/article")
        request.assert_called_once_with("https://r.jina.ai/https://example.com/article")
        self.assertEqual(result["text"], "Text")

    def test_reader_failure_falls_back_to_direct_html(self):
        with patch.object(capture, "fetch_via_jina", side_effect=OSError("offline")), \
                patch.object(capture, "fetch_direct_html", return_value={"text": "fallback"}) as direct:
            self.assertEqual(capture.fetch_url("https://example.com"), {"text": "fallback"})
        direct.assert_called_once_with("https://example.com")

    def test_pdf_query_is_not_treated_as_html(self):
        url = "https://example.com/paper.PDF?download=1#page=2"
        with patch.object(capture, "fetch_pdf", return_value={"text": "PDF"}) as pdf:
            self.assertEqual(capture.fetch_url(url)["text"], "PDF")
        pdf.assert_called_once_with(url)

    def test_index_and_catalog_capture_labels(self):
        for source_type, label, method in (
            ("lecture_index", "Captured Index", "auto_capture_index"),
            ("bibliographic_catalog_entry", "Captured Catalog Entry", "auto_capture_catalog_entry"),
        ):
            with self.subTest(source_type=source_type):
                result = capture.build_markdown(self.args(source_type), {"text": "Source listing."})
                self.assertIn("## " + label, result)
                self.assertIn(method, result)
                self.assertNotIn("Captured Full Text", result)

    def test_truncated_full_text_is_labeled_extract(self):
        result = capture.build_markdown(self.args("public_domain_book"), {"text": "x" * 80001})
        self.assertIn("## Captured Long Extract", result)
        self.assertIn('capture_method: "auto_capture_long_extract"', result)
        self.assertIn("Truncated after 80000", result)
        self.assertNotIn("Captured Full Text", result)

    def test_short_preface_and_premises_survive_full_capture(self):
        original = ["# Essay", "Premise one is necessary.", "Premise two fixes the boundary.",
                    "Premise three defines the terms.", "Premise four excludes an alternative.",
                    "All assumptions above must hold.",
                    "This later paragraph is longer than eighty characters and explains how all earlier premises determine the conclusion.",
                    "An implication follows.", "A qualification follows.", "The conclusion follows."]
        result = capture.build_markdown(self.args("public_domain_book"), {"text": "\n".join(original)})
        body = inventory.capture_sections(result)[0][1]
        for premise in original[1:]:
            self.assertIn(premise, body)
        self.assertIn("## Captured Full Text", result)
        self.assertIn('capture_method: "auto_capture_fulltext"', result)

    def test_repeated_source_answers_are_not_deleted(self):
        answer = "Yes, the premise is correct."
        text = f"# Interview\nQuestion one?\n{answer}\nQuestion two?\n{answer}\nEnd of interview."
        for mode in ("full", "extract"):
            with self.subTest(mode=mode):
                _, cleaned, _ = capture.clean_markdown(text, mode)
                self.assertEqual(cleaned.count(answer), 2)

    def test_markdown_links_preserve_labels_and_surrounding_punctuation(self):
        for original, expected in (
            ("Read [Psychological Types](https://example.com/Types_(book)).", "Read Psychological Types."),
            ("[A [nested] label](https://example.com/a)", "A [nested] label"),
            ('[Book](<https://example.com/a (book)> "A title)")!', "Book!"),
            (r"[Book](https://example.com/a\(book\))!", "Book!"),
            ("![Chart](https://example.com/chart_(1).png) Evidence.", " Evidence."),
            ("[Unfinished](https://example.com/a_(book)", "[Unfinished](https://example.com/a_(book)"),
        ):
            with self.subTest(original=original):
                self.assertEqual(capture.md_link_text(original), expected)

    def test_direct_html_preserves_each_text_node_once_in_source_order(self):
        try:
            import bs4  # noqa: F401 - optional integration dependency
        except ImportError:
            self.skipTest("BeautifulSoup is an optional capture dependency")
        html = ("<main><p>Outside the single article.</p>"
                "<article><h5>Subsection</h5><blockquote><p>Quoted evidence.</p></blockquote>"
                "<ul><li>First item<ul><li>Nested item.</li></ul>After nested item.</li></ul>"
                "<div>This <em>source</em> paragraph uses a div.<br>Second line.</div>"
                "<p>psycho<span>logical</span></p><!-- Hidden comment. --></article></main>")
        response = SimpleNamespace(text=html, status_code=200, headers={}, url="https://example.com",
                                   apparent_encoding="utf-8", encoding="utf-8")
        with patch.object(capture, "request_url", return_value=response):
            fetched = capture.fetch_direct_html(response.url)
        self.assertEqual(fetched["text"].splitlines(), [
            "##### Subsection", "Quoted evidence.", "First item", "Nested item.",
            "After nested item.", "This source paragraph uses a div.", "Second line.", "psychological",
        ])
        result = capture.build_markdown(self.args("public_domain_book"), fetched)
        self.assertIn("This source paragraph uses a div.", result)
        self.assertEqual(result.count("Quoted evidence."), 1)

    def test_direct_html_keeps_all_content_articles(self):
        try:
            import bs4  # noqa: F401 - optional integration dependency
        except ImportError:
            self.skipTest("BeautifulSoup is an optional capture dependency")
        articles = ("<article><h2>Chapter one</h2><p>First evidence.</p></article>"
                    "<article><h2>Chapter two</h2><p>Second evidence.</p></article>")
        for html in (
            f"<main>{articles}</main>",
            f"<body>{articles}</body>",
            f"<body><p>Outside the article collection.</p><section>{articles}</section></body>",
        ):
            with self.subTest(html=html):
                response = SimpleNamespace(text=html, status_code=200, headers={}, url="https://example.com",
                                           apparent_encoding="utf-8", encoding="utf-8")
                with patch.object(capture, "request_url", return_value=response):
                    fetched = capture.fetch_direct_html(response.url)
                self.assertEqual(fetched["text"].splitlines(), [
                    "## Chapter one", "First evidence.", "## Chapter two", "Second evidence.",
                ])
                result = capture.build_markdown(self.args("public_domain_book"), fetched)
                body = inventory.capture_sections(result)[0][1]
                self.assertIn("First evidence.", body)
                self.assertIn("Second evidence.", body)

    def test_direct_html_retains_footer_attribution_outside_article(self):
        try:
            import bs4  # noqa: F401 - optional integration dependency
        except ImportError:
            self.skipTest("BeautifulSoup is an optional capture dependency")
        notice = "Copyright © 2026 Example Institute. All rights reserved."
        for prose in ("Retained article prose.", "Evidence paragraph. " * 1000):
            with self.subTest(length=len(prose)):
                html = f"<html><head><title>Evidence</title></head><body><article><h1>Evidence</h1><p>{prose}</p></article><footer><p>{notice}</p></footer></body></html>"
                response = SimpleNamespace(text=html, status_code=200, headers={"content-type": "text/html"},
                                           url="https://example.com", apparent_encoding="utf-8", encoding="utf-8")
                with patch.object(capture, "request_url", return_value=response):
                    fetched = capture.fetch_direct_html("https://example.com")
                result = capture.build_markdown(self.args(), fetched)
                body = inventory.capture_sections(result)[0][1]
                self.assertIn(prose[:20], body)
                self.assertIn(notice, result)
                self.assertNotIn(notice, body)
                self.assertEqual(fetched["footer_texts"], [notice])
                if len(prose) > 16000:
                    self.assertIn("Truncated after 16000", result)

    def test_html_license_footer_survives_long_body_without_notice_keywords(self):
        try:
            import bs4  # noqa: F401 - optional integration dependency
        except ImportError:
            self.skipTest("BeautifulSoup is an optional capture dependency")
        notice = "Licensed under CC BY 4.0."
        html = "<article><p>" + "Evidence paragraph. " * 1000 + "</p></article><footer>" + notice + "</footer>"
        response = SimpleNamespace(text=html, status_code=200, headers={}, url="https://example.com",
                                   apparent_encoding="utf-8", encoding="utf-8")
        with patch.object(capture, "request_url", return_value=response):
            fetched = capture.fetch_direct_html(response.url)
        result = capture.build_markdown(self.args(), fetched)
        self.assertIn(notice, result)
        self.assertIn("Truncated after 16000", result)
        self.assertNotIn(notice, inventory.capture_sections(result)[0][1])

    def test_html_title_and_footer_alone_do_not_count_as_source_body(self):
        try:
            import bs4  # noqa: F401 - optional integration dependency
        except ImportError:
            self.skipTest("BeautifulSoup is an optional capture dependency")
        for html in (
            "<html><head><title>Evidence</title></head><body><h1>Evidence</h1><footer>Copyright © 2026 Example. All rights reserved.</footer></body></html>",
            "<!doctype html><title>Evidence</title><footer>Copyright © 2026 Example. All rights reserved.</footer>",
        ):
            with self.subTest(html=html):
                response = SimpleNamespace(text=html, status_code=200, headers={}, url="https://example.com",
                                           apparent_encoding="utf-8", encoding="utf-8")
                with patch.object(capture, "request_url", return_value=response):
                    fetched = capture.fetch_direct_html(response.url)
                with self.assertRaisesRegex(ValueError, "no usable"):
                    capture.build_markdown(self.args(), fetched)

    def test_notices_in_raw_text_survive_body_limits_without_changing_rights_note(self):
        for source_type, length, notice in (
            ("article", 17000, "Copyright 2026 Example Institute."),
            ("public_domain_book", 81000, "© 2026 Example Institute. All rights reserved."),
        ):
            with self.subTest(source_type=source_type):
                args = self.args(source_type)
                args.rights_note = "Retain the supplied rights statement."
                result = capture.build_markdown(args, {"text": "x" * length + "\n" + notice})
                self.assertIn(notice, result)
                self.assertNotIn(notice, inventory.capture_sections(result)[0][1])
                self.assertEqual(inventory.metadata(result)["rights_note"], args.rights_note)

    def test_notice_only_text_is_not_a_source_body(self):
        with self.assertRaisesRegex(ValueError, "no usable"):
            capture.build_markdown(self.args(), {"text": "# Title\nCopyright 2026 Example. All rights reserved."})

    def test_prose_discussing_copyright_is_not_rejected_as_a_notice(self):
        for prose in ("Copyright changes the economics of distributing creative work.",
                      "All rights reserved is a phrase discussed in this analysis."):
            with self.subTest(prose=prose):
                result = capture.build_markdown(self.args(), {"text": prose})
                self.assertIn(prose, inventory.capture_sections(result)[0][1])

    def test_partial_pdf_extraction_is_disclosed_and_labeled_extract(self):
        def unreadable():
            raise ValueError("unreadable page")
        pages = [SimpleNamespace(extract_text=lambda: "Retained first page."),
                 SimpleNamespace(extract_text=unreadable),
                 SimpleNamespace(extract_text=lambda: "")]
        response = SimpleNamespace(content=b"mock-pdf", status_code=200,
                                   url="https://example.com/book.pdf", headers={})
        fake_pdf = SimpleNamespace(PdfReader=lambda stream: SimpleNamespace(pages=pages))
        with patch.dict(sys.modules, {"pypdf": fake_pdf}), patch.object(capture, "request_url", return_value=response):
            fetched = capture.fetch_pdf(response.url)
        result = capture.build_markdown(self.args("public_domain_book"), fetched)
        self.assertIn("Retained first page.", result)
        self.assertIn("## Captured Long Extract", result)
        self.assertIn('capture_method: "auto_capture_long_extract"', result)
        self.assertNotIn("Captured Full Text", result)
        self.assertIn("Page 2: text extraction failed", result)
        self.assertIn("Page 3: no extractable text", result)

    def test_pdf_with_no_extractable_pages_is_rejected(self):
        fake_pdf = SimpleNamespace(PdfReader=lambda stream: SimpleNamespace(
            pages=[SimpleNamespace(extract_text=lambda: "")]))
        response = SimpleNamespace(content=b"mock-pdf", status_code=200,
                                   url="https://example.com/book.pdf", headers={})
        with patch.dict(sys.modules, {"pypdf": fake_pdf}), patch.object(capture, "request_url", return_value=response):
            fetched = capture.fetch_pdf(response.url)
        with self.assertRaisesRegex(ValueError, "no usable"):
            capture.build_markdown(self.args("public_domain_book"), fetched)

    def test_empty_capture_is_rejected(self):
        for text in ("Home\n\n---", "# Article title only\n\n## Heading only"):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "no usable"):
                capture.build_markdown(self.args(), {"text": text})

    def test_metadata_newlines_are_escaped(self):
        value = 'line one\nline "two" \\ end'
        self.assertEqual(json.loads(capture.yaml_quote(value)), value)
        self.assertNotIn("\n", capture.yaml_quote(value))

    def test_cli_requires_source_language_before_fetching(self):
        output = self.folder / "capture.md"
        arguments = ["capture_web_source.py", "https://example.com", str(output), "--title", "Test"]
        stderr = io.StringIO()
        with patch.object(sys, "argv", arguments), patch.object(capture, "fetch_url") as fetch, \
                redirect_stderr(stderr), self.assertRaises(SystemExit) as error:
            capture.main()
        self.assertEqual(error.exception.code, 2)
        self.assertIn("--language", stderr.getvalue())
        fetch.assert_not_called()
        self.assertFalse(output.exists())

    def test_cli_rejects_empty_source_language_before_fetching(self):
        output = self.folder / "capture.md"
        for language in ("", " \t "):
            with self.subTest(language=language):
                arguments = ["capture_web_source.py", "https://example.com", str(output),
                             "--title", "Test", "--language", language]
                stderr = io.StringIO()
                with patch.object(sys, "argv", arguments), patch.object(capture, "fetch_url") as fetch, \
                        redirect_stderr(stderr), self.assertRaises(SystemExit) as error:
                    capture.main()
                self.assertEqual(error.exception.code, 2)
                self.assertIn("--language", stderr.getvalue())
                fetch.assert_not_called()
                self.assertFalse(output.exists())

    def test_cli_preserves_explicit_source_language_and_original_text(self):
        for language, original in (
            ("en", "The original evidence remains in English."),
            ("zh-CN", "原始证据保持简体中文，不自动翻译。"),
            ("fr", "Les preuves originales restent en français."),
            ("und", "Original source text with unknown language."),
        ):
            with self.subTest(language=language):
                output = self.folder / f"{language}.md"
                arguments = ["capture_web_source.py", "https://example.com", str(output),
                             "--title", "Test", "--language", language]
                with patch.object(sys, "argv", arguments), \
                        patch.object(capture, "fetch_url", return_value={"text": original}):
                    self.assertEqual(capture.main(), 0)
                text = output.read_text(encoding="utf-8")
                self.assertEqual(inventory.metadata(text)["language"], language)
                self.assertIn(original, text)

    def test_help_distinguishes_metadata_from_translation(self):
        result = run_script("capture_web_source.py", "--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Original source language metadata", result.stdout)
        self.assertIn("und if unknown", result.stdout)
        self.assertIn("does not translate", result.stdout)

    def test_chinese_navigation_filter_remains_available(self):
        _, captured, _ = capture.clean_markdown("首页\n打开app\n原始证据仍然保留。", "extract")
        self.assertEqual(captured, "原始证据仍然保留。")


class TranscriptTests(TemporaryFiles):
    def test_short_vtt_timestamps_and_cue_ids(self):
        text = "WEBVTT\n\ncue-id\n00:01.000 --> 00:03.000 align:start position:0%\nHello world.\n"
        self.assertEqual(subtitles.clean_vtt(text), "Hello world.")

    def test_note_style_region_blocks_but_not_note_dialogue(self):
        text = """WEBVTT

NOTE metadata
not dialogue

STYLE
::cue { color: red; }

REGION
id:region1

00:01.000 --> 00:02.000
Take NOTE of this.

00:03.000 --> 00:04.000
Next.
"""
        self.assertEqual(subtitles.clean_vtt(text), "Take NOTE of this.\n\nNext.")

    def test_numeric_dialogue_entities_markup_and_crlf(self):
        text = "\ufeff1\r\n00:00:01,000 --> 00:00:02,000\r\n2024\r\n\r\n2\r\n00:00:03,000 --> 00:00:04,000\r\n<b>A &amp; B.</b>\r\n"
        self.assertEqual(subtitles.clean_srt(text), "2024 A & B.")

    def test_duplicate_cues_and_inline_timestamps(self):
        text = """WEBVTT

00:01.000 --> 00:02.000
<v Speaker>Hello <00:01.200>world.

00:02.000 --> 00:03.000
<v Speaker>Hello <00:02.200>world.
"""
        self.assertEqual(subtitles.clean_vtt(text), "Hello world.")

    def test_cli_paragraph_count_and_invalid_input(self):
        source = self.write("sample.srt", "1\n00:00:01,000 --> 00:00:02,000\nFirst.\n\n2\n00:00:03,000 --> 00:00:04,000\nSecond.\n")
        result = run_script("srt_to_transcript.py", source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("paragraphs: 2", result.stdout)
        self.assertTrue((self.folder / "sample_transcript.txt").is_file())
        empty = self.write("empty.vtt", "WEBVTT\n\n")
        self.assertNotEqual(run_script("srt_to_transcript.py", empty).returncode, 0)


class RepetitionTests(TemporaryFiles):
    PARAGRAPH = ("A decision needs a measurable outcome and an explicit constraint. "
                 "This paragraph has enough substantive text to exercise duplicate "
                 "detection without relying on repeated headings or shared citations.")

    def test_repeated_paragraphs_with_blank_lines(self):
        path = self.write("a.md", f"# Topic\n\n{self.PARAGRAPH}\n\nDifferent paragraph.\n\n{self.PARAGRAPH}\n")
        self.assertTrue(repetition.scan(path))

    def test_duplicates_across_files(self):
        first = self.write("a.md", "# First\n\n" + self.PARAGRAPH)
        second = self.write("b.md", "# Second\n\n" + self.PARAGRAPH)
        duplicates = repetition.scan_files([first, second])
        self.assertTrue(duplicates)
        self.assertEqual({path for locations in duplicates.values() for path, _ in locations},
                         {first, second})

    def test_shared_frontmatter_headings_links_and_code_are_ignored(self):
        text = ('---\ntitle: ' + self.PARAGRAPH + '\n---\n# Common heading\n\n'
                + '- [Shared long source label](https://example.com/source)\n'
                + '- [Another source](../sources/book.md)\n'
                + '\n```text\n' + self.PARAGRAPH + '\n```\n')
        files = [self.write("a.md", text), self.write("b.md", text)]
        self.assertEqual(repetition.scan_files(files), {})

    def test_three_line_span_across_paragraph_boundaries(self):
        a = "The first long line supplies an observable outcome for a product decision."
        b = "The second long line spells out assumptions that could change the result."
        c = "The third long line proposes a cheap experiment before making a commitment."
        first = self.write("a.md", "\n\n".join((a, b, c)))
        second = self.write("b.md", "\n".join((a, b, c)) + "\nA unique continuation.")
        self.assertTrue(repetition.scan_files([first, second]))

    def test_missing_or_empty_input_fails(self):
        for target in (self.folder / "absent", self.folder):
            with self.subTest(target=target):
                self.assertNotEqual(run_script("check_research_repetition.py", target).returncode, 0)


class DownloaderTests(TemporaryFiles):
    def setUp(self):
        super().setUp()
        self.output = self.folder / "output"
        self.output.mkdir()
        self.bin = self.folder / "bin"
        self.bin.mkdir()
        fake = self.bin / "yt-dlp"
        fake.write_text("#!" + sys.executable + """
import json, os, pathlib, re, sys
args = sys.argv[1:]
with open(os.environ["FAKE_LOG"], "a") as log:
    log.write(json.dumps(args) + "\\n")
languages = args[args.index("--sub-langs") + 1].split(",")
kind = "automatic" if "--write-auto-subs" in args else "manual"
tracks = json.loads(os.environ["FAKE_TRACKS"]).get(kind, [])
for language in tracks:
    if any(re.fullmatch(pattern, language) for pattern in languages):
        template = pathlib.Path(args[args.index("-o") + 1])
        (template.parent / ("video123." + language + ".vtt")).write_text("Current video captions.")
sys.exit(0)
""", encoding="utf-8")
        fake.chmod(0o755)
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ["PATH"],
                        FAKE_LOG=str(self.folder / "calls.jsonl"),
                        FAKE_TRACKS=json.dumps({"manual": ["en", "zh-Hans"]}))

    def invoke(self, *args):
        return subprocess.run(["bash", str(ROOT / "scripts/download_subtitles.sh"), *args],
                              cwd=self.folder, env=self.env, text=True, capture_output=True)

    def run_download(self, *options):
        return self.invoke("https://example.com/video", str(self.output), *options)

    def calls(self):
        return [json.loads(line) for line in (self.folder / "calls.jsonl").read_text().splitlines()]

    def assert_requested_languages(self, expected):
        for call in self.calls():
            self.assertIn("--ignore-config", call)
            self.assertEqual(set(call[call.index("--sub-langs") + 1].split(",")), set(expected))

    def test_default_download_uses_manual_english_and_stops(self):
        result = self.run_download()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.output / "video123.en.vtt").is_file())
        self.assertFalse((self.output / "video123.zh-Hans.vtt").exists())
        self.assertEqual(len(self.calls()), 1)
        self.assertIn("--write-subs", self.calls()[0])
        self.assert_requested_languages({"en(?:-.*)?"})
        self.assertFalse(Path(self.calls()[0][self.calls()[0].index("-o") + 1]).parent.exists())

    def test_legacy_url_only_usage_saves_english_to_current_directory(self):
        result = self.invoke("https://example.com/video")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.folder / "video123.en.vtt").is_file())
        self.assert_requested_languages({"en(?:-.*)?"})

    def test_unrelated_old_file_never_counts_as_success(self):
        stale = self.output / "unrelated.en.srt"
        stale.write_text("Old video.")
        os.utime(stale, (1000000000, 1000000000))
        self.env["FAKE_TRACKS"] = "{}"
        result = self.run_download()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Downloaded:", result.stdout)
        self.assertEqual(stale.read_text(), "Old video.")
        self.assertIn("selected language: en", result.stderr)

    def test_automatic_english_fallback_ignores_manual_chinese(self):
        self.env["FAKE_TRACKS"] = json.dumps({"manual": ["zh-Hans"], "automatic": ["en"]})
        result = self.run_download()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.output / "video123.en.vtt").is_file())
        self.assertFalse((self.output / "video123.zh-Hans.vtt").exists())
        self.assertEqual(len(self.calls()), 2)
        self.assertIn("--write-subs", self.calls()[0])
        self.assertIn("--write-auto-subs", self.calls()[1])
        self.assertIn("srt/vtt", self.calls()[1])
        self.assert_requested_languages({"en(?:-.*)?"})

    def test_explicit_simplified_chinese_option_before_or_after_positionals(self):
        self.env["FAKE_TRACKS"] = json.dumps({"manual": ["en", "zh-Hans", "zh-Hant", "zh"]})
        for args in (
            ("--language", "zh-CN", "https://example.com/video", str(self.output)),
            ("https://example.com/video", str(self.output), "--language", "zh-CN"),
            ("https://example.com/video", "--language=zh-CN", str(self.output)),
        ):
            with self.subTest(args=args):
                result = self.invoke(*args)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue((self.output / "video123.zh-Hans.vtt").is_file())
                self.assertFalse((self.output / "video123.en.vtt").exists())
                self.assert_requested_languages({"zh-Hans(?:-.*)?", "zh-CN(?:-.*)?"})

    def test_automatic_simplified_chinese_stays_in_selected_language(self):
        self.env["FAKE_TRACKS"] = json.dumps({"manual": ["en", "zh-Hant"], "automatic": ["zh-CN", "en"]})
        result = self.run_download("--language", "zh-CN")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(self.calls()), 2)
        self.assertIn("--write-auto-subs", self.calls()[1])
        self.assert_requested_languages({"zh-Hans(?:-.*)?", "zh-CN(?:-.*)?"})
        self.assertTrue((self.output / "video123.zh-CN.vtt").is_file())
        self.assertFalse((self.output / "video123.en.vtt").exists())

    def test_no_fallback_to_unselected_languages_or_traditional_chinese(self):
        for language, available, expected in (
            ("en", ["zh-Hans"], {"en(?:-.*)?"}),
            ("zh-CN", ["en"], {"zh-Hans(?:-.*)?", "zh-CN(?:-.*)?"}),
            ("zh-CN", ["zh-Hant", "zh-TW", "zh-HK", "zh"], {"zh-Hans(?:-.*)?", "zh-CN(?:-.*)?"}),
        ):
            with self.subTest(language=language, available=available):
                (self.folder / "calls.jsonl").unlink(missing_ok=True)
                self.env["FAKE_TRACKS"] = json.dumps({"manual": available, "automatic": available})
                result = self.run_download("--language", language)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Downloaded:", result.stdout)
                self.assertEqual(len(self.calls()), 2)
                self.assert_requested_languages(expected)
                self.assertIn(f"selected language: {language}", result.stderr)

    def test_explicit_english_and_simplified_chinese_variants(self):
        for language, track in (("en", "en-CA"), ("zh-CN", "zh-Hans-CN"), ("zh-CN", "zh-CN-x-test")):
            with self.subTest(language=language, track=track):
                self.env["FAKE_TRACKS"] = json.dumps({"manual": [track]})
                result = self.run_download("--language", language)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue((self.output / f"video123.{track}.vtt").is_file())

    def test_help_and_invalid_arguments_do_not_invoke_downloader(self):
        result = self.invoke("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Default language: en", result.stdout)
        for args in (
            (), ("--language",), ("--language", "--help"),
            ("--language", "zh-Hant", "https://example.com/video"),
            ("--language=", "https://example.com/video"),
            ("--unknown", "https://example.com/video"),
            ("https://example.com/video", str(self.output), "extra"),
        ):
            with self.subTest(args=args):
                result = self.invoke(*args)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertFalse((self.folder / "calls.jsonl").exists())

    def test_copy_failure_is_not_reported_as_success(self):
        fake_cp = self.bin / "cp"
        fake_cp.write_text("#!/bin/bash\nexit 1\n")
        fake_cp.chmod(0o755)
        result = self.run_download()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Downloaded:", result.stdout)
        self.assertIn("could not save", result.stderr)


if __name__ == "__main__":
    unittest.main()
