# Framework discovery and review surfaces

Read this file for every repository audit. Framework configuration can be generated, merged, or split across files. Never assume one source file equals the submitted configuration.

## Common discovery order

1. Look for native Xcode projects and workspaces.
2. Identify a cross-platform framework from its package manifest.
3. Find the native iOS output directory.
4. Distinguish authored configuration from generated configuration.
5. Prefer the archive, resolved build settings, or merged plist when available.

## Xcode and native Swift or Objective-C

Detect with:

- `*.xcodeproj/project.pbxproj`
- `*.xcworkspace`
- `Package.swift`, `Podfile`, or `Cartfile`

Inspect:

- every `PBXNativeTarget`, including widgets and extensions
- `INFOPLIST_FILE` and inline `INFOPLIST_KEY_*` settings
- `CODE_SIGN_ENTITLEMENTS`
- `PRODUCT_BUNDLE_IDENTIFIER`
- `IPHONEOS_DEPLOYMENT_TARGET`
- configuration used by the Archive action
- `PrivacyInfo.xcprivacy` membership and contents
- dependency privacy manifests where the built products are available

Use `xcodebuild -showBuildSettings` when Xcode is available and the project can be resolved safely. Static parsing of `project.pbxproj` cannot reproduce every inherited or conditional build setting.

## Expo

Detect with `package.json` containing `expo`, plus one of `app.json`, `app.config.js`, `app.config.ts`, or `app.config.json`.

Inspect authored configuration:

- `expo.ios.infoPlist`
- `expo.ios.entitlements`
- `expo.ios.bundleIdentifier`
- `expo.ios.privacyManifests`, when present
- config plugins that modify iOS settings
- permission declarations from installed Expo modules

If `ios/` exists, inspect the generated Xcode project too. If it does not exist, label native-target, target-membership, merged-plist, and archive checks `MANUAL CHECK`.

When command execution is appropriate, `npx expo config --type public --json` can expose resolved public configuration. It still does not replace an archive inspection.

## React Native

Detect with `package.json` containing `react-native`.

Inspect:

- `ios/*.xcodeproj` or `ios/*.xcworkspace`
- `ios/Podfile` and `Podfile.lock`
- native module setup and permission packages
- app and extension plist, entitlements, and privacy manifests
- JavaScript update systems such as CodePush, especially production behavior
- StoreKit or purchase libraries and restore behavior
- social login packages and native Sign in with Apple support

Do not flag React Native itself as a 4.3 risk. Shared framework code is not evidence of duplication by itself.

## Flutter

Detect with `pubspec.yaml` containing a `flutter:` section.

Inspect:

- `ios/Runner.xcodeproj` and `ios/Runner.xcworkspace`
- `ios/Runner/Info.plist`
- `ios/Runner/*.entitlements`
- `ios/Runner/PrivacyInfo.xcprivacy` and extension manifests
- `ios/Podfile.lock`
- Flutter plugin packages that invoke protected APIs
- in-app purchase, social login, tracking, UGC, and AI-service packages

Do not flag Flutter itself as a 4.3 risk. A framework false positive is a recovery hypothesis only when Apple's message and the app's provenance support it.

## Generated native projects

Generated files can be overwritten. When recommending a fix:

1. identify the authored source of truth
2. explain the generated native effect
3. verify the resolved output after regeneration
4. inspect the archive when target membership or bundled files matter

Do not patch a generated plist alone when an Expo config plugin, React Native setup script, or Flutter build step will overwrite it.

## Multi-target rule

Treat every extension as a separate executable bundle for configuration review. Associate each target with:

- bundle identifier
- plist source
- entitlements
- privacy manifest
- App Group identifiers
- protected API use

If static parsing cannot establish target membership, report that limitation instead of assigning a blocker to a specific target.

## Archive inspection

An `.ipa` is a ZIP archive. Inspect it for:

- app and extension bundles
- merged `Info.plist` files
- embedded provisioning and entitlements, when tools are available
- privacy manifests
- assistant context files, internal notes, and unexpected resources
- duplicated or obsolete frameworks

Archive evidence outranks repository guesses about what ships.
