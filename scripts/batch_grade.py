#!/usr/bin/env python3
"""
Batch grade CodePen submissions for multiple assignments.

Detects the chapter from the Canvas submission's <h1> (e.g., "Ch. 2 - ...") and
invokes the appropriate grader. Currently supports:
  - Ch. 1 (console skills)
  - Ch. 2 (variables, swap, increment)

Outputs CSV or JSON with a row per submission including score and context.

Usage:
  scripts/.venv/bin/python scripts/batch_grade.py --dir Submissions --out grades.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import parse_canvas_submissions as pcs
import grade_ch1_codepen as ch1
import grade_ch2_codepen as ch2
import grade_ch3_codepen as ch3
import grade_ch4_codepen as ch4
import grade_ch5_codepen as ch5
import grade_ch6_codepen as ch6
import grade_ch7_8_codepen as ch7_8
import grade_ch9_codepen as ch9
import grade_ch10_codepen as ch10


def detect_chapters(assignment: Optional[str]) -> List[int]:
    if not assignment:
        return []
    nums = [int(n) for n in re.findall(r"\bCh\.\s*(\d+)", assignment, re.IGNORECASE)]
    return nums


def try_capture(url: str, timeout: float) -> Tuple[List[str], Optional[str], List[str], Optional[str]]:
    """Return (console_lines, code_js, steps, error)"""
    steps: List[str] = []
    err: Optional[str] = None
    lines: List[str] = []
    code_js: Optional[str] = None

    try:
        l1, js1 = ch1.capture_console_from_codepen(url, timeout=timeout)
        lines = l1
        code_js = js1
        steps.append('direct')
    except Exception as e:
        err = f"direct: {e}"

    if (not lines) or ch1.looks_blocked(lines):
        dbg = ch1.derive_debug_url(url)
        if dbg:
            try:
                l2, js2 = ch1.capture_console_from_codepen(dbg, timeout=timeout)
                if l2:
                    lines = l2
                if js2:
                    code_js = js2
                steps.append('debug')
            except Exception as e2:
                err = (err + f"; debug: {e2}") if err else f"debug: {e2}"

    if code_js and ((not lines) or ch1.looks_blocked(lines)):
        try:
            sim = ch1.simulate_console_with_js(code_js, timeout=6.0)
            if sim:
                lines = sim
            steps.append('simulated')
        except Exception as e3:
            err = (err + f"; simulate: {e3}") if err else f"simulate: {e3}"

    return lines, code_js, steps, err


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Batch grade CodePen submissions across assignments')
    ap.add_argument('--dir', default='Submissions', help='Directory with Canvas HTML link files')
    ap.add_argument('--glob', default='*.html', help='Glob pattern')
    ap.add_argument('--timeout', type=float, default=14.0)
    ap.add_argument('--format', choices=['csv','json'], default='csv')
    ap.add_argument('--out', default='-', help='Output file or - for stdout')
    args = ap.parse_args(argv)

    import glob as _glob
    files = sorted(_glob.glob(os.path.join(args.dir, args.glob)))
    rows: List[Dict[str, Any]] = []

    for p in files:
        meta = pcs.parse_submission_file(p)
        assign = meta.get('assignment') or ''
        chapters = detect_chapters(assign)
        chapter = chapters[0] if chapters else None
        url = meta.get('best_url')
        dbg = meta.get('debug_url')

        rec: Dict[str, Any] = {
            'file': meta.get('file'),
            'username': meta.get('username'),
            'late': meta.get('late'),
            'student_id': meta.get('student_id'),
            'assignment': assign,
            'chapter': chapter if chapter is not None else '',
            'best_url': url,
            'debug_url': dbg,
        }

        if not url:
            rec.update({'total': 0, 'possible': 25, 'errors': 'No URL found'})
            rows.append(rec)
            continue

        lines: List[str] = []
        code_js: Optional[str] = None
        steps: List[str] = []
        errors: Optional[str] = None
        try:
            lines, code_js, steps, errors = try_capture(url, timeout=args.timeout)
        except Exception as e:
            errors = str(e)

        # Grade per chapter
        result: Dict[str, Any]
        if chapter == 1:
            if lines:
                result = ch1.grade_ch1(lines, code_js, assume_comments_ok=False)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        elif chapter == 2:
            if lines:
                result = ch2.grade_ch2(lines, code_js)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        elif chapter == 3:
            if lines:
                result = ch3.grade_ch3(lines, code_js)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        elif chapter == 4:
            if lines:
                result = ch4.grade_ch4(lines, code_js)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        elif chapter == 5:
            if lines:
                result = ch5.grade_ch5(lines, code_js)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        elif chapter == 6:
            if lines:
                result = ch6.grade_ch6(lines, code_js)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        elif chapter in (7, 8):
            if lines:
                result = ch7_8.grade_ch7_8(lines, code_js)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        elif chapter == 9:
            if lines:
                result = ch9.grade_ch9(lines, code_js)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        elif chapter == 10:
            if lines:
                result = ch10.grade_ch10(lines, code_js)
            else:
                result = {'total': 0, 'possible': 25, 'meta': {'captured_lines': 0, 'code_available': bool(code_js)}}
        else:
            result = {'total': 0, 'possible': 25}
            errors = (errors + '; unsupported assignment') if errors else 'unsupported assignment'

        rec.update({
            'total': result.get('total', 0),
            'possible': result.get('possible', 25),
            'captured_lines': result.get('meta', {}).get('captured_lines', ''),
            'code_available': result.get('meta', {}).get('code_available', ''),
            'attempt_steps': ';'.join(steps),
            'errors': errors or '',
        })
        rows.append(rec)

    # Output
    if args.format == 'json':
        data = json.dumps(rows, indent=2)
        if args.out == '-':
            print(data)
        else:
            with open(args.out, 'w', encoding='utf-8') as f:
                f.write(data)
        return 0

    fieldnames = [
        'file','username','late','student_id','assignment','chapter','best_url','debug_url',
        'total','possible','captured_lines','code_available','attempt_steps','errors'
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
