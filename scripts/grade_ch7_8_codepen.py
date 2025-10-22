#!/usr/bin/env python3
from __future__ import annotations

"""
Automated grader for Ch. 7 & 8: Arrays and Strings Lab (25 pts)

Rubric mapping:
- Musketeers: correct iterations and dynamic add/remove (8)
- Sum and maximum computed generically (5)
- List-of-words loop and display excluding 'stop' (2)
- Word info: length and case conversions (3)
- Vowel count (case-insensitive) (3)
- Reverse and palindrome ignoring spaces/punctuation/case (4)

Usage:
  python scripts/grade_ch7_8_codepen.py --url https://codepen.io/<user>/pen/<slug>
  python scripts/grade_ch7_8_codepen.py --from-logs path/to/console.log [--js path/to/code.js]
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import grade_ch1_codepen as common


def check_musketeers(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    names = [l for l in lines if l in ["Athos","Porthos","Aramis","D'Artagnan"]]
    has_core = all(n in names for n in ["Athos","Porthos","Aramis"])
    has_dart = "D'Artagnan" in names
    # Heuristic removal evidence: at least one occurrence of D'Artagnan and 3 consecutive name lines that do not include Aramis
    removal_ok = False
    for i in range(len(lines)-2):
        block = set(lines[i:i+3])
        if "D'Artagnan" in block and 'Aramis' not in block and (('Athos' in block) or ('Porthos' in block)):
            removal_ok = True
            break
    if has_core and has_dart and removal_ok:
        return 8, 8, "names logged; D'Artagnan added; Aramis removed in later pass"
    if (has_core and has_dart) or (has_core and removal_ok):
        return 4, 8, "partial: core names and add/remove partially detected"
    return 0, 8, "musketeers evidence not found"


def check_sum_and_max(lines: List[str]) -> Tuple[int, int, str]:
    m_sum = any(re.match(r"^sum\s*=\s*\d+$", l) for l in lines)
    m_max = any(re.match(r"^max\s*=\s*\d+$", l) for l in lines)
    score = 5 if (m_sum and m_max) else (2 if (m_sum or m_max) else 0)
    return score, 5, f"sum_label={m_sum}, max_label={m_max}"


def check_list_of_words(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = False
    if code_js:
        code_ok = ("Enter a word" in code_js) and ('words' in code_js) and ('.push(' in code_js)
    # Console heuristic: presence of multiple short words without labels may be noisy; rely on code
    return (2 if code_ok else 0), 2, f"code_ok={code_ok}"


def check_word_info(lines: List[str]) -> Tuple[int, int, str]:
    has_len = any(re.match(r"^length:\s*\d+$", l) for l in lines)
    has_low = any(l.startswith('lowercase:') for l in lines)
    has_up = any(l.startswith('uppercase:') for l in lines)
    score = 3 if (has_len and has_low and has_up) else (2 if (has_len and (has_low or has_up)) else 0)
    return score, 3, f"length={has_len}, lower={has_low}, upper={has_up}"


def check_vowel_count(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    # Prefer code evidence of counting vowels
    code_ok = False
    if code_js:
        code_ok = ('vowels' in code_js) and ("'a'" in code_js) and ("'e'" in code_js) and ("'i'" in code_js) and ("'o'" in code_js) and ("'u'" in code_js)
    console_ok = any(re.match(r"^vowels\s*[:=]\s*\d+$", l) for l in lines)
    score = 3 if (code_ok or console_ok) else 0
    return score, 3, f"code_ok={code_ok}, console_ok={console_ok}"


def check_reverse_palindrome(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    has_rev = any(l.startswith('reversed:') for l in lines)
    has_pal = any(l.startswith('palindrome:') for l in lines)
    score = 4 if (has_rev and has_pal) else (2 if (has_rev or has_pal) else 0)
    return score, 4, f"reversed={has_rev}, palindrome={has_pal}"


def grade_ch7_8(console_lines: List[str], code_js: Optional[str]) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(name: str, tpl: Tuple[int, int, str]):
        nonlocal total
        score, out_of, reason = tpl
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("Musketeers add/remove + iterations", check_musketeers(console_lines, code_js))
    add("Sum and max", check_sum_and_max(console_lines))
    add("List of words until stop", check_list_of_words(console_lines, code_js))
    add("Word info length/case", check_word_info(console_lines))
    add("Vowel count", check_vowel_count(console_lines, code_js))
    add("Reverse & palindrome", check_reverse_palindrome(console_lines, code_js))

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
    p = argparse.ArgumentParser(description='Grade Ch. 7 & 8 CodePen submission (Arrays and Strings Lab)')
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

    result = grade_ch7_8(lines, code_js)
    if args.out == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
