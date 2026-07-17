import json
import plistlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from app_store_review_scan import ScanContext, run_scan  # noqa: E402


PBXPROJ = """
/* Begin PBXNativeTarget section */
ABCDEF1234567890 /* SampleApp */ = {
  isa = PBXNativeTarget;
  name = SampleApp;
  productType = "com.apple.product-type.application";
};
ABCDEF1234567891 /* SampleWidget */ = {
  isa = PBXNativeTarget;
  name = SampleWidget;
  productType = "com.apple.product-type.app-extension";
};
/* End PBXNativeTarget section */
"""


def scan(root: Path, archive: Path = None, compare_roots=None):
    context = ScanContext(root, False, compare_roots or [], archive)
    return run_scan(context)


class ScannerTests(unittest.TestCase):
    def test_xcode_detects_missing_permission_and_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "Sample.xcodeproj"
            project.mkdir()
            (project / "project.pbxproj").write_text(PBXPROJ)
            (root / "Camera.swift").write_text(
                "AVCaptureDevice.requestAccess(for: .video) { _ in }\n"
                "UserDefaults.standard.set(true, forKey: \"seen\")\n"
            )

            report = scan(root)

            self.assertIn("xcode", report["project"]["frameworks"])
            self.assertEqual(2, len(report["project"]["targets"]))
            titles = {item["title"] for item in report["findings"]}
            self.assertIn("Camera API lacks NSCameraUsageDescription", titles)
            self.assertIn("Required Reason API declaration missing for UserDefaults", titles)
            self.assertEqual("NOT READY", report["verdict"])

    def test_expo_authored_config_satisfies_static_privacy_checks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "package.json").write_text(json.dumps({"dependencies": {"expo": "latest"}}))
            app_config = {
                "expo": {
                    "ios": {
                        "infoPlist": {
                            "NSCameraUsageDescription": "Scan parcel labels to add their tracking number."
                        },
                        "privacyManifests": {
                            "NSPrivacyAccessedAPITypes": [
                                {
                                    "NSPrivacyAccessedAPIType": "NSPrivacyAccessedAPICategoryUserDefaults",
                                    "NSPrivacyAccessedAPITypeReasons": ["CA92.1"],
                                }
                            ]
                        },
                    }
                }
            }
            (root / "app.json").write_text(json.dumps(app_config))
            (root / "Feature.swift").write_text(
                "AVCaptureDevice.requestAccess(for: .video) { _ in }\n"
                "UserDefaults.standard.set(true, forKey: \"seen\")\n"
            )

            report = scan(root)

            ids = {item["id"] for item in report["findings"]}
            self.assertIn("expo", report["project"]["frameworks"])
            self.assertFalse(any(item.startswith("ASR-PERM-") for item in ids))
            self.assertFalse(any("Required Reason API declaration missing" in item["title"] for item in report["findings"]))

    def test_react_native_feature_heuristics_are_warnings(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "package.json").write_text(
                json.dumps(
                    {
                        "dependencies": {
                            "react-native": "latest",
                            "@react-native-google-signin/google-signin": "latest",
                            "react-native-iap": "latest",
                            "openai": "latest",
                        }
                    }
                )
            )
            (root / "App.tsx").write_text(
                "const endpoint = 'https://api.openai.com/v1/responses';\n"
                "function signUp() {}\n"
                "const price = '$9.99';\n"
            )

            report = scan(root)

            ids = {item["id"] for item in report["findings"]}
            self.assertIn("react-native", report["project"]["frameworks"])
            self.assertTrue({"ASR-ACCOUNT-SIWA", "ASR-ACCOUNT-DELETE", "ASR-IAP-RESTORE", "ASR-PRIVACY-AI"}.issubset(ids))
            self.assertTrue(all(item["severity"] == "warning" for item in report["findings"] if item["id"] in ids))

    def test_archive_reports_assistant_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive_path = root / "Sample.ipa"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("Payload/Sample.app/CLAUDE.md", "internal notes")
                archive.writestr("Payload/Sample.app/Info.plist", plistlib.dumps({"CFBundleName": "Sample"}))

            report = scan(root, archive=archive_path)

            ids = {item["id"] for item in report["findings"]}
            self.assertIn("ASR-ARCHIVE-ARTIFACT", ids)

    def test_exact_asset_comparison(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_root = Path(first)
            second_root = Path(second)
            (first_root / "icon.png").write_bytes(b"same-image")
            (second_root / "old-icon.png").write_bytes(b"same-image")

            report = scan(first_root, compare_roots=[second_root])

            ids = {item["id"] for item in report["findings"]}
            self.assertIn("ASR-43-ASSET-REUSE", ids)

    def test_documentation_examples_do_not_become_findings(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text(
                "Example only: https://example.com and http://192.0.2.1 should stay in docs."
            )

            report = scan(root)

            ids = {item["id"] for item in report["findings"]}
            self.assertNotIn("ASR-COMPLETE-002", ids)
            self.assertNotIn("ASR-NETWORK-001", ids)

    def test_expo_permission_package_is_warning_not_blocker(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "package.json").write_text(
                json.dumps({"dependencies": {"expo": "latest", "expo-camera": "latest"}})
            )
            (root / "app.json").write_text(json.dumps({"expo": {"ios": {}}}))

            report = scan(root)

            finding = next(item for item in report["findings"] if "Camera package" in item["title"])
            self.assertEqual("warning", finding["severity"])


if __name__ == "__main__":
    unittest.main()
