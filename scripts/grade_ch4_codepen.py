#!/usr/bin/env python3
from __future__ import annotations

"""
Automated grader for Ch. 4: Loops Lab — Repeat Statements (25 pts)

Rubric mapping:
- Carousel 10-turn and user-defined versions (5)
- Parity: even/odd and exactly 10 numbers from start (5)
- Input validation loops (<=100 and 50..100) (5)
- Multiplication table 2..9 with validation (5)
- Neither yes nor no (3)
- FizzBuzz with correct precedence/order (2)

Usage:
  python scripts/grade_ch4_codepen.py --url https://codepen.io/<user>/pen/<slug>
  python scripts/grade_ch4_codepen.py --from-logs path/to/console.log [--js path/to/code.js]
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import grade_ch1_codepen as common


def check_carousel(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    # Check at least 10 'Turn N' lines and includes Turn 1 and Turn 10
    pattern = re.compile(r"^Turn\s+(\d+)$")
    nums = [int(m.group(1)) for l in lines for m in [pattern.match(l)] if m]
    ten_ok = set(range(1, 11)).issubset(set(nums))
    user_defined_ok = False
    if code_js and ('How many turns' in code_js or 'totalTurns' in code_js):
        user_defined_ok = True
    elif any('Invalid number of turns' in l for l in lines):
        user_defined_ok = True
    score = 5 if (ten_ok and user_defined_ok) else (3 if ten_ok else 0)
    return score, 5, f"ten_ok={ten_ok}, user_defined={user_defined_ok}, count={len(nums)}"


def check_parity(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    even = [l for l in lines if re.match(r"^\d+\s+is\s+even$", l)]
    odd = [l for l in lines if re.match(r"^\d+\s+is\s+odd$", l)]
    has_both = bool(even) and bool(odd)
    # Heuristic: look for a streak of 10 labeled lines (start + 9)
    labeled_nums = [int(re.match(r"^(\d+)\s+is\s+(?:even|odd)$", l).group(1)) for l in lines if re.match(r"^(\d+)\s+is\s+(?:even|odd)$", l)]
    ten_from_start = False
    if len(labeled_nums) >= 10:
        # Check any increasing run of length 10
        for i in range(len(labeled_nums) - 9):
            seq = labeled_nums[i:i+10]
            if all(seq[j] + 1 == seq[j+1] for j in range(9)):
                ten_from_start = True
                break
    score = 5 if (has_both and ten_from_start) else (3 if has_both else 0)
    return score, 5, f"has_both={has_both}, ten_from_start={ten_from_start}"


def check_validation(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    # Prefer presence of the prompts in code and acceptance logs
    a = (code_js and 'Enter a number (<= 100)' in code_js) or any('Accepted:' in l for l in lines)
    b = (code_js and 'Enter a number between 50 and 100' in code_js) or any('Accepted (50..100):' in l for l in lines)
    score = 5 if (a and b) else (2 if (a or b) else 0)
    return score, 5, f"<=100={bool(a)}, 50..100={bool(b)}"


def check_multiplication(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    # Look for lines like "7 x 1 = 7" and "7 x 10 = 70"
    x1 = any(re.match(r"^\d+\s+x\s+1\s+=\s+\d+$", l) for l in lines)
    x10 = any(re.match(r"^\d+\s+x\s+10\s+=\s+\d+$", l) for l in lines)
    # Validation prompt in code indicates full solution
    val = code_js and 'Enter a number (2..9):' in code_js
    score = 5 if (x1 and x10 and val) else (3 if (x1 and x10) else 0)
    return score, 5, f"x1={x1}, x10={x10}, validated={bool(val)}"


def check_neither_yes_nor_no(code_js: Optional[str], lines: List[str]) -> Tuple[int, int, str]:
    # Code presence of prompt loop cue
    ok = False
    if code_js and ('Type "yes" or "no" to end' in code_js or 'yes' in code_js and 'no' in code_js):
        ok = True
    score = 3 if ok else 0
    return score, 3, f"code_prompt_loop={ok}"


def check_fizzbuzz(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    # Console evidence includes at least 'Fizz', 'Buzz', and 'FizzBuzz'
    has_fizz = any(l == 'Fizz' for l in lines)
    has_buzz = any(l == 'Buzz' for l in lines)
    has_fizzbuzz = any(l == 'FizzBuzz' for l in lines)
    score = 2 if (has_fizz and has_buzz and has_fizzbuzz) else 0
    return score, 2, f"F={has_fizz}, B={has_buzz}, FB={has_fizzbuzz}"


def grade_ch4(console_lines: List[str], code_js: Optional[str]) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(name: str, tpl: Tuple[int, int, str]):
        nonlocal total
        score, out_of, reason = tpl
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("Carousel (10 + user-defined)", check_carousel(console_lines, code_js))
    add("Parity even/odd + 10 from start", check_parity(console_lines, code_js))
    add("Validation loops (<=100, 50..100)", check_validation(console_lines, code_js))
    add("Multiplication table 2..9", check_multiplication(console_lines, code_js))
    add("Neither yes nor no", check_neither_yes_nor_no(code_js, console_lines))
    add("FizzBuzz", check_fizzbuzz(console_lines, code_js))

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
    if result['console_preview']:
        lines.append("")
        lines.append("Console preview (first 50 lines):")
        for l in result['console_preview']:
            lines.append(f"  {l}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description='Grade Ch. 4 CodePen submission (Loops Lab)')
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

    result = grade_ch4(lines, code_js)
    if args.out == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

