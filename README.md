<div align="center">

# App Store Review Skill

**Find App Store review problems before submission. If Apple rejects the app, build a clear response.**

<a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a> <a href="https://developer.apple.com/app-store/review/guidelines/"><img alt="Guidelines verified July 17, 2026" src="https://img.shields.io/badge/guidelines-verified%202026--07--17-0A7E07.svg"></a> <a href="#quick-start"><img alt="Claude Code and Codex" src="https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex-6B4FBB.svg"></a>

[Quick start](#quick-start) · [Review modes](#three-review-modes) · [Report preview](#report-preview) · [Coverage](#coverage)

</div>

`app-store-review` reads an iOS or iPadOS project and looks for evidence that can cause trouble during App Review. Use it before submission, after a rejection, or when an app feels too close to a template. It detects Xcode, Expo, React Native, and Flutter projects. The first pass is read-only. You get the report first, then a grouped fix plan if you want one. The policy references were verified on July 17, 2026 and include Apple's June 8, 2026 change to Guideline 4.3(b). Recovery advice keeps Apple's published rules separate from documented developer cases, observed patterns, and inference.

## Why this is useful

A build can work on your phone and still be difficult for App Review. A widget may have no privacy manifest. The camera call may not match a purpose string. Account deletion may stop at the app instead of the server. Review notes may leave the reviewer with no usable path.

Guideline 4.3 needs a different kind of review. A clean build can still look generic, copied, or unfinished. This skill checks the parts Apple can actually review, such as product depth, asset reuse, template provenance, microcopy, missing states, accessibility, and the App Store product page. It does not claim to detect AI-written code.

## Quick start

Install for Codex, Claude Code, or another compatible agent:

```bash
npx skills add ElxMaj/app-store-review-skill
```

Install as a Claude Code marketplace plugin:

```text
/plugin marketplace add ElxMaj/app-store-review-skill
/plugin install app-store-review@app-store-review-skill
```

Then use normal language:

```text
Audit this Expo app before submission. Report first and do not edit files.
Apple rejected build 42 under 4.3(a). Find the cause and draft my reply.
Run the human-craft audit. Show me what feels generic or unfinished.
```

## Three review modes

### 1. Pre-submission audit

The scanner finds the project type and native targets, then collects file-level evidence. It checks permission strings, privacy manifests, Required Reason APIs, dynamic code, account deletion, Sign in with Apple, IAP restore paths, ATT, third-party AI consent, placeholders, shipped internal files, and optional exact asset reuse. Manual checks cover the areas source code cannot prove, including App Store metadata, privacy answers, purchases, reviewer access, iPad behavior, and error states.

### 2. Rejection recovery

The rejection message is kept exactly as Apple wrote it. The skill classifies the next step as `FIX`, `CLARIFY`, `APPEAL`, or `REQUEST INTERPRETATION`. For 4.3 cases, it separates portfolio duplication from the indistinguishable-app test, ranks possible remediation by evidence quality, includes a framework false-positive response, and prepares a Resolution Center reply with exact navigation, build details, and attachments to include.

### 3. Human-craft audit

The app is graded across product distinction, provenance, visual identity, microcopy and states, and product-page specificity. Grades are `DISTINCT`, `CREDIBLE`, `GENERIC`, `HIGH RISK`, or `UNVERIFIED`. The aim is to improve a thin or generic app, not hide it with a new color palette.

## Report preview

Every finding shows what was found, where it was found, why it matters, and how to verify the fix.

```text
# App Store review: ParcelTrack
Verdict: NOT READY
Policy verified: 2026-07-17
Scope: Expo, one app target, archive not supplied

## [ASR-PRIVACY-001] Camera use has no purpose string
Severity: BLOCKER
Guideline: 5.1.1(ii)
Evidence confidence: OFFICIAL
Evidence: Sources/Camera.swift:42; NSCameraUsageDescription not found
Fix: Add a specific camera purpose at the authored configuration source.
Verify: Rebuild, inspect the merged Info.plist, then open the camera flow.

No files changed. Approve fix group A to apply the confirmed blockers.
```

Reports can be returned as readable Markdown and stable JSON. Scanner findings keep stable IDs so they can be used in CI, issue reports, and later audits.

## How it works

1. **Discover:** find the framework, native iOS project, app targets, extensions, configuration sources, and available archive.
2. **Scan:** run deterministic checks and collect paths, lines, plist keys, package signals, and exact file matches.
3. **Review:** inspect each result, remove false positives, and walk the parts that need a person or a real build.
4. **Report:** give a verdict, evidence confidence, reviewer checklist, App Review Notes draft, and approval-required fix groups.

The scanner gathers evidence. It does not make the final judgment by itself. Missing context stays a `MANUAL CHECK` instead of becoming a fake defect.

## Coverage

| Guideline family | What is reviewed |
|---|---|
| 2.1 | Crashes, placeholders, demo access, broken paths, network behavior, and iPad reviewability |
| 2.3 | Build-to-metadata accuracy, screenshots, keywords, age rating, and purchase claims |
| 3.1 | Digital purchases, paywall terms, StoreKit pricing, trials, and restoration |
| 4.2 / 4.3 | Minimum functionality, templates, portfolio duplication, provenance, and distinct value |
| 5.1 | Purpose strings, privacy manifests, deletion, ATT, labels, and third-party AI consent |
| 1.2 | UGC filtering, reporting, blocking, contact details, moderation, and anonymous chat |

## Keep the evidence current

[`references/research-prompt.md`](references/research-prompt.md) is a ready-to-run quarterly research prompt. It checks official policy changes and refreshes rejection evidence without treating unresolved reports as successful recovery. New cases must include the guideline, Apple's wording when available, the response, the outcome, the date, and a source URL.

## Repository structure

```text
SKILL.md                         Main workflow and review rules
references/                      Policy, recovery, craft, framework, and report guidance
scripts/app_store_review_scan.py Read-only deterministic scanner
scripts/tests/                   Scanner regression tests
evals/                           Behavior and trigger cases
skills/app-store-review/         Cross-agent compatibility entry point
.claude-plugin/                  Claude Code marketplace files
.codex-plugin/                   Codex plugin manifest
```

## Contributing

Real rejection cases and false-positive reports are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request. Do not publish credentials, signing material, personal data, or private app details.

## Disclaimer

This project checks publicly available Apple guidance and clearly labeled community evidence. It cannot guarantee approval, does not contact Apple for you, and is not affiliated with or endorsed by Apple Inc.

Licensed under the [MIT License](LICENSE).
