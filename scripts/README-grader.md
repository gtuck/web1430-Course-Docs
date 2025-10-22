Ch. 1 Automated Grader

This tool grades student CodePen submissions for the assignment in `assignments/ch01/index.md`.

What it does
- Loads a CodePen URL in a headless browser and captures `console.log()` output.
- Scores it against the rubric (25 pts total).
- Optionally reads a local JS file to verify comments and quoting.
- Can also grade from a newline-delimited log file (offline mode).

Install (Playwright)
- Playwright is only required for URL-based grading.
- Install once:
  - `pip install playwright`
  - `python -m playwright install chromium`

Usage
- From a CodePen URL:
  - `python scripts/grade_ch1_codepen.py --url https://codepen.io/<user>/pen/<slug>`
  - If Cloudflare blocks headless access, try CodePen Debug View:
    - `python scripts/grade_ch1_codepen.py --url https://cdpn.io/<user>/debug/<slug>`
  - Add `--timeout 12` to wait longer for console output if needed.

- From saved console output (one line per console print):
  - `python scripts/grade_ch1_codepen.py --from-logs path/to/console.log`

- Include local JS code to verify comment types/quoting:
  - `python scripts/grade_ch1_codepen.py --from-logs path/to/console.log --js path/to/code.js`

- If the JS cannot be fetched from CodePen, but you want to award comment points:
  - `python scripts/grade_ch1_codepen.py --url <pen> --assume-comments-ok`

Output
- Default text report with a breakdown per rubric item, total score, and a console preview.
- JSON output: add `--out json`.

Notes in Results
- Each grader includes a Notes section summarizing any missing or partial rubric items.
- Batch CSVs include a `notes` column with concise reasons for deductions.

Rubric mapping (25 pts)
- Uses `console.log()` (2)
- Number and string values (2)
- Quote style + escaping (5) — best effort via console; verified via JS when available
- Arithmetic `+ - * /` (5)
- String concatenation with `+` (3)
- Sequential execution order (“Line A/B/C”) (3)
- Comments (`//` and `/* */`) (3) — requires JS or `--assume-comments-ok`
- Fix‑me mini‑exercises (2)

Notes
- The grader is intentionally strict about specific labeled lines used in the assignment (e.g.,
  `Next year age:`, `Age in months:`, `Half age:`, `Difference 10 - 3 =`, `Product 9 * 7 =`).
  If you change labels significantly, arithmetic credit may not be detected.
- When grading live CodePen URLs, make sure the pen auto-runs or use the Run control. The grader
  attempts to click a “Run” button if visible.
- If network or Playwright isn’t available, use `--from-logs` and optionally `--js`.

Multi-Assignment Grading
- Batch runner: `scripts/batch_grade.py` detects chapter numbers from Canvas `<h1>` (e.g., "Ch. 2 - …") and dispatches to the correct grader.
- Currently supported:
  - Ch. 1 — `scripts/grade_ch1_codepen.py`
  - Ch. 2 — `scripts/grade_ch2_codepen.py`
  - Ch. 3 — `scripts/grade_ch3_codepen.py`
  - Ch. 4 — `scripts/grade_ch4_codepen.py`
  - Ch. 5 — `scripts/grade_ch5_codepen.py`
  - Ch. 6 — `scripts/grade_ch6_codepen.py`
  - Ch. 7 & 8 — `scripts/grade_ch7_8_codepen.py`
  - Ch. 9 — `scripts/grade_ch9_codepen.py`
  - Ch. 10 — `scripts/grade_ch10_codepen.py`
- Run for a whole folder:
  - `scripts/.venv/bin/python scripts/batch_grade.py --dir Submissions --out grades.csv`
- Extend for more assignments:
  - Add `scripts/grade_chX_codepen.py` with rubric checks.
  - Update `scripts/batch_grade.py` to dispatch on `chapter == X` to your new grader.
