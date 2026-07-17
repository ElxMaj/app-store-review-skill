# Report contract

Use this contract for final audit reports and scanner output.

## Markdown

Start with:

```text
# App Store review: <app or project>
Verdict: <NO STATIC BLOCKERS FOUND | NEEDS REVIEW | NOT READY>
Policy verified: <YYYY-MM-DD | offline, bundled references dated 2026-07-17>
Scope: <framework, targets, supplied metadata, archive status>
```

Order sections as follows:

1. Scope and limitations
2. Blockers
3. Warnings
4. Manual checks
5. Info
6. Reviewer experience
7. App Review Notes draft
8. Approval-required fix plan

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
  "schema_version": "1.0",
  "generated_at": "2026-07-17T12:00:00Z",
  "root": "/absolute/project/path",
  "verdict": "NEEDS_REVIEW",
  "policy_verified_at": "2026-07-17",
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
  "findings": [],
  "manual_checks": [],
  "limitations": [],
  "scanner": {
    "name": "app_store_review_scan",
    "version": "1.0.0"
  }
}
```

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
  "reason": "The app invokes a protected API without the matching plist purpose string.",
  "fix": "Add a specific NSCameraUsageDescription at the authored configuration source.",
  "verification": "Inspect the merged archive Info.plist and trigger the camera flow."
}
```

Rules:

- Use stable IDs.
- Keep paths relative in findings and absolute only in the top-level `root`.
- Use `null` when a line number is unavailable.
- Do not omit manual checks merely to improve the verdict.
- Preserve machine-readable findings without Markdown embedded in string values.
- A later human review may remove a scanner finding, change its severity, or add context, but should preserve the original ID when it is the same issue.
