# Pre-submission checklist

Last verified against Apple's official pages: 2026-07-17.

This checklist supports iOS and iPadOS. Apply only the sections relevant to the app. Use `references/evidence-policy.md` for claim wording and `references/frameworks.md` for generated configuration.

## Contents

1. Submission gates
2. Guideline 2.1, completeness
3. Guideline 2.3, metadata
4. Guideline 5.1, privacy and data
5. Guidelines 4.2, 4.3, 4.8, design and accounts
6. Guideline 3.1, business and payments
7. Guideline 1.2, user-generated content
8. Guideline 2.5, technical behavior
9. Reviewer experience
10. Special categories

## 1. Submission gates

- [ ] `BLOCKER`, `OFFICIAL`: The uploaded build uses the current minimum Xcode and platform SDK. Since April 28, 2026 Apple requires Xcode 26 or later and an iOS 26 or iPadOS 26 SDK. Recheck `https://developer.apple.com/news/upcoming-requirements/` before reporting.
- [ ] `BLOCKER`, `OFFICIAL`: Required Reason API use is declared in the privacy manifest with an approved reason. Check app and extension bundles separately.
- [ ] `BLOCKER`, `OFFICIAL`: SDKs on Apple's required-signature and privacy-manifest list meet the current requirements. Inspect the resolved build products, not package names alone.
- [ ] `BLOCKER`, `OFFICIAL`: The App Store icon and asset catalog pass Xcode and App Store Connect validation.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Export compliance answers and any encryption documentation are complete. `ITSAppUsesNonExemptEncryption` can reduce repeated questions only when its value accurately describes the app.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Agreements, tax, banking, age rating, content rights, regional compliance, and App Store Connect required fields are complete.

Do not report `ITMS-91053` unless the user supplied that upload error or the archive validation produced it. A repository scan can establish a missing declaration, not Apple's future error code.

## 2. Guideline 2.1, app completeness

- [ ] `BLOCKER`, `OFFICIAL`: The submitted build launches and the core flow completes without a crash.
- [ ] `BLOCKER`, `OFFICIAL`: Login-required apps include working demo credentials, setup steps, and any one-time codes Apple needs.
- [ ] `BLOCKER`, `OFFICIAL`: There is no reachable placeholder content, sample content presented as real, unfinished primary flow, or disabled control that appears functional.
- [ ] `WARNING`, `OFFICIAL`: Network errors, empty responses, revoked permissions, and expired sessions lead to a useful recovery path rather than a blank screen.
- [ ] `WARNING`, `OFFICIAL`: Region restrictions, hardware dependencies, and uncommon setup are explained in App Review Information with an operable review path.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Support and privacy URLs resolve, use the intended content, and do not require credentials.
- [ ] `MANUAL CHECK`, `OFFICIAL`: The app works on an IPv6 network. Flag literal IPv4 endpoints as code evidence, but do not claim Apple's reviewer always uses one specific network topology.
- [ ] `MANUAL CHECK`, `OFFICIAL`: The app's iPad layout, rotation behavior, keyboard handling, and multitasking behavior match its declared device support.

## 3. Guideline 2.3, accurate metadata

- [ ] `BLOCKER`, `OFFICIAL`: Screenshots and previews show features and UI that exist in the submitted build.
- [ ] `BLOCKER`, `OFFICIAL`: Name, subtitle, description, promotional text, keywords, and What's New text are accurate.
- [ ] `WARNING`, `OFFICIAL`: Store copy avoids competitor names, unrelated terms, keyword chains, and references to unsupported platforms.
- [ ] `WARNING`, `OFFICIAL`: The age rating answers reflect UGC, messaging, web access, simulated gambling, medical content, and other relevant capabilities.
- [ ] `WARNING`, `OFFICIAL`: Subscription and purchase claims match the products, prices, and trial terms configured in App Store Connect.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Accessibility Nutrition Labels, privacy answers, categories, and regional fields match the build.

## 4. Guideline 5.1, privacy and data

### Permission prompts

- [ ] `BLOCKER`, `OFFICIAL`: Every protected API invocation has the matching purpose string in the resolved Info.plist.
- [ ] `WARNING`, `OFFICIAL`: Purpose strings name the data, feature, and user benefit. Vague strings such as "Camera access needed" create review risk.
- [ ] `WARNING`, `OFFICIAL`: Permissions are requested in context, when the user initiates the relevant feature.
- [ ] `WARNING`, `OFFICIAL`: Localized apps localize system-facing purpose strings and explanatory UI.

### Data collection and sharing

- [ ] `BLOCKER`, `OFFICIAL`: The privacy policy and App Store privacy answers accurately describe collection, use, retention, deletion, and sharing.
- [ ] `BLOCKER`, `OFFICIAL`: Personal data is not sent to a third party, including third-party AI, before clear disclosure and explicit permission where required by Guideline 5.1.2(i).
- [ ] `BLOCKER`, `OFFICIAL`: The pre-transfer disclosure identifies the personal data, the receiving third party, and the purpose before asking for permission.
- [ ] `MANUAL CHECK`, `OFFICIAL`: From a clean state, declining third-party AI permission sends no personal data or identifiers to that provider. If the AI feature cannot work without sharing, the UI explains that consequence without treating refusal as consent.
- [ ] `BLOCKER`, `OFFICIAL`: Tracking uses AppTrackingTransparency when the app's behavior meets Apple's tracking definition.
- [ ] `WARNING`, `OFFICIAL`: SDK initialization does not send tracking data before the ATT decision.
- [ ] `WARNING`, `OFFICIAL`: The app offers a usable way to withdraw consent where the guideline requires it.
- [ ] `WARNING`, `OFFICIAL`: Sensitive credentials and tokens use an appropriate protected store rather than plaintext files or UserDefaults.

### Accounts

- [ ] `BLOCKER`, `OFFICIAL`: If the app supports account creation, users can initiate account deletion in the app unless a documented exception applies.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Deletion removes the account and associated data server-side, subject to clearly disclosed legal retention requirements.
- [ ] `WARNING`, `OFFICIAL`: Privacy and account controls are reachable without contacting support unless the applicable rule permits another path.

## 5. Guidelines 4.2, 4.3, and 4.8

### Minimum functionality and templates

- [ ] `WARNING`, `OFFICIAL`: The app provides lasting utility or entertainment beyond a repackaged website, marketing page, or thin content shell.
- [ ] `BLOCKER`, `OFFICIAL`: An app created from a commercialized template or app-generation service is submitted by an eligible content provider and meets Guideline 4.2.6.
- [ ] `WARNING`, `OFFICIAL`: Generated or starter-kit code does not leave the product indistinguishable in purpose, assets, flow, and metadata.

### Spam and similarity

- [ ] `BLOCKER`, `OFFICIAL`: The developer is not submitting multiple Bundle IDs that are merely versions of the same app where Apple expects one configurable app.
- [ ] `WARNING`, `OFFICIAL`: Under the June 8, 2026 wording of 4.3(b), the app offers a meaningfully different or improved experience when entering a mature category.
- [ ] `WARNING`, `DOCUMENTED CASE`: Compare icons and major assets with sibling apps, starter kits, and prior rejected builds. Asset similarity was decisive in at least one documented recovery, but this is not a universal rule.
- [ ] `WARNING`, `OBSERVED PATTERN`: Identify inherited package names, upstream accounts, stock flows, and portfolio duplication. Treat these as similarity evidence, not proof of Apple's internal mechanism.
- [ ] `MANUAL CHECK`, `OFFICIAL`: The first-run experience and product page make the app's specific audience, job, and distinct value legible.

### Sign in with Apple

- [ ] `BLOCKER`, `OFFICIAL`: When Guideline 4.8 applies to third-party or social login, the app offers an equivalent privacy-preserving login option that meets the current rule.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Check the exceptions in the current 4.8 text before reporting a violation.

## 6. Guideline 3.1, business and payments

- [ ] `BLOCKER`, `OFFICIAL`: Digital goods and functionality use an allowed purchase path for the storefront and entitlement context.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Regional external-purchase options are reviewed against the current storefront rules. Do not apply one region's rule globally.
- [ ] `BLOCKER`, `OFFICIAL`: Subscription screens clearly show the billed price, billing period, renewal behavior, trial conversion terms, and required legal links.
- [ ] `WARNING`, `OFFICIAL`: A visible restore mechanism exists where restorable purchases are offered, and the flow works in the review environment.
- [ ] `WARNING`, `OFFICIAL`: Displayed prices come from StoreKit rather than hardcoded currency strings.
- [ ] `WARNING`, `OFFICIAL`: "Free" and discount claims accurately describe the usable experience and amount billed.
- [ ] `BLOCKER`, `OFFICIAL`: Paid randomized virtual items disclose odds when the guideline applies.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Products, review screenshots, localization, and availability are submitted with the build as required.

## 7. Guideline 1.2, user-generated content

- [ ] `BLOCKER`, `OFFICIAL`: UGC features include filtering where appropriate, reporting, blocking abusive users, and published contact information.
- [ ] `BLOCKER`, `OFFICIAL`: The product is not primarily a Chatroulette-style, random, or anonymous chat experience prohibited by the current 1.2 text.
- [ ] `MANUAL CHECK`, `OFFICIAL`: Moderation operations can respond promptly, not merely display nonfunctional controls.
- [ ] `MANUAL CHECK`, `OFFICIAL`: The team can explain how violating content is removed and how repeat abuse is handled.
- [ ] `WARNING`, `OFFICIAL`: Creator content, purchases, age rating, and mature-content controls follow the current 1.2 and 3.1 rules.

## 8. Guideline 2.5 and technical behavior

- [ ] `BLOCKER`, `OFFICIAL`: The app does not download, install, or execute code that changes reviewed features or functionality outside an allowed exception.
- [ ] `WARNING`, `OFFICIAL`: Remote configuration does not unlock undisclosed primary behavior or turn the submitted binary into a different product.
- [ ] `BLOCKER`, `OFFICIAL`: No private APIs or prohibited URL schemes are used.
- [ ] `WARNING`, `OFFICIAL`: Background modes correspond to real, user-facing behavior.
- [ ] `WARNING`, `OFFICIAL`: Push notifications and Live Activities are not required for unrelated core functionality and are not used for spam, phishing, or unsolicited messages under 4.5.3.
- [ ] `WARNING`, `OFFICIAL`: Third-party SDK behavior is included in the review, privacy, tracking, and technical analysis.
- [ ] `INFO`, `OFFICIAL`: Debug-only code is distinguished from Release and archive behavior.
- [ ] `WARNING`, `INFERENCE`: Assistant context files, internal notes, or configuration should not ship. Their presence is a quality and information-exposure problem, not evidence that Apple rejects AI authorship.

## 9. Reviewer experience

Execute when possible and otherwise mark `MANUAL CHECK`:

- [ ] Install the exact candidate build.
- [ ] Launch on a supported iPhone and iPad.
- [ ] Reach core value without private developer knowledge.
- [ ] Exercise login, account creation, deletion, logout, and expired-session recovery.
- [ ] Trigger each permission in context and inspect the localized prompt.
- [ ] Exercise each purchase, trial, cancellation explanation, and restore route.
- [ ] Test empty, loading, offline, timeout, denied-permission, and server-error states.
- [ ] Verify support, privacy, terms, and external links.
- [ ] Check Dynamic Type, VoiceOver, contrast, Reduce Motion, Reduce Transparency, keyboard navigation where applicable, and rotation.
- [ ] Confirm review notes explain unusual hardware, geography, accounts, permissions, and IAP.

## 10. Special categories

Load only when relevant:

- Health and medical: evidence for claims, regulatory status, emergency limitations, HealthKit restrictions, and professional review.
- Kids: Kids Category rules, parental gates, analytics and advertising limits, age-appropriate links, and privacy law obligations.
- Finance and crypto: licensing, custody, trading, personalized advice, geographic availability, and risk disclosures.
- Gambling and lotteries: licensing, geo-restriction, age controls, and contest rules.
- VPN and device management: approved APIs, organization eligibility where required, data handling, and clear user control.
- Hardware: provide a reviewable path and the form of demonstration Apple requests for the device.

For regulated categories, do not infer legal compliance from source code. List the required documentation as `MANUAL CHECK` and recommend qualified review where appropriate.
