# X campaign: App Store Review preflight

> Draft only. The planned cap is EUR 105, but authorized spend remains EUR 0 until the advertiser handle, funding source, dates, final preview, and exact payload are confirmed.

The JSON campaign file is the source of truth for every exact payload value.

## One idea

The campaign sells one job: find App Store Review risks before submission. Codex and Claude Code are delivery details on the landing page, not targeting themes or the lead message.

The copy assumes it will run from Elie's public, eligible maker account. If a company account is used instead, rewrite the first-person maker sentence and reapprove the complete payload.

The creative compresses the product into one visual story: a neutral blue checklist tile collides with a red warning symbol among privacy and purchase risks, with a green route forward. The single-object hierarchy is designed to remain recognizable in a fast mobile timeline.

## Ads Manager setup

| Field | Value |
|---|---|
| Objective | Website traffic |
| Ad-group goal | Link clicks |
| Payment | Link clicks |
| Bid | Autobid |
| Daily budget | EUR 15 |
| Duration | 7 days |
| Planned maximum | EUR 105 |
| Language | English |
| Locations | Australia, Canada, Germany, Ireland, Netherlands, New Zealand, United Kingdom, United States |
| Age | 18+ |
| Placements | Home timeline and search results |
| Optimized targeting | Off for the first controlled test |
| Audience expansion | Off for the first controlled test |
| X Pixel | Off; measure the bounded test with X link-click reporting and timestamped GitHub snapshots |

Use one ad group so the small budget is not fragmented. Launch all three creatives together; delivery is algorithmic, so compare normalized rates only after each has adequate exposure. Do not add broad AI, coding-assistant, startup, or generic developer interests.

## Creative 1 — pre-submission

**Post copy**

> A clean build can still hide App Store Review risks: privacy declarations, reviewer access, purchases, metadata, and product depth. I built a read-only, open-source preflight for iOS submissions. Independent and not affiliated with Apple.

**Card headline:** Find review risks before submission

**Destination:** `https://elxmaj.github.io/app-store-review-skill/?utm_source=x&utm_medium=paid_social&utm_campaign=app_store_review_preflight&utm_content=preflight`

## Creative 2 — rejection recovery

**Post copy**

> App Store Review rejection? Start with Apple’s exact message, then separate confirmed evidence from warnings and manual checks. I built an open-source recovery workflow for iOS teams. Independent and not affiliated with Apple.

**Card headline:** Turn a rejection into a clear next step

**Destination:** `https://elxmaj.github.io/app-store-review-skill/?utm_source=x&utm_medium=paid_social&utm_campaign=app_store_review_preflight&utm_content=rejection_recovery`

## Creative 3 — product depth

**Post copy**

> Guidelines 4.2 and 4.3 are product questions, not just build errors. I built an open-source App Store Review skill that checks template residue, product depth, metadata, and reviewer paths. Independent and not affiliated with Apple.

**Card headline:** Audit product depth before submission

**Destination:** `https://elxmaj.github.io/app-store-review-skill/?utm_source=x&utm_medium=paid_social&utm_campaign=app_store_review_preflight&utm_content=product_depth`

## Image and accessibility

- Asset: `/app-store-review-skill/assets/x-app-review-preflight-v3.png`
- Required size: 1200 x 628 PNG, under 5 MB
- Alt text: “3D App Store Review graphic reading ‘REJECTED? Find risks first,’ with a blue checklist tile colliding with a red warning symbol among privacy and purchase icons, leading toward a green check”
- Do not add Apple logos, App Store badges, device mockups, approval seals, fake testimonials, or claims that imply endorsement.

The final image is original 3D artwork. Its 3D scene uses the approved collision concept, while its title hierarchy follows the user-supplied typography reference: a widely tracked kicker, a large white condensed headline, a red light underline, and a widely tracked supporting line. It was checked at 600 x 314 feed size, then resized to the exact X card contract. The app tile is intentionally neutral and does not reproduce or alter Apple artwork.

## Included keywords

```text
App Store Review
App Review
App Review rejection
App Store rejection
App Store rejected
rejected by Apple
iOS app rejected
App Store submission
iOS submission
submit to App Store
App Store Connect
TestFlight review
App Review Guidelines
Guideline 4.3
Guideline 4.2
minimum functionality
privacy manifest
PrivacyInfo.xcprivacy
App Store metadata
App privacy details
App Review notes
reviewer access
demo account App Review
in app purchase review
subscription review
account deletion iOS
Sign in with Apple review
App Store screenshots
App Review appeal
Resolution Center
App Store rejection appeal
iOS release checklist
App Store release checklist
```

Exclude ambiguous review traffic: `book review`, `customer review`, `employee review`, `film review`, `game review`, `job review`, `movie review`, `performance review`, `restaurant review`, and `salary`.

## Decision rules

Record X spend, impressions, link clicks, click-through rate, and cost per link click by creative. At the same timestamps, record GitHub stars, unique visitors, referrers, Skills.sh installs, ClaudePluginHub copy clicks, and substantive questions or issues.

- At EUR 25: confirm the links, placements, and audience breakdown are behaving as intended. Make no optimization decision from impressions alone.
- At EUR 50: pause the campaign if it has fewer than 25 link clicks and no adoption signal. Otherwise, pause the weakest creative and let the remaining budget concentrate on the stronger message.
- At EUR 105 or day 7: call the test promising only if it produced at least 50 link clicks and three credible adoption signals. Treat stars and installs as correlated lift, not deterministic attribution.
- Seven days later: take one final snapshot to capture delayed stars, installs, and questions.

Clones are recorded for continuity but are not counted as users or installs. Likes and impressions are diagnostic signals, not campaign success.

## Final activation gate

Before spending or publishing, verify that the account is eligible for X Ads and show one final preview containing the advertiser handle, all three post bodies, image, alt text, locations, keyword list, placements, start and end time, funding source, daily budget, and EUR 105 total cap. Activation requires confirmation of that unchanged payload.

## Platform references

Verified September 3, 2026:

- [X Ads campaign objectives, bidding, budget, and creative rotation](https://business.x.com/en/help/campaign-setup/campaigns-101)
- [Website traffic campaign setup and link-click goal](https://business.x.com/en/help/campaign-setup/create-a-website-traffic-campaign)
- [Keyword targeting](https://business.x.com/en/help/campaign-setup/campaign-targeting/keyword-targeting)
- [Image-ad and website-card specifications](https://business.x.com/en/help/campaign-setup/creative-ad-specifications)
- [Advertiser account eligibility](https://business.x.com/en/help/ads-policies/campaign-considerations/about-eligibility-for-x-ads)
- [Website conversion tracking](https://business.x.com/en/help/campaign-measurement-and-analytics/conversion-tracking-for-websites)
