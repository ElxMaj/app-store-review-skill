import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / ".github" / "scripts" / "check_action_pins.py"


class ActionPinTests(unittest.TestCase):
    def run_checker(
        self,
        *,
        pinned_sha="a" * 40,
        tag_sha="a" * 40,
        ref=None,
        extra_uses=None,
        raw_extra_step=None,
    ):
        with tempfile.TemporaryDirectory() as directory:
            fixture_dir = Path(directory)
            workflows = fixture_dir / "workflows"
            api_root = fixture_dir / "api"
            tag_response = api_root / "repos" / "acme" / "example" / "git" / "ref" / "tags" / "v1"
            workflows.mkdir()
            tag_response.parent.mkdir(parents=True)

            action_ref = ref or pinned_sha
            workflow_text = (
                "name: Check\n"
                "jobs:\n"
                "  check:\n"
                "    steps:\n"
                f"      - uses: acme/example@{action_ref} # v1\n"
            )
            if extra_uses is not None:
                workflow_text += f"      - uses: {extra_uses}\n"
            if raw_extra_step is not None:
                workflow_text += f"      {raw_extra_step}\n"
            workflows.joinpath("check.yml").write_text(workflow_text, encoding="utf-8")
            tag_response.write_text(
                json.dumps(
                    {
                        "ref": "refs/tags/v1",
                        "object": {"type": "commit", "sha": tag_sha},
                    }
                ),
                encoding="utf-8",
            )

            environment = os.environ.copy()
            environment.pop("GITHUB_TOKEN", None)
            environment.update(
                {
                    "ASR_WORKFLOW_DIR": str(workflows),
                    "ASR_GITHUB_API_BASE": api_root.as_uri(),
                }
            )
            return subprocess.run(
                ["python3", str(CHECKER)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_sha_matching_the_current_major_tag_succeeds(self):
        result = self.run_checker()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Action pins: 1 verified", result.stdout)

    def test_stale_sha_fails_with_action_and_major_tag(self):
        result = self.run_checker(tag_sha="b" * 40)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("acme/example pin is stale for v1", result.stderr)
        self.assertIn("observed " + "a" * 40, result.stderr)
        self.assertIn("current " + "b" * 40, result.stderr)

    def test_non_sha_action_reference_fails(self):
        result = self.run_checker(ref="v1")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("acme/example is not pinned to a full commit SHA", result.stderr)

    def test_unpinned_subpath_cannot_hide_beside_a_valid_pin(self):
        result = self.run_checker(extra_uses="acme/example/subpath@v1")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("acme/example/subpath is not pinned to a full commit SHA", result.stderr)

    def test_quoted_uses_key_is_rejected_instead_of_ignored(self):
        result = self.run_checker(raw_extra_step='- "uses": acme/example@v1')

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported uses syntax", result.stderr)

    def test_flow_mapping_uses_key_is_rejected_instead_of_ignored(self):
        result = self.run_checker(raw_extra_step="- {uses: acme/example@v1}")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported uses syntax", result.stderr)

    def test_anchored_uses_key_is_rejected_instead_of_ignored(self):
        result = self.run_checker(raw_extra_step="- &unsafe uses: acme/example@v1")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported uses syntax", result.stderr)

    def test_combined_yaml_node_properties_are_rejected_instead_of_ignored(self):
        result = self.run_checker(raw_extra_step="- &unsafe !!map uses: acme/example@v1")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported uses syntax", result.stderr)


if __name__ == "__main__":
    unittest.main()
