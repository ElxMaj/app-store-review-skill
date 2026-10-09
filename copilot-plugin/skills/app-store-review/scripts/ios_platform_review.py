"""Bounded, read-only iOS 27 evidence collection; no build or network execution.

The policy snapshot is explicit. An API signal activates a manual check, never
proves that an optional feature works or that its adoption is required.
"""
from __future__ import annotations

import os
import json
import plistlib
import re
import zipfile
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Optional
from xml.parsers.expat import ExpatError

REFERENCE_VERIFIED_AT = "2026-10-09"
REQUIREMENTS_URL = "https://developer.apple.com/news/upcoming-requirements/"
LAUNCH_SCREEN_URL = "https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements"
MAX_PLIST_BYTES = 2_000_000
MAX_ARCHIVE_ENTRIES = 50_000
MAX_TOTAL_PLIST_BYTES = 16_000_000
LAUNCH_KEYS = ("UILaunchStoryboardName", "UILaunchStoryboards", "UILaunchScreen", "UILaunchScreens")

SUBMISSION_REQUIREMENTS = {
    "sdk_major": {"minimum": 26, "effective_at": "2026-04-28", "source": REQUIREMENTS_URL},
    "xcode_major": {"minimum": 26, "effective_at": "2026-04-28", "source": REQUIREMENTS_URL},
    "deployment_major": {"minimum": 13, "effective_at": "2026-09-09", "source": REQUIREMENTS_URL},
}

RELEASE_WATCHLIST = [
    {"id": "duo_launch", "title": "iPhone Duo customer availability", "status": "announced",
     "release_channel": "27.1 development support", "timing": "October 23, 2026",
     "source": "https://developer.apple.com/news/?id=kkphp5qo",
     "verification": "Use available development tools; record physical-device evidence only when the device was actually tested."},
    {"id": "duo_screenshots", "title": "Duo screenshot submission requirement", "status": "future_requirement",
     "release_channel": "App Store submission", "timing": "April 2027 (day not announced)",
     "source": "https://developer.apple.com/news/?id=kkphp5qo",
     "verification": "Prepare device/orientation assets and recheck the enforcement date; this is not an October 2026 blocker."},
    {"id": "xcode271", "title": "Xcode 27.1 simulator and extension limits", "status": "release_candidate",
     "release_channel": "27.1 RC", "timing": "Snapshot checked October 9, 2026",
     "source": "https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes",
     "verification": "Distinguish simulator/Device Hub limitations from app failures and check the actual tool revision."},
    {"id": "ios272_att", "title": "iOS/iPadOS 27.2 tracking changes", "status": "beta",
     "release_channel": "27.2 beta 3", "timing": "Snapshot checked October 9, 2026",
     "source": "https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27_2-release-notes",
     "verification": "Verify the expanded ATT interface, annual EU re-prompt and renamed APIs against the actual beta SDK and applicable region; do not impose a current worldwide requirement."},
    {"id": "subscription_rollout", "title": "Expanded subscription purchasing", "status": "announced",
     "release_channel": "App Store commerce rollout", "timing": "Volume: October 22, 2026; Groups: winter; Bundles/Suites: later in 2026",
     "source": "https://developer.apple.com/news/?id=likeohx4",
     "verification": "Check eligibility and actual customer availability separately from access to configuration; test StoreKit 2 ownership, seats, refunds and restore."},
    {"id": "preview_capabilities", "title": "Preview and future framework surfaces", "status": "preview",
     "release_channel": "27 SDK release notes", "timing": "Verify the owning feature's release and region",
     "source": "https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes",
     "verification": "Check AudioAccessoryKit, spatial APIs and other used preview capabilities individually. Resolved beta issues are not current app defects."},
]

# Keep detailed checks in the reference, and concise routing in scanner output.
TECHNOLOGIES = (
    ("foundation_models", "Foundation Models", r"\b(?:FoundationModels|LanguageModelSession|SystemLanguageModel|DynamicProfile)\b",
     "Test model availability, multimodal input permissions, context limits, guardrail failures, tool side effects, and provider switching."),
    ("private_cloud_compute", "Private Cloud Compute", r"\bPrivateCloudComputeLanguageModel\b",
     "Verify eligibility and signed capability, network and usage-limit failures, fallback, and accurate cloud-processing disclosure."),
    ("core_ai", "Core AI and custom models", r"\b(?:CoreAI|CoreAILanguageModel|MLXLanguageModel)\b",
     "Check model licensing, downloaded asset integrity, hardware support, memory, cancellation, thermal load, and background inference authorization."),
    ("evaluations", "AI evaluations", r"\b(?:import\s+Evaluations|EvaluationSuite|AppIntentsTesting)\b",
     "Inspect real evaluation results and system-path intent tests; test-only imports do not establish shipping feature adoption."),
    ("app_intents", "Siri and App Intents", r"\b(?:AppIntents|AppIntent|AppEntity|AppShortcutsProvider|AssistantIntent|AssistantEntity)\b",
     "Test schemas, view annotations, entity access, authentication, confirmation of destructive actions, and real Siri/Shortcuts pathways."),
    ("spotlight", "Spotlight and semantic search", r"\b(?:CoreSpotlight|CSSearchableItem|CSSearchableIndex|SpotlightSearchTool)\b",
     "Test attribution, private-content eligibility, index deletion after logout/account deletion, stale entities, and natural-language retrieval."),
    ("swiftui", "SwiftUI and document interfaces", r"\b(?:import\s+SwiftUI|TabView|DocumentGroup|ReadableDocument|WritableDocument)\b",
     "Test visible tab selection, state initialization, text gestures, image caching, async document operations, and scrolling under the actual linked SDK."),
    ("uikit", "UIKit, scenes, and adaptive layout", r"\b(?:UIKit|UIApplicationDelegate|UIScene|UIScreen|UIWindowScene|UIDragInteraction)\b",
     "Verify scene lifecycle and resizing; replace layout assumptions based on the main screen, device idiom, or orientation when they fail in resizable scenes."),
    ("widgets_live_activities", "Widgets, controls, and Live Activities", r"\b(?:WidgetKit|ActivityKit|WidgetConfiguration|ControlWidget|ActivityConfiguration)\b",
     "Test each extension's signed configuration, App Intents, dynamic styling, privacy redaction, updates, deep links, and expired data."),
    ("background_assets", "Background Assets and background work", r"\b(?:BackgroundAssets|BAAssetPack|NSBundleResourceRequest|BGTaskScheduler|BGContinuedProcessingTask)\b",
     "Check localized asset packs, low storage, interrupted downloads, legitimate background modes, and the transition from deprecated On Demand Resources."),
    ("storekit", "StoreKit and subscriptions", r"\b(?:StoreKit|SubscriptionStoreView|BundledSubscription|SKPaymentQueue|react-native-purchases|in_app_purchase)\b",
     "Verify StoreKit 2, offers, refunds, restore, assigned/revoked seats, bundles/suites eligibility and rollout, and monthly commitment disclosures."),
    ("music_understanding", "Music Understanding", r"\bMusicUnderstanding\b",
     "Verify audio provenance, permissions, model availability, analysis accuracy, cancellation, and licensed use of music."),
    ("now_playing", "Now Playing and media sharing", r"\b(?:NowPlaying|MPNowPlayingInfoCenter|MediaSharing|MediaExtension)\b",
     "Test playback state and controls on the Lock Screen, Control Center, Dynamic Island, and CarPlay; inspect each sharing extension separately."),
    ("camera_photos", "Camera, photos, RAW, and video", r"\b(?:AVFoundation|AVCaptureSession|PhotoKit|PHAssetResource|CoreImage|VideoToolbox|VNDocumentCameraViewController)\b",
     "Test limited photo access, Center Stage orientation/cropping, capture startup, RAW export, and device-supported video processing."),
    ("games_spatial", "Games, Metal, and spatial content", r"\b(?:MetalKit|import\s+Metal|GameController|GameKit|RealityKit|ARKit|ShaderGraph|USDKit)\b",
     "Test touch and controller input, resizing, GPU memory/frame pacing, content rights, and availability of announced spatial APIs."),
    ("pencil_paper", "PencilKit and PaperKit", r"\b(?:PencilKit|PaperKit|PKCanvasView)\b",
     "Test handwriting language support, latency, editing/export, assistive input, and touch/keyboard alternatives."),
    ("health_home", "HealthKit and HomeKit", r"\b(?:HealthKit|HKHealthStore|HomeKit|HMHomeManager)\b",
     "Test limited health-history authorization, unavailable samples, sensitive-data handling, accessory compatibility, and subscription/region conditions."),
    ("trust_insights", "Trust Insights", r"\bTrustInsights\b",
     "Verify the signed entitlement, connectivity failure behavior, privacy disclosures, and how results affect user access."),
    ("identity_security", "Identity, age assurance, and security", r"\b(?:AuthenticationServices|LocalAuthentication|DeclaredAgeRange|PermissionKit|FamilyControls|ManagedSettings|PassKit)\b",
     "Test credential recovery, age/parental-consent flows when applicable, protected actions, signed entitlements, and storefront-specific obligations."),
    ("network_accessories", "Networking and accessories", r"\b(?:NetworkExtension|AudioAccessoryKit|AccessorySetupKit|WiFiAware|CoreBluetooth|NearbyInteraction)\b",
     "Check accessory/region availability, denied permissions, pairing, reconnect, and stricter TLS in affected managed-device services."),
    ("metrics", "MetricKit and performance", r"\b(?:MetricKit|MetricManager|MXMetricManager|StateReporting|ScrollHitchTimeMetric)\b",
     "Validate crash/memory diagnostics, state reporting, hitch metrics, privacy-safe telemetry, and compatibility of renamed/removed APIs."),
    ("web", "WebKit and embedded web content", r"\b(?:WebKit|WKWebView|SafariServices|SFSafariViewController)\b",
     "Test web permissions, auth redirects, content rules, downloads, resizing, and legitimate navigation under the candidate OS."),
    ("tracking", "Tracking and ATT", r"\b(?:AppTrackingTransparency|ATTrackingManager|requestTrackingAuthorization|NSUserTrackingUsageDescription)\b",
     "Trace tracking behavior and denial first; separately verify iOS 27.2 beta expanded-interface rules for affected EU countries and exact SDK API names before adopting them."),
)


@dataclass
class ArchiveEvidence:
    entries: List[str] = field(default_factory=list)
    bundles: List[Dict[str, Any]] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)


def bundle_plist_kind(name: str) -> Optional[str]:
    parts = PurePosixPath(name).parts
    if not parts or any(part in {"..", "."} for part in parts) or name.startswith("/"):
        return None
    if len(parts) < 2 or parts[-1] != "Info.plist":
        return None
    if any(part.endswith(".framework") for part in parts):
        return None
    if parts[-2].endswith(".appex"):
        return "extension"
    if parts[-2].endswith(".app"):
        return "app"
    return None


def read_archive(path: Optional[Path]) -> ArchiveEvidence:
    """Read ZIP/IPA or xcarchive metadata without extracting or following links."""
    result = ArchiveEvidence()
    if path is None:
        return result
    if not path.exists():
        result.limitations.append("The supplied archive does not exist.")
        return result
    budget = 0

    def collect(name: str, size: int, reader: Any) -> None:
        nonlocal budget
        kind = bundle_plist_kind(name)
        if not kind:
            return
        if size > MAX_PLIST_BYTES or budget + size > MAX_TOTAL_PLIST_BYTES:
            result.limitations.append("An archive bundle plist exceeded the bounded inspection limit; inspect it with Apple tooling.")
            return
        budget += size
        try:
            value = plistlib.loads(reader())
        except (OSError, ValueError, TypeError, OverflowError, RuntimeError, zipfile.BadZipFile, ExpatError):
            result.limitations.append("An archive bundle plist could not be parsed; its build checks remain manual.")
            return
        if isinstance(value, dict):
            result.bundles.append({"path": name, "kind": kind, "values": value})
        else:
            result.limitations.append("An archive bundle plist has no dictionary root; inspect the built bundle manually.")

    try:
        if path.is_dir() and path.suffix == ".xcarchive" and not path.is_symlink():
            for current, directories, filenames in os.walk(path, followlinks=False):
                directories[:] = sorted(name for name in directories if not (Path(current) / name).is_symlink())
                for filename in sorted(filenames):
                    file_path = Path(current) / filename
                    if file_path.is_symlink():
                        continue
                    name = file_path.relative_to(path).as_posix()
                    result.entries.append(name)
                    if len(result.entries) > MAX_ARCHIVE_ENTRIES:
                        raise ValueError("entry limit")
                    collect(name, file_path.stat().st_size, file_path.read_bytes)
        elif path.is_file() and zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as archive:
                entries = sorted(archive.infolist(), key=lambda item: item.filename)
                if len(entries) > MAX_ARCHIVE_ENTRIES:
                    raise ValueError("entry limit")
                names = Counter(entry.filename.replace("\\", "/") for entry in entries)
                for entry in entries:
                    # ZIP symlinks cannot establish a shipped plist's contents.
                    if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                        result.limitations.append("Archive symlinks were excluded; linked contents remain manual.")
                        continue
                    name = entry.filename.replace("\\", "/")
                    if name.startswith("/") or ".." in PurePosixPath(name).parts:
                        result.limitations.append("Unsafe archive member paths were excluded; inspect the candidate manually.")
                        continue
                    result.entries.append(name)
                    if names[name] > 1 and bundle_plist_kind(name):
                        result.limitations.append("A duplicate archive bundle plist is ambiguous; its build checks remain manual.")
                        continue
                    collect(name, entry.file_size, lambda entry=entry: archive.read(entry))
        else:
            result.limitations.append("The supplied archive is not a readable IPA, ZIP, or xcarchive directory.")
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile):
        result.limitations.append("Archive inspection did not complete within the bounded reader; remaining checks are manual.")
    result.bundles.sort(key=lambda item: item["path"])
    members = set(result.entries)
    for bundle in result.bundles:
        executable = bundle["values"].get("CFBundleExecutable")
        if (not isinstance(executable, str) or not executable or "/" in executable or "\\" in executable
                or (PurePosixPath(bundle["path"]).parent / executable).as_posix() not in members):
            result.limitations.append("An app or extension's executable entry could not be established from the archive; verify the complete candidate with Apple tooling.")
    result.limitations = sorted(set(result.limitations))
    return result


def normalized_version(key: str, value: Any) -> Optional[str]:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        return None
    raw = str(value).strip().strip('"\'')
    if key in {"SDKROOT", "DTSDKName"}:
        match = re.fullmatch(r"iphoneos(\d{1,2}(?:\.\d{1,2}){0,2})", raw)
        return match.group(1) if match else None
    if key == "DTXcode":
        return str(int(raw) // 100) if re.fullmatch(r"\d{3,4}", raw) else None
    return raw if re.fullmatch(r"\d{1,2}(?:\.\d{1,2}){0,2}", raw) else None


def version_major(value: Optional[str]) -> Optional[int]:
    return int(value.split(".")[0]) if value else None


def is_test_source(relative: str) -> bool:
    lowered = relative.lower()
    return any(part in {"test", "tests", "testing", "__tests__", "uitests"} for part in lowered.split("/")) or any(
        token in lowered for token in ("tests.swift", "test.swift", ".spec.", ".test.")
    )


def collect_platform_review(ctx: Any, archive: ArchiveEvidence) -> Dict[str, Any]:
    build_evidence: List[Dict[str, Any]] = []
    findings: List[Dict[str, Any]] = []
    source_suffixes = {".swift", ".m", ".mm", ".h", ".js", ".jsx", ".ts", ".tsx", ".dart"}
    source = sorted((item for item in ctx.text_files if item.path.suffix.lower() in source_suffixes
                     and not is_test_source(item.relative)), key=lambda item: item.relative)

    def signal(path: str, key: str, line: Optional[int] = None) -> Dict[str, Any]:
        return {"path": path, "line": line, "signal": f"Platform evidence: {key}"}

    def add_build(kind: str, path: str, key: str, value: Any, line: Optional[int] = None) -> Optional[int]:
        normalized = normalized_version(key, value)
        build_evidence.append({"kind": kind, "key": key, "version": normalized,
                               "evidence": signal(path, key, line)})
        return version_major(normalized)

    def blocker(finding_id: str, title: str, evidence: Dict[str, Any], reason: str, fix: str, source_url: str) -> None:
        findings.append({"id": finding_id, "severity": "blocker", "title": title,
                         "guideline": "Submission requirement", "evidence_confidence": "official",
                         "evidence": [evidence], "reason": reason + " Source: " + source_url,
                         "fix": fix, "verification": "Rebuild the release archive, rerun this check, and validate the exact candidate in App Store Connect."})

    for text_file in sorted(ctx.text_files, key=lambda item: item.relative):
        if text_file.path.name == "project.pbxproj" or text_file.path.suffix == ".xcconfig":
            for match in re.finditer(r"\b(IPHONEOS_DEPLOYMENT_TARGET|SDKROOT)\s*(?:\[[^\]\n]+\])?\s*=\s*([^;\n]+)", text_file.text):
                add_build("authored", text_file.relative, match.group(1), match.group(2), text_file.text.count("\n", 0, match.start()) + 1)
        if text_file.path.name == "Podfile":
            for match in re.finditer(r"platform\s*:ios\s*,\s*['\"]([^'\"]+)['\"]", text_file.text):
                add_build("authored", text_file.relative, "IPHONEOS_DEPLOYMENT_TARGET", match.group(1), text_file.text.count("\n", 0, match.start()) + 1)
    for path in sorted(ctx.files):
        if path.suffix != ".plist" or path.is_symlink():
            continue
        try:
            if path.stat().st_size > MAX_PLIST_BYTES:
                continue
            value = plistlib.loads(path.read_bytes())
            if isinstance(value, dict):
                for key in ("DTSDKName", "DTXcode", "MinimumOSVersion"):
                    if key in value:
                        add_build("authored", ctx.rel(path), key, value[key])
        except (OSError, ValueError, TypeError, OverflowError, ExpatError):
            continue
    # Parse JSON only; never evaluate dynamic Expo config or execute plugins.
    for path in sorted(ctx.files):
        if path.name not in {"app.json", "app.config.json"}:
            continue
        try:
            if path.stat().st_size > MAX_PLIST_BYTES:
                continue
            data = json.loads(path.read_text())
            expo = data.get("expo", data)
            for plugin in expo.get("plugins", []):
                if isinstance(plugin, list) and len(plugin) == 2 and plugin[0] == "expo-build-properties" and isinstance(plugin[1], dict):
                    ios = plugin[1].get("ios", {})
                    if isinstance(ios, dict) and "deploymentTarget" in ios:
                        add_build("authored", ctx.rel(path), "IPHONEOS_DEPLOYMENT_TARGET", ios["deploymentTarget"])
        except (OSError, ValueError, TypeError, AttributeError):
            continue

    for bundle in archive.bundles:
        values = bundle["values"]
        sdk_raw = values.get("DTSDKName")
        # Do not apply iOS rules to watchOS companions or ambiguous bundles.
        platform = values.get("DTPlatformName")
        if (platform is not None and platform != "iphoneos") or (platform is None and not isinstance(sdk_raw, str)):
            continue
        if platform is None and not sdk_raw.startswith("iphoneos"):
            continue
        path = f"archive:{ctx.archive.name}/{bundle['path']}"
        sdk = add_build("archive", path, "DTSDKName", sdk_raw)
        xcode = add_build("archive", path, "DTXcode", values.get("DTXcode"))
        minimum = add_build("archive", path, "MinimumOSVersion", values.get("MinimumOSVersion"))
        if sdk is not None and sdk < SUBMISSION_REQUIREMENTS["sdk_major"]["minimum"]:
            blocker("ASR-UPLOAD-SDK", "Archive uses an SDK below the submission minimum", signal(path, "DTSDKName"),
                    f"The bundle plist records iOS SDK {sdk}; the bundled policy requires iOS SDK 26 or later since April 28, 2026.",
                    "Update the build toolchain at its authored CI/Xcode source and rebuild with a supported iOS SDK.", REQUIREMENTS_URL)
        if xcode is not None and xcode < SUBMISSION_REQUIREMENTS["xcode_major"]["minimum"]:
            blocker("ASR-UPLOAD-XCODE", "Archive uses Xcode below the submission minimum", signal(path, "DTXcode"),
                    f"The bundle plist records Xcode {xcode}; the bundled policy requires Xcode 26 or later since April 28, 2026.",
                    "Select an eligible Xcode toolchain for the release build and verify CI actually used it.", REQUIREMENTS_URL)
        if minimum is not None and minimum < SUBMISSION_REQUIREMENTS["deployment_major"]["minimum"]:
            blocker("ASR-UPLOAD-MINIMUM-OS", "Archive deployment target is below iOS 13", signal(path, "MinimumOSVersion"),
                    f"The bundle plist declares iOS {minimum}; iOS/iPadOS uploads must target iOS 13 or later since September 9, 2026.",
                    "Raise the relevant authored app/extension deployment setting to an eligible version and rebuild.", REQUIREMENTS_URL)
        if sdk is not None and sdk >= 27 and bundle["kind"] == "app" and not any(key in values for key in LAUNCH_KEYS):
            blocker("ASR-IOS27-LAUNCH-SCREEN", "iOS 27 archive has no launch-screen declaration", signal(path, "Launch screen keys absent"),
                    "An iOS/iPadOS app built with SDK 27 or later must include one of the four supported launch-screen plist keys. The inspected app bundle has none.",
                    "Configure a launch screen at the authored native or framework configuration source; verify its resource exists in the rebuilt app bundle.", LAUNCH_SCREEN_URL)

    ctx.add_manual("ASR-MANUAL-DEPLOYMENT", "Verify supported OS and per-target build settings",
                   "Authored settings, a compiler language mode, and SDKROOT alone do not establish the submitted toolchain or every executable bundle's minimum OS.",
                   "Compare Release settings, resolved Expo/native output, and every app/extension archive plist with the dated SDK 26 / Xcode 26 / deployment iOS 13 requirements; test the oldest OS you advertise.")
    ctx.add_manual("ASR-MANUAL-IOS27-RUNTIME", "Run the iOS 27 compatibility matrix",
                   "No runtime test was executed by this read-only scanner. SDK linking, OS version, device capability, region, and language are independent.",
                   "Test the exact candidate on iOS/iPadOS 27, supported older OSes, AI-capable and other supported hardware, accessibility settings, and release-specific failure states; track 27.1 Duo and 27.2 beta separately.")
    ctx.add_manual("ASR-MANUAL-IOS27-ADAPTIVITY", "Verify scenes, iPad, Mirroring, and iPhone Duo layouts",
                   "SDK 27 scene-lifecycle requirements and resizable windows need a built app. Main-screen, orientation, or device-idiom signals cannot prove a layout failure.",
                   "Check scene lifecycle, launch/restoration, live resizing, keyboard, focus, safe areas, and view-sized layout. Use Xcode 27.1 Device Hub for Duo fold/unfold and poses; record simulator versus hardware evidence.")
    ctx.add_manual("ASR-MANUAL-IOS27-DESIGN", "Review design and accessibility on the candidate OS",
                   "Static code cannot establish readable materials, responsive navigation, icon rendering, or assistive-technology behavior.",
                   "Inspect refreshed system materials, typography, tab/navigation bars, branded content, icon appearances, VoiceOver, Dynamic Type, Increase Contrast, Reduce Transparency, and Reduce Motion on the built app.")
    ctx.add_manual("ASR-MANUAL-IOS27-PRODUCT-PAGE", "Verify new store assets and feature availability claims",
                   "Product-page headers, search assets, Asset Library approvals, screenshots, and device/provider eligibility may exist only in App Store Connect. The Duo screenshot requirement is announced for April 2027, not an October 2026 gate.",
                   "Inspect approved localized assets in App Store Connect's preview, including dark appearance and Duo orientations. Reconcile AI/local/cloud, Siri, subscription, hardware, language, and regional claims with the shipped build and rollout dates.")

    technologies = []
    for feature_id, title, pattern, verification in TECHNOLOGIES:
        evidence = []
        for text_file in source:
            match = re.search(pattern, text_file.text)
            if match:
                evidence.append(signal(text_file.relative, title + " source signal", text_file.text.count("\n", 0, match.start()) + 1))
        status = "manual" if evidence else "not_detected"
        technologies.append({"id": feature_id, "title": title, "status": status,
                             "evidence_confidence": "inference", "evidence": evidence[:12],
                             "evidence_total": len(evidence), "evidence_omitted": max(0, len(evidence) - 12),
                             "verification": verification})
        if evidence:
            ctx.add_manual("ASR-MANUAL-IOS27-" + feature_id.upper().replace("_", "-"), title + " behavior",
                           "A source signal was found; actual feature use, availability, permissions, signed capabilities, and runtime behavior remain unverified.", verification)

    return {"target_os": "iOS 27 / iPadOS 27", "reference_verified_at": REFERENCE_VERIFIED_AT,
            "verification_status": "bundled_reference", "runtime_test_status": "not_run",
            "submission_requirements": deepcopy(SUBMISSION_REQUIREMENTS),
            "release_watchlist": deepcopy(RELEASE_WATCHLIST),
            "build_evidence": sorted(build_evidence, key=lambda item: (item["kind"], item["evidence"]["path"], item["key"], item["evidence"]["line"] or 0)),
            "technologies": technologies, "reference": "references/ios27-readiness.md",
            "findings": findings}
