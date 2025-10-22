#!/usr/bin/env python3
from __future__ import annotations

"""
Automated grader for Ch. 3: Conditions and Switch (25 pts)

Rubric mapping:
- Number classification with correct if/else if/else (5)
- Range check with && and messages (5)
- Following day with switch/default/breaks (10)
- Weather choices with strict equality (2)
- Fix-me mini-exercises corrected (3)

Usage:
  python scripts/grade_ch3_codepen.py --url https://codepen.io/<user>/pen/<slug>
  python scripts/grade_ch3_codepen.py --from-logs path/to/console.log [--js path/to/code.js]
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import grade_ch1_codepen as common


def normalize_line(s: str) -> str:
    return s.strip()


def check_number_classification(lines: List[str]) -> Tuple[int, int, str]:
    msgs = {
        'The number is positive',
        'The number is negative',
        'The number is zero',
    }
    hit = any(l in msgs for l in lines)
    return (5 if hit else 0), 5, ('found classification message' if hit else 'no classification message')


def check_range_check(lines: List[str]) -> Tuple[int, int, str]:
    in_msg = any(re.search(r"\bis between 0 and 100\b", l) for l in lines)
    out_msg = any(re.search(r"\bis outside 0.?100\b", l) for l in lines)
    hit = in_msg or out_msg
    return (5 if hit else 0), 5, f"between={in_msg}, outside={out_msg}"


def check_following_day(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    # Console evidence: a line starting with "Tomorrow is " and a valid day
    valid_days = { 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday' }
    console_ok = any(
        l.startswith('Tomorrow is ') and l.replace('Tomorrow is ', '') in valid_days
        for l in lines
    ) or any(l == 'Unrecognized day name' for l in lines)

    # Code evidence: presence of switch with cases and default and breaks
    code_ok = False
    if code_js:
        has_switch = 'switch' in code_js and 'default' in code_js
        case_count = sum(1 for _ in re.finditer(r"\bcase\s+'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'\s*:", code_js))
        break_count = code_js.count('break')
        code_ok = has_switch and case_count >= 6 and break_count >= 6

    score = 10 if (console_ok or code_ok) else 0
    return score, 10, f"console_ok={console_ok}, switch_cases={case_count if code_js else 0}, breaks={break_count if code_js else 0}"


def check_weather(code_js: Optional[str], lines: List[str]) -> Tuple[int, int, str]:
    # Prefer strict equality presence for weather checks
    strict_ok = False
    if code_js:
        strict_ok = bool(re.search(r"weather\s*===\s*'(?:sunny|windy|rainy|snowy)'", code_js))
    # Console: any of expected messages
    messages = {
        'T-shirt time!',
        'Windbreaker life.',
        'Bring that umbrella!',
        'Just stay inside!',
        'Not a valid weather type',
    }
    console_ok = any(l in messages for l in lines)
    score = 2 if (strict_ok or console_ok) else 0
    return score, 2, f"strict_ok={strict_ok}, console_ok={console_ok}"


def check_fix_me(lines: List[str]) -> Tuple[int, int, str]:
    # 5a) expects OK
    ok_a = 'OK' in lines
    # 5b) expects only 'greater'
    count_greater = sum(1 for l in lines if l == 'greater')
    count_not = sum(1 for l in lines if l == 'not greater')
    ok_b = count_greater >= 1 and count_not == 0
    # 5c) for v=2 expects only 'two'
    count_two = sum(1 for l in lines if l == 'two')
    count_one = sum(1 for l in lines if l == 'one')
    count_other = sum(1 for l in lines if l == 'other')
    ok_c = count_two >= 1 and (count_one + count_other) == 0
    # Score: any two -> 2 points, all three -> 3
    ok_count = sum([ok_a, ok_b, ok_c])
    score = 3 if ok_count == 3 else (2 if ok_count >= 2 else 0)
    return score, 3, f"a={ok_a}, b={ok_b}, c={ok_c}"


def grade_ch3(console_lines: List[str], code_js: Optional[str]) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(name: str, tpl: Tuple[int, int, str]):
        nonlocal total
        score, out_of, reason = tpl
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("Number classification", check_number_classification(console_lines))
    add("Range check (0..100)", check_range_check(console_lines))
    add("Following day (switch)", check_following_day(console_lines, code_js))
    add("Weather choices (strict ===)", check_weather(code_js, console_lines))
    add("Fix-me corrections", check_fix_me(console_lines))

    return {
        "total": total,
        "possible": possible,
        "checks": checks,
        "meta": {"captured_lines": len(console_lines), "code_available": bool(code_js)},
        "console_preview": console_lines[:50],
    }


def format_text_report(result: Dict[str, Any]) -> str:
    out = [f"Total: {result['total']} / {result['possible']}", ""]
    for c in result['checks']:
        status = 'OK' if c['score'] == c['out_of'] else ('PARTIAL' if c['score'] > 0 else 'MISS')
        out.append(f"- {c['name']}: {c['score']}/{c['out_of']} [{status}] - {c['reason']}")
    out.append("")
    out.append(f"Captured console lines: {result['meta']['captured_lines']}")
    out.append(f"JS code available: {result['meta']['code_available']}")
    # Notes section summarizing any misses/partials
    checks = result.get('checks', [])
    misses = [c for c in checks if c.get('score', 0) < c.get('out_of', 0)]
    out.append("")
    out.append("Notes:")
    if not misses:
        out.append("- All rubric items satisfied.")
    else:
        for c in misses:
            out.append(f"- {c['name']}: {c['reason']}")
    if result['console_preview']:
        out.append("")
        out.append("Console preview (first 50 lines):")
        for l in result['console_preview']:
            out.append(f"  {l}")
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description='Grade Ch. 3 CodePen submission (Conditions and Switch)')
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

    result = grade_ch3(lines, code_js)
    if args.out == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
