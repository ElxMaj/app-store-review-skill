# Quarterly App Review evidence refresh

Run this after each material App Review Guidelines update and at least quarterly. Replace `<LAST VERIFIED DATE>` with the current value from `references/evidence-policy.md`.

## Research prompt

Research Apple App Store review policy and enforcement changes since `<LAST VERIFIED DATE>` for iOS and iPadOS apps.

Use sources in this order:

1. Apple App Review Guidelines and Apple's change notices.
2. Apple Upcoming Requirements and App Store Connect Help.
3. Apple Developer Forums, separating Apple staff guidance from developer reports.
4. First-person developer accounts that include Apple's wording, the response or change, and the final outcome.
5. Secondary reporting only when it links to primary evidence or documents an otherwise unavailable enforcement action.

For official policy:

- Diff the current guideline text against the stored version dated `<LAST VERIFIED DATE>`.
- Record every changed clause, date, old meaning, new meaning, and direct URL.
- Recheck submission SDKs, privacy manifests, age ratings, purchase rules by storefront, and App Store Connect fields.
- Do not infer a new requirement from a product announcement or an unrelated Apple content-labeling program.

For rejection cases, search Apple Developer Forums, Reddit communities for iOS development, RevenueCat Community, Hacker News, and developer postmortems. Focus on:

- 2.1 completeness and review access
- 2.3 metadata
- 3.1 purchases and subscriptions
- 4.2 minimum functionality and templates
- 4.3(a) portfolio or similarity spam
- 4.3(b) indistinguishable or low-effort apps
- 4.8 login services
- 5.1 privacy, account deletion, tracking, and third-party AI consent
- 1.2 UGC and random or anonymous chat
- 2.5.2 downloaded or executed code

Capture each case as:

```text
Case ID:
Source date:
Source URL:
App category:
Technology stack:
Guideline:
Apple wording:
Submission timing:
Changes before each resubmission:
Reply or appeal strategy:
Final outcome:
Outcome date:
Causal change isolated: yes | no | unclear
Evidence confidence: OFFICIAL | DOCUMENTED CASE | OBSERVED PATTERN | INFERENCE
Limitations:
```

Investigate these questions without assuming their answers:

1. Are fast 4.3 decisions still being reported, and what evidence distinguishes automated triage from a short human-assisted review?
2. Which source, asset, portfolio, metadata, or concept similarities were actually identified?
3. Which recoveries isolate one change, and which changed several variables at once?
4. Are developers being asked to disclose AI-assisted development, or only data sharing with third-party AI?
5. Which saturated categories are named by Apple, and which are only community observations?
6. Have App Review Board, Meet with Apple, attachment, or expedited-review procedures changed?
7. Which existing checks now create false positives?

Deliver:

1. Official policy changelog with direct links.
2. Case table containing only reports with outcomes.
3. Open-evidence table for unresolved reports.
4. Proposed edits to this skill, each tied to a source and confidence label.
5. Proposed scanner checks only when the repository signal is deterministic enough to test.
6. Claims that should be removed or downgraded.

Quality rules:

- Preserve exact Apple wording only when the source exposes it.
- Never calculate a success rate without a defined denominator.
- Never treat one case as a general rule.
- Label timing-based automation claims as inference unless Apple confirms the mechanism.
- Check links and dates.
- Use plain, direct prose.
