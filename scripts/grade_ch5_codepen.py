#!/usr/bin/env python3
from __future__ import annotations

"""
Automated grader for Ch. 5: Functions Lab (25 pts)

Rubric mapping:
- Improved hello: prompts and shows sayHello() result (3)
- Number squaring: square1 and arrow square2 plus loop 0..10 (7)
- min(a, b) implemented and tested (5)
- calculate(a, op, b) handles +, -, *, / (incl. divide by 0) (5)
- Circle math: circumference(r) and area(r) using Math.PI and ** with input conversion (5)

Usage:
  python scripts/grade_ch5_codepen.py --url https://codepen.io/<user>/pen/<slug>
  python scripts/grade_ch5_codepen.py --from-logs path/to/console.log [--js path/to/code.js]
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import grade_ch1_codepen as common


def check_say_hello(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = False
    if code_js:
        code_ok = ('function sayHello' in code_js) and ('prompt' in code_js) and ('console.log(sayHello' in code_js)
    console_ok = any(re.match(r"^Hello,\s+.+!$", l) for l in lines)
    score = 3 if (code_ok or console_ok) else 0
    return score, 3, f"code_ok={code_ok}, console_ok={console_ok}"


def check_square(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = False
    if code_js:
        code_ok = ('function square1' in code_js) and re.search(r"const\s+square2\s*=\s*\w+\s*=>", code_js) is not None
    # console checkpoints include 0, 4, 25 (twice), and a loop with ' squared = '
    basics = sum(1 for l in lines if l in {'0','4','25'}) >= 3
    loop_ok = any(' squared = ' in l for l in lines)
    score = 7 if (code_ok and basics and loop_ok) else (4 if (code_ok and (basics or loop_ok)) else 0)
    return score, 7, f"code_ok={code_ok}, basics={basics}, loop={loop_ok}"


def check_min(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('function min' in code_js)
    # console outputs include: 4.5, 9, 1 (exact values)
    vals = set(l for l in lines if re.fullmatch(r"-?\d+(?:\.\d+)?", l))
    ok = {'4.5','9','1'}.issubset(vals)
    score = 5 if (code_ok and ok) else (3 if ok else 0)
    return score, 5, f"code_ok={bool(code_ok)}, outputs_ok={ok}"


def check_calculate(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('function calculate' in code_js)
    # console outputs include 10, -2, 0, Infinity — but overlaps other lines. Use proximity via keyword 'Infinity'.
    has_infty = any(l == 'Infinity' for l in lines)
    nums = set(l for l in lines if re.fullmatch(r"-?\d+(?:\.\d+)?", l))
    ok = has_infty and {'10','-2','0'}.issubset(nums)
    score = 5 if (code_ok and ok) else (3 if ok else 0)
    return score, 5, f"code_ok={bool(code_ok)}, outputs_ok={ok}"


def check_circle_math(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = False
    if code_js:
        code_ok = ('function circumference' in code_js) and ('function area' in code_js) and ('Math.PI' in code_js) and ('**' in code_js)
    console_ok = any(l.startswith('circumference(') for l in lines) and any(l.startswith('area(') for l in lines)
    score = 5 if (code_ok and console_ok) else (3 if (code_ok or console_ok) else 0)
    return score, 5, f"code_ok={code_ok}, console_ok={console_ok}"


def grade_ch5(console_lines: List[str], code_js: Optional[str]) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(name: str, tpl: Tuple[int, int, str]):
        nonlocal total
        score, out_of, reason = tpl
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("sayHello() with prompts", check_say_hello(console_lines, code_js))
    add("square1/square2 + loop", check_square(console_lines, code_js))
    add("min(a,b) implemented & tested", check_min(console_lines, code_js))
    add("calculate + - * / (Infinity)", check_calculate(console_lines, code_js))
    add("Circle math with Math.PI and **", check_circle_math(console_lines, code_js))

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
    p = argparse.ArgumentParser(description='Grade Ch. 5 CodePen submission (Functions Lab)')
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

    result = grade_ch5(lines, code_js)
    if args.out == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
