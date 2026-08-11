import json
import re
import sys
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from render_app_store_report import render_report_html  # noqa: E402


ARCHIVE = ROOT / "app-store-review-skill.skill"
PACKAGE_ROOT = "app-store-review"
COPILOT_SKILL = ROOT / "copilot-plugin" / "skills" / "app-store-review"
ROOT_REFERENCES = sorted((ROOT / "references").glob("*.md"))
ROOT_SCRIPTS = sorted((ROOT / "scripts").glob("*.py"))
MANIFESTS = (
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".tessl-plugin" / "plugin.json",
    ROOT / "copilot-plugin" / ".github" / "plugin" / "plugin.json",
)
EXPECTED_VERSION = "1.2.1"


class PackageConsistencyTests(unittest.TestCase):
    def test_claude_review_command_delegates_to_canonical_skill(self):
        command_path = ROOT / "commands" / "review.md"
        self.assertTrue(command_path.is_file(), "commands/review.md is missing")

        command = command_path.read_text(encoding="utf-8")
        self.assertIn("app-store-review:app-store-review", command)
        self.assertIn("$ARGUMENTS", command)
        self.assertNotIn("Mode A:", command)
        self.assertNotIn("Mode B:", command)
        self.assertLessEqual(len(command.splitlines()), 16)

    def test_install_guide_covers_every_supported_distribution_path(self):
        install_path = ROOT / "INSTALL.md"
        self.assertTrue(install_path.is_file(), "INSTALL.md is missing")

        install = install_path.read_text(encoding="utf-8")
        required_commands = (
            "npx skills add ElxMaj/app-store-review-skill",
            "npx claudepluginhub elxmaj/app-store-review-skill --plugin app-store-review",
            "/plugin marketplace add ElxMaj/app-store-review-skill",
            "/plugin install app-store-review@app-store-review-skill",
            "npx tessl install maj-labs/app-store-review",
            "/app-store-review",
        )
        for command in required_commands:
            with self.subTest(command=command):
                self.assertIn(command, install)

    def test_manifest_and_report_contract_versions_are_current(self):
        for manifest in MANIFESTS:
            with self.subTest(manifest=manifest):
                self.assertEqual(EXPECTED_VERSION, json.loads(manifest.read_text(encoding="utf-8"))["version"])

        scanners = (
            ROOT / "scripts" / "app_store_review_scan.py",
            COPILOT_SKILL / "scripts" / "app_store_review_scan.py",
        )
        contract = (ROOT / "references" / "report-contract.md").read_text(encoding="utf-8")
        for scanner in scanners:
            with self.subTest(scanner=scanner):
                self.assertRegex(
                    scanner.read_text(encoding="utf-8"),
                    r'(?m)^VERSION = "1\.2\.1"$',
                )
        self.assertIn('"version": "1.2.1"', contract)

    def test_public_sample_uses_current_report_contract(self):
        sample = json.loads(
            (ROOT / "examples" / "parceltrack-report.json").read_text(encoding="utf-8")
        )

        self.assertEqual("1.1", sample["schema_version"])
        self.assertEqual("2026-08-10", sample["policy_verified_at"])
        self.assertEqual("NOT READY", sample["verdict"])
        self.assertEqual(
            {
                "files_discovered": 0,
                "files_scanned": 0,
                "files_skipped": 0,
                "fields": [],
                "locales": [],
                "pricing_rule_fields": [],
            },
            sample["metadata_scan"],
        )
        self.assertEqual(
            {"name": "app_store_review_scan", "version": EXPECTED_VERSION},
            sample["scanner"],
        )
        rendered = (ROOT / "examples" / "parceltrack-report.html").read_text(encoding="utf-8")
        self.assertEqual(render_report_html(sample), rendered)
        self.assertIn("Policy / 2026-08-10", rendered)
        self.assertIn("Generated 2026-08-10T12:00:00Z", rendered)
        self.assertIn('<span class="verdict">NOT READY</span>', rendered)

    def test_report_contract_metadata_coverage_matches_the_example(self):
        contract = (ROOT / "references" / "report-contract.md").read_text(encoding="utf-8")

        for key in ("files_discovered", "files_scanned", "files_skipped"):
            with self.subTest(key=key):
                self.assertIn(f'"{key}"', contract)
        self.assertIn('"fields": ["description", "subtitle"]', contract)
        self.assertIn('"pricing_rule_fields": ["subtitle"]', contract)
        self.assertNotIn('"verdict": "NEEDS_REVIEW"', contract)

    def test_metadata_rejection_eval_uses_established_weighted_schema(self):
        eval_root = ROOT / "evals" / "rejection-recovery-metadata"
        criteria = json.loads((eval_root / "criteria.json").read_text(encoding="utf-8"))
        scenario = json.loads((eval_root / "scenario.json").read_text(encoding="utf-8"))

        self.assertEqual({"context", "type", "checklist"}, set(criteria))
        self.assertEqual("weighted_checklist", criteria["type"])
        self.assertEqual(100, sum(item["max_score"] for item in criteria["checklist"]))
        self.assertTrue(
            all(set(item) == {"name", "description", "max_score"} for item in criteria["checklist"])
        )
        self.assertEqual({"description", "include"}, set(scenario))
        self.assertEqual(["./inputs"], scenario["include"])
        semantics = " ".join(item["description"] for item in criteria["checklist"]).lower()
        for required in (
            "complete supplied message",
            "exactly one response classification",
            "fix",
            "guideline 2.3.7",
            "every live subtitle localization",
            "fallback metadata",
            "price-change copy",
            "no binary or bundled configuration changed",
            "app store connect status permits the edit",
            "only verified fields, locales, version, build, changes, and attachments",
            "does not recommend an appeal",
            "blanket ban",
        ):
            with self.subTest(required=required):
                self.assertIn(required, semantics)

    def test_copilot_and_archive_match_canonical_resources(self):
        with zipfile.ZipFile(ARCHIVE) as archive:
            for source in [*ROOT_REFERENCES, *ROOT_SCRIPTS]:
                relative = source.relative_to(ROOT).as_posix()
                with self.subTest(resource=relative):
                    self.assertEqual(source.read_bytes(), (COPILOT_SKILL / relative).read_bytes())
                    self.assertEqual(source.read_bytes(), archive.read(f"{PACKAGE_ROOT}/{relative}"))

            self.assertEqual(
                (ROOT / "SKILL.md").read_bytes(),
                archive.read(f"{PACKAGE_ROOT}/SKILL.md"),
            )
            self.assertEqual(
                (ROOT / "agents" / "openai.yaml").read_bytes(),
                archive.read(f"{PACKAGE_ROOT}/agents/openai.yaml"),
            )

    def test_copilot_body_loader_and_resource_appendix_are_intentional(self):
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        copilot_skill = (COPILOT_SKILL / "SKILL.md").read_text(encoding="utf-8")
        appendix = copilot_skill.removeprefix(root_skill)

        self.assertNotEqual(copilot_skill, root_skill)
        self.assertTrue(copilot_skill.startswith(root_skill))
        self.assertTrue(appendix.startswith("\n## Packaged resources\n"))
        for source in [*ROOT_REFERENCES, *ROOT_SCRIPTS]:
            relative = source.relative_to(ROOT).as_posix()
            with self.subTest(resource=relative):
                self.assertIn(f"]({relative})", appendix)

        loader = (ROOT / "skills" / "app-store-review" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("# Compatibility loader", loader)
        self.assertIn("Read `../../SKILL.md` completely before acting.", loader)
        self.assertIn("Follow the root skill exactly.", loader)

    def test_archive_excludes_private_eval_and_test_fixtures(self):
        with zipfile.ZipFile(ARCHIVE) as archive:
            members = set(archive.namelist())

        expected_files = {
            f"{PACKAGE_ROOT}/SKILL.md",
            f"{PACKAGE_ROOT}/agents/openai.yaml",
            *(f"{PACKAGE_ROOT}/{path.relative_to(ROOT).as_posix()}" for path in ROOT_REFERENCES),
            *(f"{PACKAGE_ROOT}/{path.relative_to(ROOT).as_posix()}" for path in ROOT_SCRIPTS),
        }
        archived_files = {member for member in members if not member.endswith("/")}
        self.assertEqual(expected_files, archived_files)

        self.assertNotIn(f"{PACKAGE_ROOT}/evals/", members)
        self.assertFalse(
            any(
                part in {"tests", "test", "evals", "fixtures", "__pycache__"}
                or "rejection-evidence" in member.lower()
                for member in members
                for part in member.lower().split("/")
            ),
            members,
        )


if __name__ == "__main__":
    unittest.main()
