#!/usr/bin/env python3
"""
Convert HTML assignment files in "Canvas Export" to Markdown.

This script performs a lightweight HTML→Markdown conversion without external
dependencies. It handles common tags used in Canvas exports:
  - Headings <h1>.. <h6>
  - Paragraphs <p>, line breaks <br>, horizontal rules <hr>
  - Emphasis <strong>/<b>, <em>/<i>
  - Inline code <code> and code blocks <pre> (with optional nested <code>)
  - Lists <ul>/<ol>/<li>
  - Links <a href="...">text</a>
  - Images <img alt src>

Usage:
  python scripts/convert_canvas_export_html_to_md.py [--force]

By default, it will skip writing a .md file if it already exists next to the
source .html. Use --force to overwrite existing .md files.
"""

from __future__ import annotations

import os
import sys
from html.parser import HTMLParser
from typing import List, Dict, Optional


class MarkdownConverter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)  # we handle char refs ourselves
        self._buffers: List[List[str]] = [[]]  # stack of output buffers; top is current
        self._list_stack: List[Dict[str, object]] = []  # track nested lists
        self._link_stack: List[Dict[str, Optional[str]]] = []
        self._in_pre: bool = False
        self._in_inline_code: bool = False
        self._pending_heading_level: Optional[int] = None
        self._in_li: bool = False
        self._no_space_before = ('(', '[', '{', '"', "'")
        self._in_head: bool = False
        self._in_title: bool = False

    # Utilities
    def _buf(self) -> List[str]:
        return self._buffers[-1]

    def _write(self, s: str) -> None:
        self._buf().append(s)

    def _text(self) -> str:
        return "".join(self._buf())

    def _ensure_newline(self) -> None:
        buf = self._buf()
        if not buf:
            return
        if not buf[-1].endswith("\n"):
            buf[-1] = buf[-1] + "\n"

    def _blank_line(self) -> None:
        # Ensure a blank line separation (two newlines)
        text = self._text()
        if not text.endswith("\n\n"):
            if not text.endswith("\n"):
                self._write("\n")
            self._write("\n")

    def _prev_char(self) -> Optional[str]:
        buf = self._buf()
        if not buf:
            return None
        if not buf[-1]:
            return None
        return buf[-1][-1]

    def _space_if_needed(self) -> None:
        ch = self._prev_char()
        if ch and not ch.isspace() and ch not in self._no_space_before:
            self._write(" ")

    def _current_indent(self) -> str:
        # Two spaces per nesting level (excluding the current list item itself)
        depth = max(0, len(self._list_stack) - 1)
        return "  " * depth

    # HTMLParser overrides
    def handle_starttag(self, tag: str, attrs):
        attrs_dict = {k.lower(): v for k, v in attrs}

        if tag == "head":
            self._in_head = True
        elif tag == "title":
            self._in_title = True
        elif tag in {"p", "div", "section"}:
            # Start a new block (but not inside list items)
            if not self._in_li:
                self._blank_line()
        elif tag in {"br"}:
            self._write("\n")
        elif tag in {"hr"}:
            self._blank_line()
            self._write("---\n")
            self._blank_line()
        elif tag in {"strong", "b"}:
            self._space_if_needed()
            self._write("**")
        elif tag in {"em", "i"}:
            self._space_if_needed()
            self._write("*")
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            self._blank_line()
            self._write("#" * level + " ")
            self._pending_heading_level = level
        elif tag == "code":
            if self._in_pre:
                # code inside pre → already fenced
                pass
            else:
                self._in_inline_code = True
                self._space_if_needed()
                self._write("`")
        elif tag == "pre":
            self._blank_line()
            self._write("```\n")
            self._in_pre = True
        elif tag == "ul":
            self._blank_line()
            self._list_stack.append({"type": "ul"})
        elif tag == "ol":
            self._blank_line()
            self._list_stack.append({"type": "ol", "index": 0})
        elif tag == "li":
            # begin list item
            if not self._list_stack:
                # Treat stray li as ul item
                self._list_stack.append({"type": "ul"})
            ctx = self._list_stack[-1]
            indent = self._current_indent()
            if ctx["type"] == "ul":
                bullet = "- "
            else:
                idx = int(ctx.get("index", 0)) + 1
                ctx["index"] = idx
                bullet = f"{idx}. "
            # Ensure we’re on a new line
            self._ensure_newline()
            self._write(indent + bullet)
            self._in_li = True
        elif tag == "a":
            href = attrs_dict.get("href", "")
            self._link_stack.append({"href": href})
            # Push a new buffer to capture link text
            self._buffers.append([])
        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            self._write(f"![{alt}]({src})")
        elif tag == "blockquote":
            self._blank_line()
            # Represent blockquote by prefixing the next line
            self._write("> ")
        # Ignore other tags (span, html, head, body, etc.)

    def handle_endtag(self, tag: str):
        if tag == "head":
            self._in_head = False
        elif tag == "title":
            self._in_title = False
        elif tag in {"p", "div", "section"}:
            if self._in_li:
                # Within list items, don't add extra blank lines
                self._write("\n")
            else:
                self._write("\n")
                self._blank_line()
        elif tag in {"strong", "b"}:
            self._write("**")
        elif tag in {"em", "i"}:
            self._write("*")
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._write("\n")
            self._blank_line()
            self._pending_heading_level = None
        elif tag == "code":
            if self._in_pre:
                pass
            else:
                self._write("`")
                self._in_inline_code = False
        elif tag == "pre":
            # close fenced block
            # ensure content ends with newline before closing fence
            self._ensure_newline()
            self._write("```\n")
            self._blank_line()
            self._in_pre = False
        elif tag in {"ul", "ol"}:
            if self._list_stack:
                self._list_stack.pop()
            self._blank_line()
        elif tag == "li":
            self._write("\n")
            self._in_li = False
        elif tag == "a":
            if not self._link_stack:
                return
            link_ctx = self._link_stack.pop()
            text_buf = self._buffers.pop()  # captured link text
            link_text = "".join(text_buf).strip() or link_ctx.get("href") or ""
            href = link_ctx.get("href") or ""
            self._write(f"[{link_text}]({href})")
        elif tag == "blockquote":
            self._write("\n")
            self._blank_line()

    def handle_data(self, data: str):
        if not data:
            return
        if self._in_head or self._in_title:
            return
        if self._in_pre:
            # Preserve as-is in code blocks
            self._write(data)
        else:
            # Collapse whitespace sequences to single spaces outside code/blocks
            raw = data
            s = raw.replace("\r", " ").replace("\n", " ")
            # Avoid excessive spaces but preserve leading/trailing separation
            parts = s.split()
            if not parts:
                # whitespace-only node between tags → ignore
                return
            middle = " ".join(parts)
            leading_ws = raw[0].isspace()
            trailing_ws = raw[-1].isspace()
            out = (" " if leading_ws else "") + middle + (" " if trailing_ws else "")
            if out:
                self._write(out)

    def handle_entityref(self, name: str):
        if self._in_head or self._in_title:
            return
        try:
            # Convert named entities like &amp;
            from html import unescape
            self._write(unescape(f"&{name};"))
        except Exception:
            self._write(f"&{name};")

    def handle_charref(self, name: str):
        if self._in_head or self._in_title:
            return
        try:
            from html import unescape
            if name.lower().startswith("x"):
                char = chr(int(name[1:], 16))
            else:
                char = chr(int(name))
            self._write(char)
        except Exception:
            self._write(f"&#{name};")

    def get_markdown(self) -> str:
        # Trim leading/trailing whitespace lines
        text = self._text()
        # Normalize 3+ blank lines to 2
        import re
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def convert_html_to_md(html: str) -> str:
    parser = MarkdownConverter()
    parser.feed(html)
    parser.close()
    return parser.get_markdown()


def main() -> int:
    force = "--force" in sys.argv
    root = os.getcwd()
    export_dir = os.path.join(root, "Canvas Export")

    if not os.path.isdir(export_dir):
        print(f"Canvas Export directory not found at: {export_dir}", file=sys.stderr)
        return 1

    html_files = [
        f for f in os.listdir(export_dir)
        if f.lower().endswith(".html") and os.path.isfile(os.path.join(export_dir, f))
    ]

    if not html_files:
        print("No .html files found in Canvas Export.")
        return 0

    written = 0
    skipped = 0
    for fname in sorted(html_files):
        html_path = os.path.join(export_dir, fname)
        md_path = os.path.join(export_dir, os.path.splitext(fname)[0] + ".md")

        if (not force) and os.path.exists(md_path):
            skipped += 1
            continue

        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        md = convert_html_to_md(html)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)

        written += 1

    print(f"Converted: {written}  Skipped(existing): {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
