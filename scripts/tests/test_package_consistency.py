import json
import re
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
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
EXPECTED_VERSION = "1.2.0"


class PackageConsistencyTests(unittest.TestCase):
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
                    r'(?m)^VERSION = "1\.2\.0"$',
                )
        self.assertIn('"version": "1.2.0"', contract)

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
