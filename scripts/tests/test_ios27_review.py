import json
import plistlib
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app_store_review_scan import ScanContext, render_markdown, run_scan
from render_app_store_report import render_report_html
from ios_platform_review import read_archive


class IOS27ReviewTests(unittest.TestCase):
    def project(self, root, source="import SwiftUI\n", settings=""):
        project = root / "Sample.xcodeproj"
        project.mkdir()
        (project / "project.pbxproj").write_text(settings)
        (root / "Sample.swift").write_text(source)

    def archive(self, root, values, extra=None):
        path = root / "Sample.ipa"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("Payload/Sample.app/Info.plist", plistlib.dumps(values, fmt=plistlib.FMT_BINARY))
            for name, content in (extra or {}).items():
                archive.writestr(name, plistlib.dumps(content))
        return path

    def valid_build(self, **changes):
        values = dict(DTPlatformName="iphoneos", DTSDKName="iphoneos27.0", DTXcode="2700",
                      MinimumOSVersion="15.0", UILaunchScreen={})
        values.update(changes)
        return values

    def scan(self, root, archive=None):
        return run_scan(ScanContext(root, False, [], archive))

    def test_archive_sdk_and_deployment_gates_have_bundle_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            archive = self.archive(root, dict(DTPlatformName="iphoneos", DTSDKName="iphoneos25.0",
                                               DTXcode="2500", MinimumOSVersion="12.0"))
            report = self.scan(root, archive)
            findings = {item["id"]: item for item in report["findings"]}
            for finding_id in ("ASR-UPLOAD-SDK", "ASR-UPLOAD-XCODE", "ASR-UPLOAD-MINIMUM-OS"):
                self.assertEqual("blocker", findings[finding_id]["severity"])
                self.assertIn("Payload/Sample.app/Info.plist", findings[finding_id]["evidence"][0]["path"])
            self.assertEqual("NOT READY", report["verdict"])

    def test_ios26_sdk_is_still_accepted_and_sdkroot_is_not_a_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root, settings="SDKROOT = iphoneos; IPHONEOS_DEPLOYMENT_TARGET = 13.0;")
            archive = self.archive(root, dict(DTPlatformName="iphoneos", DTSDKName="iphoneos26.0",
                                               DTXcode="2600", MinimumOSVersion="13.0"))
            report = self.scan(root, archive)
            self.assertFalse(any(item["severity"] == "blocker" for item in report["findings"]))
            self.assertEqual(26, report["platform_review"]["submission_requirements"]["sdk_major"]["minimum"])

    def test_authored_settings_do_not_become_archive_blockers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root, settings="IPHONEOS_DEPLOYMENT_TARGET = 12.0; SDKROOT = iphoneos25.0;")
            (root / "Info.plist").write_bytes(plistlib.dumps(dict(DTSDKName="iphoneos25.0", MinimumOSVersion="12.0")))
            report = self.scan(root)
            self.assertFalse(any(item["severity"] == "blocker" for item in report["findings"]))
            self.assertTrue(all(item["kind"] == "authored" for item in report["platform_review"]["build_evidence"]))
            self.assertTrue(any(item["id"] == "ASR-MANUAL-DEPLOYMENT" for item in report["manual_checks"]))

    def test_ios27_launch_screen_is_required_for_apps_but_not_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            values = self.valid_build()
            del values["UILaunchScreen"]
            archive = self.archive(root, values)
            report = self.scan(root, archive)
            self.assertIn("ASR-IOS27-LAUNCH-SCREEN", {item["id"] for item in report["findings"]})
            values["UILaunchScreen"] = {}
            extension = {key: value for key, value in values.items() if key != "UILaunchScreen"}
            archive = self.archive(root, values, {"Payload/Sample.app/PlugIns/Widget.appex/Info.plist": extension})
            report = self.scan(root, archive)
            self.assertNotIn("ASR-IOS27-LAUNCH-SCREEN", {item["id"] for item in report["findings"]})

    def test_all_supported_launch_screen_keys_are_accepted(self):
        for key, value in (("UILaunchScreen", {}), ("UILaunchScreens", {}),
                           ("UILaunchStoryboardName", "LaunchScreen"), ("UILaunchStoryboards", {})):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.project(root)
                values = self.valid_build()
                del values["UILaunchScreen"]
                values[key] = value
                report = self.scan(root, self.archive(root, values))
                self.assertNotIn("ASR-IOS27-LAUNCH-SCREEN", {item["id"] for item in report["findings"]})

    def test_watch_and_framework_plists_are_not_ios_upload_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            extra = {
                "Payload/Sample.app/Watch/Watch.app/Info.plist": dict(DTPlatformName="watchos", DTSDKName="watchos26.0", MinimumOSVersion="10.0"),
                "Payload/Sample.app/Frameworks/Old.framework/Info.plist": dict(DTPlatformName="iphoneos", DTSDKName="iphoneos17.0", MinimumOSVersion="9.0"),
            }
            report = self.scan(root, self.archive(root, self.valid_build(), extra))
            self.assertFalse(any(item["severity"] == "blocker" for item in report["findings"]))

    def test_xcarchive_directory_and_nested_extension_use_own_plists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            archive = root / "Sample.xcarchive"
            app = archive / "Products/Applications/Sample.app"
            widget = app / "PlugIns/Widget.appex"
            widget.mkdir(parents=True)
            (app / "Info.plist").write_bytes(plistlib.dumps(self.valid_build()))
            (widget / "Info.plist").write_bytes(plistlib.dumps(dict(DTPlatformName="iphoneos", DTSDKName="iphoneos25.0", MinimumOSVersion="13.0")))
            report = self.scan(root, archive)
            sdk = next(item for item in report["findings"] if item["id"] == "ASR-UPLOAD-SDK")
            self.assertIn("Widget.appex/Info.plist", sdk["evidence"][0]["path"])
            self.assertFalse(any("not a readable IPA" in item for item in report["limitations"]))

    def test_missing_or_unparseable_build_versions_remain_manual(self):
        for values in ({}, {"DTSDKName": "iphoneos$(SECRET)", "DTXcode": "<script>alert(1)</script>"}):
            with self.subTest(values=values), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.project(root)
                report = self.scan(root, self.archive(root, values))
                self.assertFalse(any(item["severity"] == "blocker" for item in report["findings"]))
                self.assertNotIn("$(SECRET)", json.dumps(report))
                self.assertNotIn("<script>", json.dumps(report))
                self.assertIn("ASR-MANUAL-SDK", {item["id"] for item in report["manual_checks"]})

    def test_optional_technology_signals_create_checks_without_adoption_violations(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root, source="import FoundationModels\nimport CoreAI\nimport AppIntents\nimport AppIntentsTesting\nimport CoreSpotlight\nimport MusicUnderstanding\nimport NowPlaying\nimport TrustInsights\nimport PaperKit\n")
            report = self.scan(root)
            technologies = {item["id"]: item for item in report["platform_review"]["technologies"]}
            for feature in ("foundation_models", "core_ai", "app_intents", "spotlight", "music_understanding", "now_playing", "trust_insights", "pencil_paper"):
                self.assertEqual("manual", technologies[feature]["status"])
                self.assertTrue(technologies[feature]["evidence"])
            self.assertEqual("not_detected", technologies["health_home"]["status"])
            self.assertFalse(any(item["severity"] == "blocker" for item in report["findings"]))
            self.assertEqual("not_run", report["platform_review"]["runtime_test_status"])
            self.assertEqual("bundled_reference", report["platform_review"]["verification_status"])

    def test_test_and_documentation_mentions_do_not_activate_optional_features(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root, source="import Foundation\n")
            (root / "README.md").write_text("import FoundationModels\nimport TrustInsights")
            tests = root / "Tests"
            tests.mkdir()
            (tests / "AI.swift").write_text("import FoundationModels\n")
            report = self.scan(root)
            technologies = {item["id"]: item for item in report["platform_review"]["technologies"]}
            self.assertEqual("not_detected", technologies["foundation_models"]["status"])
            self.assertEqual("not_detected", technologies["trust_insights"]["status"])

    def test_private_cloud_compute_is_not_classified_as_third_party_ai(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root, source="import FoundationModels\nlet model = PrivateCloudComputeLanguageModel()\n")
            report = self.scan(root)
            self.assertNotIn("ASR-PRIVACY-AI", {item["id"] for item in report["findings"]})
            technologies = {item["id"]: item for item in report["platform_review"]["technologies"]}
            self.assertEqual("manual", technologies["private_cloud_compute"]["status"])

    def test_swift_cloud_provider_packages_receive_consent_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root, source="import AnthropicLanguageModel\nlet model = AnthropicLanguageModel()\n")
            report = self.scan(root)
            self.assertIn("ASR-PRIVACY-AI", {item["id"] for item in report["findings"]})

    def test_legacy_screen_api_is_a_review_signal_not_a_proven_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root, source="import UIKit\nlet width = UIScreen.main.bounds.width\n")
            report = self.scan(root)
            checks = {item["id"]: item for item in report["manual_checks"]}
            self.assertIn("ASR-MANUAL-IOS27-ADAPTIVITY", checks)
            self.assertFalse(any(item["severity"] == "blocker" for item in report["findings"]))

    def test_platform_section_renders_without_claiming_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root, source="import FoundationModels\n")
            report = self.scan(root)
            html = render_report_html(report)
            markdown = render_markdown(report)
            self.assertIn('id="platform-review"', html)
            self.assertIn("iOS 27", html)
            self.assertIn("Foundation Models", html)
            self.assertIn("Runtime tests: not run", html)
            self.assertIn("## iOS 27 platform review", markdown)
            self.assertNotIn("100% ready", html)
            self.assertEqual("1.2", report["schema_version"])

    def test_platform_html_escapes_supplied_evidence_and_status(self):
        report = {"platform_review": {"target_os": "<script>bad</script>", "runtime_test_status": "not_run",
                  "verification_status": "bundled_reference", "reference_verified_at": "2026-10-09",
                  "technologies": [{"id": "x", "title": "<img src=x>", "status": "manual", "evidence": [], "verification": "<script>bad</script>"}]}}
        html = render_report_html(report)
        self.assertIn("&lt;img src=x&gt;", html)
        self.assertNotIn("<script>bad</script>", html)

    def test_reviewed_platform_status_is_preserved_in_both_renderers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            report = self.scan(root)
            report["platform_review"]["runtime_test_status"] = "partial"
            report["platform_review"]["verification_status"] = "live_checked"
            report["platform_review"]["reference_verified_at"] = "2026-10-10"
            for rendered in (render_markdown(report), render_report_html(report)):
                self.assertIn("Runtime tests: partial", rendered)
                self.assertIn("live checked", rendered)
                self.assertIn("2026-10-10", rendered)

    def test_duplicate_archive_plist_is_ambiguous_not_a_policy_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            archive = root / "Ambiguous.ipa"
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(archive, "w") as output:
                    for values in (self.valid_build(), self.valid_build(MinimumOSVersion="12.0")):
                        output.writestr("Payload/Sample.app/Info.plist", plistlib.dumps(values))
            report = self.scan(root, archive)
            self.assertFalse(any(item["id"] == "ASR-UPLOAD-MINIMUM-OS" for item in report["findings"]))
            self.assertTrue(any("duplicate" in item.lower() for item in report["limitations"]))

    def test_plist_only_archive_never_implies_a_valid_executable_or_signature(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            report = self.scan(root, self.archive(root, self.valid_build()))
            limits = " ".join(report["limitations"]).lower()
            self.assertIn("executable", limits)
            self.assertIn("signing", limits)
            self.assertTrue(any(item["id"] == "ASR-MANUAL-ARCHIVE-VALIDATION" for item in report["manual_checks"]))

    def test_future_and_beta_scope_survives_markdown_html_and_print(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            report = self.scan(root)
            watchlist = report["platform_review"].get("release_watchlist", [])
            self.assertTrue(any(item["id"] == "duo_screenshots" and item["timing"] == "April 2027 (day not announced)" for item in watchlist))
            self.assertTrue(any(item["id"] == "ios272_att" and item["status"] == "beta" for item in watchlist))
            for rendered in (render_markdown(report), render_report_html(report)):
                self.assertIn("April 2027", rendered)
                self.assertIn("27.2", rendered)
            html = render_report_html(report)
            self.assertIn('class="print-only"', html)
            self.assertIn("not detected", html)

    def test_oversized_and_malformed_archive_plists_remain_manual(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            archive = root / "Oversized.ipa"
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr("Payload/Sample.app/Info.plist", plistlib.dumps(self.valid_build(MinimumOSVersion="12.0")))
                output.writestr("Payload/Sample.app/PlugIns/Bad.appex/Info.plist", b"private malformed bytes")
            with patch("ios_platform_review.MAX_PLIST_BYTES", 100):
                report = self.scan(root, archive)
            self.assertFalse(any(item["id"].startswith("ASR-UPLOAD-") for item in report["findings"]))
            self.assertTrue(any("inspection limit" in item for item in report["limitations"]))
            self.assertTrue(any("could not be parsed" in item for item in report["limitations"]))
            self.assertNotIn("private malformed bytes", json.dumps(report))

    def test_truncated_xml_archive_plist_does_not_crash_or_expose_contents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            archive = root / "Truncated.ipa"
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr("Payload/Sample.app/Info.plist", b'<?xml version="1.0"?><plist><dict><key>ASR_SECRET_TRUNCATED_8ff92')
            report = self.scan(root, archive)
            self.assertTrue(any("could not be parsed" in item for item in report["limitations"]))
            self.assertNotIn("ASR_SECRET_TRUNCATED_8ff92", json.dumps(report))

    def test_archive_symlinks_and_unsafe_paths_do_not_establish_build_facts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            unsafe = root / "Unsafe.ipa"
            bad = plistlib.dumps(self.valid_build(MinimumOSVersion="12.0"))
            with zipfile.ZipFile(unsafe, "w") as output:
                output.writestr("../Payload/Sample.app/Info.plist", bad)
                entry = zipfile.ZipInfo("Payload/Symlink.app/Info.plist")
                entry.create_system = 3
                entry.external_attr = 0o120777 << 16
                output.writestr(entry, bad)
            self.assertEqual([], read_archive(unsafe).bundles)
            archive = root / "Sample.xcarchive"
            app = archive / "Products/Applications/Sample.app"
            app.mkdir(parents=True)
            outside = root / "Outside.plist"
            outside.write_bytes(bad)
            (app / "Info.plist").symlink_to(outside)
            self.assertEqual([], read_archive(archive).bundles)

    def test_expo_and_xcconfig_values_are_authored_evidence_without_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.project(root)
            (root / "Release.xcconfig").write_text('IPHONEOS_DEPLOYMENT_TARGET = 12.0\nSDKROOT = iphoneos\n')
            (root / "app.json").write_text(json.dumps({"expo": {"plugins": [["expo-build-properties", {"ios": {"deploymentTarget": "12.0"}}]]}}))
            (root / "app.config.js").write_text('throw new Error("Never execute the project")')
            report = self.scan(root)
            evidence = report["platform_review"]["build_evidence"]
            self.assertTrue(any(item["evidence"]["path"] == "app.json" and item["version"] == "12.0" for item in evidence))
            self.assertTrue(any(item["evidence"]["path"] == "Release.xcconfig" and item["version"] == "12.0" for item in evidence))
            self.assertTrue(all(item["kind"] == "authored" for item in evidence))
            self.assertFalse(any(item["id"].startswith("ASR-UPLOAD-") for item in report["findings"]))


if __name__ == "__main__":
    unittest.main()
