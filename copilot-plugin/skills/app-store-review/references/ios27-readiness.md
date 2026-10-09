# iOS 27 and iPadOS 27 readiness

Public Apple sources checked **2026-10-09**. Use this reference for Mode A platform review and the relevant Mode C design/product-page checks. Read [ios27-sources.md](ios27-sources.md) for dated source links and release channels. This is a maintained review map, not a claim that a static scan can verify every OS change.

## Contents

1. Establish version and evidence
2. Submission gates and migration
3. AI, Siri, search, and privacy
4. Design, accessibility, and adaptive interfaces
5. Technology coverage map
6. Commerce and product-page marketing
7. Runtime matrix and handoff
8. Minor-release and future-requirement watchlist

## 1. Establish version and evidence

Record the **linked SDK**, **Xcode/compiler**, **deployment target**, **test OS build**, **device**, **feature eligibility**, **language/region**, and **distribution channel** separately. A deployment target of 13 does not mean the binary was built with SDK 13. `SDKROOT = iphoneos` is not a version. `SWIFT_VERSION` is a language mode, not proof of the compiler version. Local Xcode is not evidence of CI's upload toolchain.

Prefer each submitted executable bundle's `DTSDKName`, `DTXcode`, and `MinimumOSVersion`, plus signed entitlements and the build log. Review app and extension targets independently. Framework and watchOS companion plists do not establish an iOS app's upload compliance. Repository settings, Podfiles, `.xcconfig`, and Expo build properties are authored evidence that needs resolution, not proof of the archive.

The scanner accepts an IPA, ZIP, or `.xcarchive` directory. It reads bounded plist metadata without extracting files, executing project code, installing dependencies, compiling, or accessing the network. A readable plist is not proof of a valid executable, signature, profile, or successful upload. Malformed, missing, ambiguous, and oversized evidence stays manual.

`platform_review.verification_status = bundled_reference` means the scanner used this dated snapshot. It did not perform live policy verification. `runtime_test_status = not_run` means exactly that. Technology `manual` means a source signal exists; `not_detected` does not prove the feature is absent or inapplicable. Resolve applicability using product evidence, native bridges, dependencies, and the submitted build.

Do not require optional adoption of Siri, Foundation Models, Core AI, widgets, glass effects, subscription bundles, or a foldable-specific feature. Require compliance only when the published rule applies. Assess quality through observable behavior. Use the existing severity and evidence-confidence contracts.

## 2. Submission gates and migration

| Check | Published scope | Evidence and result |
|---|---|---|
| Minimum SDK and Xcode | `OFFICIAL`: Xcode 26+ and iOS/iPadOS SDK 26+ since 2026-04-28 | A lower version in an iOS executable bundle produces `ASR-UPLOAD-SDK` / `ASR-UPLOAD-XCODE`. Source-only or unresolved values remain manual. The arrival of SDK 27 does not itself change this minimum. [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) |
| Minimum deployment target | `OFFICIAL`: iOS/iPadOS uploads must target 13+ since 2026-09-09 | A lower `MinimumOSVersion` in the iOS app/extension produces `ASR-UPLOAD-MINIMUM-OS`. Check all configurations before recommending an authored change. [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) |
| Launch screen when linking SDK 27+ | `OFFICIAL`: the app plist must contain `UILaunchStoryboardName`, `UILaunchStoryboards`, `UILaunchScreen`, or `UILaunchScreens` | `ASR-IOS27-LAUNCH-SCREEN` requires an inspected SDK 27+ app bundle with all four absent. Do not apply this app-only check to an `.appex`; source absence is manual. Then verify referenced resources and clean-install appearance. [TN3208](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements) |
| Scene lifecycle | `OFFICIAL`: apps built with the latest 27 SDK need the scene-based lifecycle to launch | Inspect scene configuration or dynamic app-delegate configuration and SwiftUI's generated output. Absence of one source file or `UIApplicationSceneManifest` alone does not settle programmatic configuration. Confirm failure on the candidate before assigning a runtime blocker. [Migration guide](https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle) |
| Actual upload validation | `MANUAL CHECK`: architecture, signing, provisioning, capabilities, privacy manifests, icon, and required fields | Use Xcode/App Store Connect on the exact candidate. Preserve supplied validation messages. Never predict an `ITMS-` code from a static signal, including the new launch-screen check. |

`OFFICIAL`: Xcode 27 includes Swift 6.4, requires an Apple silicon Mac with macOS Tahoe 26.6+, and supports iOS deployment targets starting at **15** and device debugging starting at **17**. These toolchain limits are separate from App Store Connect's upload floor of **13**. A 13/14 value can meet that stated upload floor without establishing a target supported by the accepted toolchain. Do not promise that Xcode 27 can build it; reconcile the actual CI configuration and supported targets. Recheck the precise Xcode version against [Xcode release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes) and [Xcode system requirements](https://developer.apple.com/xcode/system-requirements). A developer-tool preview, coding agent, or simulator limitation is not automatically an app defect.

`INFERENCE`: For SDK-linked behavioral migrations, compile both the existing release configuration and the proposed configuration, then compare actual launch, navigation, layout, persistence, and resource loading. Compiler failures or deprecations require context; a deprecated but supported API is not automatically prohibited by App Review.

## 3. AI, Siri, search, and privacy

### Foundation Models and provider boundaries

`OFFICIAL`: iOS 27 expands Foundation Models with image input, system-backed tools, model-provider abstraction, and dynamic profiles. [Foundation Models update](https://developer.apple.com/videos/play/wwdc2026/241/)

`MANUAL CHECK`, `INFERENCE`: Build a provider-and-data map for every profile and fallback:

| Route | Review evidence |
|---|---|
| `SystemLanguageModel` / local custom model | Actual availability result, downloaded model state, supported hardware/language, image and audio access, context budgets, cancellation, and safe unavailable/refusal UI. A local model may still call networked tools. |
| Apple Private Cloud Compute | Capability/eligibility, signed configuration where required, connectivity, rate/usage limits, and fallback. PCC is cloud processing; calling it “100% on-device” is inaccurate when data leaves the device. It is not automatically an unrelated third-party AI provider. |
| Claude, Gemini, or another remote provider | Actual endpoint and payload, provider identity, auth/token handling, retention, processing region, explicit permission before personal-data transfer, and decline/revocation behavior. A Foundation Models wrapper does not make this data local. |
| Dynamic profile or automatic provider fallback | What data/history/tools persist across the switch, whether the user's permission covers the new recipient, visible processing status, cancellation, and unexpected paid usage. Permission for one recipient is not evidence of permission for another. |

`OFFICIAL`: Apple's overview identifies Small Business Program participation and fewer than two million total first-time downloads for no-cloud-API-cost PCC access. Recheck actual program terms; do not infer eligibility, unlimited usage, or a free end-user subscription from package presence. [iOS developer overview](https://developer.apple.com/ios/whats-new/), [PCC availability and limits](https://developer.apple.com/videos/play/wwdc2026/319/)

`OFFICIAL`: Personal-data sharing with third-party AI requires the disclosure and explicit permission described in 5.1.2(i). Use the privacy checklist for policy, labels, retention, deletion, ATT when applicable, and a verified decline path. Apple's cloud services, third-party AI transfer, and tracking are distinct data flows. [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)

`MANUAL CHECK`, `INFERENCE`: Test generated output and tool effects separately. Include malformed structured results, hallucinations, unsafe user requests, hostile retrieved text, unauthorized tools, duplicate/retried writes, destructive actions, cancellation, and an unavailable provider. Inspect actual evaluations rather than treating an `import Evaluations` as evidence of quality. Recommended evaluations are not a universal App Store submission requirement. [Evaluations framework](https://developer.apple.com/videos/play/wwdc2026/241/)

### Siri, App Intents, view annotations, and semantic search

`OFFICIAL`: Entity/intent schemas, view annotations, and semantic indexing can expose app content and actions to Siri. [App Intents capabilities](https://developer.apple.com/videos/play/wwdc2026/345/)

`MANUAL CHECK`, `INFERENCE`:

- Map each advertised action to a real intent, entity schema, current visible entity, and stable identifier. Inspect native modules when the UI is cross-platform.
- Exercise ambiguous requests, deleted entities, no matches, locked devices, logout, expired accounts, permission refusal, and language/region availability.
- Require appropriate authentication and confirmation around destructive or sensitive actions. Test tools and shortcuts outside the app's foreground UI, including retries.
- Confirm private content is indexed only as intended and that logout/deletion/revocation removes or invalidates retained entries. Verify attribution and app deep links from search results.
- Use AppIntentsTesting for reproducible system-path coverage where available, then verify real Siri behavior separately. A unit test or schema import does not prove an end-to-end Siri conversation.

[AppIntentsTesting](https://developer.apple.com/videos/play/wwdc2026/295/), [Core Spotlight search](https://developer.apple.com/videos/play/wwdc2026/246/)

## 4. Design, accessibility, and adaptive interfaces

`OFFICIAL`: Apple refines materials, typography, and navigation in 27; Liquid Glass originated in the previous design cycle. Use the current system's controls and materials where they support the task, while preserving the product's identity. Do not prescribe decorative glass everywhere or describe a system restyle as product differentiation. [Design principles](https://developer.apple.com/videos/play/wwdc2026/250/), [Brand identity](https://developer.apple.com/videos/play/wwdc2026/251/)

`MANUAL CHECK`, `INFERENCE`: Review real screens in light/dark appearance, tinted/clear icon appearances offered by the system, larger text, VoiceOver/Voice Control, Increase Contrast, Reduce Transparency, and Reduce Motion. Check busy content behind translucent controls, focus order, hit regions, dismissibility, empty/error/loading states, readable subscription terms, and discoverable actions when navigation minimizes. Do not give a passing grade from modifier names or screenshots alone.

`OFFICIAL`: SDK 27 makes iPhone interfaces resizable in Mirroring and on iPad. Layout must adapt to the current scene rather than rely on `UIScreen.main`, orientation, or device-idiom identity. `UIRequiresFullScreen` needs current behavior review rather than an assumption that it prevents all resizing. [UIKit modernization](https://developer.apple.com/videos/play/wwdc2026/278/)

`MANUAL CHECK`, `INFERENCE`: Inspect per-scene state, restoration, screen changes, safe areas, keyboard avoidance, pointer/focus, popovers, document windows, external displays, and iPhone-only apps on iPad. A phone idiom or regular size class does not reliably identify the physical device. Resolve dimensions from the current container. Check React Native/Flutter/Expo bridges and layout libraries as well as native source.

`OFFICIAL`: iPhone Duo support includes dynamic inner/outer-display transitions and poses; Xcode 27.1 adds device development support. [Prepare for Duo](https://developer.apple.com/iphone-duo/prepare/), [Adaptive poses](https://developer.apple.com/videos/play/tech-talks/111463/)

`MANUAL CHECK`, `INFERENCE`: Test fold/unfold while editing, purchasing, showing a sheet, recording, or running an AI task. Preserve content, selection, scroll position, playback, camera coordinates, and focused controls. Check both displays, all supported poses/orientations, intermediate widths, hinge/occlusion handling where relevant, touch reach, and parallel scenes. Record simulation separately from hardware results. [Duo design](https://developer.apple.com/videos/play/tech-talks/111466/), [Multiple displays/scenes](https://developer.apple.com/videos/play/tech-talks/111464/)

## 5. Technology coverage map

Each row is a routing area, not a mandatory feature. `OFFICIAL` sources establish the capability; the suggested tests are `INFERENCE` until executed. Mark unused areas `NOT APPLICABLE` only after establishing scope. Search the exact release notes for relevant **New Features**, **Deprecations**, **Known Issues**, and **Resolved Issues**; a resolved beta bug is not a current app defect.

| Area / source | Review when relevant |
|---|---|
| [Core AI](https://developer.apple.com/videos/play/wwdc2026/324/) | Custom/local model loading, specialization, licensed model distribution, memory pressure, cancellation, hardware availability, and foreground/background execution. Verify any background-inference entitlement in the signed product before recommending a key. |
| [SwiftUI](https://developer.apple.com/videos/play/wwdc2026/269/) | SDK-dependent state initialization, visible tab selection, selectable-text/custom-gesture interaction, async documents and disk access, lists/grids/reordering, lazy content, image caching, menus, status bars, and external-display accessories. |
| [UIKit](https://developer.apple.com/videos/play/wwdc2026/278/) | Scene lifecycle, trait propagation, adaptable navigation/sidebar/search, restoration, drag-loaded content used by Siri, and resizable scenes. Test modal/presentation behavior with actual traits. |
| [WidgetKit](https://developer.apple.com/videos/play/wwdc2026/277/) and ActivityKit | Intent configuration, dynamic styling, interactivity, redaction, updates, App Groups, extension budgets, stale/expired state, Live Activity controls and deep links. |
| [Background Assets](https://developer.apple.com/documentation/backgroundassets) | Localized asset delivery, low disk, interrupted/failed downloads, asset integrity and launch without optional packs. Review legacy On Demand Resources separately from downloaded code. |
| [Music Understanding](https://developer.apple.com/videos/play/wwdc2026/253/) / MusicKit | Consent and content rights, audio analysis, model/resource availability, denial, accuracy claims, and offline degradation. |
| [Now Playing](https://developer.apple.com/videos/play/wwdc2026/312/) / media sharing | Remote controls, playback state, interruptions, Lock Screen/Control Center/Dynamic Island/CarPlay, device changes, and each media-sharing executable bundle. |
| [Camera and RAW](https://developer.apple.com/ios/whats-new/) | Protected API purpose strings, limited Photos access, capture latency, Center Stage hardware/crop/orientation, high-resolution capture, RAW quality, and supported VideoToolbox configurations. |
| [PencilKit / PaperKit](https://developer.apple.com/ipados/whats-new/) | Handwriting-language coverage, editing/selection, low-latency inking, export, touch and keyboard alternatives, and availability on non-Pencil devices. |
| [Games and Metal](https://developer.apple.com/games/) | Touch/controller parity, accessible controller mappings, window/display resizing, shader/resource compilation, frame pacing, memory/thermal limits, Game Center and purchase setup. A desktop porting tool is not itself an iOS app capability. |
| [HealthKit](https://developer.apple.com/documentation/healthkit) / [HomeKit](https://developer.apple.com/documentation/homekit) | Limited-history permission states, newly supported sample types, invalid/empty samples, accessory support, user controls, and truthful claims about entitlement, subscriptions, and cloud processing. Use the regulated-category rules. |
| [Trust Insights](https://developer.apple.com/documentation/trustinsights) / identity | Signed capabilities, internet dependency, denial/offline behavior, account recovery, fraud decisions, passkeys/Wallet and sensitive action protection. A risk signal does not prove legal identity or authorization. |
| [Accessories](https://developer.apple.com/documentation/audioaccessorykit), Bluetooth, Wi-Fi Aware, Nearby Interaction | Pairing, reconnect, denied/limited access, hardware requirements, permitted regions, and announced-versus-shipped features. |
| [MetricKit](https://developer.apple.com/documentation/metrickit) / StateReporting | Real crash/memory/hitch diagnostics, renamed or removed payload types, state attribution, bounded telemetry and collection disclosure. |
| [WebKit](https://developer.apple.com/documentation/webkit), NetworkExtension, managed networking | Auth redirects, downloads, web permissions, extension scope, TLS/certificates in affected managed services, VPN eligibility and regional restrictions. Do not generalize an MDM TLS rule to every app request. |
| Foundation/System, TextKit, PhotoKit, RealityKit, ShaderGraph, USDKit, SensorKit, Core Motion/Location, Watch Connectivity | Search the owning release note for used APIs; test persistence/file access, rich text, nullable metadata, data exports, spatial assets, measurement coordinates, permission loss and companion interoperability. |

`MANUAL CHECK`: The scanner's 23 technology families are **source heuristics**, with no guarantee of exhaustive detection. Objective-C runtime calls, cross-platform packages, native bridges, dynamically generated projects, entitlements, and remote/server behavior may need manual discovery. Absence of `import` syntax does not close a review area.

## 6. Commerce and product-page marketing

### Commerce

`OFFICIAL`: StoreKit 2 supports new Bundles/Suites configurations and multiseat purchase flows. Eligibility, server-side lifecycle, storefront availability and staged launch matter. A Suite is not a paid app bundle, and a subscription bundle is not multiple interchangeable individual entitlements. [Bundles/Suites requirements](https://developer.apple.com/app-store/subscriptions/bundles-and-suites/), [September rollout notice](https://developer.apple.com/news/?id=likeohx4)

`MANUAL CHECK`, `INFERENCE`: Review transaction ownership and seat assignment/revocation, shared access, refunds, family behavior where applicable, upgrades/downgrades, offer redemption results, restore/reinstall, sandbox versus production configuration, and server notifications. Check bundle membership and purchase availability before promising access across apps. [In-App Purchase changes](https://developer.apple.com/videos/play/wwdc2026/210/)

`MANUAL CHECK`, `INFERENCE`: For monthly billing with a 12-month commitment, display both billing frequency and total commitment accurately. Test cancellation/renewal explanation, unpaid periods, regional eligibility and existing-subscription transitions. “Monthly” alone can misrepresent a longer obligation. Do not apply a region's external-payment option worldwide or assume OS 27 removes IAP rules.

### Store assets and truthful claims

`OFFICIAL`: Product-page headers, search-result creative assets, Asset Library management, independent creative-asset review and App Store Connect previews expand the marketing surfaces. [October asset announcement](https://developer.apple.com/news/?id=ljpl7kyn), [Asset Library help](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets)

`MANUAL CHECK`, `INFERENCE`:

- Inventory icon, screenshots, app previews/poster frames, header images/video, search-result creative assets, in-app events, custom product pages, localizations and fallback assets.
- Check current size/format/duration/placement specifications instead of reusing one device's crop. Inspect light/dark and device/orientation previews, readability, safe content regions, and rights to every asset. [Creative specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications), [Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)
- Confirm each asset's actual approval status and placement. A local export is not approved or published evidence. Keep marketing review distinct from candidate-build review.
- Match every AI, Siri, compatibility, subscription, privacy and performance claim to the exact shipped behavior and audience. Distinguish OS support from AI-device eligibility, language support, network requirements and regional rollout.
- Show genuine task outcomes. New system styling alone does not establish distinct value under 4.2/4.3. Keep all five existing Mode C grades and highest-impact interventions.
- Verify age-rating answers, data-flow disclosures, privacy labels and Accessibility Nutrition Labels against demonstrated capabilities. System intelligence does not give a third-party app permission to advertise capabilities it does not implement.

`OFFICIAL`: Accessibility Nutrition Labels cover completing the app's common tasks with each claimed feature, assessed per supported device. Their help page still describes voluntary initial participation; do not invent an iOS 27 submission deadline. Include first launch, login, purchases and settings in the evaluation. [Accessibility label criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels)

`MANUAL CHECK`: Inspect App Store Connect's Digital Goods and Services questionnaire and any storefront-specific commerce settings using the current account state. Repository code alone cannot establish an answer or eligibility. [Questionnaire help](https://developer.apple.com/help/app-store-connect/manage-app-information/complete-the-digital-goods-and-services-questionnaire)

`OFFICIAL`: No questionnaire action is required when the form is absent. When it
appears, answers describe digital-goods access/payment by region; submitted EU
choices remain locked for 12 months. Prepare answers from verified commerce flows
and obtain scoped approval before saving them. [Questionnaire help](https://developer.apple.com/help/app-store-connect/manage-app-information/complete-the-digital-goods-and-services-questionnaire)

## 7. Runtime matrix and handoff

`INFERENCE`: Use a risk-based matrix and record exactly which cells were executed. Avoid a meaningless “tested on iOS 27” checkbox.

| Dimension | Minimum useful evidence for relevant behavior |
|---|---|
| Runtime and SDK | Candidate linked SDK + OS build; current 27 release, supported oldest OS, and separate 27.1/27.2 tests when relevant |
| Devices and performance | Compact/larger iPhone, supported iPad, AI-capable/non-capable devices, low memory/storage, battery/thermal pressure |
| Adaptive scenes | Rotation, live resizing, Mirroring, keyboard, external display, multiwindow; Duo outer/inner/folded/intermediate poses using 27.1 tools |
| AI state | Enabled/disabled, model missing/downloading, refusal, timeout/offline, usage limit, unsupported language/region, provider switch, cancel/retry |
| User and commerce | Fresh install, denied permissions, anonymous/signed-in/expired/deleted account, locked device, purchase/restore/refund/seat revocation |
| Accessibility and locale | Large text, VoiceOver, keyboard/Voice Control, contrast, motion/transparency preferences, right-to-left and long strings |
| Extensions and services | Each target's launch/path/budget/privacy; terminated process, stale data, notifications, deep links and server failures |

Keep `MANUAL CHECK` when no evidence exists. A reliable supplied test record may establish an observed pass; a simulator run does not prove hardware camera, Neural Engine, signing entitlement or real Siri behavior. Preserve exact failures and reproduction steps. The scanner never launches the app.

In the final report, include `iOS 27 platform review` after scope, retain the canonical `platform_review` JSON, and state:

```text
Linked SDK / Xcode: <archive and CI evidence, or MANUAL CHECK>
Deployment target: <per-bundle evidence, or MANUAL CHECK>
Policy verification: <live date and URLs, or bundled_reference dated 2026-10-09>
Runtime tests: <executed matrix with evidence, or not_run>
Applicable platform areas: <manual / verified / not applicable, with reason>
Future and beta items: <version, release channel, date, source>
```

App Review Notes should describe real feature paths, provider/data routing, prerequisites, fallback, hardware/region limitations and reviewer access. Include only verified information; do not invent credentials, tests, entitlement approvals or a privileged relationship with Apple.

## 8. Minor-release and future-requirement watchlist

| Item | Snapshot on 2026-10-09 | Review treatment |
|---|---|---|
| iPhone Duo / 27.1 | `OFFICIAL`: customer availability announced for **2026-10-23**; Xcode 27.1 development support | Test available simulator/Device Hub today; do not claim a physical-device test without one. [Duo notice](https://developer.apple.com/news/?id=kkphp5qo) |
| Duo screenshots | `OFFICIAL`: requirement announced for **April 2027**, without a precise day in the notice | Future preparation, not a current blocker. Recheck exact enforcement date and specifications before submission. [Duo notice](https://developer.apple.com/news/?id=kkphp5qo) |
| Xcode 27.1 RC | `OFFICIAL`: release notes list simulator/extension and Catalyst limitations | Separate tool limitations from app failures; check the current revision before relying on a workaround. [27.1 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes) |
| iOS/iPadOS 27.2 beta | `OFFICIAL`: beta release notes cover expanded ATT prompts, EU annual re-prompt support, and API renames; the expanded prompt is required for France, Germany, Italy, Poland and Romania in that beta documentation | Verify distribution/runtime scope and final API name; do not apply a 27.2 beta rule to every 27.0 build or treat a rename as a privacy violation. Test refusal and pre-consent network traffic. [27.2 notes](https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27_2-release-notes) |
| UIView layout margins | `OFFICIAL`: 27.2 notes document a default-margin change on 27.1+ | Check nested view margins and intended inheritance in the actual version; do not hardcode yesterday's padding. [27.2 notes](https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27_2-release-notes) |
| Subscription expansion | `OFFICIAL`: September notice announces Volume Purchasing for **2026-10-22**, Group Purchases for winter, and Bundles/Suites later in 2026 | Configuration/eligibility can precede customer availability. Avoid declaring these universally shipped on October 9. [Rollout notice](https://developer.apple.com/news/?id=likeohx4) |
| Release-note-only previews | `OFFICIAL`: base release notes include future/preview capabilities and resolved beta issues | Recheck AudioAccessoryKit region/availability, spatial APIs and other used preview surfaces in the owning documentation. A marketing announcement is not an SDK availability guarantee. [27 notes](https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes) |

Refresh this watchlist after point releases, new deadlines, HIG changes, or App Store Connect changes. Prefer exact version/build and channel to a blanket “all iOS 27 features” claim.
