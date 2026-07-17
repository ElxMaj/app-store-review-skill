#!/usr/bin/env python3
"""Read-only static evidence collector for iOS and iPadOS App Store review.

The scanner intentionally prefers a missed heuristic over a noisy accusation.
It uses only the Python standard library and never edits the project it scans.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import re
import sys
import zipfile
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from render_app_store_report import render_report_html


VERSION = "1.1.0"
POLICY_VERIFIED_AT = "2026-07-17"

DEFAULT_IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".build",
    ".dart_tool",
    ".expo",
    ".next",
    ".turbo",
    ".yarn",
    "DerivedData",
    "Pods",
    "build",
    "dist",
    "node_modules",
    "vendor",
}

DEPENDENCY_DIRS = {"Pods", "node_modules", ".build", "Carthage", "vendor"}

TEXT_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".dart",
    ".entitlements",
    ".gradle",
    ".h",
    ".html",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".m",
    ".md",
    ".mm",
    ".pbxproj",
    ".plist",
    ".properties",
    ".strings",
    ".storyboard",
    ".swift",
    ".toml",
    ".ts",
    ".tsx",
    ".xib",
    ".xml",
    ".yaml",
    ".yml",
}

SOURCE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".dart",
    ".h",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".m",
    ".mm",
    ".swift",
    ".ts",
    ".tsx",
}

USER_FACING_SUFFIXES = {".dart", ".js", ".jsx", ".strings", ".storyboard", ".swift", ".tsx", ".xib"}

ASSET_SUFFIXES = {".gif", ".jpeg", ".jpg", ".lottie", ".m4a", ".mp3", ".png", ".svg", ".wav", ".webp"}

ASSISTANT_ARTIFACT_PATTERNS = (
    "CLAUDE.md",
    "AGENTS.md",
    ".cursorrules",
    ".windsurfrules",
    ".cursor/",
    ".claude/",
    ".aider",
)


@dataclass(frozen=True)
class Evidence:
    path: str
    line: Optional[int]
    excerpt: str


@dataclass
class Finding:
    id: str
    severity: str
    title: str
    guideline: str
    evidence_confidence: str
    evidence: List[Evidence]
    reason: str
    fix: str
    verification: str


@dataclass
class TextFile:
    path: Path
    relative: str
    text: str
    lines: List[str]


class ScanContext:
    def __init__(
        self,
        root: Path,
        include_dependencies: bool,
        compare_roots: Sequence[Path],
        archive: Optional[Path],
    ) -> None:
        self.root = root.resolve()
        self.include_dependencies = include_dependencies
        self.compare_roots = [path.resolve() for path in compare_roots]
        self.archive = archive.resolve() if archive else None
        self.files: List[Path] = []
        self.text_files: List[TextFile] = []
        self.findings: List[Finding] = []
        self.manual_checks: List[Dict[str, str]] = []
        self.limitations: List[str] = []
        self.frameworks: List[str] = []
        self.native_ios_root: Optional[str] = None
        self.targets: List[Dict[str, str]] = []
        self.config_values: Dict[str, List[Tuple[Any, Evidence]]] = defaultdict(list)
        self.privacy_categories: Dict[str, List[Evidence]] = defaultdict(list)

    def rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    def add_finding(self, finding: Finding) -> None:
        existing = next((item for item in self.findings if item.id == finding.id), None)
        if existing:
            seen = {(e.path, e.line, e.excerpt) for e in existing.evidence}
            for evidence in finding.evidence:
                key = (evidence.path, evidence.line, evidence.excerpt)
                if key not in seen and len(existing.evidence) < 20:
                    existing.evidence.append(evidence)
                    seen.add(key)
            return
        self.findings.append(finding)

    def add_manual(self, check_id: str, title: str, reason: str, verification: str) -> None:
        if any(item["id"] == check_id for item in self.manual_checks):
            return
        self.manual_checks.append(
            {"id": check_id, "title": title, "reason": reason, "verification": verification}
        )


def safe_read_text(path: Path, max_bytes: int = 2_000_000) -> Optional[str]:
    try:
        if path.stat().st_size > max_bytes:
            return None
        data = path.read_bytes()
    except (OSError, PermissionError):
        return None
    if b"\x00" in data[:4096]:
        return None
    return data.decode("utf-8", errors="replace")


def walk_files(root: Path, include_dependencies: bool = False) -> Iterable[Path]:
    ignored = DEFAULT_IGNORED_DIRS.copy()
    if include_dependencies:
        ignored -= DEPENDENCY_DIRS
    for current, directories, filenames in os.walk(root):
        directories[:] = [
            name
            for name in directories
            if name not in ignored and not name.endswith(".xcarchive")
        ]
        current_path = Path(current)
        for filename in filenames:
            yield current_path / filename


def evidence_for_match(text_file: TextFile, match: re.Match[str]) -> Evidence:
    line_number = text_file.text.count("\n", 0, match.start()) + 1
    line = text_file.lines[line_number - 1].strip() if text_file.lines else ""
    return Evidence(text_file.relative, line_number, line[:240])


def first_matches(
    text_files: Iterable[TextFile], patterns: Sequence[str], limit: int = 12, flags: int = re.IGNORECASE
) -> List[Evidence]:
    compiled = [re.compile(pattern, flags) for pattern in patterns]
    found: List[Evidence] = []
    for text_file in text_files:
        if is_test_path(text_file.relative):
            continue
        for pattern in compiled:
            match = pattern.search(text_file.text)
            if match:
                found.append(evidence_for_match(text_file, match))
                break
        if len(found) >= limit:
            break
    return found


def is_test_path(relative: str) -> bool:
    lowered = relative.lower()
    parts = lowered.split("/")
    return any(part in {"test", "tests", "testing", "__tests__", "uitests"} for part in parts) or any(
        token in lowered for token in ("tests.swift", "test.swift", ".spec.", ".test.")
    )


def load_files(ctx: ScanContext) -> None:
    ctx.files = list(walk_files(ctx.root, ctx.include_dependencies))
    for path in ctx.files:
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
            "Podfile",
            "Package.swift",
            "pubspec.yaml",
        }:
            continue
        text = safe_read_text(path)
        if text is None:
            continue
        ctx.text_files.append(TextFile(path, ctx.rel(path), text, text.splitlines()))


def parse_json(path: Path) -> Optional[Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def discover_project(ctx: ScanContext) -> None:
    names = {path.name for path in ctx.files}
    package_jsons = [path for path in ctx.files if path.name == "package.json"]
    package_data: List[Dict[str, Any]] = []
    for path in package_jsons:
        data = parse_json(path)
        if isinstance(data, dict):
            package_data.append(data)
    package_blob = json.dumps(package_data).lower()

    pbx_files = [path for path in ctx.files if path.name == "project.pbxproj"]
    if pbx_files:
        ctx.frameworks.append("xcode")
        native_roots = []
        for path in pbx_files:
            project_dir = path.parent.parent
            native_roots.append(project_dir.parent if project_dir.parent.name == "ios" else project_dir)
            parse_targets(ctx, path)
        shortest = min(native_roots, key=lambda item: len(item.parts))
        ctx.native_ios_root = ctx.rel(shortest)

    if '"expo"' in package_blob or any(name.startswith("app.config.") for name in names):
        ctx.frameworks.append("expo")
    if '"react-native"' in package_blob:
        ctx.frameworks.append("react-native")
    pubspecs = [path for path in ctx.files if path.name == "pubspec.yaml"]
    if any(re.search(r"(?m)^\s*flutter\s*:", safe_read_text(path) or "") for path in pubspecs):
        ctx.frameworks.append("flutter")
    if not ctx.frameworks:
        ctx.frameworks.append("unknown")
        ctx.limitations.append("No Xcode, Expo, React Native, or Flutter project marker was found.")

    if any(framework in ctx.frameworks for framework in ("expo", "react-native", "flutter")) and not pbx_files:
        ctx.limitations.append(
            "No generated native Xcode project was found. Target membership, merged plist, entitlements, and archive checks remain manual."
        )


def parse_targets(ctx: ScanContext, pbx_path: Path) -> None:
    text = safe_read_text(pbx_path, max_bytes=10_000_000) or ""
    pattern = re.compile(
        r"[A-F0-9]{8,}\s+/\*\s*(?P<label>.*?)\s*\*/\s*=\s*\{\s*isa\s*=\s*PBXNativeTarget;(?P<body>.*?)\n\s*\};",
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        body = match.group("body")
        name_match = re.search(r"\bname\s*=\s*(.*?);", body)
        product_match = re.search(r"\bproductType\s*=\s*(.*?);", body)
        name = strip_pbx_value(name_match.group(1)) if name_match else match.group("label").strip()
        product_type = strip_pbx_value(product_match.group(1)) if product_match else "unknown"
        target = {"name": name, "product_type": product_type, "project": ctx.rel(pbx_path)}
        if target not in ctx.targets:
            ctx.targets.append(target)


def strip_pbx_value(value: str) -> str:
    return value.strip().strip('"')


def collect_configuration(ctx: ScanContext) -> None:
    for path in ctx.files:
        if path.suffix.lower() not in {".plist", ".entitlements", ".xcprivacy"}:
            continue
        try:
            with path.open("rb") as handle:
                value = plistlib.load(handle)
        except (OSError, plistlib.InvalidFileException, ValueError):
            if path.name == "PrivacyInfo.xcprivacy":
                ctx.add_finding(
                    Finding(
                        "ASR-PRIVACY-004",
                        "warning",
                        "Privacy manifest could not be parsed",
                        "Privacy manifest submission requirement",
                        "official",
                        [Evidence(ctx.rel(path), None, "Invalid or unsupported plist")],
                        "A malformed manifest cannot establish Required Reason API declarations.",
                        "Open the manifest in Xcode or plutil and correct its plist structure.",
                        "Run plutil -lint on the manifest and inspect the built bundle.",
                    )
                )
            continue
        if isinstance(value, dict):
            record_config_dict(ctx, value, path)
            if path.name == "PrivacyInfo.xcprivacy":
                record_privacy_manifest(ctx, value, path)

    for text_file in ctx.text_files:
        if text_file.path.name != "project.pbxproj":
            continue
        for match in re.finditer(r"\bINFOPLIST_KEY_([A-Za-z0-9_]+)\s*=\s*(.*?);", text_file.text):
            key = match.group(1)
            raw = strip_pbx_value(match.group(2))
            ctx.config_values[key].append((raw, evidence_for_match(text_file, match)))

    collect_expo_config(ctx)


def record_config_dict(ctx: ScanContext, value: Dict[str, Any], path: Path) -> None:
    for key, item in value.items():
        excerpt = f"{key} = {render_value(item)}"
        ctx.config_values[key].append((item, Evidence(ctx.rel(path), None, excerpt[:240])))


def record_privacy_manifest(ctx: ScanContext, value: Dict[str, Any], path: Path) -> None:
    entries = value.get("NSPrivacyAccessedAPITypes", [])
    if not isinstance(entries, list):
        return
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        category = entry.get("NSPrivacyAccessedAPIType")
        if isinstance(category, str):
            reasons = entry.get("NSPrivacyAccessedAPITypeReasons", [])
            ctx.privacy_categories[category].append(
                Evidence(ctx.rel(path), None, f"{category}: {render_value(reasons)}")
            )


def collect_expo_config(ctx: ScanContext) -> None:
    for path in ctx.files:
        if path.name not in {"app.json", "app.config.json"}:
            continue
        data = parse_json(path)
        if not isinstance(data, dict):
            continue
        expo = data.get("expo", data)
        if not isinstance(expo, dict):
            continue
        ios = expo.get("ios", {})
        if not isinstance(ios, dict):
            continue
        for group in ("infoPlist", "entitlements"):
            values = ios.get(group, {})
            if isinstance(values, dict):
                for key, value in values.items():
                    ctx.config_values[key].append(
                        (value, Evidence(ctx.rel(path), None, f"expo.ios.{group}.{key} = {render_value(value)}"))
                    )
        privacy = ios.get("privacyManifests", {})
        if isinstance(privacy, dict):
            entries = privacy.get("NSPrivacyAccessedAPITypes", [])
            if isinstance(entries, list):
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    category = entry.get("NSPrivacyAccessedAPIType")
                    if isinstance(category, str):
                        ctx.privacy_categories[category].append(
                            Evidence(ctx.rel(path), None, f"expo.ios.privacyManifests: {category}")
                        )


def render_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


PROTECTED_APIS: Dict[str, Tuple[Sequence[str], str, str]] = {
    "NSCameraUsageDescription": (
        (r"requestAccess\s*\(\s*for\s*:\s*\.video", r"sourceType\s*=\s*\.camera", r"VNDocumentCameraViewController"),
        "Camera",
        "5.1.1(ii)",
    ),
    "NSMicrophoneUsageDescription": (
        (r"AVAudioRecorder", r"requestRecordPermission", r"SFSpeechAudioBufferRecognitionRequest"),
        "Microphone",
        "5.1.1(ii)",
    ),
    "NSPhotoLibraryUsageDescription": (
        (r"PHPhotoLibrary", r"\bPHAsset\b"),
        "Photo library",
        "5.1.1(ii)",
    ),
    "NSLocationWhenInUseUsageDescription": (
        (r"requestWhenInUseAuthorization", r"showsUserLocation\s*=\s*true"),
        "Location",
        "5.1.1(ii)",
    ),
    "NSContactsUsageDescription": ((r"CNContactStore\s*\(", r"requestAccess\s*\(\s*for\s*:\s*\.contacts"), "Contacts", "5.1.1(ii)"),
    "NSBluetoothAlwaysUsageDescription": ((r"CBCentralManager\s*\(", r"CBPeripheralManager\s*\("), "Bluetooth", "5.1.1(ii)"),
    "NSMotionUsageDescription": ((r"CMMotionManager\s*\(", r"CMPedometer\s*\("), "Motion", "5.1.1(ii)"),
    "NSSpeechRecognitionUsageDescription": ((r"SFSpeechRecognizer\s*\(",), "Speech recognition", "5.1.1(ii)"),
    "NSFaceIDUsageDescription": ((r"LAPolicy\.deviceOwnerAuthenticationWithBiometrics", r"biometryType\s*==\s*\.faceID"), "Face ID", "5.1.1(ii)"),
    "NSLocalNetworkUsageDescription": ((r"NWBrowser\s*\(", r"NWListener\s*\(", r"NetServiceBrowser"), "Local network", "5.1.1(ii)"),
    "NSUserTrackingUsageDescription": ((r"requestTrackingAuthorization", r"advertisingIdentifier"), "Tracking", "5.1.2"),
}


REQUIRED_REASON_APIS: Dict[str, Tuple[str, Sequence[str]]] = {
    "NSPrivacyAccessedAPICategoryUserDefaults": ("UserDefaults", (r"\bUserDefaults\b",)),
    "NSPrivacyAccessedAPICategoryFileTimestamp": (
        "file timestamps",
        (r"attributesOfItem", r"contentModificationDateKey", r"\bfstat\s*\(", r"\bstat\s*\("),
    ),
    "NSPrivacyAccessedAPICategorySystemBootTime": (
        "system boot time",
        (r"systemUptime", r"mach_absolute_time", r"clock_gettime_nsec_np"),
    ),
    "NSPrivacyAccessedAPICategoryDiskSpace": (
        "disk space",
        (r"volumeAvailableCapacity", r"attributesOfFileSystem", r"\bstatfs\s*\("),
    ),
    "NSPrivacyAccessedAPICategoryActiveKeyboards": (
        "active keyboards",
        (r"UITextInputMode\.activeInputModes",),
    ),
}


CROSS_PLATFORM_PERMISSION_PACKAGES: Dict[str, Tuple[str, Sequence[str]]] = {
    "NSCameraUsageDescription": (
        "camera",
        (r"expo-camera", r"react-native-vision-camera", r"camera_avfoundation"),
    ),
    "NSMicrophoneUsageDescription": (
        "microphone",
        (r"expo-audio", r"react-native-audio-recorder-player", r"record:"),
    ),
    "NSPhotoLibraryUsageDescription": (
        "photo library",
        (r"expo-media-library", r"photo_manager", r"@react-native-camera-roll/camera-roll"),
    ),
    "NSLocationWhenInUseUsageDescription": (
        "location",
        (r"expo-location", r"react-native-geolocation", r"geolocator:"),
    ),
    "NSContactsUsageDescription": (
        "contacts",
        (r"expo-contacts", r"react-native-contacts", r"contacts_service:"),
    ),
    "NSCalendarsUsageDescription": (
        "calendar",
        (r"expo-calendar", r"react-native-calendar-events"),
    ),
    "NSBluetoothAlwaysUsageDescription": (
        "Bluetooth",
        (r"react-native-ble-plx", r"flutter_blue", r"flutter_reactive_ble"),
    ),
    "NSMotionUsageDescription": (
        "motion",
        (r"expo-sensors", r"pedometer:"),
    ),
    "NSFaceIDUsageDescription": (
        "Face ID",
        (r"expo-local-authentication", r"react-native-biometrics", r"local_auth:"),
    ),
}


def scan_protected_apis(ctx: ScanContext) -> None:
    source_files = [item for item in ctx.text_files if item.path.suffix.lower() in SOURCE_SUFFIXES]
    for key, (patterns, label, guideline) in PROTECTED_APIS.items():
        matches = first_matches(source_files, patterns)
        if not matches:
            continue
        if key not in ctx.config_values:
            ctx.add_finding(
                Finding(
                    f"ASR-PERM-{stable_suffix(key)}",
                    "blocker",
                    f"{label} API lacks {key}",
                    guideline,
                    "official",
                    matches,
                    f"Protected {label.lower()} access was found, but the matching purpose string was not found in parsed plist, build-setting, or Expo configuration sources.",
                    f"Add a specific {key} at the authored configuration source. Describe the feature and why the data is needed.",
                    "Inspect the merged Info.plist in the release archive, then trigger the permission on a clean install.",
                )
            )
        else:
            for value, evidence in ctx.config_values[key]:
                if isinstance(value, str) and vague_purpose_string(value):
                    ctx.add_finding(
                        Finding(
                            f"ASR-PERM-QUALITY-{stable_suffix(key)}",
                            "warning",
                            f"{key} is vague",
                            guideline,
                            "official",
                            [evidence],
                            "The purpose string does not clearly identify a feature-specific reason for access.",
                            "Rewrite the string to name the feature, the data, and the user benefit.",
                            "Trigger the permission on a clean install in every supported localization.",
                        )
                    )


def scan_cross_platform_permissions(ctx: ScanContext) -> None:
    manifests = [
        item
        for item in ctx.text_files
        if item.path.name in {"package.json", "pubspec.yaml", "Podfile", "Podfile.lock", "Package.swift"}
    ]
    for key, (label, patterns) in CROSS_PLATFORM_PERMISSION_PACKAGES.items():
        matches = first_matches(manifests, patterns, limit=8)
        if not matches or key in ctx.config_values:
            continue
        ctx.add_finding(
            Finding(
                f"ASR-PERM-PACKAGE-{stable_suffix(key)}",
                "warning",
                f"{label.capitalize()} package needs resolved permission review",
                "5.1.1(ii)",
                "official",
                matches,
                f"A dependency capable of requesting {label} access is installed, but {key} was not found in parsed authored or native configuration. Installed packages can be unused or configured by a plugin, so this is not a confirmed invocation.",
                f"Confirm whether the release build invokes {label} access. If it does, add a feature-specific {key} at the authored configuration source.",
                "Inspect the resolved native configuration or archive and trigger the feature on a clean install.",
            )
        )


def stable_suffix(value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:6].upper()
    return digest


def vague_purpose_string(value: str) -> bool:
    words = re.findall(r"[A-Za-z0-9]+", value)
    lowered = value.lower()
    generic = any(phrase in lowered for phrase in ("access needed", "requires access", "need access"))
    return len(words) < 7 or generic


def scan_privacy_manifests(ctx: ScanContext) -> None:
    source_files = [item for item in ctx.text_files if item.path.suffix.lower() in SOURCE_SUFFIXES]
    for category, (label, patterns) in REQUIRED_REASON_APIS.items():
        matches = first_matches(source_files, patterns)
        if not matches:
            continue
        if category not in ctx.privacy_categories:
            ctx.add_finding(
                Finding(
                    f"ASR-PRIVACY-{stable_suffix(category)}",
                    "blocker",
                    f"Required Reason API declaration missing for {label}",
                    "Privacy manifest submission requirement",
                    "official",
                    matches,
                    f"The scanner found {label} API use but no parsed privacy manifest declared {category}.",
                    "Add the category with an Apple-approved reason that accurately matches the use. Configure every executable target that contains the API.",
                    "Validate each built app and extension bundle, then upload through App Store Connect validation.",
                )
            )
    if len(ctx.targets) > 1 and ctx.privacy_categories:
        ctx.add_manual(
            "ASR-MANUAL-TARGET-MANIFEST",
            "Verify privacy manifest target membership",
            "Static category discovery does not prove that each declaration is copied into the executable bundle that uses the API.",
            "Inspect the release archive for a privacy manifest in each relevant app and extension bundle.",
        )


def scan_completeness(ctx: ScanContext) -> None:
    candidates = [item for item in ctx.text_files if item.path.suffix.lower() in USER_FACING_SUFFIXES]
    operational = [
        item
        for item in ctx.text_files
        if item.path.suffix.lower()
        in SOURCE_SUFFIXES.union({".json", ".pbxproj", ".plist", ".strings", ".storyboard", ".xib"})
    ]
    placeholder_patterns = (
        r"[\"']\s*lorem ipsum",
        r"[\"'][^\"'\n]{0,60}\bcoming soon\b",
        r"[\"']\s*(?:placeholder|sample text|your app name)\s*[\"']",
    )
    matches = first_matches(candidates, placeholder_patterns, limit=12)
    if matches:
        ctx.add_finding(
            Finding(
                "ASR-COMPLETE-001",
                "warning",
                "Potential user-visible placeholder content",
                "2.1",
                "official",
                matches,
                "Reachable placeholder or unfinished content can make the submitted app incomplete.",
                "Confirm whether each string ships and is reachable. Replace or remove every production placeholder.",
                "Exercise the release build and search localized resources and storyboards again.",
            )
        )

    url_patterns = (r"https?://(?:www\.)?(?:example\.com|yourdomain\.com|placeholder\.)",)
    url_matches = first_matches(operational, url_patterns, limit=8)
    if url_matches:
        ctx.add_finding(
            Finding(
                "ASR-COMPLETE-002",
                "warning",
                "Placeholder URL found",
                "2.1",
                "official",
                url_matches,
                "Reviewers can encounter nonfunctional support, privacy, terms, or feature links.",
                "Replace the placeholder with the production URL at the authored source of truth.",
                "Open every external link from the release build without an authenticated developer session.",
            )
        )

    ip_matches = first_matches(operational, (r"https?://(?:\d{1,3}\.){3}\d{1,3}\b",), limit=8)
    if ip_matches:
        ctx.add_finding(
            Finding(
                "ASR-NETWORK-001",
                "warning",
                "Literal IPv4 endpoint found",
                "2.1",
                "official",
                ip_matches,
                "A literal IPv4 endpoint can fail in IPv6-only environments and can indicate a local or staging dependency.",
                "Use a production hostname with DNS and ensure the service works from IPv6-only networks, unless local-device discovery is the intended feature.",
                "Test the release build on an IPv6-only network and document any local-network requirement.",
            )
        )


def scan_technical_patterns(ctx: ScanContext) -> None:
    source = [item for item in ctx.text_files if item.path.suffix.lower() in SOURCE_SUFFIXES]
    uiwebview = first_matches(source, (r"\bUIWebView\b",), limit=10)
    if uiwebview:
        ctx.add_finding(
            Finding(
                "ASR-TECH-UIWEBVIEW",
                "blocker",
                "UIWebView API found",
                "2.5.1",
                "official",
                uiwebview,
                "UIWebView is deprecated and App Store uploads must use supported web-view APIs.",
                "Migrate the shipping path to WKWebView and update dependencies that still link UIWebView.",
                "Scan the release archive and run upload validation.",
            )
        )

    dynamic = first_matches(
        source,
        (r"\bJSPatch\b", r"\bdlopen\s*\(", r"\bdlsym\s*\(", r"react-native-code-push", r"\bCodePush\b"),
        limit=12,
    )
    if dynamic:
        ctx.add_finding(
            Finding(
                "ASR-TECH-DYNAMIC-CODE",
                "warning",
                "Runtime code-update or loading signal found",
                "2.5.2",
                "official",
                dynamic,
                "The matched API or package can be used to load code after review. Its actual production behavior determines compliance.",
                "Trace the release path. Remove prohibited code loading or constrain updates so they do not change reviewed features or functionality.",
                "Inspect network behavior and the release archive, then explain any permitted interpreted-content use in review notes.",
            )
        )

    dev_endpoints = first_matches(
        source,
        (r"https?://(?:localhost|127\.0\.0\.1)(?::\d+)?", r"https?://[^\s\"']*\b(?:staging|dev)\."),
        limit=8,
    )
    if dev_endpoints:
        ctx.add_finding(
            Finding(
                "ASR-TECH-ENDPOINT",
                "warning",
                "Development endpoint found in source",
                "2.1",
                "official",
                dev_endpoints,
                "A release build that points to a local or staging backend can block review.",
                "Confirm build-configuration selection and remove production references to local or staging services.",
                "Inspect release configuration and exercise the archive on a clean device.",
            )
        )

    ats_evidence: List[Evidence] = []
    for value, evidence in ctx.config_values.get("NSAppTransportSecurity", []):
        if isinstance(value, dict) and value.get("NSAllowsArbitraryLoads") is True:
            ats_evidence.append(evidence)
    if ats_evidence:
        ctx.add_finding(
            Finding(
                "ASR-TECH-ATS",
                "warning",
                "App Transport Security allows arbitrary loads",
                "2.5.1",
                "official",
                ats_evidence,
                "A global ATS exception broadens insecure transport beyond a specific documented need.",
                "Use HTTPS and the narrowest domain-specific exception that the app genuinely requires.",
                "Inspect the merged plist and test every endpoint with the exception removed or narrowed.",
            )
        )


def scan_feature_heuristics(ctx: ScanContext) -> None:
    searchable = [item for item in ctx.text_files if item.path.suffix.lower() in SOURCE_SUFFIXES or item.path.name in {"package.json", "pubspec.yaml", "Podfile.lock", "Package.swift"}]

    social = first_matches(
        searchable,
        (r"GoogleSignIn|GIDSignIn|@react-native-google-signin", r"FBSDKLogin|LoginManager\s*\(|flutter_facebook_auth"),
        limit=8,
    )
    apple = first_matches(searchable, (r"ASAuthorizationAppleIDProvider|SignInWithApple|sign_in_with_apple|expo-apple-authentication",), limit=4)
    if social and not apple:
        ctx.add_finding(
            Finding(
                "ASR-ACCOUNT-SIWA",
                "warning",
                "Third-party login found without a Sign in with Apple signal",
                "4.8",
                "official",
                social,
                "Guideline 4.8 can require an equivalent login service, but its exceptions depend on the account model.",
                "Check the current 4.8 exceptions. If none applies, add Sign in with Apple with equivalent prominence and capability.",
                "Exercise every login option and document any exception with evidence.",
            )
        )

    signup = first_matches(searchable, (r"\b(?:signUp|signup|registerAccount|createAccount)\b", r"create_user_with_email"), limit=8)
    deletion = first_matches(searchable, (r"\b(?:deleteAccount|deleteUser|removeAccount)\b", r"account deletion", r"delete_user"), limit=8)
    if signup and not deletion:
        ctx.add_finding(
            Finding(
                "ASR-ACCOUNT-DELETE",
                "warning",
                "Account creation found without an in-app deletion signal",
                "5.1.1(v)",
                "official",
                signup,
                "Apps that support account creation generally must let users initiate deletion in the app. Static naming heuristics cannot see every implementation.",
                "Locate or add the in-app deletion route and ensure it deletes server-side data subject to disclosed retention requirements.",
                "Create an account in the release environment, delete it in-app, and verify authentication and retained data afterward.",
            )
        )

    iap = first_matches(searchable, (r"\bStoreKit\b", r"react-native-iap", r"in_app_purchase", r"RevenueCat|Purchases\.configure", r"expo-in-app-purchases"), limit=8)
    restore = first_matches(searchable, (r"restoreCompletedTransactions|restorePurchases|syncPurchases|Transaction\.currentEntitlements",), limit=8)
    if iap and not restore:
        ctx.add_finding(
            Finding(
                "ASR-IAP-RESTORE",
                "warning",
                "In-app purchase code found without a restore signal",
                "3.1.1 and 3.1.2",
                "official",
                iap,
                "Restorable purchases need a usable restoration path. Consumable-only products can be an exception to this heuristic.",
                "Classify every product and add a visible restore or entitlement-sync path where required.",
                "Test purchases and restore with a sandbox account on a clean install.",
            )
        )
    if iap:
        price_matches = first_matches(
            [item for item in searchable if item.path.suffix.lower() in USER_FACING_SUFFIXES],
            (r"[\"'][^\"'\n]{0,40}(?:\$|€|£)\s?\d+(?:[.,]\d{2})?[^\"'\n]*[\"']",),
            limit=10,
        )
        if price_matches:
            ctx.add_finding(
                Finding(
                    "ASR-IAP-PRICE",
                    "warning",
                    "Hardcoded purchase price found",
                    "2.3 and 3.1.2",
                    "official",
                    price_matches,
                    "A hardcoded currency amount can disagree with the storefront price and localization.",
                    "Render the StoreKit product's localized display price and period.",
                    "Test the paywall with sandbox accounts from more than one storefront.",
                )
            )

    ai = first_matches(
        searchable,
        (
            r"api\.openai\.com|\bOpenAIClient\b|from\s+[\"']openai[\"']",
            r"api\.anthropic\.com|\bAnthropic\s*\(",
            r"generativelanguage\.googleapis\.com|GoogleGenerativeAI|GoogleGenerativeAI",
        ),
        limit=10,
    )
    consent = first_matches(searchable, (r"(?:ai|third.?party).{0,50}(?:consent|permission|disclosure)", r"(?:consent|permission|disclosure).{0,50}(?:ai|OpenAI|Anthropic|Gemini)"), limit=8)
    if ai and not consent:
        ctx.add_finding(
            Finding(
                "ASR-PRIVACY-AI",
                "warning",
                "Third-party AI service found without a consent signal",
                "5.1.2(i)",
                "official",
                ai,
                "If personal data is sent to the service, Apple requires clear disclosure of where it is shared and explicit permission before sharing. The scanner cannot determine the payload.",
                "Trace the payload. When personal data is shared, add provider-specific disclosure and explicit permission before the first request, then align the privacy policy and App Store answers.",
                "Use a clean account, decline permission, and confirm no personal data reaches the third-party AI endpoint.",
            )
        )

    tracking_sdk = first_matches(searchable, (r"GoogleMobileAds|GADMobileAds", r"AppsFlyerLib|AppsFlyer", r"Adjust\.appDidLaunch|react-native-adjust", r"FBSDKCoreKit|FacebookCore"), limit=8)
    att_prompt = first_matches(searchable, (r"requestTrackingAuthorization",), limit=4)
    tracking_key = "NSUserTrackingUsageDescription" in ctx.config_values
    if tracking_sdk and (not att_prompt or not tracking_key):
        ctx.add_finding(
            Finding(
                "ASR-PRIVACY-ATT",
                "warning",
                "Tracking-capable SDK needs ATT behavior review",
                "5.1.2",
                "official",
                tracking_sdk,
                "The SDK can participate in tracking, but package presence alone does not prove that the app tracks. The purpose string or authorization signal was not fully present.",
                "Determine whether the configured data use meets Apple's tracking definition. If it does, request ATT before tracking and provide the purpose string. Otherwise disable tracking behavior and align privacy answers.",
                "Inspect network calls before and after the ATT choice and compare them with App Store privacy answers.",
            )
        )

    ugc = first_matches(searchable, (r"(?:anonymous|random).{0,20}chat", r"(?:reportUser|blockUser|moderateContent)", r"\b(?:comments|user posts|chat messages)\b"), limit=8)
    if ugc:
        ctx.add_manual(
            "ASR-MANUAL-UGC",
            "Exercise UGC safety controls",
            "Source signals suggest user-generated content or chat. Static analysis cannot prove filtering, reporting, blocking, contact information, and operational response.",
            "Run each control with two accounts and review the current Guideline 1.2 requirements, including random or anonymous chat restrictions.",
        )

    health = first_matches(searchable, (r"\bHKHealthStore\b", r"\bHealthKit\b", r"health_kit_reporter"), limit=6)
    if health:
        ctx.add_manual(
            "ASR-MANUAL-HEALTH",
            "Map HealthKit read and write permissions",
            "HealthKit usage strings depend on whether the app reads, writes, or does both. Package presence alone cannot select the correct keys or validate health claims.",
            "Trace requested HealthKit types, verify the matching share and update purpose strings, inspect entitlements, and review health claims under current policy.",
        )


def scan_archive(ctx: ScanContext) -> None:
    if not ctx.archive:
        ctx.add_manual(
            "ASR-MANUAL-ARCHIVE",
            "Inspect the release archive",
            "Repository contents do not prove which files, manifests, plist values, frameworks, and extensions ship.",
            "Create the release archive and rerun the scanner with --archive, then inspect merged configuration with Apple tooling.",
        )
        return
    if not ctx.archive.exists():
        ctx.limitations.append(f"Archive does not exist: {ctx.archive}")
        return
    if not zipfile.is_zipfile(ctx.archive):
        ctx.limitations.append("The supplied archive is not a readable IPA or ZIP archive.")
        return
    artifacts: List[Evidence] = []
    bundles: Set[str] = set()
    manifests: Set[str] = set()
    try:
        with zipfile.ZipFile(ctx.archive) as archive:
            for name in archive.namelist():
                normalized = name.replace("\\", "/")
                if ".app/" in normalized or ".appex/" in normalized:
                    bundle_match = re.search(r"(.+?\.(?:app|appex))/", normalized)
                    if bundle_match:
                        bundles.add(bundle_match.group(1))
                if normalized.endswith("PrivacyInfo.xcprivacy"):
                    parent_match = re.search(r"(.+?\.(?:app|appex))/.+PrivacyInfo\.xcprivacy$", normalized)
                    if parent_match:
                        manifests.add(parent_match.group(1))
                lowered = normalized.lower()
                if any(pattern.lower() in lowered for pattern in ASSISTANT_ARTIFACT_PATTERNS):
                    artifacts.append(Evidence(f"archive:{ctx.archive.name}", None, normalized[:240]))
    except (OSError, zipfile.BadZipFile) as exc:
        ctx.limitations.append(f"Archive inspection failed: {exc}")
        return
    if artifacts:
        ctx.add_finding(
            Finding(
                "ASR-ARCHIVE-ARTIFACT",
                "warning",
                "Assistant or internal context artifact ships in the archive",
                "2.1 quality and information exposure",
                "inference",
                artifacts[:20],
                "Internal instructions or notes add no product value and can expose private implementation context. This is not evidence of AI-authorship detection.",
                "Remove the files from Copy Bundle Resources or the packaging step at the authored source of truth.",
                "Rebuild and confirm the archive no longer contains them.",
            )
        )
    if bundles:
        missing = sorted(bundle for bundle in bundles if bundle not in manifests)
        if missing:
            ctx.add_manual(
                "ASR-MANUAL-ARCHIVE-MANIFESTS",
                "Confirm privacy manifests in built bundles",
                "Some app or extension bundles did not contain a discoverable PrivacyInfo.xcprivacy. A bundle only needs relevant declarations when its code requires them.",
                "Map Required Reason API use to these bundles and add accurate manifests where required: " + ", ".join(missing[:12]),
            )


def scan_asset_reuse(ctx: ScanContext) -> None:
    if not ctx.compare_roots:
        return
    own = hash_assets(ctx.root, ctx.include_dependencies)
    matches: List[Evidence] = []
    for compare_root in ctx.compare_roots:
        if not compare_root.exists():
            ctx.limitations.append(f"Comparison root does not exist: {compare_root}")
            continue
        other = hash_assets(compare_root, ctx.include_dependencies)
        for digest in sorted(set(own).intersection(other)):
            for own_path in own[digest][:3]:
                for other_path in other[digest][:3]:
                    matches.append(Evidence(own_path, None, f"Exact asset match: {compare_root.name}/{other_path}"))
                    if len(matches) >= 20:
                        break
                if len(matches) >= 20:
                    break
            if len(matches) >= 20:
                break
    if matches:
        ctx.add_finding(
            Finding(
                "ASR-43-ASSET-REUSE",
                "warning",
                "Exact asset reuse found across compared projects",
                "4.3",
                "documented-case",
                matches,
                "Exact reuse can support a portfolio, template, or provenance similarity concern. One documented 4.3 recovery isolated an icon change, but asset reuse is not a universal rejection rule.",
                "Determine whether each shared asset is intentional, licensed, and appropriate. Replace primary identity assets when products should be distinct.",
                "Rehash the assets and review the product pages and first-run identity side by side.",
            )
        )


def hash_assets(root: Path, include_dependencies: bool) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = defaultdict(list)
    for path in walk_files(root, include_dependencies):
        if path.suffix.lower() not in ASSET_SUFFIXES:
            continue
        try:
            if path.stat().st_size == 0 or path.stat().st_size > 50_000_000:
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            result[digest].append(path.relative_to(root).as_posix())
        except (OSError, ValueError):
            continue
    return result


def add_baseline_manual_checks(ctx: ScanContext) -> None:
    ctx.add_manual(
        "ASR-MANUAL-SDK",
        "Verify the submission SDK from the archive",
        "Source files do not reliably establish the Xcode and SDK used to upload the build. Apple requires Xcode 26 or later with an iOS 26-family SDK since April 28, 2026.",
        "Inspect the archive and CI build environment, then recheck Apple's Upcoming Requirements before submission.",
    )
    ctx.add_manual(
        "ASR-MANUAL-METADATA",
        "Compare App Store metadata with the candidate build",
        "Descriptions, screenshots, keywords, age rating, privacy answers, Accessibility Nutrition Labels, and review notes may live outside the repository.",
        "Export or open the App Store Connect metadata and compare every claim and image with the exact build.",
    )
    ctx.add_manual(
        "ASR-MANUAL-REVIEWER-PATH",
        "Execute the reviewer experience",
        "Static analysis cannot prove launch stability, demo access, purchases, server state, links, iPad layout, offline behavior, or accessibility.",
        "Run the release candidate through install, launch, login, core flow, permissions, purchases, restore, links, failure states, and iPad accessibility checks.",
    )
    ctx.add_manual(
        "ASR-MANUAL-PRIVACY",
        "Reconcile real data flows with App Store privacy answers",
        "Static SDK and endpoint signals do not establish every payload, purpose, retention rule, or third-party use.",
        "Trace production data flows, including analytics and AI providers, then update consent, policy, manifests, and App Store answers together.",
    )


def run_scan(ctx: ScanContext) -> Dict[str, Any]:
    load_files(ctx)
    discover_project(ctx)
    collect_configuration(ctx)
    scan_protected_apis(ctx)
    scan_cross_platform_permissions(ctx)
    scan_privacy_manifests(ctx)
    scan_completeness(ctx)
    scan_technical_patterns(ctx)
    scan_feature_heuristics(ctx)
    scan_archive(ctx)
    scan_asset_reuse(ctx)
    add_baseline_manual_checks(ctx)

    severity_order = {"blocker": 0, "warning": 1, "info": 2}
    ctx.findings.sort(key=lambda item: (severity_order.get(item.severity, 9), item.id))
    ctx.manual_checks.sort(key=lambda item: item["id"])
    counts = {
        "blocker": sum(item.severity == "blocker" for item in ctx.findings),
        "warning": sum(item.severity == "warning" for item in ctx.findings),
        "manual_check": len(ctx.manual_checks),
        "info": sum(item.severity == "info" for item in ctx.findings),
    }
    if counts["blocker"]:
        verdict = "NOT READY"
    elif counts["warning"] or counts["manual_check"]:
        verdict = "NEEDS REVIEW"
    else:
        verdict = "NO STATIC BLOCKERS FOUND"

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "root": str(ctx.root),
        "verdict": verdict,
        "policy_verified_at": POLICY_VERIFIED_AT,
        "project": {
            "frameworks": sorted(set(ctx.frameworks)),
            "native_ios_root": ctx.native_ios_root,
            "targets": ctx.targets,
        },
        "counts": counts,
        "findings": [finding_to_dict(item) for item in ctx.findings],
        "manual_checks": ctx.manual_checks,
        "limitations": ctx.limitations,
        "scanner": {"name": "app_store_review_scan", "version": VERSION},
    }


def finding_to_dict(finding: Finding) -> Dict[str, Any]:
    value = asdict(finding)
    value["evidence"] = [asdict(item) for item in finding.evidence]
    return value


def render_markdown(report: Dict[str, Any]) -> str:
    project = report["project"]
    target_names = ", ".join(item["name"] for item in project["targets"]) or "not resolved"
    lines = [
        f"# App Store review: {Path(report['root']).name}",
        "",
        f"Verdict: {report['verdict']}",
        f"Policy verified: {report['policy_verified_at']}",
        f"Frameworks: {', '.join(project['frameworks'])}",
        f"Targets: {target_names}",
        "",
        "## Scope and limitations",
        "",
    ]
    if report["limitations"]:
        lines.extend(f"- {item}" for item in report["limitations"])
    else:
        lines.append("- Static repository scan completed. Runtime and App Store Connect checks remain manual.")

    for severity, heading in (("blocker", "Blockers"), ("warning", "Warnings"), ("info", "Info")):
        selected = [item for item in report["findings"] if item["severity"] == severity]
        lines.extend(["", f"## {heading}", ""])
        if not selected:
            lines.append("None found by the static scanner.")
            continue
        for item in selected:
            lines.extend(render_markdown_finding(item))

    lines.extend(["", "## Manual checks", ""])
    for item in report["manual_checks"]:
        lines.extend(
            [
                f"### [{item['id']}] {item['title']}",
                "",
                f"Reason: {item['reason']}",
                "",
                f"Verify: {item['verification']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Scanner note",
            "",
            "This report is an evidence collection pass. Read each location, remove false positives, execute the reviewer path, and review current Apple policy before making a final submission decision.",
            "",
        ]
    )
    return "\n".join(lines)


def render_markdown_finding(item: Dict[str, Any]) -> List[str]:
    lines = [
        f"### [{item['id']}] {item['title']}",
        "",
        f"Severity: {item['severity'].upper()}",
        f"Guideline: {item['guideline']}",
        f"Evidence confidence: {item['evidence_confidence'].upper()}",
        "Evidence:",
    ]
    for evidence in item["evidence"]:
        location = evidence["path"]
        if evidence["line"] is not None:
            location += f":{evidence['line']}"
        lines.append(f"- `{location}`: {evidence['excerpt']}")
    lines.extend(
        [
            "",
            f"Why it matters: {item['reason']}",
            "",
            f"Fix: {item['fix']}",
            "",
            f"Verify: {item['verification']}",
            "",
        ]
    )
    return lines


def write_outputs(report: Dict[str, Any], args: argparse.Namespace) -> None:
    markdown = render_markdown(report)
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    html_text = render_report_html(report)
    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        if args.format in {"markdown", "both", "all"}:
            (output_dir / "app-store-review-report.md").write_text(markdown, encoding="utf-8")
        if args.format in {"json", "both", "all"}:
            (output_dir / "app-store-review-report.json").write_text(json_text, encoding="utf-8")
        if args.format in {"html", "all"}:
            (output_dir / "app-store-review-report.html").write_text(html_text, encoding="utf-8")
        return
    if args.format == "markdown":
        sys.stdout.write(markdown)
    elif args.format == "json":
        sys.stdout.write(json_text)
    elif args.format == "html":
        sys.stdout.write(html_text)
    else:
        raise ValueError(f"--format {args.format} requires --output-dir")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project root to scan")
    parser.add_argument(
        "--format",
        choices=("markdown", "json", "html", "both", "all"),
        default="markdown",
        help="Output type. 'both' writes Markdown and JSON; 'all' also writes visual HTML.",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for app-store-review-report.md, .json, and optional .html",
    )
    parser.add_argument("--archive", help="Optional IPA or ZIP release archive to inspect")
    parser.add_argument(
        "--compare-root",
        action="append",
        default=[],
        help="Sibling, template, or prior project root for exact asset comparison; repeatable",
    )
    parser.add_argument(
        "--include-dependencies",
        action="store_true",
        help="Include dependency directories such as Pods and node_modules in text scanning",
    )
    parser.add_argument(
        "--fail-on",
        choices=("never", "blocker", "warning"),
        default="never",
        help="Return exit code 2 when the chosen threshold is reached",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.project).expanduser()
    if not root.is_dir():
        parser.error(f"project root is not a directory: {root}")
    if args.format in {"both", "all"} and not args.output_dir:
        parser.error(f"--format {args.format} requires --output-dir")
    archive = Path(args.archive).expanduser() if args.archive else None
    compare_roots = [Path(item).expanduser() for item in args.compare_root]
    ctx = ScanContext(root, args.include_dependencies, compare_roots, archive)
    report = run_scan(ctx)
    write_outputs(report, args)
    counts = report["counts"]
    if args.fail_on == "blocker" and counts["blocker"]:
        return 2
    if args.fail_on == "warning" and (counts["blocker"] or counts["warning"]):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
