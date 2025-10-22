#!/usr/bin/env python3
"""
Parse Canvas HTML submission link files to extract CodePen URLs and metadata.

Inputs: directory of HTML files (e.g., Submissions/*.html) exported from Canvas.
Each file typically includes:
  - <meta http-equiv="Refresh" content="0; url=https://codepen.io/<user>/pen/<slug>">
  - <a href="https://codepen.io/<user>/pen/<slug>"> first link to submission
  - <h1>Assignment Title: Student Name</h1>
  - Filename pattern: <username>[_LATE]_<_studentId_>_link.html

Outputs: CSV (default) or JSON with fields per file:
  username, late, student_id, assignment, student_name, best_url, meta_url, anchor_url, debug_url, file

Usage:
  python scripts/parse_canvas_submissions.py --dir Submissions --out submissions.csv
  python scripts/parse_canvas_submissions.py --dir Submissions --format json
"""

from __future__ import annotations

import argparse
import csv
import html
import os
import re
import sys
import json
from typing import Dict, List, Optional, Tuple
from html.parser import HTMLParser


class SubmissionHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta_url: Optional[str] = None
        self.anchor_url: Optional[str] = None
        self.h1_text: Optional[str] = None
        self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'meta':
            attrd = {k.lower(): v for k, v in attrs}
            http_equiv = attrd.get('http-equiv', '')
            content = attrd.get('content', '')
            # Prefer Refresh meta with url=...
            if http_equiv.lower() == 'refresh' and content:
                m = re.search(r"url\s*=\s*([^;]+)$", content, re.IGNORECASE)
                if m:
                    url = m.group(1).strip().strip('"\'')
                    if 'codepen.io' in url:
                        self.meta_url = url
            elif content and 'codepen.io' in content and not self.meta_url:
                # Fallback: any meta content with a CodePen URL
                m2 = re.search(r"https?://[^\s'\"]+codepen\.io[^\s'\"]*", content)
                if m2:
                    self.meta_url = m2.group(0)

        if tag.lower() == 'a' and self.anchor_url is None:
            href = None
            for k, v in attrs:
                if k.lower() == 'href':
                    href = v
                    break
            if href and 'codepen.io' in href:
                self.anchor_url = href

        if tag.lower() == 'h1':
            self._in_h1 = True

    def handle_endtag(self, tag):
        if tag.lower() == 'h1':
            self._in_h1 = False

    def handle_data(self, data):
        if self._in_h1:
            text = data.strip()
            if text:
                self.h1_text = (self.h1_text or '') + text


def parse_filename_meta(basename: str) -> Tuple[Optional[str], bool, Optional[str]]:
    """Extract username, late flag, student_id from filename.
    Examples:
      decariaxander_2059405_link.html -> (decariaxander, False, 2059405)
      wadmanzack_LATE_2083885_link.html -> (wadmanzack, True, 2083885)
    """
    name = os.path.splitext(basename)[0]
    m = re.match(r"^(?P<user>[^_]+)_(?:(?P<late>LATE)_)?(?P<id>\d+)_link$", name, re.IGNORECASE)
    if not m:
        # tolerate files without _link suffix or different order
        m = re.match(r"^(?P<user>[^_]+)_(?:(?P<late>LATE)_)?(?P<id>\d+)", name, re.IGNORECASE)
    if m:
        return m.group('user'), bool(m.group('late')), m.group('id')
    return None, False, None


def parse_h1_assignment_and_name(h1_text: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    if not h1_text:
        return None, None
    # Common format: "Ch. 1 - Coding time!: First Last"
    # Use the last colon as the delimiter between assignment and student name.
    text = h1_text.strip()
    if ':' in text:
        parts = text.rsplit(':', 1)
        assignment = parts[0].strip()
        student_name = parts[1].strip()
        return assignment, student_name
    # Fallback: try an em-dash or hyphen
    for sep in ['—', '-']:
        if sep in text:
            parts = text.split(sep)
            if len(parts) >= 2:
                return parts[0].strip(), parts[-1].strip()
    return text, None


def best_url(meta_url: Optional[str], anchor_url: Optional[str]) -> Optional[str]:
    return meta_url or anchor_url


def derive_debug_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    m = re.match(r"^https?://codepen\.io/([^/]+)/(?:(?:pen)|(?:full))/([^/?#]+)", url.strip())
    if m:
        user, slug = m.group(1), m.group(2)
        return f"https://cdpn.io/{user}/debug/{slug}"
    return None


def parse_submission_file(path: str) -> Dict[str, Optional[str]]:
    base = os.path.basename(path)
    username, late, student_id = parse_filename_meta(base)
    parser = SubmissionHTMLParser()
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    parser.feed(content)

    assignment, student_name = parse_h1_assignment_and_name(parser.h1_text)
    meta_url = parser.meta_url
    a_url = parser.anchor_url
    best = best_url(meta_url, a_url)
    dbg = derive_debug_url(best)

    return {
        'file': base,
        'username': username,
        'late': 'TRUE' if late else 'FALSE',
        'student_id': student_id,
        'assignment': assignment,
        'student_name': student_name,
        'meta_url': meta_url,
        'anchor_url': a_url,
        'best_url': best,
        'debug_url': dbg,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Extract CodePen links and metadata from Canvas submission link HTML files')
    ap.add_argument('--dir', default='Submissions', help='Directory containing Canvas link HTML files')
    ap.add_argument('--glob', default='*.html', help='Glob pattern within the directory')
    ap.add_argument('--format', choices=['csv', 'json'], default='csv', help='Output format')
    ap.add_argument('--out', default='-', help='Output file path or - for stdout')
    args = ap.parse_args(argv)

    root = args.dir
    if not os.path.isdir(root):
        print(f"Error: directory not found: {root}", file=sys.stderr)
        return 2

    import glob as _glob
    files = sorted(_glob.glob(os.path.join(root, args.glob)))
    rows = [parse_submission_file(p) for p in files]

    if args.format == 'json':
        data = json.dumps(rows, indent=2)
        if args.out == '-':
            print(data)
        else:
            with open(args.out, 'w', encoding='utf-8') as f:
                f.write(data)
        return 0

    # CSV
    fieldnames = [
        'file', 'username', 'late', 'student_id', 'assignment', 'student_name',
        'best_url', 'meta_url', 'anchor_url', 'debug_url'
    ]
    if args.out == '-':
        w = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') or '' for k in fieldnames})
    else:
        with open(args.out, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, '') or '' for k in fieldnames})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

