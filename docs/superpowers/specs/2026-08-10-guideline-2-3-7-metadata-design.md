# Guideline 2.3.7 Metadata Review Design

## Goal

Release app-store-review-skill v1.2.0 with a deterministic, field-aware check for pricing language in App Store metadata, a complete recovery path for Guideline 2.3.7 rejections, and a tighter core skill that addresses Tessl's current quality feedback.

## Evidence and policy boundary

Apple's August 5, 2026 feedback states that an app subtitle must not refer to the price of the app or service, and that references to free or discounted services count as price references. Apple's current Guideline 2.3.7 also bars pricing information from metadata fields where it is not specific to the field. The rejection explicitly suggests using the app description when the developer needs to advertise a price change.

The public skill will contain only an anonymized regression fixture. It will not include the developer's name, email address, submission ID, app name, screenshots, or other personal submission data.

## Detection architecture

Add a field-aware metadata pass to `scripts/app_store_review_scan.py`.

The scanner will consume metadata from two trusted entry paths:

1. Explicit files supplied through repeatable `--metadata <path>` arguments.
2. Conventional Fastlane metadata files under `fastlane/metadata/<locale>/`.

Supported text fields are app name, subtitle, keywords, promotional text, screenshot captions, and preview captions. Description and release notes are deliberately excluded from the pricing-language blocker because Apple's rejection directs developers to the description for price-change information.

The first deterministic rule will recognize:

- standalone `free`, excluding compounds such as `gluten-free` and `ad-free`
- `free trial`, `no cost`, `discount`, `discounted`, `sale`, percentage-off, and save-price language
- currency symbols and common currency-code amounts

A confirmed match in a supported metadata field produces stable finding ID `ASR-METADATA-PRICE-237`, severity `blocker`, guideline `2.3.7`, and evidence confidence `official`. Arbitrary source strings and general Markdown documentation will not be scanned as App Store metadata.

## Skill and reference changes

Update the pre-submission checklist with a specific 2.3.7 blocker that distinguishes prohibited pricing fields from the permitted description context.

Update the rejection playbook with a dedicated mapping for subtitle, free, discount, and price-reference messages. The normal classification is `FIX` when the submitted metadata contains the cited language. The recovery guidance will:

- remove pricing language from the cited metadata field and every localization
- preserve pricing or price-change copy only in an appropriate description context
- explain that a metadata-only correction may allow the same binary to be resubmitted
- draft a concise Resolution Center reply naming the corrected field and localization

Refresh policy verification dates to 2026-08-10 after checking Apple's App Review Guidelines, Upcoming Requirements, and App Store Connect metadata reference.

## Tessl quality improvement

The live baseline on 2026-08-10 is overall 95, quality 94%, content 85%, impact 99%, and a 1.67x factor. Tessl's quality review identifies repeated output contracts and an overly long core `SKILL.md` as the remaining weakness.

Refactor the canonical `SKILL.md` without changing behavior:

- keep one output-contract section
- reference `references/report-contract.md`, `references/rejection-playbook.md`, and `references/human-craft-audit.md` instead of repeating their templates
- remove the duplicated reviewer-path enumeration because it already lives in `references/guidelines-checklist.md`
- retain copy-paste scanner and renderer commands, evidence rules, read-only gates, and mode selection

Add a realistic Tessl evaluation for the new metadata rejection path. The evaluation must require exact-message preservation, `FIX`, 2.3.7 mapping, removal from every subtitle localization, description-placement nuance, same-binary guidance for a metadata-only change, and a factual reply. It must reject appeals, invented binary changes, and blanket bans on price information in descriptions.

The release will request a fresh Tessl review after publication and report the resulting score. No score increase is guaranteed before Tessl completes its evaluation.

## Packaging and compatibility

Treat the root skill as canonical, then synchronize it to:

- `skills/app-store-review/` for cross-agent and Codex installation
- `copilot-plugin/skills/app-store-review/` for GitHub Copilot and Tessl packaging
- `app-store-review-skill.skill` for direct Claude-compatible installation

Bump the scanner and all plugin manifests to `1.2.0`. Keep the existing v1.1.6 human-craft evaluation work and the ClaudePluginHub README badge when reconciling the current branch with `main`.

## Verification

Use test-first development:

1. Add a scanner test where a subtitle containing standalone `free` fails before implementation.
2. Add negative tests proving that description pricing and non-price compounds do not trigger the finding.
3. Add the rejection-recovery evaluation and validate its criteria structure.
4. Run scanner and renderer unit tests.
5. Validate every packaged skill copy and verify byte-for-byte synchronization.
6. Build and inspect the `.skill` archive.
7. Run repository validation and security checks already configured in CI.

## Deployment

Publish v1.2.0 through every configured channel:

1. Commit the implementation and merge it into GitHub `main` without discarding existing work.
2. Push `main`, create tag `v1.2.0`, and publish a GitHub Release with the `.skill` artifact.
3. Publish `maj-labs/app-store-review` to Tessl and request a fresh quality and impact review.
4. Update the repo-backed Claude Code, Codex, GitHub Copilot, and `npx skills add` distributions through the main branch and versioned manifests.
5. Request a ClaudePluginHub refresh if the listing does not update from GitHub automatically.

Any browser action that submits a public form will pause for confirmation immediately before the final submission.
