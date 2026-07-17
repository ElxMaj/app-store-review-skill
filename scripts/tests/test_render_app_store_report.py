import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from app_store_review_scan import ScanContext, run_scan, write_outputs  # noqa: E402
from render_app_store_report import main as render_main  # noqa: E402
from render_app_store_report import render_report_html  # noqa: E402


def sample_report():
    return {
        "schema_version": "1.0",
        "app_name": "Example <script>alert(1)</script>",
        "root": "/example/App",
        "verdict": "NEEDS_REVIEW",
        "policy_verified_at": "2026-07-17",
        "counts": {"blocker": 0, "warning": 1, "manual_check": 1, "info": 0},
        "project": {
            "frameworks": ["expo"],
            "native_ios_root": "ios",
            "targets": [{"name": "Example"}],
        },
        "findings": [
            {
                "id": "ASR-TEST-001",
                "severity": "warning",
                "title": "Purpose string needs review",
                "guideline": "5.1.1(ii)",
                "evidence_confidence": "official",
                "evidence": [{"path": "app.json", "line": 4, "excerpt": "<unsafe>"}],
                "reason": "The supplied text is generic.",
                "fix": "Write a feature-specific explanation.",
                "verification": "Inspect the merged plist.",
            }
        ],
        "manual_checks": [
            {
                "id": "ASR-MANUAL-001",
                "title": "Run the reviewer path",
                "reason": "Source does not prove runtime behavior.",
                "verification": "Execute the release build.",
            }
        ],
        "limitations": [],
    }


class VisualReportTests(unittest.TestCase):
    def test_renderer_is_self_contained_and_escapes_report_values(self):
        output = render_report_html(sample_report())

        self.assertIn("<!doctype html>", output)
        self.assertIn("Example &lt;script&gt;alert(1)&lt;/script&gt;", output)
        self.assertIn("app.json:4", output)
        self.assertNotIn("<script>", output)
        self.assertNotIn('src="http', output)
        self.assertNotIn('href="http', output)

    def test_renderer_avoids_generic_dashboard_chrome(self):
        output = render_report_html(sample_report())

        self.assertIn('class="report-index"', output)
        self.assertIn('class="verdict-block"', output)
        self.assertFalse(any(line.endswith((" ", "\t")) for line in output.splitlines()))
        self.assertNotIn("gradient(", output)
        self.assertNotIn("border-radius", output)
        self.assertNotIn("box-shadow", output)
        self.assertNotIn("mode-chip", output)

    def test_renderer_cli_writes_beside_json_by_default(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "review.json"
            source.write_text(json.dumps(sample_report()), encoding="utf-8")

            self.assertEqual(0, render_main([str(source)]))

            destination = source.with_suffix(".html")
            self.assertTrue(destination.is_file())
            self.assertIn("Purpose string needs review", destination.read_text(encoding="utf-8"))

    def test_scanner_all_format_writes_markdown_json_and_html(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            output = Path(temporary) / "report"
            project.mkdir()
            report = run_scan(ScanContext(project, False, [], None))
            args = argparse.Namespace(output_dir=str(output), format="all")

            write_outputs(report, args)

            self.assertTrue((output / "app-store-review-report.md").is_file())
            self.assertTrue((output / "app-store-review-report.json").is_file())
            self.assertTrue((output / "app-store-review-report.html").is_file())


if __name__ == "__main__":
    unittest.main()
