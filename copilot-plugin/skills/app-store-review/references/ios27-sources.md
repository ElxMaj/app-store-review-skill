# iOS 27 source register

Checked **2026-10-09** against public Apple pages. This register supports the iOS 27 update; retained community recovery evidence has its own dates in [evidence-policy.md](evidence-policy.md). Capabilities are `OFFICIAL`; unexecuted review procedures remain `INFERENCE` / `MANUAL CHECK`.

## Release and submission sources

| Source | Scope and freshness limit |
|---|---|
| [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) | Current policy; verify wording and storefront scope when judging a finding |
| [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) | Enforced SDK/Xcode and deployment-target floors, not the newest optional SDK |
| [iOS 27 overview](https://developer.apple.com/ios/whats-new/) | Capability map; still includes beta wording, so do not use it alone to establish release status |
| [iPadOS 27 overview](https://developer.apple.com/ipados/whats-new/) | Capability map and Pencil/Paper surfaces; actual model/device availability is separate |
| [iOS/iPadOS 27 release notes](https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes) | SDK-linked changes, framework sections, known/resolved issues and deprecations |
| [Xcode 27 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes) | Compiler/SDKs, host support, Device Hub, performance and testing tools |
| [Xcode Support](https://developer.apple.com/support/xcode/) | Current compatibility table; distinguish build host, debugging and deployment support |
| [27 SDK submissions open](https://developer.apple.com/news/?id=k1mtkt1k) | 2026-09-09 announcement; establishes acceptance without imposing a new minimum |
| [TN3208 launch screen](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements) | SDK 27+ app launch-screen upload gate; revised 2026-09-14 |
| [Scene lifecycle migration](https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle) | Runtime adoption requirement and static versus programmatic scene configuration |
| [Xcode 27.1 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes) | Returned title: Xcode 27.1 RC; do not present RC tool limitations as universal runtime failures |
| [27.2 release notes](https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27_2-release-notes) | Returned title: 27.2 Beta 3; ATT and margins changes need exact-version verification |

## Engineering and design sessions

| Area | Primary source |
|---|---|
| Foundation Models, providers, images, profiles and evaluations | [WWDC26 / 241](https://developer.apple.com/videos/play/wwdc2026/241/) |
| PCC availability, usage limits and fallback | [WWDC26 / 319](https://developer.apple.com/videos/play/wwdc2026/319/) |
| Core AI | [WWDC26 / 324](https://developer.apple.com/videos/play/wwdc2026/324/) |
| App Intents and Siri | [WWDC26 / 345](https://developer.apple.com/videos/play/wwdc2026/345/) |
| AppIntentsTesting | [WWDC26 / 295](https://developer.apple.com/videos/play/wwdc2026/295/) |
| Core Spotlight / LLM retrieval | [WWDC26 / 246](https://developer.apple.com/videos/play/wwdc2026/246/) |
| SwiftUI | [WWDC26 / 269](https://developer.apple.com/videos/play/wwdc2026/269/) |
| UIKit, scene lifecycle and adaptive windows | [WWDC26 / 278](https://developer.apple.com/videos/play/wwdc2026/278/) |
| Design principles | [WWDC26 / 250](https://developer.apple.com/videos/play/wwdc2026/250/) |
| Brand identity | [WWDC26 / 251](https://developer.apple.com/videos/play/wwdc2026/251/) |
| Widgets | [WWDC26 / 277](https://developer.apple.com/videos/play/wwdc2026/277/) |
| Music Understanding | [WWDC26 / 253](https://developer.apple.com/videos/play/wwdc2026/253/) |
| Now Playing | [WWDC26 / 312](https://developer.apple.com/videos/play/wwdc2026/312/) |
| In-App Purchase | [WWDC26 / 210](https://developer.apple.com/videos/play/wwdc2026/210/) |

## Duo, commerce and marketing sources

| Source | Scope and freshness limit |
|---|---|
| [Prepare and submit for Duo](https://developer.apple.com/news/?id=kkphp5qo) | 2026-10-05; customer launch 2026-10-23 and screenshot requirement April 2027 |
| [Duo preparation](https://developer.apple.com/iphone-duo/prepare/) | SDK versus display adaptation; current-container layout guidance |
| [Duo design](https://developer.apple.com/videos/play/tech-talks/111466/) | Foldable task continuity and layout design |
| [Duo adaptive poses](https://developer.apple.com/videos/play/tech-talks/111463/) | Poses and adaptive interface implementation |
| [Duo displays/scenes](https://developer.apple.com/videos/play/tech-talks/111464/) | Multi-display/scene behavior |
| [Subscription rollout](https://developer.apple.com/news/?id=likeohx4) | 2026-09-16; distinguish configuration access from customer launch dates |
| [Subscription Bundles and Suites](https://developer.apple.com/app-store/subscriptions/bundles-and-suites/) | Eligibility, StoreKit 2 and configuration requirements |
| [New store assets](https://developer.apple.com/news/?id=ljpl7kyn) | 2026-10-05; headers, search assets, previews and Asset Library |
| [Manage store assets](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets) | Independent asset submission and approval, placements and roles |
| [Creative specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications) | Recheck dimensions, formats, duration and placement limits rather than copying fixed values |
| [Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) | Device/orientation requirements and accepted sizes |
| [App Store Connect release notes](https://developer.apple.com/help/app-store-connect/release-notes/) | Further changes to submission, metadata and commerce surfaces |
| [Accessibility Nutrition Labels](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels) | Per-device common-task criteria; voluntary initial participation, with no inferred mandatory deadline |
| [Digital Goods and Services questionnaire](https://developer.apple.com/help/app-store-connect/manage-app-information/complete-the-digital-goods-and-services-questionnaire) | Account-state applicability, regional payment answers and 12-month EU choice lock |

## Refresh method

For a new audit, recheck requirements, exact runtime/SDK release notes and relevant App Store Connect Help. When JavaScript documentation returns only a shell, use Apple's linked Markdown representation (the same URL with `.md`) or Apple's documentation data rather than claiming the text was read. The `.md` pages above were retrieved when the HTML was a shell. If retrieval fails, name the missing source and retain the dated baseline; do not infer an unpublished API or deadline.

Capture verification date, page title/release channel, the applicable requirement, effective date if supplied, source URL and what changed. Move a beta item into the active baseline only after verifying its release and applicability. Revalidate scanner fixtures and all installable package copies together. Never update an old community case's verification date merely because this platform register was refreshed.
