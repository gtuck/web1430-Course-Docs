#!/usr/bin/env python3
"""
Batch grade all Canvas CodePen submissions in a directory using the Ch. 1 grader.

Reads Submissions/*.html via parse_canvas_submissions, then for each best_url
attempts to capture console output (with automatic Debug View + simulation fallbacks)
and computes a score. Emits CSV or JSON.

Usage:
  # Using repo venv with Playwright installed (recommended)
  scripts/.venv/bin/python scripts/batch_grade_ch1.py --dir Submissions --out grades.csv

  # Or system Python (requires playwright to be installed globally)
  python scripts/batch_grade_ch1.py --dir Submissions --out grades.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional


# Ensure we can import sibling modules in this folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    import parse_canvas_submissions as pcs
    import grade_ch1_codepen as grader
except Exception as e:
    print(f"Error: failed to import helper modules from scripts/: {e}", file=sys.stderr)
    sys.exit(2)


def try_grade_url(url: str, timeout: float = 12.0, assume_comments_ok: bool = False) -> Dict[str, Any]:
    console_lines: List[str] = []
    code_js: Optional[str] = None
    steps: List[str] = []
    err: Optional[str] = None

    def attach_result(src: str, lines: List[str], js: Optional[str]):
        nonlocal console_lines, code_js
        if lines and (len(lines) > len(console_lines)):
            console_lines = lines
        if js and not code_js:
            code_js = js
        steps.append(src)

    # First attempt: direct URL
    try:
        lines, js = grader.capture_console_from_codepen(url, timeout=timeout)
        attach_result("direct", lines, js)
    except Exception as e:
        err = f"direct: {e}"

    # If blocked or empty, try Debug View
    if (not console_lines) or grader.looks_blocked(console_lines):
        dbg = grader.derive_debug_url(url)
        if dbg:
            try:
                lines, js = grader.capture_console_from_codepen(dbg, timeout=timeout)
                attach_result("debug", lines, js)
            except Exception as e:
                err = (err + f"; debug: {e}") if err else f"debug: {e}"

    # If still not useful, try simulation with extracted JS
    if (not console_lines) and code_js:
        try:
            lines = grader.simulate_console_with_js(code_js, timeout=6.0)
            attach_result("simulated", lines, code_js)
        except Exception as e:
            err = (err + f"; simulate: {e}") if err else f"simulate: {e}"

    result: Dict[str, Any]
    if console_lines:
        result = grader.grade_ch1(console_lines, code_js, assume_comments_ok=assume_comments_ok)
    else:
        # Return minimal structure with error
        result = {
            "total": 0,
            "possible": 25,
            "checks": [],
            "meta": {"captured_lines": 0, "code_available": bool(code_js)},
            "console_preview": [],
        }

    result["_attempt_steps"] = steps
    if err:
        result["_errors"] = err
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Batch grade Ch. 1 CodePen submissions from Canvas HTML link files")
    ap.add_argument('--dir', default='Submissions', help='Directory with Canvas HTML link files')
    ap.add_argument('--glob', default='*.html', help='Glob pattern')
    ap.add_argument('--timeout', type=float, default=14.0, help='Seconds to wait for console output')
    ap.add_argument('--assume-comments-ok', action='store_true', help='Award comment points if JS cannot be fetched')
    ap.add_argument('--format', choices=['csv','json'], default='csv')
    ap.add_argument('--out', default='-', help='Output path or - for stdout')
    args = ap.parse_args(argv)

    # Collect submissions
    import glob as _glob
    paths = sorted(_glob.glob(os.path.join(args.dir, args.glob)))
    if not paths:
        print(f"No files matched in {args.dir}/{args.glob}")
        return 0

    rows: List[Dict[str, Any]] = []
    for p in paths:
        meta = pcs.parse_submission_file(p)
        url = meta.get('best_url')
        dbg = meta.get('debug_url')
        rec: Dict[str, Any] = {
            'file': meta.get('file'),
            'username': meta.get('username'),
            'late': meta.get('late'),
            'student_id': meta.get('student_id'),
            'assignment': meta.get('assignment'),
            'student_name': meta.get('student_name'),
            'best_url': url,
            'debug_url': dbg,
        }
        if not url:
            rec.update({'total': 0, 'possible': 25, 'note': 'No URL found'})
            rows.append(rec)
            continue
        try:
            result = try_grade_url(url, timeout=args.timeout, assume_comments_ok=args.assume_comments_ok)
            rec.update({
                'total': result.get('total', 0),
                'possible': result.get('possible', 25),
                'captured_lines': result.get('meta', {}).get('captured_lines', 0),
                'code_available': result.get('meta', {}).get('code_available', False),
                'attempt_steps': ";".join(result.get('_attempt_steps', [])),
                'errors': result.get('_errors', ''),
            })
        except Exception as e:
            rec.update({'total': 0, 'possible': 25, 'errors': str(e)})
        rows.append(rec)

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
        'file','username','late','student_id','assignment','student_name',
        'best_url','debug_url','total','possible','captured_lines','code_available','attempt_steps','errors'
    ]
    if args.out == '-':
        w = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fieldnames})
    else:
        with open(args.out, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, '') for k in fieldnames})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

