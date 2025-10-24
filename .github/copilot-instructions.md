# Copilot instructions for web1430-Course-Docs

This repo is a course documentation site (Markdown + Jekyll) plus Python scripts that automate grading CodePen assignments. Optimize contributions around these two tracks.

## Big picture
- Site: static Jekyll with remote theme `pages-themes/primer@v0.6.0` (`_config.yml`) and a simple layout (`_layouts/default.html`). Primary content lives in Markdown.
- Content structure:
  - `index.md` — Syllabus (primary landing page)
  - `schedule.md` — Class schedule (single source of truth for the schedule table)
  - `assignments/chXX/index.md` — Per‑chapter assignment pages
  - `Interviews/*.md`, `images/` — Additional content and assets
- Grading automation (`scripts/`): per‑chapter graders and batch tools that parse Canvas exports, capture CodePen console output (Playwright), and score against rubrics.
- Data flow for grading:
  1) Canvas submission HTML → `scripts/parse_canvas_submissions.py` extracts URLs/metadata
  2) `scripts/batch_grade.py` picks a chapter from the Canvas `<h1>` (e.g., `Ch. 2 - …`), captures console/code, calls the chapter grader
  3) CSV/JSON output with per‑submission breakdown

## Developer workflows
- Site preview:
  - GitHub Pages builds via remote theme; no `Gemfile` present. For local preview either:
    - Use VS Code Markdown Preview for individual pages; or
    - Install Jekyll locally and serve (optional) knowing the remote theme may need local install.
- Grading (Python 3):
  - Playwright (only for URL-based capture):
    - `pip install playwright`
    - `python -m playwright install chromium`
  - Chapter 1 example:
    - URL live grading: `python scripts/grade_ch1_codepen.py --url https://codepen.io/<user>/pen/<slug>`
    - From saved logs: `python scripts/grade_ch1_codepen.py --from-logs path/to/console.log`
    - Include local JS (quote/comments check): `--js path/to/code.js`
    - JSON report: `--out json`
  - Chapter 12 example:
    - `python scripts/grade_ch12_codepen.py --url https://codepen.io/<user>/pen/<slug>`
    - Offline grading supported via `--html`, `--css`, `--js` (see script)
  - Batch grading across a folder:
    - `scripts/.venv/bin/python scripts/batch_grade.py --dir Submissions --out grades.csv`
  - Parse Canvas submission link pages (pre-step or standalone):
    - `python scripts/parse_canvas_submissions.py --dir Submissions --format csv --out parsed.csv`

## Project conventions and gotchas
- Syllabus vs Schedule:
  - Treat `schedule.md` as the schedule source. If you mirror schedule content in `index.md`, script or copy from `schedule.md` to avoid drift.
- Assignment labels matter:
  - Graders match specific console labels and patterns (e.g., Ch.1 expects `Next year age:`). Significant wording changes on assignment pages can break auto-grading.
- Grader composition:
  - Many graders import shared helpers from `scripts/grade_ch1_codepen.py` (console capture, debug URL, JS simulation). Reuse those helpers for new chapters.
- Batch router:
  - `scripts/batch_grade.py` maps `Ch. X` → `scripts/grade_chX_codepen.py`. When adding a new grader, implement `grade_chX(...)` and register it in the batch script.
- Outputs:
  - Graders return a dict with `total`, `possible`, and `notes/meta`. Batch output includes `steps` used to capture (direct/debug/simulated) and any `errors`.
- Virtual env:
  - A local `scripts/.venv/` may exist. Prefer `scripts/.venv/bin/python` when present for reproducibility, or document the active interpreter.

## File touchpoints to know
- Site
  - `_config.yml` — remote theme. Minimal Jekyll config.
  - `_layouts/default.html` — HTML wrapper with anchor.js; Markdown pages render inside.
  - `index.md`, `schedule.md`, `assignments/**/index.md` — core editable content.
- Grading
  - `scripts/README-grader.md` — concrete usage, rubrics, and notes (start here).
  - `scripts/grade_ch1_codepen.py` — shared capture logic and Ch.1 rubric (others import this as `common`).
  - `scripts/batch_grade.py` — folder runner; dispatch by chapter.
  - `scripts/parse_canvas_submissions.py` — extract CodePen links and metadata from Canvas HTML.
  - `Submissions/` — place Canvas HTML link files here; outputs like `grades.csv` are often written to repo root or specified via `--out`.

## When making changes
- Keep assignment text synchronized with grader expectations or update the rubric logic accordingly.
- Prefer editing `schedule.md` and then copy or programmatically include it into `index.md` to avoid divergence.
- Avoid introducing build-time dependencies for the site unless adding a `Gemfile`/lockfile and documenting the preview path.
