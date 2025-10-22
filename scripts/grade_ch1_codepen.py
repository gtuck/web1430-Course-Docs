#!/usr/bin/env python3
"""
Automated grader for Ch. 1 assignment: Console Skills.

Features:
- Accepts a CodePen URL and captures console output via Playwright (headless Chromium).
- Scores the submission against the rubric in assignments/ch01/index.md (25 pts).
- Optional: grade from a local JS file or a newline-delimited log file (offline mode).

Usage examples:
  python scripts/grade_ch1_codepen.py --url https://codepen.io/<user>/pen/<slug>
  python scripts/grade_ch1_codepen.py --from-logs path/to/console.log
  python scripts/grade_ch1_codepen.py --js path/to/code.js --from-logs path/to/console.log

Notes:
- Playwright is optional; if not installed, you can still grade from logs via --from-logs.
- To install Playwright: pip install playwright && python -m playwright install chromium
- Network access is required to grade from a CodePen URL.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import List, Optional, Tuple, Dict, Any
from urllib.parse import urlparse


def try_import_playwright():
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        return sync_playwright
    except Exception:
        return None


def is_number_line(s: str) -> bool:
    s = s.strip()
    return bool(re.fullmatch(r"-?\d+(?:\.\d+)?", s))


def normalize_line(s: str) -> str:
    return s.strip()


def capture_console_from_codepen(url: str, timeout: float = 10.0) -> Tuple[List[str], Optional[str]]:
    """
    Navigate to the CodePen URL with Playwright, capture console output, and attempt to
    fetch the JS code from the editor page (best effort). Returns (console_lines, js_code or None).
    """
    sync_playwright = try_import_playwright()
    if not sync_playwright:
        raise RuntimeError(
            "Playwright not available. Install with: pip install playwright && python -m playwright install chromium"
        )

    console_lines: List[str] = []
    js_code: Optional[str] = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def on_console(msg):
            # Collect page-level console messages (includes iframes)
            try:
                text = msg.text()
            except Exception:
                text = str(msg)
            console_lines.append(text)

        page.on("console", on_console)

        page.goto(url, wait_until="domcontentloaded")

        # Best-effort: Click a Run button if present to ensure execution
        run_selectors = [
            'button[title="Run"]',
            'button[aria-label="Run"]',
            'button:has-text("Run")',
            'button.run-button',
        ]
        for sel in run_selectors:
            try:
                if page.is_visible(sel):
                    page.click(sel, timeout=1000)
                    break
            except Exception:
                pass

        # Wait a bit to collect console logs
        end = time.time() + timeout
        while time.time() < end:
            time.sleep(0.2)

        # Attempt to extract JS code from the editor page (best effort, may fail)
        # Strategy 1: Next.js data blob
        try:
            handle = page.query_selector('#__NEXT_DATA__')
            if handle:
                data_text = handle.text_content() or ""
                if data_text.strip():
                    try:
                        next_data = json.loads(data_text)
                        # Probe common shapes for embedded code
                        js_code = (
                            next_data.get("props", {})
                            .get("pageProps", {})
                            .get("pen", {})
                            .get("js", None)
                        )
                    except Exception:
                        pass
        except Exception:
            pass

        # Strategy 2: Look for CodeMirror textareas that may mirror JS content
        if not js_code:
            try:
                # A few possible selectors
                candidates = [
                    'textarea#box-js',
                    'textarea[name="js"]',
                    'textarea[data-type="js"]',
                    'div[data-test-id="editor-javascript"] textarea',
                    'div.js textarea',
                    '.CodeMirror textarea',
                ]
                for sel in candidates:
                    el = page.query_selector(sel)
                    if not el:
                        continue
                    val = el.input_value(timeout=500)
                    if val and len(val.strip()) > 0:
                        js_code = val
                        break
            except Exception:
                pass

        # Strategy 3: Execute code in page to try common global stores
        if not js_code:
            try:
                js_code = page.evaluate(
                    """
                    () => {
                        try {
                            // Some CodePen pages may expose store-like globals; probe carefully
                            if (window.__NEXT_DATA__ && window.__NEXT_DATA__.props && window.__NEXT_DATA__.props.pageProps && window.__NEXT_DATA__.props.pageProps.pen) {
                                const pen = window.__NEXT_DATA__.props.pageProps.pen;
                                if (pen && pen.js) return pen.js;
                            }
                        } catch (e) {}
                        return null;
                    }
                    """
                )
            except Exception:
                pass

        # Strategy 4: Inline <script> tags on the page (e.g., debug or full views)
        if not js_code:
            try:
                handles = page.query_selector_all('script')
                best_code = None
                best_score = -1
                for h in handles:
                    try:
                        txt = h.text_content() or ""
                    except Exception:
                        txt = ""
                    if not txt or not txt.strip():
                        continue
                    # Heuristic: prefer scripts with console.log and assignment markers
                    score = 0
                    score += txt.count('console.log')
                    if 'Starting Chapter 1 assignment' in txt:
                        score += 5
                    if "//" in txt:
                        score += 1
                    if "/*" in txt and "*/" in txt:
                        score += 1
                    if score > best_score:
                        best_score = score
                        best_code = txt
                if best_code and best_score >= 1:
                    js_code = best_code
            except Exception:
                pass

        # Strategy 5: Scan all frames for inline <script> tags (some debug views render in frames)
        if not js_code:
            try:
                best_code = None
                best_score = -1
                for frame in page.frames:
                    try:
                        scripts = frame.query_selector_all('script')
                    except Exception:
                        scripts = []
                    for h in scripts:
                        try:
                            txt = h.text_content() or ""
                        except Exception:
                            txt = ""
                        if not txt or not txt.strip():
                            continue
                        score = 0
                        score += txt.count('console.log')
                        if 'Starting Chapter 1 assignment' in txt:
                            score += 5
                        if "//" in txt:
                            score += 1
                        if "/*" in txt and "*/" in txt:
                            score += 1
                        if score > best_score:
                            best_score = score
                            best_code = txt
                if best_code and best_score >= 1:
                    js_code = best_code
            except Exception:
                pass

        context.close()
        browser.close()

    return [normalize_line(l) for l in console_lines if normalize_line(l)], js_code


def derive_debug_url(url: str) -> Optional[str]:
    """Best-effort transform of a CodePen URL to Debug View.
    Examples:
      https://codepen.io/user/pen/slug -> https://cdpn.io/user/debug/slug
      https://codepen.io/user/full/slug -> https://cdpn.io/user/debug/slug
    Returns None if it can't parse.
    """
    try:
        m = re.match(r"^https?://codepen\.io/([^/]+)/(?:(?:pen)|(?:full))/([^/?#]+)", url.strip())
        if m:
            user, slug = m.group(1), m.group(2)
            return f"https://cdpn.io/{user}/debug/{slug}"
    except Exception:
        pass
    return None


def looks_blocked(console_lines: List[str]) -> bool:
    """Heuristic to detect when headless access is blocked by CF or COEP."""
    text = "\n".join(console_lines).lower()
    signals = [
        "cloudflare",
        "private access token",
        "status of 401",
        "status of 403",
        "net::err_blocked_by_response",
        "not same origin",
    ]
    return any(s in text for s in signals)


def simulate_console_with_js(js_code: str, timeout: float = 5.0) -> List[str]:
    """Run the provided JS code in a fresh headless page and capture console lines.
    This provides a fallback when CodePen blocks direct console capture.
    """
    sync_playwright = try_import_playwright()
    if not sync_playwright:
        return []

    lines: List[str] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            def on_console(msg):
                try:
                    text = msg.text()
                except Exception:
                    text = str(msg)
                lines.append(normalize_line(text))

            page.on("console", on_console)
            page.goto("about:blank")

            # Evaluate the user's JS code in the page context.
            page.evaluate(
                """
                (code) => {
                    try {
                        (0, eval)(code);
                    } catch (e) {
                        console.error(String(e && e.message ? e.message : e));
                    }
                }
                """,
                js_code,
            )

            end = time.time() + timeout
            while time.time() < end:
                time.sleep(0.1)

            context.close()
            browser.close()
    except Exception:
        pass
    return [l for l in lines if l]


def load_lines_from_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [normalize_line(l) for l in f.read().splitlines() if normalize_line(l)]


def load_code_from_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check_console_usage(lines: List[str]) -> Tuple[int, int, str]:
    # If anything was printed, assume console.log was used.
    score = 2 if len(lines) > 0 else 0
    reason = f"Captured {len(lines)} console lines."
    return score, 2, reason


def check_number_and_string(lines: List[str]) -> Tuple[int, int, str]:
    has_number = any(is_number_line(l) for l in lines)
    # Any non-numeric line counts as a string demonstration
    has_string = any(not is_number_line(l) for l in lines)
    score = 2 if (has_number and has_string) else 0
    reason = []
    reason.append("Found numeric output" if has_number else "No numeric-only line found")
    reason.append("Found string output" if has_string else "No string line found")
    return score, 2, "; ".join(reason)


def find_line_index(lines: List[str], predicate) -> Optional[int]:
    for i, l in enumerate(lines):
        if predicate(l):
            return i
    return None


def check_quote_style_escaping(lines: List[str], code_js: Optional[str]) -> Tuple[int, int, str]:
    # Console-based heuristic: if output contains both a double-quoted substring and an apostrophe
    # in the same line (e.g., He said, "It's fine."), consider escaping/quote-handling demonstrated.
    # If JS is available, also check for consistent quote usage and presence of escape sequences.
    target_mixed = any(('"' in l and "'" in l) for l in lines)

    js_checks = []
    consistent = None
    has_escape = None
    if code_js:
        # Count single vs double quotes used for string literals (rough heuristic)
        single_lit = len(re.findall(r"'[^'\\]*(?:\\.[^'\\]*)*'", code_js))
        double_lit = len(re.findall(r'"[^"\\]*(?:\\.[^"\\]*)*"', code_js))
        consistent = (single_lit == 0) or (double_lit == 0)
        has_escape = bool(re.search(r"\\['\"]", code_js))
        js_checks.append(f"string literals: single={single_lit}, double={double_lit}")
        js_checks.append(f"has escape: {bool(has_escape)}")

    # Scoring logic:
    # - If JS available and shows consistent quoting and escape usage -> 5/5
    # - Else if console shows mixed quotes in a line (e.g., He said, "It's fine.") -> 5/5
    # - Else -> 0/5
    if code_js is not None:
        if (consistent is True) and (has_escape is True or target_mixed):
            return 5, 5, "Consistent quote style with escapes verified from code."
        elif target_mixed:
            return 5, 5, "Console output demonstrates correct handling of quotes."
        else:
            return 0, 5, "Could not verify consistent quote style and escaping. " + "; ".join(js_checks)
    else:
        if target_mixed:
            return 5, 5, "Console output demonstrates correct handling of quotes."
        return 0, 5, "No JS available; could not verify quoting/escaping beyond console."


def check_arithmetic(lines: List[str]) -> Tuple[int, int, str]:
    # Look for labels and numeric outputs around them.
    # Expect presence of these label lines:
    #  - Next year age:
    #  - Age in months:
    #  - Half age:
    #  - Difference 10 - 3 =
    #  - Product 9 * 7 =
    labels = ["Next year age:", "Age in months:", "Half age:"]

    found = {lab: None for lab in labels}
    for i, l in enumerate(lines):
        if l in found:
            found[l] = i

    numeric_after = []
    for lab, idx in found.items():
        if idx is None:
            continue
        # Check for a numeric line immediately after the label
        if idx + 1 < len(lines) and is_number_line(lines[idx + 1]):
            numeric_after.append(lab)

    # Additional generic patterns for difference/product labels
    diff_idx = None
    prod_idx = None
    for i, l in enumerate(lines):
        if diff_idx is None and re.match(r"^Difference\s+\d+\s*-\s*\d+\s*=\s*$", l):
            diff_idx = i
        if prod_idx is None and re.match(r"^Product\s+\d+\s*\*\s*\d+\s*=\s*$", l):
            prod_idx = i

    # Score heuristics: award 1 point for each operator demonstrated up to 5
    # '+' via Next year age:
    # '-' via Difference X - Y = -> next line numeric
    # '*' via Age in months: or Product X * Y =
    # '/' via Half age:
    score = 0
    reasons = []

    if found["Next year age:"] is not None and ("Next year age:" in numeric_after):
        score += 1
        reasons.append("plus: ok")
    else:
        reasons.append("plus: missing or not followed by number")

    if diff_idx is not None and (diff_idx + 1 < len(lines) and is_number_line(lines[diff_idx + 1])):
        score += 1
        reasons.append("minus: ok")
    else:
        reasons.append("minus: missing or not followed by number")

    mult_ok = False
    if found["Age in months:"] is not None and ("Age in months:" in numeric_after):
        mult_ok = True
    if prod_idx is not None and (prod_idx + 1 < len(lines) and is_number_line(lines[prod_idx + 1])):
        mult_ok = True
    if mult_ok:
        score += 1
        reasons.append("multiply: ok")
    else:
        reasons.append("multiply: missing or not followed by number")

    if found["Half age:"] is not None and ("Half age:" in numeric_after):
        score += 1
        reasons.append("divide: ok")
    else:
        reasons.append("divide: missing or not followed by number")

    # Award a bonus point if at least 4 relevant numeric outputs exist (to total 5 pts)
    # This gives flexibility if student demonstrates an extra arithmetic computation.
    numeric_count = sum(1 for l in lines if is_number_line(l))
    if numeric_count >= 4 and score < 5:
        score += 1
        reasons.append("bonus: sufficient numeric outputs")

    score = min(score, 5)
    return score, 5, "; ".join(reasons)


def check_concat_strings(lines: List[str]) -> Tuple[int, int, str]:
    # Look for friendly message patterns
    hello = any(re.match(r"^Hello,\s+.+!$", l) for l in lines)
    you_are = any(re.match(r"^You are\s+\d+(?:\.\d+)?\s+years old\.$", l) for l in lines)
    next_year = any(re.match(r"^Next year you will be\s+\d+(?:\.\d+)?\s+years old\.$", l) for l in lines)

    # Score: 1 point per pattern found, up to 3
    score = int(hello) + int(you_are) + int(next_year)
    return score, 3, f"hello={hello}, you_are={you_are}, next_year={next_year}"


def check_sequential_execution(lines: List[str]) -> Tuple[int, int, str]:
    idx_a = find_line_index(lines, lambda l: l == "Line A")
    idx_b = find_line_index(lines, lambda l: l == "Line B")
    idx_c = find_line_index(lines, lambda l: l == "Line C")
    if None not in (idx_a, idx_b, idx_c) and idx_a < idx_b < idx_c:
        return 3, 3, "Line A, B, C found in order"
    return 0, 3, "Did not find Line A/B/C in order"


def check_comments(code_js: Optional[str], assume_ok: bool = False) -> Tuple[int, int, str]:
    if not code_js:
        if assume_ok:
            return 3, 3, "Assumed comments present (flag)."
        return 0, 3, "No JS code available to verify comments."
    has_single = "//" in code_js
    has_block = ("/*" in code_js) and ("*/" in code_js)
    score = 0
    if has_single:
        score += 1
    if has_block:
        score += 2
    return score, 3, f"single-line: {has_single}, block: {has_block}"


def check_fix_me(lines: List[str]) -> Tuple[int, int, str]:
    # a) Name: <your name>
    name_ok = any(re.match(r"^Name:\s+.+$", l) for l in lines)

    # b) Age next year printed as a number, either on same line or next line
    age_idx = find_line_index(lines, lambda l: l.startswith("Age next year:"))
    age_ok = False
    if age_idx is not None:
        # Same line numeric at end
        m = re.match(r"^Age next year:\s*(-?\d+(?:\.\d+)?)$", lines[age_idx])
        if m:
            age_ok = True
        # Next line numeric only
        elif age_idx + 1 < len(lines) and is_number_line(lines[age_idx + 1]):
            age_ok = True

    # c) He said, "It's fine."
    said_ok = any(l == 'He said, "It\'s fine."' for l in lines)

    # Score: 1 point if (a) name, 1 point if (b and c) both ok, else 0
    score = 0
    if name_ok:
        score += 1
    if age_ok and said_ok:
        score += 1
    return score, 2, f"name={name_ok}, age_next_year={age_ok}, quote_line={said_ok}"


def grade_ch1(console_lines: List[str], code_js: Optional[str], *, assume_comments_ok: bool = False) -> Dict[str, Any]:
    checks = []
    total = 0
    possible = 25

    def add(check_name: str, fn):
        nonlocal total
        score, out_of, reason = fn
        checks.append({
            "name": check_name,
            "score": score,
            "out_of": out_of,
            "reason": reason,
        })
        total += score

    add("Uses console.log()", check_console_usage(console_lines))
    add("Number and string values", check_number_and_string(console_lines))
    add("Quote style + escaping", check_quote_style_escaping(console_lines, code_js))
    add("Arithmetic + - * /", check_arithmetic(console_lines))
    add("String concatenation with +", check_concat_strings(console_lines))
    add("Sequential execution order", check_sequential_execution(console_lines))
    add("Comments (// and /* */)", check_comments(code_js, assume_ok=assume_comments_ok))
    add("Fix-me mini-exercises", check_fix_me(console_lines))

    return {
        "total": total,
        "possible": possible,
        "checks": checks,
        "meta": {
            "captured_lines": len(console_lines),
            "code_available": bool(code_js),
        },
        "console_preview": console_lines[:50],
    }


def format_text_report(result: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"Total: {result['total']} / {result['possible']}")
    lines.append("")
    for c in result["checks"]:
        name = c["name"]
        score = c["score"]
        out_of = c["out_of"]
        reason = c["reason"]
        status = "OK" if score == out_of else ("PARTIAL" if score > 0 else "MISS")
        lines.append(f"- {name}: {score}/{out_of} [{status}] - {reason}")
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


def summarize_notes(checks: List[Dict[str, Any]]) -> str:
    """Summarize missing/partial rubric items into a single notes string."""
    misses = [c for c in checks if c.get('score', 0) < c.get('out_of', 0)]
    if not misses:
        return "All rubric items satisfied."
    parts = [f"{c['name']}: {c['reason']}" for c in misses]
    # Keep it reasonably short
    return " | ".join(parts)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Grade Ch. 1 CodePen submission")
    p.add_argument("--url", help="CodePen URL", default=None)
    p.add_argument("--timeout", type=float, default=10.0, help="Seconds to capture console output")
    p.add_argument("--from-logs", dest="logs", help="Path to a newline-delimited console log file")
    p.add_argument("--js", dest="js_path", help="Optional path to local JS code for comment/quote checks")
    p.add_argument("--out", choices=["text", "json"], default="text", help="Output format")
    p.add_argument("--assume-comments-ok", action="store_true", help="If JS code is unavailable, award full comment points.")
    args = p.parse_args(argv)

    console_lines: List[str] = []
    code_js: Optional[str] = None

    if args.logs:
        if not os.path.exists(args.logs):
            print(f"Error: log file not found: {args.logs}", file=sys.stderr)
            return 2
        console_lines = load_lines_from_file(args.logs)

    if args.js_path:
        if not os.path.exists(args.js_path):
            print(f"Error: JS file not found: {args.js_path}", file=sys.stderr)
            return 2
        code_js = load_code_from_file(args.js_path)

    if args.url and not console_lines:
        # First attempt: given URL
        try:
            console_lines, js_from_web = capture_console_from_codepen(args.url, timeout=args.timeout)
            if js_from_web:
                code_js = js_from_web
        except Exception as e:
            print(f"Warning: failed to capture from URL: {e}", file=sys.stderr)
            # Try Debug View fallback if parseable
            dbg = derive_debug_url(args.url)
            if dbg:
                print(f"Info: retrying with Debug View: {dbg}", file=sys.stderr)
                try:
                    console_lines, js_from_web = capture_console_from_codepen(dbg, timeout=args.timeout)
                    if js_from_web:
                        code_js = js_from_web
                except Exception as e2:
                    print(f"Warning: debug retry also failed: {e2}", file=sys.stderr)
            if not console_lines:
                print("Hint: Provide --from-logs or ensure Playwright is installed and network is available.", file=sys.stderr)
                return 3

        # If first attempt succeeded but looks blocked (errors only), try Debug View
        if console_lines and not code_js and looks_blocked(console_lines):
            if 'cdpn.io' not in (args.url or ''):
                dbg = derive_debug_url(args.url)
                if dbg:
                    print(f"Info: attempting Debug View due to blocked signals: {dbg}", file=sys.stderr)
                    try:
                        lines2, js2 = capture_console_from_codepen(dbg, timeout=args.timeout)
                        # Prefer the debug capture if it produced more meaningful lines
                        if lines2:
                            console_lines = lines2
                        if js2:
                            code_js = js2
                    except Exception as e3:
                        print(f"Warning: debug attempt failed: {e3}", file=sys.stderr)

    if code_js and (not console_lines or looks_blocked(console_lines)):
        # Fallback: simulate console output by executing JS code in a blank page
        simulated = simulate_console_with_js(code_js)
        if simulated:
            console_lines = simulated

    if not console_lines:
        print("Error: No console lines available. Provide --url or --from-logs.", file=sys.stderr)
        return 2

    result = grade_ch1(console_lines, code_js, assume_comments_ok=args.assume_comments_ok)
    if args.out == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
