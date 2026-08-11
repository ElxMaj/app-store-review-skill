import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "check_registry_health.sh"


class RegistryHealthTests(unittest.TestCase):
    def run_checker(
        self,
        *,
        claude_version="1.2.1",
        claude_document=None,
        security_level="NONE",
        multiplier=2.02,
    ):
        with tempfile.TemporaryDirectory() as directory:
            fixture_dir = Path(directory)
            claude_manifest = fixture_dir / "claude-plugin.json"
            tessl_manifest = fixture_dir / "tessl-plugin.json"
            claude_listing = fixture_dir / "claude-listing.html"
            tessl_tile = fixture_dir / "tessl-tile.json"
            tessl_version = fixture_dir / "tessl-version.json"

            claude_manifest.write_text(
                json.dumps({"name": "app-store-review", "version": "1.2.1"}),
                encoding="utf-8",
            )
            tessl_manifest.write_text(
                json.dumps({"name": "maj-labs/app-store-review", "version": "1.2.1"}),
                encoding="utf-8",
            )
            if claude_document is None:
                claude_document = (
                    '<script type="application/ld+json">'
                    + json.dumps(
                        {
                            "url": claude_listing.as_uri(),
                            "softwareVersion": claude_version,
                        }
                    )
                    + "</script>"
                )
            claude_listing.write_text(claude_document, encoding="utf-8")
            tessl_tile.write_text(
                json.dumps(
                    {
                        "links": {"self": "https://api.tessl.io/example"},
                        "data": {
                            "id": "tile-id",
                            "type": "tile",
                            "attributes": {
                                "name": "app-store-review",
                                "fullName": "maj-labs/app-store-review",
                                "latestVersion": "1.2.1",
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            tessl_version.write_text(
                json.dumps(
                    {
                        "links": {"self": "https://api.tessl.io/example/1.2.1"},
                        "data": {
                            "id": "version-id",
                            "type": "tile-version",
                            "attributes": {
                                "version": "1.2.1",
                                "moderationStatus": "pass",
                                "moderationPassed": True,
                                "evalScore": 95,
                                "evalBaselineScore": 47,
                                "evalImprovement": 48,
                                "evalImprovementMultiplier": multiplier,
                                "scores": {
                                    "version": "1.2.1",
                                    "aggregate": 0.95,
                                    "quality": None,
                                    "impact": 0.95,
                                    "security": "LOW",
                                    "securityLevel": security_level,
                                    "evalAvg": 0.95,
                                    "evalBaseline": 0.47,
                                    "evalImprovement": 0.48,
                                    "evalImprovementMultiplier": multiplier,
                                    "evalCount": 4,
                                    "validationErrors": [],
                                },
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            environment = os.environ.copy()
            environment.update(
                {
                    "ASR_CLAUDE_MANIFEST": str(claude_manifest),
                    "ASR_TESSL_MANIFEST": str(tessl_manifest),
                    "ASR_CLAUDE_URL": claude_listing.as_uri(),
                    "ASR_TESSL_TILE_URL": tessl_tile.as_uri(),
                    "ASR_TESSL_VERSION_URL": tessl_version.as_uri(),
                }
            )
            return subprocess.run(
                ["bash", str(CHECKER)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_matching_public_versions_and_scores_succeed(self):
        result = self.run_checker()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ClaudePluginHub: 1.2.1", result.stdout)
        self.assertIn("Tessl: 1.2.1", result.stdout)
        self.assertIn("multiplier 2.02x", result.stdout)

    def test_stale_claudepluginhub_version_fails_with_observed_version(self):
        result = self.run_checker(claude_version="1.1.4")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "ClaudePluginHub version mismatch: expected 1.2.1, observed 1.1.4",
            result.stderr,
        )

    def test_version_outside_json_ld_does_not_satisfy_listing_check(self):
        result = self.run_checker(
            claude_document=(
                '<div data-cache=\'{"softwareVersion":"1.2.1"}\'></div>'
                '<script type="application/ld+json">{"name":"App Store Review"}</script>'
            )
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ClaudePluginHub softwareVersion is missing", result.stderr)

    def test_version_for_another_json_ld_identity_does_not_satisfy_check(self):
        result = self.run_checker(
            claude_document=(
                '<script type="application/ld+json">'
                '{"url":"https://example.com/another-plugin","softwareVersion":"1.2.1"}'
                "</script>"
            )
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ClaudePluginHub softwareVersion is missing", result.stderr)

    def test_missing_tessl_security_level_fails(self):
        result = self.run_checker(security_level=None)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Tessl security level is missing", result.stderr)

    def test_missing_tessl_multiplier_fails(self):
        result = self.run_checker(multiplier=None)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Tessl evaluation multiplier is missing", result.stderr)


if __name__ == "__main__":
    unittest.main()
