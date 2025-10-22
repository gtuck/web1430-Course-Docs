#!/usr/bin/env python3
from __future__ import annotations

"""
Automated grader for Ch. 6: Objects Lab (25 pts)

Rubric mapping:
- Aurora object with xp and working describe() using this (8)
- Dog object with bark() and correct logs (5)
- Circle object with circumference() and area() using Math.PI (5)
- Account object with credit() and describe(), correct before/after (5)
- Clear, readable console output (2)

Usage:
  python scripts/grade_ch6_codepen.py --url https://codepen.io/<user>/pen/<slug>
  python scripts/grade_ch6_codepen.py --from-logs path/to/console.log [--js path/to/code.js]
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import grade_ch1_codepen as common


def check_aurora(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = False
    if code_js:
        code_ok = ('const aurora' in code_js) and ('xp' in code_js) and ('describe(' in code_js) and ('this.name' in code_js)
    console_ok = any((' has ' in l and ' XP points' in l) for l in lines)
    score = 8 if (code_ok and console_ok) else (5 if (code_ok or console_ok) else 0)
    return score, 8, f"code_ok={code_ok}, console_ok={console_ok}"


def check_dog(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('const dog' in code_js and 'bark()' in code_js)
    l1 = any(re.search(r"^\w+\s+is\s+a\s+\w+\s+dog\s+measuring\s+\d+", l) for l in lines)
    l2 = any(re.search(r"^Look, a cat!\s+\w+\s+barks:\s+", l) for l in lines)
    score = 5 if (code_ok and l1 and l2) else (3 if (l1 and l2) else 0)
    return score, 5, f"code_ok={bool(code_ok)}, logs_ok={l1 and l2}"


def check_circle(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('const circle' in code_js and 'Math.PI' in code_js and ('circumference()' in code_js or 'circumference (' in code_js) and ('area()' in code_js or 'area (' in code_js))
    c_ok = any(l.startswith('Its circumference is ') for l in lines)
    a_ok = any(l.startswith('Its area is ') for l in lines)
    score = 5 if (code_ok and c_ok and a_ok) else (3 if (c_ok and a_ok) else 0)
    return score, 5, f"code_ok={bool(code_ok)}, logs_ok={c_ok and a_ok}"


def check_account(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('const account' in code_js and 'credit(' in code_js and 'describe(' in code_js)
    before = any(l.strip() == 'Owner: Alex, balance: 0' for l in lines)
    after = any(l.strip() == 'Owner: Alex, balance: 170' for l in lines)
    score = 5 if (code_ok and before and after) else (3 if (before and after) else 0)
    return score, 5, f"code_ok={bool(code_ok)}, before={before}, after={after}"


def check_readable_output(lines: List[str]) -> Tuple[int, int, str]:
    # Heuristic: enough lines and some labeled messages
    labeled = sum(1 for l in lines if re.search(r":| is | has ", l))
    score = 2 if (len(lines) >= 6 and labeled >= 3) else 0
    return score, 2, f"lines={len(lines)}, labeled={labeled}"


def grade_ch6(console_lines: List[str], code_js: Optional[str]) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(name: str, tpl: Tuple[int, int, str]):
        nonlocal total
        score, out_of, reason = tpl
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("Aurora object + describe()", check_aurora(console_lines, code_js))
    add("Dog with bark() logs", check_dog(console_lines, code_js))
    add("Circle circumference/area", check_circle(console_lines, code_js))
    add("Account credit() before/after", check_account(console_lines, code_js))
    add("Readable output", check_readable_output(console_lines))

    return {
        "total": total,
        "possible": possible,
        "checks": checks,
        "meta": {"captured_lines": len(console_lines), "code_available": bool(code_js)},
        "console_preview": console_lines[:50],
    }


def format_text_report(result: Dict[str, Any]) -> str:
    lines = [f"Total: {result['total']} / {result['possible']}", ""]
    for c in result['checks']:
        status = 'OK' if c['score'] == c['out_of'] else ('PARTIAL' if c['score'] > 0 else 'MISS')
        lines.append(f"- {c['name']}: {c['score']}/{c['out_of']} [{status}] - {c['reason']}")
    lines.append("")
    lines.append(f"Captured console lines: {result['meta']['captured_lines']}")
    lines.append(f"JS code available: {result['meta']['code_available']}")
    # Notes section summarizing any misses/partials
    checks = result.get('checks', [])
    misses = [c for c in checks if c.get('score', 0) < c.get('out_of', 0)]
    lines.append("")
    lines.append("Notes:")
    if not misses:
        lines.append("- All rubric items satisfied.")
    else:
        for c in misses:
            lines.append(f"- {c['name']}: {c['reason']}")
    if result['console_preview']:
        lines.append("")
        lines.append("Console preview (first 50 lines):")
        for l in result['console_preview']:
            lines.append(f"  {l}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description='Grade Ch. 6 CodePen submission (Objects Lab)')
    p.add_argument('--url', help='CodePen URL')
    p.add_argument('--from-logs', dest='logs', help='Path to newline-delimited console logs')
    p.add_argument('--js', dest='js_path', help='Optional path to JS code for checks')
    p.add_argument('--timeout', type=float, default=12.0)
    p.add_argument('--out', choices=['text','json'], default='text')
    args = p.parse_args(argv)

    lines: List[str] = []
    code_js: Optional[str] = None

    if args.logs:
        if not os.path.exists(args.logs):
            print(f"Error: log file not found: {args.logs}", file=sys.stderr)
            return 2
        lines = common.load_lines_from_file(args.logs)

    if args.js_path:
        if not os.path.exists(args.js_path):
            print(f"Error: JS file not found: {args.js_path}", file=sys.stderr)
            return 2
        code_js = common.load_code_from_file(args.js_path)

    if args.url and not lines:
        try:
            l1, js1 = common.capture_console_from_codepen(args.url, timeout=args.timeout)
            lines = l1
            code_js = code_js or js1
        except Exception:
            dbg = common.derive_debug_url(args.url)
            if dbg:
                try:
                    l2, js2 = common.capture_console_from_codepen(dbg, timeout=args.timeout)
                    lines = l2
                    code_js = code_js or js2
                except Exception:
                    pass

    if code_js and (not lines or common.looks_blocked(lines)):
        sim = common.simulate_console_with_js(code_js, timeout=6.0)
        if sim:
            lines = sim

    if not lines:
        print('Error: No console lines available. Provide --url or --from-logs.', file=sys.stderr)
        return 2

    result = grade_ch6(lines, code_js)
    if args.out == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
