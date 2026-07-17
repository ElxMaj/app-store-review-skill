# Visual HTML Report from App Store Audit

## Problem/Feature Description

Meridian Studio has been preparing FocusFlow, a productivity app, for App Store submission. A compliance consultant ran an independent pre-submission audit and produced a complete, manually-reviewed audit package: a Markdown summary, a structured JSON report, and now wants a polished visual HTML report to share with the engineering lead before the submission meeting.

The JSON audit report is already finalized and human-reviewed — it lives at `inputs/audit-report.json`. The engineering lead needs a visual HTML version they can open in a browser to read through findings, check the verdict, and share with the team. The report should be professional and readable — appropriate to show at a client meeting — and must work offline since the meeting room has spotty connectivity.

The bundled render script at `scripts/render_app_store_report.py` (from the App Store review skill) is available to generate the HTML. Use it to produce the report, then inspect the output and confirm it is complete and well-formed. At the end, report the paths to all three output formats together (Markdown summary if you create one, JSON, and HTML).

## Output Specification

Produce the following files in your working directory:

- `audit-report.html` — the visual HTML report generated from `inputs/audit-report.json`
- `report-summary.md` — a brief Markdown summary covering the verdict, finding count by severity, and the three output paths

In `report-summary.md`, include:
- The verdict from the JSON
- A count of findings by severity type
- The paths to all three output files (Markdown, JSON, HTML)
- A brief note documenting that you checked the HTML output (e.g., approximate file size, that it opened successfully, or observations about its responsiveness at different widths)
