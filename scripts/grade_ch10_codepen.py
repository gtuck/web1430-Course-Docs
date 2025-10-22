#!/usr/bin/env python3
from __future__ import annotations

"""
Automated grader for Ch. 10: Batman Movies — Functional Programming Lab (25 pts)

Rubric mapping:
- Pure function design (no mutations; parameters in, values out) (5) [heuristic]
- Titles, post‑2000, unique directors implemented with map/filter (8)
- Counts, earliest/latest, highest/lowest rating (8)
- Averages overall and by director (2)
- Clear console output and organization (2)
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import grade_ch1_codepen as common


def has_functions(code_js: Optional[str], names: List[str]) -> bool:
    if not code_js:
        return False
    return all(n in code_js for n in names)


def check_titles(lines: List[str]) -> Tuple[int, int, str]:
    ok = any(l.startswith('Titles:') for l in lines)
    after = any(l.startswith('After 2000:') for l in lines)
    dirs = any(l.startswith('Directors:') for l in lines)
    score = 8 if (ok and after and dirs) else (4 if (ok and (after or dirs)) else 0)
    return score, 8, f"titles={ok}, after2000={after}, directors={dirs}"


def check_counts_minmax(lines: List[str]) -> Tuple[int, int, str]:
    count = any(l.startswith('Count:') for l in lines)
    earliest = any(l.startswith('Earliest:') for l in lines)
    latest = any(l.startswith('Latest:') for l in lines)
    highest = any(l.startswith('Highest rated:') for l in lines)
    lowest = any(l.startswith('Lowest rated:') for l in lines)
    found = sum([count, earliest, latest, highest, lowest])
    score = 8 if found >= 5 else (5 if found >= 3 else 0)
    return score, 8, f"found={found}"


def check_averages(lines: List[str]) -> Tuple[int, int, str]:
    all_avg = any(l.startswith('Average IMDB rating (all):') for l in lines)
    by_dir = any(l.startswith('Average IMDB rating (') and '):' in l for l in lines)
    score = 2 if (all_avg and by_dir) else (1 if (all_avg or by_dir) else 0)
    return score, 2, f"all={all_avg}, by_dir={by_dir}"


def check_pure_functions(code_js: Optional[str]) -> Tuple[int, int, str]:
    # Heuristic: presence of map/filter/reduce and absence of push/splice on movieList in function bodies
    if not code_js:
        return 0, 5, 'no code'
    uses_hof = any(k in code_js for k in ['.map(', '.filter(', '.reduce('])
    mutates = any(k in code_js for k in ['.push(', '.splice('])
    score = 5 if (uses_hof and not mutates) else (2 if uses_hof else 0)
    return score, 5, f"map/filter/reduce={uses_hof}, mutates={mutates}"


def check_clear_output(lines: List[str]) -> Tuple[int, int, str]:
    labels = ['Titles:', 'After 2000:', 'Directors:', 'Count:', 'Earliest:', 'Latest:', 'Average IMDB rating', 'Highest rated:', 'Lowest rated:', 'Most prolific director:']
    hits = sum(1 for l in lines for lab in labels if l.startswith(lab))
    score = 2 if hits >= 5 else 0
    return score, 2, f"labeled_lines={hits}"


def grade_ch10(console_lines: List[str], code_js: Optional[str]) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(name: str, tpl: Tuple[int, int, str]):
        nonlocal total
        score, out_of, reason = tpl
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("map/filter titles/after2000/directors", check_titles(console_lines))
    add("count/earliest/latest/highest/lowest", check_counts_minmax(console_lines))
    add("averages overall/by director", check_averages(console_lines))
    add("pure functions (heuristic)", check_pure_functions(code_js))
    add("clear labeled output", check_clear_output(console_lines))

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
    p = argparse.ArgumentParser(description='Grade Ch. 10 CodePen submission (Batman FP)')
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

    result = grade_ch10(lines, code_js)
    if args.out == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

