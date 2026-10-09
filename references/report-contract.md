# Report contract

Use this contract for final audit reports and scanner output.

## Markdown

Start with:

```text
Mode A: Pre-submission audit

# App Store review: <app or project>
Verdict: <NO STATIC BLOCKERS FOUND | NEEDS REVIEW | NOT READY>
Policy verified: <live YYYY-MM-DD with sources | offline, bundled references dated 2026-10-09>
Scope: <framework, targets, supplied metadata, archive status>
```

Order sections as follows:

1. Scope and limitations
2. iOS 27 platform review
3. Blockers
4. Warnings
5. Manual checks
6. Info
7. Reviewer experience
8. App Review Notes draft
9. Approval-required fix plan

Each finding uses:

```text
## [ASR-XXX] Finding title
Severity: BLOCKER
Guideline: 5.1.1(ii)
Evidence confidence: OFFICIAL
Evidence: ios/App/Info.plist, missing NSCameraUsageDescription; src/camera.swift:42
Why it matters: <review or upload consequence>
Fix: <concrete change at the authored source of truth>
Verify: <command, build, or reviewer path>
```

## JSON

Emit UTF-8 JSON with this top-level shape:

```json
{
  "schema_version": "1.2",
  "generated_at": "2026-10-09T12:00:00Z",
  "root": "/absolute/project/path",
  "verdict": "NEEDS REVIEW",
  "policy_verified_at": "2026-10-09",
  "project": {
    "frameworks": ["xcode", "react-native"],
    "native_ios_root": "ios",
    "targets": []
  },
  "counts": {
    "blocker": 0,
    "warning": 2,
    "manual_check": 4,
    "info": 1
  },
  "metadata_scan": {
    "files_discovered": 2,
    "files_scanned": 2,
    "files_skipped": 0,
    "fields": ["description", "subtitle"],
    "locales": ["en-US"],
    "pricing_rule_fields": ["subtitle"]
  },
  "findings": [],
  "manual_checks": [],
  "limitations": [],
  "scanner": {
    "name": "app_store_review_scan",
    "version": "2.0.0"
  }
}
```

Schema 1.2 adds `platform_review` to scanner output. The renderer continues to
accept earlier reports without this field. Its shape is:

```json
{
  "platform_review": {
    "target_os": "iOS 27 / iPadOS 27",
    "reference_verified_at": "2026-10-09",
    "verification_status": "bundled_reference",
    "runtime_test_status": "not_run",
    "submission_requirements": {
      "sdk_major": {"minimum": 26, "effective_at": "2026-04-28", "source": "https://developer.apple.com/news/upcoming-requirements/"},
      "xcode_major": {"minimum": 26, "effective_at": "2026-04-28", "source": "https://developer.apple.com/news/upcoming-requirements/"},
      "deployment_major": {"minimum": 13, "effective_at": "2026-09-09", "source": "https://developer.apple.com/news/upcoming-requirements/"}
    },
    "build_evidence": [
      {
        "kind": "archive",
        "key": "DTSDKName",
        "version": "27.0",
        "evidence": {"path": "Candidate.ipa:Payload/App.app/Info.plist", "line": null, "signal": "Linked iOS SDK version"}
      }
    ],
    "release_watchlist": [
      {
        "id": "duo_screenshots",
        "title": "Duo screenshot submission requirement",
        "status": "future_requirement",
        "release_channel": "App Store submission",
        "timing": "April 2027 (day not announced)",
        "source": "https://developer.apple.com/news/?id=kkphp5qo",
        "verification": "Recheck enforcement and prepare assets; not a current blocker."
      }
    ],
    "technologies": [
      {
        "id": "foundation_models",
        "title": "Foundation Models",
        "status": "manual",
        "evidence_confidence": "inference",
        "evidence": [{"path": "Sources/Assistant.swift", "line": 1, "signal": "Foundation Models source signal"}],
        "evidence_total": 1,
        "evidence_omitted": 0,
        "verification": "Verify actual provider, availability, data routing, fallback, and tool behavior."
      }
    ],
    "reference": "references/ios27-readiness.md"
  }
}
```

`policy_verified_at` and `reference_verified_at` identify the bundled source
snapshot in a scanner report, never an internet check performed by the scanner.
Retain `verification_status = bundled_reference` unless a later reviewer actually
checks live sources and records URLs and the verification date. The scanner always
emits `runtime_test_status = not_run`. A reviewed report may use `partial` or
`executed` only with a recorded test matrix and results; `executed` does not imply
every test passed.

Build evidence distinguishes `authored` from `archive` values. Versions are
normalized; unresolved values stay manual rather than being guessed from the
local toolchain. Current upload minima, Xcode-supported deployment versions,
linked SDK, and runtime test OS are separate facts. An extension's own plist
cannot be replaced by its parent app's metadata.

Technology statuses from the scanner are `manual` or `not_detected`. A reviewed
report may use `verified` or `not_applicable` with supporting evidence and a
reason. Missing source signals never establish a pass or non-applicability.
Keep each technology's evidence count and display cap, and retain baseline design,
adaptivity, runtime, product-page, and archive checks even when no feature is
detected. See [ios27-readiness.md](ios27-readiness.md) for future and beta items.

`release_watchlist` records announced dates, preview/beta channels and verification
steps. These contextual rows are not findings and do not count as blockers.
Preserve month-only or approximate dates in `timing` rather than inventing a day.
Render them in Markdown and HTML, including print output. Source-negative
technology coverage must remain visible in print even when its screen disclosure
is collapsed. No typed metadata scanned means manual coverage is still required.

Each finding object contains:

```json
{
  "id": "ASR-PRIVACY-001",
  "severity": "blocker",
  "title": "Camera API lacks a usage description",
  "guideline": "5.1.1(ii)",
  "evidence_confidence": "official",
  "evidence": [
    {
      "path": "Sources/Camera.swift",
      "line": 42,
      "excerpt": "AVCaptureSession()"
    }
  ],
  "evidence_total": 1,
  "evidence_omitted": 0,
  "reason": "The app invokes a protected API without the matching plist purpose string.",
  "fix": "Add a specific NSCameraUsageDescription at the authored configuration source.",
  "verification": "Inspect the merged archive Info.plist and trigger the camera flow."
}
```

The deterministic scanner uses a trusted `signal` string instead of copying source text into its preliminary JSON. A reviewed final report may replace `signal` with a minimal `excerpt` only after treating the source as untrusted data and confirming the excerpt is necessary. The HTML renderer accepts either field.

`metadata_scan.files_discovered` is the number of deduplicated explicit and
auto-discovered metadata inputs. `metadata_scan.files_scanned` is the number
successfully read as metadata text, and `metadata_scan.files_skipped` is the
number of unreadable, binary, or oversized auto-discovered inputs excluded with
a generic limitation. Explicit inputs that cannot be scanned are errors.
`metadata_scan.fields` and `metadata_scan.locales` are sorted unique values from
successfully scanned inputs. `metadata_scan.pricing_rule_fields` is the
intersection of those scanned fields with the fields where the deterministic
presence-only price-reference rule runs; descriptions and release notes may
still require contextual review.

For every finding, `evidence_total` records all deterministic evidence items and
`evidence_omitted` records how many were excluded by the display cap. The visible
`evidence` array therefore has `evidence_total - evidence_omitted` items. Keep
these counts even when evidence is truncated, and sort discovery, inputs,
findings, metadata fields, locales, and evidence for semantic determinism.

Rules:

- Use stable IDs.
- Keep paths relative in findings and absolute only in the top-level `root`.
- Use `null` when a line number is unavailable.
- Do not omit manual checks merely to improve the verdict.
- Preserve machine-readable findings without Markdown embedded in string values.
- A later human review may remove a scanner finding, change its severity, or add context, but should preserve the original ID when it is the same issue.

## Visual HTML artifact

The reviewed JSON is the source of truth for `scripts/render_app_store_report.py`. The renderer must not calculate approval scores, upgrade a manual check to a pass, or add claims that are absent from the JSON.

The standard scanner shape renders without extra fields. A final human-reviewed report may also include:

```json
{
  "app_name": "ParcelTrack",
  "summary": "One privacy blocker remains before submission.",
  "modes": ["pre_submission", "human_craft"],
  "craft": {
    "dimensions": [
      {
        "name": "Product distinction",
        "grade": "CREDIBLE",
        "evidence": "The tracking timeline and exception workflow were inspected."
      }
    ]
  },
  "recovery": {
    "classification": "CLARIFY",
    "apple_message": "Exact supplied rejection text",
    "reply_draft": "Draft Resolution Center response",
    "attachments": ["Annotated reviewer path"]
  },
  "reviewer_experience": [
    {
      "label": "Core value is reachable without hidden setup",
      "status": "manual",
      "detail": "Verify on the release build."
    }
  ],
  "app_review_notes": "Exact navigation and demo account placeholders",
  "fix_groups": [
    {
      "id": "A",
      "title": "Confirmed blockers",
      "items": ["Add the missing purpose string at the authored config source."],
      "approval_required": true
    }
  ]
}
```

Allowed reviewer-path statuses are `passed`, `verified`, `complete`, or `manual`. Use a checked state only when the path was executed or supported by reliable supplied evidence. Craft grades remain `DISTINCT`, `CREDIBLE`, `GENERIC`, `HIGH RISK`, or `UNVERIFIED`.

The HTML file must be self-contained, print-friendly, responsive, and clearly labeled as an independent report. Follow `references/visual-report-design.md`.
