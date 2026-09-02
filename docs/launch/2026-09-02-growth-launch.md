# App Store Review Skill Growth Launch

> Draft only. Do not publish without action-time approval.

## Objective

Reach the first 10 genuine GitHub stars by turning the repository's strongest proof into a clear product page, then sharing it in a small number of relevant channels. Optimize for qualified developers who may install, save, test, report a false positive, or return before their next submission.

## Verified baseline on September 2, 2026

| Signal | Baseline | Interpretation |
|---|---:|---|
| GitHub stars | 1 | Primary public save signal |
| GitHub traffic, latest 14 days | 6 views from 5 unique visitors | Very little qualified discovery |
| GitHub clones, latest 14 days | 49 clones from 31 unique cloners | May include registries or automation; not proof of human adoption |
| Skills.sh | 2 installs | Small but verified distribution signal |
| ClaudePluginHub | 1 copy click | Clear conversion gap on the listing |
| Tessl v1.2.1 | 97% quality, 98% impact | Independent evaluation proof, not an approval-rate claim |
| Tessl security | Low, W011 | The report flags local project-text reads during static analysis as third-party content exposure |

Thirty-day targets are 10 genuine GitHub stars, 50 GitHub unique visitors, 10 Skills.sh installs, 5 ClaudePluginHub copy clicks, and at least one substantive issue or false-positive report. These are operating targets, not forecasts.

The live registry-health script currently fails because it requires Tessl's security level to be `NONE`. Do not describe registry health as green while W011 remains. A classification-feedback action is listed below, but it needs separate approval.

## Publication gate

Before outreach:

1. Merge and deploy the new product page, guide, `/report/` route, sitemap, and `llms.txt`.
2. Check the deployed URLs, social preview, install command, and GitHub links.
3. Apply the proposed GitHub and ClaudePluginHub metadata only after the owner approves those external changes.
4. Capture one 1270 × 760 landing-page image for Product Hunt. Pair it with the existing report image. Product Hunt recommends a gallery with at least two assets.

This is a GitHub Pages project site. Its project-level `robots.txt` is available under `/app-store-review-skill/`, while crawlers request the origin-wide `https://elxmaj.github.io/robots.txt`. The origin-wide URL currently returns 404, which does not block crawling. Submit `https://elxmaj.github.io/app-store-review-skill/sitemap.xml` directly to Google Search Console and Bing Webmaster Tools after deployment.

## Channel decision table

| Priority | Channel | Current rule fit | Decision |
|---:|---|---|---|
| 1 | r/ClaudeCode weekly showcase | The current weekly thread welcomes tools and open-source projects; short promotion belongs in that thread. No spam or referral schemes. [Current thread](https://www.reddit.com/r/ClaudeCode/comments/1w3b38v/weekly_showcase_thread_what_are_you_building_with/) | Draft ready; publish in the thread after approval |
| 2 | Product Hunt | Requires a personal account, direct product URL, concise product fields, maker attribution, a 240 × 240 thumbnail, and gallery media. [Official posting guide](https://help.producthunt.com/en/articles/479557-how-to-post-a-product) | Package ready except final gallery capture; publish after approval |
| 3 | LinkedIn | Maker-owned profile, factual disclosure, no community self-promotion gate | Draft ready; publish after approval |
| 4 | X | Maker-owned profile, short demo-led post | Draft ready; publish after approval |
| Hold | One iOS developer community | Eligibility and current self-promotion rules must be checked from the signed-in account immediately before posting | No post until the rule and account gate are verified |
| Exclude | Show HN | Hacker News currently says not to post generated or AI-edited text. [HN guidelines](https://news.ycombinator.com/newsguidelines.html) | No AI-authored submission copy. The maker may write an original post independently |
| Defer | Awesome lists | High-fit lists ask for established community use; one prominent list requires at least 10 stars | Revisit only after the 10-star milestone |

## Channel-specific drafts

### r/ClaudeCode weekly showcase comment

Maker disclosure: I built an open-source App Store review skill for Claude Code and Codex after seeing how often a clean build still leaves review risk in privacy declarations, metadata, reviewer access, or a generic product experience.

It has three modes: a read-only pre-submission audit, rejection recovery that preserves Apple's exact message, and a human-craft pass for 4.2/4.3 risks. Findings separate confirmed evidence from warnings and manual checks, and the sample output is a full report rather than a chat summary.

Repo and install: https://github.com/ElxMaj/app-store-review-skill

I would value concrete false positives or missing checks from anyone shipping iOS, Expo, React Native, or Flutter apps.

### Product Hunt package

- **Name:** App Store Review Skill
- **Tagline:** Find App Review risks before Apple does
- **Product URL:** https://elxmaj.github.io/app-store-review-skill/
- **Description:** A read-only first pass for iOS and iPadOS projects. Audit before submission, investigate Apple rejections, and find template-like or unfinished product choices in Codex or Claude Code.
- **Topics:** Developer Tools, Artificial Intelligence, Open Source
- **Thumbnail:** A 240 × 240 crop based on the report's red rule and AS monogram
- **Gallery:** Product-page capture; sample report image; optional three-mode diagram

**Maker comment**

Hi, I’m Elie, the maker of App Store Review Skill.

I built it around a gap I kept seeing in release work: a project can compile and still be hard for App Review to assess. The missing pieces may live in privacy manifests, permission copy, purchases, account deletion, App Store metadata, reviewer access, or in a product that still looks too close to a template.

The skill starts read-only and keeps three evidence levels separate: confirmed findings, warnings, and manual checks. It also has a rejection-recovery mode that preserves Apple's message before suggesting whether to fix, clarify, appeal, or request interpretation.

The project is MIT licensed. I’m especially interested in false positives and framework-specific gaps from people shipping real iOS apps.

### LinkedIn post

An iOS build can be technically green and still be difficult for App Review.

The problem may be a missing privacy manifest, an inaccurate purpose string, a purchase path the reviewer cannot reach, metadata that no longer matches the binary, or a product that still feels like a lightly changed template.

I built App Store Review Skill to inspect those risks in Codex and Claude Code. The first pass is read-only. It supports pre-submission audits, rejection recovery, and a human-craft review for Guidelines 4.2 and 4.3.

Each finding separates confirmed evidence, warnings, and manual checks. There is no approval guarantee and no claim to detect AI-written code.

Open source, install command, and sample report:
https://elxmaj.github.io/app-store-review-skill/

If you work on iOS, Expo, React Native, or Flutter releases, I would welcome a concrete false positive or missing check.

### X post

I built an App Store review skill for Codex + Claude Code: pre-submission audits, rejection recovery, and a human-craft pass for 4.2/4.3. It starts read-only and shows evidence, not an approval promise. Open source + report: https://elxmaj.github.io/app-store-review-skill/

## Proposed discovery metadata

These are external mutations and remain pending owner approval.

### GitHub

- **Homepage:** `https://elxmaj.github.io/app-store-review-skill/`
- **Description:** `Read-only App Store submission audits, rejection recovery, and human-craft reviews for Codex and Claude Code.`
- **Topics:** keep `app-store-review`, `app-store-connect`, `apple-developer`, `claude-code`, `codex`, `developer-tools`, `ios`, `ipados`; add `ai-coding`, `expo`, `flutter`, `react-native`, `swiftui`

### ClaudePluginHub

- **Preferred category:** Developer Tools, if the listing taxonomy offers it; otherwise keep Utilities
- **Description:** `Audit iOS and iPadOS apps before submission, investigate App Review rejections, and find generic product risks. Read-only first pass with evidence-backed reports.`
- **Keywords:** `app store review`, `ios`, `ipados`, `rejection recovery`, `app store connect`, `swiftui`, `expo`, `react native`, `flutter`
- **After save:** request a listing resync, then verify the public version, category, description, install command, and copy-click counter

## Launch order

1. Deploy the product page and verify the public artifact.
2. Apply GitHub homepage, description, and topics.
3. Update and resync ClaudePluginHub.
4. Publish the r/ClaudeCode showcase comment.
5. Publish the LinkedIn and X posts several hours apart.
6. Prepare Product Hunt assets and launch on a day when the maker can answer comments.
7. Review results after 48 hours before using another community.

## Measurement

Record the baseline again immediately before the first post, then collect the same fields at 48 hours, 7 days, 14 days, and 30 days:

- GitHub stars, forks, unique visitors, top referrers, and popular content
- Skills.sh installs
- ClaudePluginHub copy clicks and listing signals
- Product Hunt visits, saves, comments, and referrals if launched
- Substantive GitHub issues, pull requests, and false-positive reports

GitHub traffic is a rolling 14-day window. Treat clone totals as ambiguous and do not present them as users or installs. Without site analytics, channel attribution comes from platform analytics, GitHub referrers, and timestamped before-and-after snapshots.

## Red line

No fake accounts, purchased stars, engagement rings, automated reactions, identical cross-post spam, hidden maker affiliation, fabricated approval rates, or Apple endorsement claims. Never publish from an account or change a public listing without action-time approval.

## Approval ledger

| Action | State |
|---|---|
| Merge and deploy repository changes | Pending review and action-time approval |
| Change GitHub homepage, description, or topics | Pending action-time approval |
| Change or resync ClaudePluginHub listing | Pending action-time approval |
| Send Tessl evidence about the W011 classification | Pending action-time approval |
| Submit the sitemap in search-engine dashboards | Pending action-time approval |
| Publish Reddit, Product Hunt, LinkedIn, or X copy | Pending action-time approval per final payload |
| Submit to another community or directory | Not authorized |
