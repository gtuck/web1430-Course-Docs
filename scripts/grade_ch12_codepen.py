#!/usr/bin/env python3
from __future__ import annotations

"""
Automated grader for Ch. 12: Personal Portfolio (25 pts)

Rubric mapping:
- Customized header and tagline (5)
- About section with personal bio and image (5)
- Projects grid with personalized cards (5)
- Footer/contact links to real destinations (5)
- Styling polish and interactive JS (5)

Usage:
  python scripts/grade_ch12_codepen.py --url https://codepen.io/<user>/pen/<slug>
  python scripts/grade_ch12_codepen.py --html path/to/index.html --css path/to/styles.css --js path/to/script.js
"""

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

import grade_ch1_codepen as common


# Placeholder phrases from the starter template to detect whether the student updated content.
PLACEHOLDER_HEADER = "your name"
PLACEHOLDER_TAGLINE = "your title or tagline"
PLACEHOLDER_ABOUT_SNIPPETS = [
    "introduce yourself with a brief bio",
]
PLACEHOLDER_CARD_TITLES = {
    "highlight one",
    "highlight two",
    "highlight three",
}
PLACEHOLDER_CARD_BODIES = [
    "describe a project",
    "use consistent formatting",
    "add more cards if you have additional items to showcase",
]
PLACEHOLDER_LINK_TOKENS = [
    "yourhandle",
    "you@example.com",
    "example.com",
    "placeholder",
]
DEFAULT_CSS_COLORS = {
    "#fafafa",
    "#333",
    "#003366",
    "#f0f4f8",
}


def load_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class PortfolioHTMLParser(HTMLParser):
    """Lightweight HTML parser to extract portfolio metrics when grading from files."""

    def __init__(self) -> None:
        super().__init__()
        self.metrics: Dict[str, Any] = {
            "header_text": "",
            "tagline": "",
            "header_placeholder": False,
            "tagline_placeholder": False,
            "about_text_chunks": [],
            "about_img_src": "",
            "about_img_alt": "",
            "about_img_placeholder": False,
            "has_grid_class": False,
            "card_titles": [],
            "card_descriptions": [],
            "card_placeholder_count": 0,
            "card_placeholder_descriptions": 0,
            "card_count": 0,
            "footer_links": [],
        }
        self._stack: List[str] = []
        self._in_header = False
        self._in_header_h1 = False
        self._in_header_p = False
        self._in_about = False
        self._in_about_p = False
        self._in_projects = False
        self._in_card = False
        self._in_card_h3 = False
        self._in_card_p = False
        self._current_link: Optional[Dict[str, str]] = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        attrs_dict = {k.lower(): (v or "") for k, v in attrs}
        self._stack.append(tag.lower())

        if tag == "header":
            self._in_header = True
        elif self._in_header and tag == "h1":
            self._in_header_h1 = True
        elif self._in_header and tag == "p":
            self._in_header_p = True

        if tag == "section":
            section_id = attrs_dict.get("id", "").lower()
            if section_id == "about":
                self._in_about = True
            elif section_id == "projects":
                self._in_projects = True

        if self._in_about and tag == "p":
            self._in_about_p = True
        if self._in_about and tag == "img" and not self.metrics["about_img_src"]:
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            self.metrics["about_img_src"] = src
            self.metrics["about_img_alt"] = alt
            self.metrics["about_img_placeholder"] = "placeholder.com" in src.lower()

        if self._in_projects and tag == "div":
            class_attr = attrs_dict.get("class", "")
            classes = {c.strip().lower() for c in class_attr.split()}
            if "grid" in classes:
                self.metrics["has_grid_class"] = True
            if "card" in classes:
                self._in_card = True
                self.metrics["card_count"] += 1
                self.metrics["card_titles"].append("")
                self.metrics["card_descriptions"].append("")

        if self._in_card and tag == "h3":
            self._in_card_h3 = True
        if self._in_card and tag == "p":
            self._in_card_p = True

        if tag == "footer":
            # nothing to do here beyond tracking with stack
            pass

        if tag == "a" and "footer" in self._stack:
            link = {
                "href": attrs_dict.get("href", ""),
                "text": "",
            }
            self.metrics["footer_links"].append(link)
            self._current_link = link

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        while self._stack and self._stack[-1] != tag:
            self._stack.pop()
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

        if tag == "header":
            self._in_header = False
        elif tag == "h1":
            self._in_header_h1 = False
        elif tag == "p" and self._in_header_p:
            self._in_header_p = False

        if tag == "section":
            self._in_about = False
            self._in_projects = False
            self._in_about_p = False

        if tag == "p" and self._in_about_p:
            self._in_about_p = False

        if tag == "div" and self._in_card:
            self._in_card = False
            self._in_card_h3 = False
            self._in_card_p = False

        if tag == "h3":
            self._in_card_h3 = False
        if tag == "p" and self._in_card_p:
            self._in_card_p = False

        if tag == "a":
            self._current_link = None

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return

        lowered = text.lower()

        if self._in_header_h1:
            current = self.metrics["header_text"]
            combined = normalize_whitespace((current + " " + text).strip())
            self.metrics["header_text"] = combined
            if PLACEHOLDER_HEADER in combined.lower():
                self.metrics["header_placeholder"] = True

        elif self._in_header_p:
            current = self.metrics["tagline"]
            combined = normalize_whitespace((current + " " + text).strip())
            self.metrics["tagline"] = combined
            if PLACEHOLDER_TAGLINE in combined.lower():
                self.metrics["tagline_placeholder"] = True

        elif self._in_about_p:
            self.metrics["about_text_chunks"].append(text)

        elif self._in_card_h3 and self.metrics["card_titles"]:
            idx = len(self.metrics["card_titles"]) - 1
            current = self.metrics["card_titles"][idx]
            combined = normalize_whitespace((current + " " + text).strip())
            self.metrics["card_titles"][idx] = combined
            if combined.lower() in PLACEHOLDER_CARD_TITLES:
                self.metrics["card_placeholder_count"] += 1

        elif self._in_card_p and self.metrics["card_descriptions"]:
            idx = len(self.metrics["card_descriptions"]) - 1
            current = self.metrics["card_descriptions"][idx]
            combined = normalize_whitespace((current + " " + text).strip())
            self.metrics["card_descriptions"][idx] = combined
            lowered_desc = combined.lower()
            if any(snippet in lowered_desc for snippet in PLACEHOLDER_CARD_BODIES):
                self.metrics["card_placeholder_descriptions"] += 1

        if self._current_link is not None:
            current = self._current_link["text"]
            self._current_link["text"] = normalize_whitespace((current + " " + text).strip())


def finalize_metrics(parsed: Dict[str, Any]) -> Dict[str, Any]:
    about_text = normalize_whitespace(" ".join(parsed.get("about_text_chunks", [])))
    about_words = len([w for w in about_text.split() if w])
    about_placeholder = any(snippet in about_text.lower() for snippet in PLACEHOLDER_ABOUT_SNIPPETS)
    return {
        "header_text": parsed.get("header_text", ""),
        "tagline": parsed.get("tagline", ""),
        "header_placeholder": bool(parsed.get("header_placeholder", False)),
        "tagline_placeholder": bool(parsed.get("tagline_placeholder", False)),
        "about_text": about_text,
        "about_words": about_words,
        "about_placeholder": about_placeholder,
        "about_img_src": parsed.get("about_img_src", ""),
        "about_img_alt": parsed.get("about_img_alt", ""),
        "about_img_placeholder": bool(parsed.get("about_img_placeholder", False)),
        "has_grid_class": bool(parsed.get("has_grid_class", False)),
        "card_titles": parsed.get("card_titles", []),
        "card_descriptions": parsed.get("card_descriptions", []),
        "card_count": int(parsed.get("card_count", 0)),
        "card_placeholder_count": int(parsed.get("card_placeholder_count", 0)),
        "card_placeholder_descriptions": int(parsed.get("card_placeholder_descriptions", 0)),
        "footer_links": parsed.get("footer_links", []),
    }


def analyze_html_structure(html_text: str) -> Dict[str, Any]:
    parser = PortfolioHTMLParser()
    parser.feed(html_text)
    return finalize_metrics(parser.metrics)


def capture_dom_snapshot(url: str, timeout: float = 12.0) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[str], List[str], Optional[str]]:
    """Load the CodePen page with Playwright and extract DOM metrics, HTML, and CSS."""
    sync_playwright = common.try_import_playwright()
    if not sync_playwright:
        return None, None, None, [], "Playwright not available. Install with: pip install playwright"

    steps: List[str] = []
    error: Optional[str] = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            except Exception as nav_exc:  # pragma: no cover - navigation errors captured for diagnostics
                error = f"navigate: {nav_exc}"
                context.close()
                browser.close()
                return None, None, None, steps, error

            page.wait_for_timeout(500)
            try:
                page.evaluate(
                    """
                    () => {
                        const runButtons = [
                            'button[title="Run"]',
                            'button[aria-label="Run"]',
                            'button:has-text("Run")',
                            'button.run-button'
                        ];
                        for (const sel of runButtons) {
                            const btn = document.querySelector(sel);
                            if (btn) {
                                btn.click();
                                break;
                            }
                        }
                    }
                    """
                )
            except Exception:
                pass

            page.wait_for_timeout(400)

            metrics: Optional[Dict[str, Any]] = None
            try:
                metrics = page.evaluate(
                    """
                    () => {
                        const normalize = (value) => {
                            if (!value) return "";
                            return value.replace(/\\s+/g, " ").trim();
                        };
                        const header = document.querySelector("header h1");
                        const tagline = document.querySelector("header p");
                        const about = document.querySelector("#about p");
                        const aboutText = normalize(about ? about.textContent : "");
                        const aboutWords = aboutText ? aboutText.split(/\\s+/).filter(Boolean).length : 0;
                        const aboutImg = document.querySelector("#about img");
                        const cards = Array.from(document.querySelectorAll("#projects .card"));
                        const footerLinks = Array.from(document.querySelectorAll("footer a")).map((a) => ({
                            href: a.getAttribute("href") || "",
                            text: normalize(a.textContent || "")
                        }));
                        const cardTitles = cards.map((card) => {
                            const t = card.querySelector("h3");
                            return normalize(t ? t.textContent : "");
                        });
                        const cardDescriptions = cards.map((card) => {
                            const p = card.querySelector("p");
                            return normalize(p ? p.textContent : "");
                        });
                        const placeholderTitles = cardTitles.filter((title) =>
                            ["highlight one","highlight two","highlight three"].includes(title.toLowerCase())
                        ).length;
                        const placeholderBodies = cardDescriptions.filter((body) => {
                            const lower = body.toLowerCase();
                            return lower.includes("describe a project") ||
                                   lower.includes("use consistent formatting") ||
                                   lower.includes("add more cards if you have additional items to showcase");
                        }).length;
                        return {
                            header_text: normalize(header ? header.textContent : ""),
                            tagline: normalize(tagline ? tagline.textContent : ""),
                            header_placeholder: header ? header.textContent.toLowerCase().includes("your name") : false,
                            tagline_placeholder: tagline ? tagline.textContent.toLowerCase().includes("your title or tagline") : false,
                            about_text: aboutText,
                            about_words: aboutWords,
                            about_placeholder: aboutWords === 0 ? false : aboutText.toLowerCase().includes("introduce yourself with a brief bio"),
                            about_img_src: aboutImg ? aboutImg.getAttribute("src") || "" : "",
                            about_img_alt: aboutImg ? aboutImg.getAttribute("alt") || "" : "",
                            about_img_placeholder: aboutImg ? (aboutImg.getAttribute("src") || "").toLowerCase().includes("placeholder.com") : false,
                            has_grid_class: !!document.querySelector("#projects .grid"),
                            card_titles: cardTitles,
                            card_descriptions: cardDescriptions,
                            card_count: cards.length,
                            card_placeholder_count: placeholderTitles,
                            card_placeholder_descriptions: placeholderBodies,
                            footer_links: footerLinks,
                        };
                    }
                    """
                )
                steps.append("dom")
            except Exception as e:  # pragma: no cover - evaluation failures captured for diagnostics
                error = f"metrics: {e}"

            html_text = ""
            css_text = ""

            try:
                html_text = page.evaluate("() => document.documentElement.outerHTML || ''")
            except Exception:
                pass

            try:
                css_text = page.evaluate(
                    """
                    () => {
                        const chunks = [];
                        const sheets = Array.from(document.styleSheets || []);
                        for (const sheet of sheets) {
                            try {
                                const rules = sheet.cssRules || [];
                                for (const rule of Array.from(rules)) {
                                    chunks.push(rule.cssText);
                                }
                            } catch (err) {
                                if (sheet.ownerNode && sheet.ownerNode.tagName === "STYLE") {
                                    chunks.push(sheet.ownerNode.textContent || "");
                                }
                            }
                        }
                        return chunks.join("\\n");
                    }
                    """
                )
            except Exception:
                pass

            context.close()
            browser.close()
            return metrics, html_text, css_text, steps, error
    except Exception as outer_exc:  # pragma: no cover - top-level Playwright failures
        return None, None, None, steps, str(outer_exc)


def detect_css_customization(css_text: Optional[str]) -> Tuple[bool, List[str]]:
    if not css_text:
        return False, ["No CSS captured"]
    css_lower = css_text.lower()
    reasons: List[str] = []
    color_tokens = {token for token in re.findall(r"#[0-9a-f]{3,6}", css_lower)}
    custom_colors = sorted(token for token in color_tokens if token not in DEFAULT_CSS_COLORS)
    if custom_colors:
        reasons.append(f"custom colors: {', '.join(custom_colors)}")
    if ".card:hover" in css_lower:
        reasons.append("card hover styling")
    if "@media" in css_lower:
        reasons.append("media queries")
    if "linear-gradient" in css_lower or "background-image" in css_lower:
        reasons.append("gradient/background-image")
    if "box-shadow" in css_lower and "0 2px 4px rgba(0, 0, 0, 0.1)" not in css_lower:
        reasons.append("custom box-shadow")
    customized = bool(reasons)
    if not customized:
        reasons.append("No evident custom styles beyond starter palette")
    return customized, reasons


def detect_js_interactivity(js_code: Optional[str]) -> Tuple[bool, List[str]]:
    if not js_code:
        return False, ["No JS captured"]
    js_lower = js_code.lower()
    reasons: List[str] = []
    if "addEventListener" in js_code:
        if ".card" in js_lower or "card" in js_lower:
            reasons.append("addEventListener on cards")
        if "mouseover" in js_lower or "mouseenter" in js_lower:
            reasons.append("mouse hover listener")
        if "click" in js_lower or "scroll" in js_lower:
            reasons.append("interactive event handler")
    if "gsap" in js_lower or "anime" in js_lower:
        reasons.append("animation library usage")
    interactive = bool(reasons)
    if not interactive and "console.log" in js_lower:
        reasons.append("Only console logs detected")
    return interactive, reasons


def link_is_valid(link: Dict[str, str]) -> bool:
    href = (link.get("href") or "").strip()
    text = (link.get("text") or "").strip()
    if not href:
        return False
    lower_href = href.lower()
    if lower_href in {"#", "javascript:void(0)", "javascript:;"}:
        return False
    if any(token in lower_href for token in PLACEHOLDER_LINK_TOKENS):
        return False
    if lower_href.startswith(("http://", "https://", "mailto:", "tel:")):
        return True
    # allow in-page hash links only if accompanied by descriptive text
    if lower_href.startswith("#") and text:
        return True
    return False


def check_header(metrics: Dict[str, Any]) -> Tuple[int, int, str]:
    header = metrics.get("header_text", "").strip()
    tagline = metrics.get("tagline", "").strip()
    header_placeholder = metrics.get("header_placeholder", False) or header.lower() == PLACEHOLDER_HEADER
    tagline_placeholder = metrics.get("tagline_placeholder", False) or tagline.lower() == PLACEHOLDER_TAGLINE
    header_ok = bool(header) and not header_placeholder and len(header.split()) >= 2
    tagline_ok = bool(tagline) and not tagline_placeholder
    if header_ok and tagline_ok:
        return 5, 5, f"Header '{header}' and tagline present."
    if header_ok or tagline_ok:
        return 3, 5, f"header_ok={header_ok}, tagline_ok={tagline_ok}"
    return 0, 5, "Header and tagline still look like placeholders."


def check_about(metrics: Dict[str, Any]) -> Tuple[int, int, str]:
    about_words = int(metrics.get("about_words", 0))
    about_placeholder = bool(metrics.get("about_placeholder", False))
    img_src = metrics.get("about_img_src", "")
    img_placeholder = bool(metrics.get("about_img_placeholder", False))
    has_img = bool(img_src)
    criteria_met = []
    if about_words >= 20 and not about_placeholder:
        criteria_met.append(f"bio length {about_words} words")
    elif about_words >= 12:
        criteria_met.append(f"bio length {about_words} words (partial)")
    if has_img and not img_placeholder:
        criteria_met.append("custom photo/graphic")
    elif has_img:
        criteria_met.append("image present but placeholder URL")

    if about_words >= 20 and not about_placeholder and has_img and not img_placeholder:
        return 5, 5, "; ".join(criteria_met)
    if (about_words >= 12 and not about_placeholder) or (has_img and not img_placeholder):
        return 3, 5, "; ".join(criteria_met) if criteria_met else "Partial bio customization."
    if about_words >= 8 or has_img:
        return 2, 5, "; ".join(criteria_met) if criteria_met else "Minimal about section detected."
    return 0, 5, "About section is missing, extremely short, or still template text."


def check_projects(metrics: Dict[str, Any]) -> Tuple[int, int, str]:
    card_count = int(metrics.get("card_count", 0))
    placeholder_titles = int(metrics.get("card_placeholder_count", 0))
    placeholder_texts = int(metrics.get("card_placeholder_descriptions", 0))
    if card_count >= 3 and placeholder_titles == 0 and placeholder_texts == 0:
        return 5, 5, f"{card_count} project cards with custom titles/descriptions."
    if card_count >= 3:
        return 3, 5, f"{card_count} cards detected but {placeholder_titles + placeholder_texts} still look like template."
    if card_count >= 2:
        return 2, 5, f"Only {card_count} cards detected."
    return 0, 5, "Could not find three project cards."


def check_contact(metrics: Dict[str, Any]) -> Tuple[int, int, str]:
    links = metrics.get("footer_links", [])
    valid_links = [link for link in links if link_is_valid(link)]
    if len(valid_links) >= 2:
        return 5, 5, f"{len(valid_links)} real contact links found."
    if len(valid_links) == 1:
        return 3, 5, "Only one valid contact link detected."
    if links:
        return 1, 5, "Footer links present but still placeholders."
    return 0, 5, "No footer/contact links detected."


def check_polish(css_text: Optional[str], js_code: Optional[str]) -> Tuple[int, int, str]:
    css_customized, css_reasons = detect_css_customization(css_text)
    js_interactive, js_reasons = detect_js_interactivity(js_code)
    reasons = []
    if css_reasons:
        reasons.append("CSS: " + "; ".join(css_reasons))
    if js_reasons:
        reasons.append("JS: " + "; ".join(js_reasons))

    if css_customized and js_interactive:
        return 5, 5, " | ".join(reasons)
    if css_customized or js_interactive:
        return 3, 5, " | ".join(reasons)
    return 0, 5, " | ".join(reasons) if reasons else "No styling or interactivity evidence captured."


def grade_ch12(metrics: Dict[str, Any], css_text: Optional[str], js_code: Optional[str], console_lines: List[str]) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    total = 0

    def add(name: str, result: Tuple[int, int, str]) -> None:
        nonlocal total
        score, out_of, reason = result
        checks.append({"name": name, "score": score, "out_of": out_of, "reason": reason})
        total += score

    add("Header + tagline customized", check_header(metrics))
    add("About section personalized", check_about(metrics))
    add("Project cards populated", check_projects(metrics))
    add("Footer/contact links active", check_contact(metrics))
    add("Styling & interactivity polish", check_polish(css_text, js_code))

    return {
        "total": total,
        "possible": 25,
        "checks": checks,
        "meta": {
            "captured_lines": len(console_lines),
            "code_available": bool(js_code),
            "css_available": bool(css_text),
            "html_available": bool(metrics),
            "about_words": metrics.get("about_words", 0),
            "card_count": metrics.get("card_count", 0),
        },
        "console_preview": console_lines[:30],
    }


def format_text_report(result: Dict[str, Any]) -> str:
    lines = [f"Total: {result['total']} / {result['possible']}", ""]
    for check in result.get("checks", []):
        status = "OK" if check["score"] == check["out_of"] else ("PARTIAL" if check["score"] > 0 else "MISS")
        lines.append(f"- {check['name']}: {check['score']}/{check['out_of']} [{status}] - {check['reason']}")
    lines.append("")
    meta = result.get("meta", {})
    lines.append(f"Captured console lines: {meta.get('captured_lines', 0)}")
    lines.append(f"JS code available: {meta.get('code_available', False)}")
    lines.append(f"CSS captured: {meta.get('css_available', False)}")
    lines.append(f"HTML metrics captured: {meta.get('html_available', False)}")
    if result.get("console_preview"):
        lines.append("")
        lines.append("Console preview (first 30 lines):")
        for line in result["console_preview"]:
            lines.append(f"  {line}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Grade Ch. 12 CodePen submission (Personal Portfolio)")
    parser.add_argument("--url", help="CodePen URL")
    parser.add_argument("--html", help="Path to exported HTML snippet")
    parser.add_argument("--css", help="Path to CSS file used in the pen")
    parser.add_argument("--js", help="Path to JS file used in the pen")
    parser.add_argument("--timeout", type=float, default=12.0, help="Seconds to wait when loading a URL")
    parser.add_argument("--out", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    metrics: Optional[Dict[str, Any]] = None
    css_text: Optional[str] = None
    js_code: Optional[str] = None
    html_text: Optional[str] = None
    console_lines: List[str] = []
    attempts: List[str] = []
    errors: List[str] = []

    if args.html:
        if not os.path.exists(args.html):
            print(f"Error: HTML file not found: {args.html}", file=sys.stderr)
            return 2
        html_text = load_text_file(args.html)
        metrics = analyze_html_structure(html_text)

    if args.css:
        if not os.path.exists(args.css):
            print(f"Error: CSS file not found: {args.css}", file=sys.stderr)
            return 2
        css_text = load_text_file(args.css)

    if args.js:
        if not os.path.exists(args.js):
            print(f"Error: JS file not found: {args.js}", file=sys.stderr)
            return 2
        js_code = load_text_file(args.js)

    if args.url:
        try:
            lines, js_from_url = common.capture_console_from_codepen(args.url, timeout=args.timeout)
            console_lines = lines
            if js_from_url:
                js_code = js_code or js_from_url
            attempts.append("console")
        except Exception as exc:
            errors.append(f"console: {exc}")

        if metrics is None or css_text is None or html_text is None:
            snap_metrics, html_snap, css_snap, steps, snap_error = capture_dom_snapshot(args.url, timeout=args.timeout)
            attempts.extend(steps)
            if snap_metrics:
                metrics = metrics or snap_metrics
            if html_snap:
                html_text = html_text or html_snap
            if css_snap:
                css_text = css_text or css_snap
            if snap_error:
                errors.append(snap_error)

        if (metrics is None or css_text is None) and args.url:
            debug_url = common.derive_debug_url(args.url)
            if debug_url:
                snap_metrics, html_snap, css_snap, steps, snap_error = capture_dom_snapshot(debug_url, timeout=args.timeout)
                attempts.extend(steps)
                if snap_metrics:
                    metrics = metrics or snap_metrics
                if html_snap:
                    html_text = html_text or html_snap
                if css_snap:
                    css_text = css_text or css_snap
                if snap_error:
                    errors.append(f"debug: {snap_error}")

    if metrics is None:
        print("Error: Could not gather HTML structure metrics. Provide --html or ensure Playwright can load the CodePen URL.", file=sys.stderr)
        if errors:
            print("Details:", "; ".join(errors), file=sys.stderr)
        return 2

    result = grade_ch12(metrics, css_text, js_code, console_lines)
    if attempts:
        result.setdefault("meta", {})["attempt_steps"] = ";".join(attempts)
    if errors:
        result.setdefault("meta", {})["errors"] = "; ".join(errors)

    if args.out == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_text_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
