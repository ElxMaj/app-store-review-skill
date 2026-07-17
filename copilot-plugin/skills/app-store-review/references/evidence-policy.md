# Evidence policy and source register

Use this file whenever a report makes claims about Apple's policy, review behavior, or remediation outcomes.

## Confidence labels

### OFFICIAL

Use for current Apple guideline text, App Store Connect Help, Apple developer agreements, official submission requirements, and Apple technical documentation.

Write: "Apple requires..." or "Guideline 5.1.2(i) states..."

Do not extend the claim beyond the source. For example, Apple's reference to similar binaries, metadata, or concepts does not reveal the implementation of its comparison system.

### DOCUMENTED CASE

Use when a developer provides the rejection wording, the change or reply, and the eventual outcome in a first-person account.

Write: "In one documented case..." Include the date and source. Do not convert one case into a rule or success rate.

### OBSERVED PATTERN

Use when several independent reports point in the same direction but Apple has not confirmed the mechanism.

Write: "Multiple reports are consistent with..." State the important limitations, selection bias, and missing denominator.

### INFERENCE

Use for a reasoned hypothesis that has not been established by Apple or a documented outcome.

Write: "A possible explanation is..." Include what evidence would confirm or falsify it.

## Claim rules

1. Prefer current official sources for requirements.
2. Preserve Apple's exact rejection wording when the user supplies it.
3. Distinguish submission gates from human-review risks.
4. Do not state that a sub-minute rejection proves a fully automated decision. Timing can support an assisted-triage hypothesis only.
5. Do not claim Apple detects Cursor, Claude, Codex, Copilot, or another coding tool from a hidden watermark. No reliable public evidence in the reviewed corpus establishes this.
6. Do not call an app "AI generated" based on generic code, copy, or visuals. Report the specific symptom.
7. Do not assign approval probabilities or success rates without a defined dataset and denominator.
8. If a source reports several simultaneous changes before approval, do not attribute the outcome to one change.
9. Mark policy facts that can age, such as SDK minimums and regional purchase rules, with a verification date.

## Official sources

Last verified: 2026-07-17.

| Subject | Source |
|---|---|
| App Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ |
| Submission SDK and other upcoming requirements | https://developer.apple.com/news/upcoming-requirements/ |
| App Review process and support paths | https://developer.apple.com/distribute/app-review/ |
| Replying to App Review messages and attachments | https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/reply-to-app-review-messages/ |
| Submitting an app for review | https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-app-for-review/ |
| App privacy details | https://developer.apple.com/app-store/app-privacy-details/ |
| Privacy manifests and Required Reason APIs | https://developer.apple.com/documentation/bundleresources/privacy_manifest_files |

## Selected case evidence

These sources are useful for hypotheses and recovery examples. Recheck availability and wording before quoting them.

| Case | What it supports | Confidence and limit | Source |
|---|---|---|---|
| Tomo icon change | An icon was the decisive reported change after earlier metadata changes failed | DOCUMENTED CASE, one app | https://tomolog.reafo.io/en/article/guidline4-3-design-spam-push-into-sleeplessweek |
| Rockhopper built with Godot | A developer reported approval after explaining shared engine code and unique functionality | DOCUMENTED CASE, self-report | https://forum.godotengine.org/t/ios-app-failing-app-store-review-flagged-as-spam/82336 |
| In-house app matched to a terminated account | A developer reported a 4.3 false positive and later approval after clarification | DOCUMENTED CASE, details are incomplete | https://developer.apple.com/forums/thread/741593 |
| Similar icon discussion | Apple forum guidance identifies very similar icons as a spam concern | OFFICIAL FORUM GUIDANCE, not a complete detection specification | https://developer.apple.com/forums/thread/86587 |
| Capacitor similarity appeal | A developer reported repeated 4.3 rejections followed by Board approval | DOCUMENTED CASE, self-report | https://www.reddit.com/r/iOSProgramming/comments/1jq44yf/the_app_was_rejected_6_times_before_finally/ |
| Resolution Center paywall walkthrough | A developer reported approval after supplying exact navigation and screenshots | DOCUMENTED CASE, one app | https://community.revenuecat.com/general-questions-7/app-rejected-by-app-store-apple-couldn-t-find-paywall-6138 |

## Refresh procedure

When adding a case, capture:

- source date and URL
- app category and stack, if stated
- Apple's exact wording, if the author shared it
- changes made before each resubmission
- final outcome and date
- whether the causal change is isolated or confounded
- confidence label

Remove or downgrade a case when the link disappears, the outcome cannot be verified from the source, or later evidence contradicts the interpretation.
