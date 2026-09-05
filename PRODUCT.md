# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The primary user is an iOS maker or product team using Codex or Claude Code while preparing an App Store submission, responding to an App Review rejection, or checking whether a technically working app is review-ready and product-complete.

## Product Purpose

App Store Review Skill runs an evidence-first preflight against the project behind an iOS or iPadOS app. It helps the user find submission risks, understand where each signal comes from, verify proposed fixes, and prepare review work before Apple makes its decision.

Success means the user can inspect a report, distinguish confirmed findings from manual checks and unknowns, and choose what to fix without the first pass changing project files.

## Positioning

The product traces each review claim back to a repository path, published rule or labeled inference, and a concrete verification step. It combines pre-submission audit, rejection recovery, and human-craft review behind one report-first workflow.

## Operating Context

- Runs through Codex, Claude Code, or another agent that supports the open skills format.
- Recognizes Xcode, Expo, React Native, and Flutter project structures.
- Installs through Skills CLI, Tessl, or the Claude Code marketplace.
- Uses repository files, supplied App Store metadata, Apple’s published guidance, release-build checks, and App Store Connect state as distinct evidence sources.
- Produces a review report before proposing approval-gated fix groups.

## Capabilities and Constraints

- First-pass inspection is read-only and changes zero project files.
- Modes are pre-submission audit, rejection recovery, and human-craft audit.
- The report separates confirmed evidence, inference, manual checks, and unknowns.
- Apple makes every App Review decision; the skill does not guarantee approval.
- The skill does not detect AI-written code or claim knowledge of Apple’s internal review systems.
- Product and policy claims must remain tied to current repository or public-source evidence.
- The public product page is a static GitHub Pages site with no runtime framework or third-party script.

## Brand Commitments

- Product name: App Store Review Skill.
- Voice is direct, concrete, calm, and evidence-led; it avoids hype, magic, certainty, and generic AI marketing language.
- The campaign promise is “Rejected? Find risks first.” The product page must answer that urgency with proof and a clear preflight action.
- The original review-gate symbol may provide campaign continuity.
- The product is independent and not affiliated with or endorsed by Apple Inc. Apple-owned marks and proprietary interface chrome are not product assets.

## Evidence on Hand

- Canonical skill contract: `SKILL.md`.
- Install contract: `INSTALL.md`.
- Fictional ParcelTrack report: `examples/parceltrack-report.html` and `examples/parceltrack-report.json`.
- ParcelTrack report image: `assets/visual-report-example.png`.
- Original gate artwork: `site/assets/review-gate-cinematic.png` and `site/assets/review-gate-mark.svg`.
- Campaign creative: `site/assets/x-app-review-preflight-v3.png`.
- Public Tessl evaluation for v1.2.2, last scored 2026-09-03: 97% quality and 99% impact. These values evaluate the skill package, not App Store outcomes.
- There are no approved testimonials, App Store approval-rate data, or Apple endorsements. Future work must not fabricate them.

## Product Principles

1. Evidence before certainty.
2. Report before fix.
3. Unknown stays unknown until a real check resolves it.
4. Make the next verifiable action obvious.
5. Keep independent evaluation and product limitations visible.

## Accessibility & Inclusion

The public experience must meet WCAG 2.2 AA for essential text and controls, preserve keyboard and zoom usability, avoid color-only status, and respect reduced motion, reduced transparency, increased contrast, and forced-colors preferences.
