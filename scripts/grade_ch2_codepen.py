#!/usr/bin/env python3
"""
Automated grader for Ch. 2 assignment: Console Practice — Variables, Swap, Increment.

Reuses the CodePen capture and fallbacks from grade_ch1_codepen.py. Grades against
the rubric in assignments/ch02/index.md (25 pts):
- Temp variable swap works and prints 3 then 5 (8)
- Arithmetic swap works after reset (5)
- Correct use of let/const, assignment, and comments (5)
- Increment demo shows expected value (2)
- Prompt + Number() conversion + swap logs before/after (5)

Usage:
  python scripts/grade_ch2_codepen.py --url https://codepen.io/<user>/pen/<slug>
  python scripts/grade_ch2_codepen.py --from-logs path/to/console.log [--js path/to/code.js]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# Reuse capture helpers from ch1 grader
try:
    import grade_ch1_codepen as common
except Exception as e:
    print(f"Error: cannot import grade_ch1_codepen helpers: {e}", file=sys.stderr)
    raise


def normalize_line(s: str) -> str:
    return s.strip()


def is_number_line(s: str) -> bool:
    s = s.strip()
    return bool(re.fullmatch(r"-?\d+(?:\.\d+)?", s))


def check_temp_swap_3_5(lines: List[str]) -> Tuple[int, int, str]:
    # Look for two consecutive numeric lines: 3 then 5
    for i in range(len(lines) - 1):
        if lines[i] == '3' and lines[i + 1] == '5':
            return 8, 8, "Detected swap output 3 then 5"
    return 0, 8, "Did not find consecutive '3' then '5'"


def check_arithmetic_swap(code_js: Optional[str], lines: List[str]) -> Tuple[int, int, str]:
    # Prefer code-based detection of arithmetic swap sequence
    if code_js:
        has_seq = all(
            pat in code_js for pat in [
                'number1 = number1 + number2',
                'number2 = number1 - number2',
                'number1 = number1 - number2',
            ]
        )
        if has_seq:
            return 5, 5, "Arithmetic swap sequence present in code"
    # Heuristic console fallback (rare): Look for two distinct numeric-only lines that appear to be swapped around other content
    # Not very reliable without labels; leave as miss
    return 0, 5, "Could not verify arithmetic swap (needs JS code)"


def check_let_const_comments(code_js: Optional[str]) -> Tuple[int, int, str]:
    if not code_js:
        return 0, 5, "No JS code available to verify let/const/comments"
    has_let = 'let ' in code_js
    has_const = 'const ' in code_js
    has_assign = '=' in code_js
    has_comment = ('//' in code_js) or ('/*' in code_js and '*/' in code_js)
    score = 0
    if has_let:
        score += 1
    if has_const:
        score += 1
    if has_assign:
        score += 1
    if has_comment:
        score += 2
    return score, 5, f"let={has_let}, const={has_const}, assign={has_assign}, comment={has_comment}"


def check_increment(lines: List[str]) -> Tuple[int, int, str]:
    # Expect a line like: 'counter: 2'
    ok = any(re.fullmatch(r"counter:\s*2", l) for l in lines)
    return (2 if ok else 0), 2, ("Found 'counter: 2'" if ok else "Missing 'counter: 2'")


def check_prompt_number_swap(lines: List[str]) -> Tuple[int, int, str]:
    # Look for 'Before swap:' followed by two numbers on same line, and 'After swap:' with the numbers reversed
    before = None
    after = None
    for l in lines:
        m = re.match(r"^Before swap:\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)$", l)
        if m:
            before = (m.group(1), m.group(2))
        m2 = re.match(r"^After swap:\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)$", l)
        if m2:
            after = (m2.group(1), m2.group(2))
    if before and after and before[0] == after[1] and before[1] == after[0]:
        return 5, 5, f"Before {before} -> After {after}"
    if before or after:
        return 2, 5, "Found partial before/after, but not reversed as expected"
    return 0, 5, "Missing 'Before swap'/'After swap' logs with two numbers"


def grade_ch2(console_lines: List[str], code_js: Optional[str]) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(name: str, tpl: Tuple[int, int, str]):
        nonlocal total
        score, out_of, reason = tpl
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("Temp swap prints 3 then 5", check_temp_swap_3_5(console_lines))
    add("Arithmetic swap present", check_arithmetic_swap(code_js, console_lines))
    add("let/const/assignment/comments", check_let_const_comments(code_js))
    add("Increment shows counter: 2", check_increment(console_lines))
    add("Prompt+Number swap before/after", check_prompt_number_swap(console_lines))

    return {
        "total": total,
        "possible": possible,
        "checks": checks,
        "meta": {"captured_lines": len(console_lines), "code_available": bool(code_js)},
        "console_preview": console_lines[:50],
    }


def format_text_report(result: Dict[str, Any]) -> str:
    lines = [f"Total: {result['total']} / {result['possible']}", ""]
    for c in result["checks"]:
        status = "OK" if c["score"] == c["out_of"] else ("PARTIAL" if c["score"] > 0 else "MISS")
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
    if result["console_preview"]:
        lines.append("")
        lines.append("Console preview (first 50 lines):")
        for l in result["console_preview"]:
            lines.append(f"  {l}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Grade Ch. 2 CodePen submission")
    p.add_argument("--url", help="CodePen URL")
    p.add_argument("--from-logs", dest="logs", help="Path to newline-delimited console logs")
    p.add_argument("--js", dest="js_path", help="Optional path to JS code for checks")
    p.add_argument("--timeout", type=float, default=12.0, help="Seconds to capture console output")
    p.add_argument("--out", choices=["text","json"], default="text")
    args = p.parse_args(argv)

    console_lines: List[str] = []
    code_js: Optional[str] = None

    if args.logs:
        if not os.path.exists(args.logs):
            print(f"Error: log file not found: {args.logs}", file=sys.stderr)
            return 2
        console_lines = common.load_lines_from_file(args.logs)

    if args.js_path:
        if not os.path.exists(args.js_path):
            print(f"Error: JS file not found: {args.js_path}", file=sys.stderr)
            return 2
        code_js = common.load_code_from_file(args.js_path)

    if args.url and not console_lines:
        try:
            lines, js = common.capture_console_from_codepen(args.url, timeout=args.timeout)
            console_lines = lines
            code_js = code_js or js
        except Exception as e:
            dbg = common.derive_debug_url(args.url)
            if dbg:
                print(f"Info: retrying with Debug View: {dbg}", file=sys.stderr)
                try:
                    lines, js = common.capture_console_from_codepen(dbg, timeout=args.timeout)
                    console_lines = lines
                    code_js = code_js or js
                except Exception as e2:
                    print(f"Warning: capture failed: {e2}", file=sys.stderr)

    # If blocked, try simulating console from code
    if code_js and (not console_lines or common.looks_blocked(console_lines)):
        sim = common.simulate_console_with_js(code_js, timeout=6.0)
        if sim:
            console_lines = sim

    if not console_lines:
        print("Error: No console lines available. Provide --url or --from-logs.", file=sys.stderr)
        return 2

    result = grade_ch2(console_lines, code_js)
    if args.out == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
