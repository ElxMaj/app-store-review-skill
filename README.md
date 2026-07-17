# App Store Review Skill

Catch the rejection in your repository, then give Apple a clearer build and a stronger case.

<a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
<a href="https://developer.apple.com/app-store/review/guidelines/"><img alt="Guidelines verified July 17, 2026" src="https://img.shields.io/badge/guidelines-verified%202026--07--17-0A7E07.svg"></a>
<a href="https://code.claude.com/docs/en/plugins"><img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-6B4FBB.svg"></a>

`app-store-review` is a full-lifecycle review companion for iOS and iPadOS projects built with Xcode, Expo, React Native, or Flutter. It runs a pre-submission compliance audit, diagnoses rejections and drafts Resolution Center replies, and performs a human-craft audit for Guideline 4.3 similarity and low-effort risk. Policy references were verified against Apple's public guidance on July 17, 2026, including the June 8, 2026 Guideline 4.3(b) update. Recovery guidance separates official rules from documented developer outcomes and unconfirmed patterns.

## Quick Start

Install as a portable agent skill for Codex, Claude Code, and other compatible clients:

```bash
npx skills add ElxMaj/app-store-review-skill
```

Or install from this repository as a Claude Code marketplace plugin:

```text
/plugin marketplace add ElxMaj/app-store-review-skill
/plugin install app-store-review@app-store-review-skill
```

Then just say:

```text
Audit this Expo app before I submit it. Report first and do not change files.
Apple rejected build 42 under 4.3(a). Diagnose it and draft a factual reply.
Run the human-craft audit and tell me what makes this app look generic.
```

## What it does

### Pre-submission audit

The scanner detects the project type, inventories native targets, and collects file-level evidence for permission strings, privacy manifests, Required Reason APIs, dynamic code, account deletion, Sign in with Apple, IAP restore paths, ATT, third-party AI consent, placeholder content, and exact asset reuse. The agent then checks the parts code cannot prove, including App Store metadata, privacy answers, reviewer access, iPad behavior, purchases, links, and failure states. Reports are available as dense Markdown and stable JSON.

### Rejection recovery

The playbook maps Apple's exact wording to `FIX`, `CLARIFY`, `APPEAL`, or `REQUEST INTERPRETATION`. Its 4.3 path separates portfolio duplication from the newer indistinguishable-app test, ranks remediation by evidence quality, includes a framework false-positive response, and gives Resolution Center reply mechanics with exact navigation and attachment prompts. Fast rejections are treated as possible assisted triage, not proof of a fully automated decision.

### Human-craft audit

This mode audits the symptoms Apple can review: thin product depth, template provenance, reused assets, generic microcopy, missing interaction states, weak accessibility, and an interchangeable product page. It does not pretend to detect AI authorship. The goal is to make the app genuinely more specific and complete, not disguise a thin clone.

## What's covered

| Guideline family | Coverage |
|---|---|
| 2.1 | Crashes, placeholders, demo access, broken paths, network and iPad reviewability |
| 2.3 | Build-to-metadata accuracy, screenshots, keywords, age rating, and purchase claims |
| 3.1 | Digital purchase paths, paywall terms, StoreKit pricing, and restoration |
| 4.2 / 4.3 | Minimum functionality, templates, portfolio duplication, provenance, and distinct value |
| 5.1 | Purpose strings, privacy manifests, deletion, ATT, labels, and third-party AI consent |
| 1.2 | Filtering, reporting, blocking, contact details, moderation, and anonymous chat |

## How it stays current

[`references/research-prompt.md`](references/research-prompt.md) is a ready-to-run quarterly research prompt. It diffs official policy, separates closed cases from unresolved reports, and requires dates, URLs, exact wording when available, outcomes, and confidence labels. Pull requests with real rejection cases are welcome.

## Repository structure

```text
.
├── SKILL.md
├── references/
│   ├── evidence-policy.md
│   ├── frameworks.md
│   ├── guidelines-checklist.md
│   ├── human-craft-audit.md
│   ├── rejection-playbook.md
│   ├── report-contract.md
│   └── research-prompt.md
├── scripts/
│   ├── app_store_review_scan.py
│   └── tests/
├── skills/app-store-review/
├── evals/
├── agents/openai.yaml
├── .claude-plugin/
├── .codex-plugin/
├── CONTRIBUTING.md
└── LICENSE
```

## Credits

- [JustinPerea/app-store-review-skill](https://github.com/JustinPerea/app-store-review-skill) demonstrated precise Xcode target discovery, file-level evidence, false-positive guards, and eval-driven reports.
- [cruisediary/apple-app-review-skills](https://github.com/cruisediary/apple-app-review-skills) demonstrated focused routing across privacy, payments, metadata, layout, UGC, and project types.
- [github/awesome-copilot apple-appstore-reviewer](https://github.com/github/awesome-copilot/blob/main/skills/apple-appstore-reviewer/SKILL.md) demonstrated a disciplined report-first review with confidence, effort, and reviewer-experience sections.

## Disclaimer

This skill checks publicly available Apple guidance and clearly labeled community evidence. It cannot guarantee approval and is not affiliated with or endorsed by Apple Inc.

Licensed under the [MIT License](LICENSE).
