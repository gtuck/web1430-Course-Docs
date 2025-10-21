#!/usr/bin/env python3
"""
Standardize Markdown produced from Canvas HTML exports:

- Insert a top-level H1 using the HTML <title> when missing.
- Normalize any 'Objective' heading to '## Objective'.
- Collapse 3+ blank lines to at most 2.

Usage:
  python scripts/format_markdown.py
"""

from __future__ import annotations

import os
import re
from typing import Optional


def read_file(p: str) -> str:
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def write_file(p: str, s: str) -> None:
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def extract_html_title(html: str) -> Optional[str]:
    # A permissive extraction of <title>...</title> (single line ok)
    m = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    # Unescape common entities
    title = m.group(1).strip()
    try:
        from html import unescape
        title = unescape(title)
    except Exception:
        pass
    return title


def ensure_h1(md_text: str, title: Optional[str]) -> str:
    if not title:
        return md_text

    # Find first non-empty line
    lines = md_text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1

    if i < len(lines) and lines[i].lstrip().startswith('#'):
        # Has a heading; only keep if it already matches the title as H1
        current = lines[i].lstrip()
        if current == f"# {title}":
            return md_text
        # Otherwise, insert H1 above existing heading
        new_lines = lines[:i] + [f"# {title}", ""] + lines[i:]
        return "\n".join(new_lines) + ("\n" if md_text.endswith("\n") else "\n")

    # If the first non-empty line equals the title, convert to H1
    if i < len(lines) and lines[i].strip() == title:
        lines[i] = f"# {title}"
        return "\n".join(lines) + ("\n" if md_text.endswith("\n") else "\n")

    # Otherwise, insert H1 at top
    new_lines = lines[:i] + [f"# {title}", ""] + lines[i:]
    return "\n".join(new_lines) + ("\n" if md_text.endswith("\n") else "\n")


def normalize_objective_heading(md_text: str) -> str:
    out_lines = []
    for line in md_text.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"\*\*Objective\*\*:?", stripped):
            out_lines.append("## Objective")
            continue
        if re.fullmatch(r"#{1,6}\s*Objective:?", stripped):
            out_lines.append("## Objective")
            continue
        out_lines.append(line)
    text = "\n".join(out_lines)
    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text if text.endswith("\n") else text + "\n"


def _is_code_fence(line: str) -> bool:
    return line.strip().startswith("```")


def _is_heading(line: str) -> bool:
    s = line.lstrip()
    return s.startswith("#") and not s.startswith("#") and False  # placeholder


def _heading_level_and_text(line: str):
    s = line.lstrip()
    if not s.startswith('#'):
        return 0, None
    m = re.match(r"^(#+)\s*(.*?)\s*$", s)
    if not m:
        return 0, None
    level = len(m.group(1))
    text = m.group(2)
    return level, text


def normalize_headings_and_sections(md_text: str) -> str:
    lines = md_text.splitlines()
    out = []
    in_code = False
    for line in lines:
        if _is_code_fence(line):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        level, text = _heading_level_and_text(line)
        if level >= 2 and text:
            t = text.strip().rstrip(':')
            tl = t.lower()
            if tl == 'objective':
                out.append('## Objective')
                continue
            if tl.startswith('instruction'):
                out.append('## Instructions')
                continue
            if ('submission' in tl) or tl in {'submissions', 'what to submit', 'what/how to submit', 'how to submit', 'what & how to submit'}:
                out.append('## What to Submit')
                continue
        out.append(line)
    return "\n".join(out) + ("\n" if not md_text.endswith("\n") else "")


def ensure_description_and_instructions(md_text: str) -> str:
    lines = md_text.splitlines()
    in_code = False
    # Find H1 index
    h1_idx = None
    for i, line in enumerate(lines):
        if _is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        lvl, txt = _heading_level_and_text(line)
        if lvl == 1:
            h1_idx = i
            break
    if h1_idx is None:
        return md_text

    # Check for existing Description and Objective headings
    has_description = False
    has_instructions = False
    has_objective = False
    for line in lines:
        if _is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        lvl, txt = _heading_level_and_text(line)
        if lvl >= 2 and txt:
            t = txt.strip().rstrip(':').lower()
            if t == 'description':
                has_description = True
            elif t == 'instructions':
                has_instructions = True
            elif t == 'objective':
                has_objective = True

    # Ensure Description: wrap intro block after H1 until next heading
    if not has_description:
        # find start after H1 (skip blank)
        i = h1_idx + 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        # find next heading (lvl>=2) or end
        in_code = False
        j = i
        while j < len(lines):
            if _is_code_fence(lines[j]):
                in_code = not in_code
            if not in_code:
                lvl, _ = _heading_level_and_text(lines[j])
                if lvl >= 2:
                    break
            j += 1
        # Insert Description heading above block (even if empty)
        insert_at = i
        # If the block is empty (i == j), still insert heading at i
        lines[insert_at:insert_at] = ['## Description', '']

    # Recompute positions after potential insertion
    md_text2 = "\n".join(lines) + ("\n" if not md_text.endswith("\n") else "")
    lines = md_text2.splitlines()

    # Attempt to split Description block into Description + Instructions if needed
    # Find Description section bounds
    in_code = False
    desc_idx = None
    for i, line in enumerate(lines):
        if _is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        lvl, txt = _heading_level_and_text(line)
        if lvl >= 2 and txt and txt.strip().lower() == 'description':
            desc_idx = i
            break
    if desc_idx is not None:
        desc_start = desc_idx + 1
        # find end of description section (next H2+ or end)
        in_code = False
        desc_end = len(lines)
        for j in range(desc_start, len(lines)):
            if _is_code_fence(lines[j]):
                in_code = not in_code
                continue
            if in_code:
                continue
            lvl, _ = _heading_level_and_text(lines[j])
            if lvl >= 2:
                desc_end = j
                break
        # If there is no Instructions section, try to split when encountering lists/code/examples
        if not has_instructions:
            in_code = False
            split_idx = None
            for j in range(desc_start, desc_end):
                line = lines[j]
                if _is_code_fence(line):
                    # Starting a code block can mark the beginning of instructions
                    prev_in_code = in_code
                    in_code = not in_code
                    if (not prev_in_code) and split_idx is None and j > desc_start:
                        split_idx = j
                    continue
                if in_code:
                    continue
                if re.match(r"\s*([-*]\s+|\d+[\.)]\s+)", line):
                    split_idx = j
                    break
                if re.match(r"\s*###\s+", line):
                    split_idx = j
                    break
                if re.match(r"\s*(Sample|Example) output:\s*$", line, re.IGNORECASE):
                    split_idx = j
                    break
            if split_idx is not None and split_idx > desc_start:
                # Insert Objective (empty) immediately before instructions start
                if not has_objective:
                    lines[split_idx:split_idx] = ['## Objective', '']
                    has_objective = True
                    split_idx += 2
                    desc_end += 2
                # Insert Instructions heading at split point
                lines[split_idx:split_idx] = ['## Instructions', '']
                has_instructions = True
                # Update desc_end after insertion
                if desc_end >= split_idx:
                    desc_end += 2
        # Ensure Objective heading exists if still missing (no split point)
        if not has_objective:
            # Insert '## Objective' just before the next section (desc_end)
            lines[desc_end:desc_end] = ['## Objective', '']

    # Final pass: if Objective ended up after Instructions and is empty, move it above Instructions
    in_code = False
    obj_idx = ins_idx = None
    for i, line in enumerate(lines):
        if _is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        lvl, txt = _heading_level_and_text(line)
        if lvl >= 2 and txt:
            t = txt.strip().lower()
            if t == 'objective' and obj_idx is None:
                obj_idx = i
            elif t == 'instructions' and ins_idx is None:
                ins_idx = i
        if obj_idx is not None and ins_idx is not None:
            break
    if obj_idx is not None and ins_idx is not None and obj_idx > ins_idx:
        # Determine if Objective section is empty (no non-blank text until next H2)
        in_code = False
        next_h2 = len(lines)
        for j in range(obj_idx + 1, len(lines)):
            if _is_code_fence(lines[j]):
                in_code = not in_code
                continue
            if in_code:
                continue
            lvl, _ = _heading_level_and_text(lines[j])
            if lvl >= 2:
                next_h2 = j
                break
        has_content = any(l.strip() for l in lines[obj_idx + 1:next_h2])
        if not has_content:
            block = lines[obj_idx:next_h2]
            del lines[obj_idx:next_h2]
            # Insert above Instructions
            lines[ins_idx:ins_idx] = block

    # Guarantee an Instructions heading exists
    in_code = False
    has_instructions = False
    for line in lines:
        if _is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        lvl, txt = _heading_level_and_text(line)
        if lvl >= 2 and txt and txt.strip().lower() == 'instructions':
            has_instructions = True
            break
    if not has_instructions:
        # Insert after Objective block if present, else at end
        in_code = False
        obj_idx = None
        for i, line in enumerate(lines):
            if _is_code_fence(line):
                in_code = not in_code
                continue
            if in_code:
                continue
            lvl, txt = _heading_level_and_text(line)
            if lvl >= 2 and txt and txt.strip().lower() == 'objective':
                obj_idx = i
                break
        if obj_idx is not None:
            # Find end of objective block
            in_code = False
            end_idx = len(lines)
            for j in range(obj_idx + 1, len(lines)):
                if _is_code_fence(lines[j]):
                    in_code = not in_code
                    continue
                if in_code:
                    continue
                lvl, _ = _heading_level_and_text(lines[j])
                if lvl >= 2:
                    end_idx = j
                    break
            lines[end_idx:end_idx] = ['## Instructions', '']
        else:
            lines.extend(['', '## Instructions', ''])

    return "\n".join(lines) + ("\n" if not md_text.endswith("\n") else "")


def ensure_what_to_submit(md_text: str) -> str:
    lines = md_text.splitlines()
    in_code = False
    has_wts = False
    # Normalize or detect existing
    for line in lines:
        if _is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        lvl, txt = _heading_level_and_text(line)
        if lvl >= 2 and txt and txt.strip().lower().startswith('what to submit'):
            has_wts = True
            break
    # Promote numbered list Submission item to What to Submit heading if present
    if not has_wts:
        promoted = False
        new_lines = []
        in_code2 = False
        for i, line in enumerate(lines):
            if _is_code_fence(line):
                in_code2 = not in_code2
                new_lines.append(line)
                continue
            if not in_code2:
                if re.match(r"\s*\d+[\.)]\s*.*submission.*$", line, flags=re.IGNORECASE):
                    new_lines.append('## What to Submit')
                    promoted = True
                    continue
            new_lines.append(line)
        if promoted:
            lines = new_lines
            has_wts = True

    if has_wts:
        # Also dedupe any accidental duplicate What to Submit headings
        lines2 = []
        in_code2 = False
        seen = False
        i = 0
        while i < len(lines):
            line = lines[i]
            if _is_code_fence(line):
                in_code2 = not in_code2
                lines2.append(line)
                i += 1
                continue
            if not in_code2:
                lvl, txt = _heading_level_and_text(line)
                if lvl >= 2 and txt and txt.strip().lower().startswith('what to submit'):
                    if seen:
                        # Skip this heading and a single following blank line if present
                        i += 1
                        if i < len(lines) and not lines[i].strip():
                            i += 1
                        continue
                    seen = True
            lines2.append(line)
            i += 1
        return "\n".join(lines2) + ("\n" if not md_text.endswith("\n") else "")

    # Find a suitable spot where a "Submit the URL" line exists and insert heading above it
    in_code = False
    for idx, line in enumerate(lines):
        if _is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.search(r"(?i)\bsubmit\b.*\b(codepen|codepen\.io)\b", line):
            # Insert heading above this line if not already preceded by a heading
            ins = idx
            # Avoid if previous non-blank line is a heading already
            k = idx - 1
            while k >= 0 and not lines[k].strip():
                k -= 1
            lvl, _ = _heading_level_and_text(lines[k]) if k >= 0 else (0, None)
            if lvl < 2:
                lines[ins:ins] = ['## What to Submit', '']
                return "\n".join(lines) + ("\n" if not md_text.endswith("\n") else "")
            else:
                # Already under some heading; leave as-is
                return md_text

    # If still not present, append a consistent section with standard guidance
    lines.append('')
    lines.append('## What to Submit')
    lines.append('')
    lines.append('Submit the URL to your CodePen.')
    return "\n".join(lines) + ("\n" if not md_text.endswith("\n") else "")


def process_pair(html_path: str, md_path: str) -> None:
    html = read_file(html_path)
    title = extract_html_title(html)
    md = read_file(md_path)
    md1 = ensure_h1(md, title)
    md2 = normalize_objective_heading(md1)
    md3 = normalize_headings_and_sections(md2)
    md4 = ensure_description_and_instructions(md3)
    md5 = ensure_what_to_submit(md4)
    final = md5
    if final != md:
        write_file(md_path, final)


def main() -> int:
    root = os.getcwd()
    export_dir = os.path.join(root, "Canvas Export")
    if not os.path.isdir(export_dir):
        print(f"Canvas Export directory not found: {export_dir}")
        return 1

    for name in os.listdir(export_dir):
        if not name.lower().endswith(".md"):
            continue
        base = os.path.splitext(name)[0]
        html_path = os.path.join(export_dir, base + ".html")
        md_path = os.path.join(export_dir, name)
        if os.path.isfile(html_path):
            process_pair(html_path, md_path)

    print("Formatting completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
