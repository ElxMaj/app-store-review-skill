# Guideline 2.3.7 Metadata Review Design

## Goal

Release app-store-review-skill v1.2.0 with a deterministic, field-aware check for pricing language in App Store metadata, a complete recovery path for Guideline 2.3.7 rejections, and a tighter core skill that addresses Tessl's current quality feedback.

## Evidence and policy boundary

Apple's August 5, 2026 feedback states that an app subtitle must not refer to the price of the app or service, and that references to free or discounted services count as price references. Apple's current Guideline 2.3.7 is contextual: metadata must not contain prices or terms that are not specific to that metadata type. The rejection explicitly suggests using the app description when the developer needs to advertise a price change, but that does not exempt descriptions from accuracy, purchase-disclosure, or relevance requirements.

The public skill will contain only an anonymized regression fixture. It will not include the developer's name, email address, submission ID, app name, screenshots, or other personal submission data.

## Detection architecture

Add a field-aware metadata pass to `scripts/app_store_review_scan.py`.

The scanner will consume metadata from three trusted entry paths:

1. Explicit text files supplied through repeatable `--metadata FIELD[:LOCALE]=PATH` arguments.
2. Explicit Fastlane roots supplied through repeatable `--metadata-root PATH` arguments.
3. The conventional `<project>/fastlane/metadata` root when it exists.

The explicit field is an enum: `name`, `subtitle`, `keywords`, `promotional_text`, `description`, or `release_notes`. Invalid specifications, unsupported fields, missing files, and directories supplied as files are CLI errors. Fastlane discovery whitelists only `name.txt`, `subtitle.txt`, `keywords.txt`, `promotional_text.txt`, `description.txt`, and `release_notes.txt` directly beneath locale directories, including `default/`. It never scans review-contact, credential, or arbitrary text files. Screenshot and preview assets have no caption text field, so price text in those assets remains a contextual visual check.

The deterministic rule normalizes Unicode with NFKC, case-folds text, and recognizes high-precision price-advertising categories:

- explicit free claims such as `100% free`, `always free`, `completely free`, `free trial`, `free-to-play`, and `free to use`
- `no cost`, `at no cost`, and `zero cost`
- `on sale`, `sale price`, and discounted price, plan, or service phrases
- percentage-off, save-amount, currency-symbol amounts, and common currency-code amounts

A high-precision match in `name`, `subtitle`, `keywords`, or `promotional_text` produces stable finding ID `ASR-METADATA-PRICE-237`, severity `blocker`, guideline `2.3.7`, and evidence confidence `official`. Ambiguous standalone `free` in those fields produces `ASR-METADATA-PRICE-237-REVIEW` as a warning requiring contextual review. Compounds and non-price uses such as `ad-free`, `gluten-free`, `hands-free`, `freeform`, `freestyle`, `point of sale`, `sales tax`, and `discount calculator` do not match. English lexical coverage is explicit; the scanner does not claim to understand every localization.

Descriptions and release notes are recorded in scan coverage but excluded from this presence-only 2.3.7 rule. The report adds a contextual manual check for their accuracy and relevance instead of declaring pricing copy universally safe. Official pricing, subscription, introductory-offer, promotional-offer, and in-app purchase fields are outside this rule because pricing is expected there.

The report schema becomes `1.1` and adds `metadata_scan` with deterministic counts and sorted field and locale lists. Evidence signals contain only enumerated field, locale, and category values, never matched copy. Discovery, inputs, findings, and evidence are sorted. When evidence exceeds the display cap, the report records the total and omitted count. Semantic output must be identical across runs after removing `generated_at`.

## Skill and reference changes

Update the pre-submission checklist with a field-and-context matrix for 2.3.7. Clear price advertising in names, subtitles, keywords, and promotional text is a blocker. Ambiguous wording, screenshot or preview overlays, genuine in-app price UI, descriptions, and release notes require contextual review. Expected pricing fields are excluded.

Update the rejection playbook with a dedicated mapping for subtitle, free, discount, and price-reference messages. The normal classification is `FIX` when the submitted metadata contains the cited language. The recovery guidance will:

- remove equivalent pricing claims from the cited field in every live localization where they occur
- inspect all live localizations and fallback assets instead of claiming local files prove storefront state
- preserve accurate and relevant pricing or price-change copy only in an appropriate description context
- explain that when only editable metadata or product-page assets changed, a new build is normally unnecessary if the current App Store Connect status permits retaining the selected build
- draft a concise Resolution Center reply naming the corrected field and localization

`FIX` is the normal classification only when Apple's cited field and the submitted metadata prove the price claim. `CLARIFY`, `REQUEST INTERPRETATION`, and `APPEAL` remain valid when the cited field is wrong, unavailable, or contextually legitimate.

Refresh policy verification dates to 2026-08-10 after checking Apple's App Review Guidelines, Upcoming Requirements, and App Store Connect metadata reference.

## Tessl quality improvement

The live baseline on 2026-08-10 is overall 95, quality 94%, content 85%, impact 99%, and a 1.67x factor. Tessl's quality review identifies repeated output contracts and an overly long core `SKILL.md` as the remaining weakness.

Refactor the canonical `SKILL.md` without changing behavior:

- keep one output-contract section
- reference `references/report-contract.md`, `references/rejection-playbook.md`, and `references/human-craft-audit.md` instead of repeating their templates
- remove the duplicated reviewer-path enumeration because it already lives in `references/guidelines-checklist.md`
- retain copy-paste scanner and renderer commands, evidence rules, read-only gates, and mode selection

Add a realistic Tessl evaluation for a tightly scoped rejection fixture where Apple cites a subtitle and the supplied subtitle clearly advertises `always free`. The evaluation must require exact-message preservation, `FIX`, 2.3.7 mapping, inspection and correction of every live subtitle localization where equivalent claims occur, description-placement nuance, conditional same-build guidance for a metadata-only change, and a factual reply. For this proven fixture it must reject an appeal, invented binary changes, and blanket bans on price information in descriptions. Existing playbook paths remain available for different evidence.

The release will request a fresh Tessl review after publication and report the resulting score. No score increase is guaranteed before Tessl completes its evaluation.

## Packaging and compatibility

Treat the root skill as canonical, then synchronize artifacts according to their intended roles:

- `skills/app-store-review/` for cross-agent and Codex installation
- `copilot-plugin/skills/app-store-review/` for GitHub Copilot and Tessl packaging
- `app-store-review-skill.skill` for direct Claude-compatible installation

Bump the scanner, report-contract sample, and all plugin manifests to `1.2.0`. The root scanner and references must match the Copilot package and `.skill` archive exactly. The archive `SKILL.md` must match the root. Validate the short compatibility loader and the Copilot resource appendix functionally instead of forcing those intentional wrappers to be byte-identical to the root. Keep the existing v1.1.6 human-craft evaluation work and the ClaudePluginHub README badge when reconciling the current branch with `main`.

## Verification

Use test-first development:

1. Add failing tests for typed CLI parsing, Fastlane discovery, high-precision blocker categories, ambiguous `free` warnings, and deterministic scan coverage.
2. Add negative tests proving that accurate context-specific description pricing, release notes, secret-bearing review files, arbitrary text files, and listed non-price compounds do not trigger the finding.
3. Test default locale handling, duplicate inputs, evidence truncation counts, malicious text redaction, invalid CLI inputs, and semantic determinism.
4. Add the rejection-recovery evaluation and validate its criteria structure.
5. Run scanner and renderer unit tests and JSON smoke tests.
6. Validate the intentional packaging matrix, manifest agreement, archive contents, and archive freshness.
7. Build and inspect the `.skill` archive, then run `tessl plugin lint .` before publication.

## Deployment

Publish v1.2.0 through every configured channel:

1. Commit the implementation and merge it into GitHub `main` without discarding existing work.
2. Push `main`, create tag `v1.2.0`, and publish a GitHub Release with the `.skill` artifact.
3. Publish `maj-labs/app-store-review` to Tessl and request a fresh quality and impact review.
4. Update the repo-backed Claude Code, Codex, GitHub Copilot, and `npx skills add` distributions through the main branch and versioned manifests.
5. Request a ClaudePluginHub refresh if the listing does not update from GitHub automatically.

Any browser action that submits a public form will pause for confirmation immediately before the final submission.
