# Visual report design

Read this before generating or reviewing the HTML report.

## Design direction

Build a calm editorial compliance dossier, not a SaaS dashboard and not a marketing landing page. The app name is the focal point. The verdict is prominent but not theatrical. Evidence must feel more important than decoration.

The visual language should feel at home beside Apple documentation:

- system typography with optical sizing
- strong hierarchy built from size, weight, leading, and spacing
- one semantic accent chosen by the verdict
- quiet neutral paper and precise rules
- generous space around major sections, tighter space within related evidence
- direct labels and predictable reading order
- light and dark appearances designed together

Do not copy App Store Connect or use Apple logos, product artwork, or proprietary interface chrome. The report is independent.

## Applying the Apple design skill

Use the `apple-design` principles as decisions, not decoration:

- Purpose: every element must help someone understand the release decision or act on evidence.
- Agency: proposed fixes remain clearly separated and require the developer's approval.
- Responsibility: never imply Apple endorsement, certainty, or an approval probability.
- Familiarity: use document conventions, stable section order, direct labels, and a visible contents list.
- Flexibility: work on phones, desktops, light mode, dark mode, increased contrast, and print.
- Simplicity: show the verdict and common reading path first without hiding necessary context.
- Craft: make spacing, tracking, rules, wrapping, and alignment deliberate at every width.
- Delight: aim for calm confidence. Do not add celebration, bounce, or ornament to a compliance report.

## Anti-slop rules

Do not use:

- a giant sentence such as "App is not ready" as a landing-page hero
- gradients, glowing backgrounds, glass panels, or decorative blur
- a row of floating KPI cards
- rounded cards around every section or finding
- pills for ordinary metadata
- shadows used to manufacture hierarchy
- multiple accent colors competing for attention
- generic headings such as "Evidence before opinion" or "Unlock the next step"
- centered body content, fake device frames, stock illustrations, or ornamental charts
- scroll reveals, staggered entrances, parallax, or motion with no functional purpose

If the page still looks polished after removing its color, the hierarchy is doing its job.

## Structure

Use this order:

1. report identity and policy date
2. app name, release verdict, and a short evidence-based summary
3. one ruled count ledger
4. report contents for wayfinding
5. scope and limitations
6. findings
7. manual checks and product-craft grades
8. rejection recovery, reviewer path, and App Review Notes when present
9. grouped fixes that still require approval
10. disclaimer and generation date

Keep scope and counts compact. Give findings the most space. Place evidence beside the reason, correction, and verification step.

## Typography

- Use `-apple-system`, `BlinkMacSystemFont`, and system fallbacks. Do not fetch fonts.
- Enable optical sizing and let the platform tune the system face.
- Use one sans-serif family plus a system monospace for paths and stable IDs.
- Tighten large display tracking and keep body tracking near zero.
- Use tight leading for the app name, comfortable leading for summaries, and denser leading for technical evidence.
- Use no more than two visible weights.
- Scale in `rem`, `em`, or `clamp()` so larger text does not break the layout.

## Color and material

- Use a warm neutral canvas and one paper surface. The page itself may be the only bounded surface.
- Select one verdict accent: red for `NOT READY`, amber for `NEEDS REVIEW`, green for `NO STATIC BLOCKERS FOUND`.
- Use the accent sparingly for the top rule, verdict, section coordinates, and confirmed blocker marks.
- Keep warnings, manual checks, and information understandable from text. Color is secondary.
- Avoid translucency in the static document. Apple-style materials communicate floating functional layers, and this report has none.
- Print on white with no shadows or background effects.

## Motion

The default report has no animation. It is a document people scan repeatedly, so motion would slow reading without explaining state.

If a future interactive control genuinely needs motion, load `apple-design` from `emilkowalski/skills` and follow its rules: respond immediately, animate from the current state, keep motion interruptible, preserve spatial consistency, and provide a reduced-motion equivalent. Animate only `transform` and `opacity` unless the interaction requires a different property.

## Accessibility

- Pair every status color with a written severity, grade, symbol, or verdict.
- Keep normal text contrast at least 4.5:1 and large text at least 3:1.
- Use semantic headings, navigation, lists, and landmarks in reading order.
- Do not hide material information in hover states.
- Support light mode, dark mode, increased contrast, and print.
- Escape every report string before inserting it into HTML.
- Keep the document usable at 390 px and 1440 px without horizontal scrolling.

## Three-pass build

Follow three focused passes instead of trying to decorate and structure the report at once:

1. Structure: order, hierarchy, reading path, and evidence grouping.
2. Type and color: system type scale, one accent, neutral palette, and rules.
3. Polish: wrapping, alignment, contrast, mobile reflow, dark mode, and print.

At the end of each pass, remove anything that does not help the reader understand the release decision.

## Content integrity

- JSON is canonical. Never infer or decorate missing values into facts.
- Do not add pass rates, risk percentages, approval odds, or invented test results.
- A scanner-only report is preliminary until each finding is reviewed and manual paths are executed.
- Keep evidence confidence visible for every finding.
- Preserve exact rejection wording separately from diagnosis and reply drafts.

## Verification checklist

- Open the HTML locally with networking disabled.
- Inspect at roughly 1440 px and 390 px in light and dark appearances.
- Check long paths, rejection text, empty sections, and zero counts.
- Confirm body and document scroll widths never exceed the viewport.
- Print to PDF and inspect page breaks.
- Confirm there are no script tags, remote styles, images, fonts, or tracking calls.
- Compare the result against the anti-slop list before approving the screenshot.

## Design sources

Verified 2026-07-17:

- Apple design skill: `https://github.com/emilkowalski/skills/tree/main/skills/apple-design`
- Emil design engineering skill: `https://github.com/emilkowalski/skills/tree/main/skills/emil-design-eng`
- Luke Web Design free premium workflow: `https://lukewebdesign.com/free-guide`
- Apple Human Interface Guidelines: `https://developer.apple.com/design/human-interface-guidelines`
- Apple accessibility guidance: `https://developer.apple.com/design/human-interface-guidelines/accessibility`
