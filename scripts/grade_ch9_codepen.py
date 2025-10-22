#!/usr/bin/env python3
from __future__ import annotations

"""
Automated grader for Ch. 9: OOP Lab — Classes, Methods, RPG (25 pts)

Rubric mapping:
- Dog class with correct bark() behavior and logs (6)
- Character class: combat flow with attack() and describe() (8)
- Inventory added: appears in description and transfers on defeat (8)
- Account class: array of accounts credited and described (3)
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import grade_ch1_codepen as common


def check_dog(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('class Dog' in code_js and 'bark(' in code_js)
    fang1 = any(re.search(r"Fang\s+is\s+a\s+boarhound\s+dog\s+measuring\s+75", l) for l in lines)
    fang2 = any(re.search(r"Look, a cat!\s+Fang\s+barks:\s+Grrr! Grrr!", l) for l in lines)
    snowy1 = any(re.search(r"Snowy\s+is\s+a\s+terrier\s+dog\s+measuring\s+22", l) for l in lines)
    snowy2 = any(re.search(r"Look, a cat!\s+Snowy\s+barks:\s+Woof! Woof!", l) for l in lines)
    ok = fang1 and fang2 and snowy1 and snowy2
    score = 6 if (code_ok and ok) else (4 if ok else 0)
    return score, 6, f"code_ok={bool(code_ok)}, logs_ok={ok}"


def check_character(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('class Character' in code_js and 'attack(' in code_js and 'describe(' in code_js)
    welcome = any(l.startswith('Welcome to the adventure!') for l in lines)
    has_attack = any('attacks' in l and 'damage points' in l for l in lines)
    has_health = any('health points left' in l for l in lines)
    has_elim = any('eliminated' in l and 'experience points' in l for l in lines)
    desc = any('XP points' in l and 'inventory:' in l for l in lines)
    ok = welcome and has_attack and (has_health or has_elim) and desc
    score = 8 if (code_ok and ok) else (5 if ok else 0)
    return score, 8, f"code_ok={bool(code_ok)}, flow_ok={ok}"


def check_inventory(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('gold' in code_js and 'keys' in code_js and 'inventory' in code_js)
    # Verify that after combat, one of the heroes shows higher gold or keys
    # Heuristic: look for 'inventory: X gold, Y key(s)' lines and see if any line shows >10 gold or >1 keys
    inv_lines = [l for l in lines if 'inventory:' in l and 'gold' in l and 'key(s)' in l]
    gained = False
    for l in inv_lines:
        m = re.search(r"inventory:\s*(\d+)\s+gold,\s*(\d+)\s+key\(s\)\)?", l)
        if m:
            g = int(m.group(1)); k = int(m.group(2))
            if g > 10 or k > 1:
                gained = True
                break
    score = 8 if (code_ok and gained) else (5 if gained else 0)
    return score, 8, f"code_ok={bool(code_ok)}, gained={gained}"


def check_accounts(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    code_ok = code_js and ('class Account' in code_js and 'credit(' in code_js and 'describe(' in code_js)
    expected = {
        'Owner: Sean, balance: 1000',
        'Owner: Brad, balance: 1000',
        'Owner: Georges, balance: 1000',
    }
    logs_ok = expected.issubset(set(l.strip() for l in lines))
    score = 3 if (code_ok and logs_ok) else (2 if logs_ok else 0)
    return score, 3, f"code_ok={bool(code_ok)}, logs_ok={logs_ok}"


def grade_ch9(console_lines: List[str], code_js: Optional[str]) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(name: str, tpl: Tuple[int, int, str]):
        nonlocal total
        score, out_of, reason = tpl
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("Dog class + logs", check_dog(console_lines, code_js))
    add("Character combat flow", check_character(console_lines, code_js))
    add("Inventory in describe + transfer", check_inventory(console_lines, code_js))
    add("Accounts credited + described", check_accounts(console_lines, code_js))

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
    p = argparse.ArgumentParser(description='Grade Ch. 9 CodePen submission (OOP Lab)')
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

    result = grade_ch9(lines, code_js)
    if args.out == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
