# From Alarm to Evidence landing-page design

> **Status note (2026-09-05):** The original dark evidence-gate composition was superseded after visual review by the campaign-poster implementation in `site/index.html` and `site/home.css`. The later user-approved journey distillation keeps the complete HTML report as the sole visible report route; the source JSON remains published and is linked from the README instead of adding another landing-page action. Its product-truth, accessibility, route, and publication constraints still apply. Shipped font provenance lives in `site/assets/fonts/README.md`.

**Date:** 2026-09-05

**Status:** Implemented; final campaign-poster overrides are documented in the status note above

**Surface:** GitHub Pages product landing page

**Mode:** Persuade

**Implementation base:** `origin/main` at `e4c78ff2e9ee263d252bf86c318634ef3c76a4f1`

**Selected direction:** From Alarm to Evidence

## Summary

The campaign ad creates urgency with the line “Rejected? Find risks first.” The landing page must complete that thought instead of replaying the ad. It turns the alarm into a controlled, evidence-backed path: inspect the project, see the source of each risk, and run a read-only preflight before submission.

The page will be recomposed around one memorable transition: repository evidence passes through a red review gate and resolves into the real, inspectable sample report. The CGI gate remains as a campaign echo and atmospheric rear plane. The report, source paths, verification steps, and install command become the protagonists.

The primary conversion is installing and running the preflight. Opening the sample report is secondary. Starring the repository is tertiary and never competes with the install path in the hero.

## Why this direction

The current page becomes authored and credible after its first viewport, but its opening can be mistaken for a generic AI security product. It relies on familiar category cues: a dark two-column hero, luminous CGI, terminal styling, glow fields, a proof-metric strip, and a dominant “Star on GitHub” button. On mobile, those pieces stack into a long introduction before the report or install path appears.

The redesign keeps the ad’s useful emotional grammar—black space, electric blue evidence, red risk, and a small green release signal—but assigns every color and visual effect a job. It removes decorative proof theater and makes the visitor’s next action obvious.

## Product truth and claim boundary

The page may claim only what the repository and current public evidence support:

- The skill supports Codex and Claude Code.
- It recognizes Xcode, Expo, React Native, and Flutter projects.
- Its first pass is read-only and changes zero project files.
- It supports pre-submission audit, rejection recovery, and human-craft audit modes.
- It produces a report that separates confirmed findings, manual checks, and unknowns.
- The ParcelTrack example is fictional and contains no private project data.
- Apple makes the review decision; the skill cannot guarantee approval.
- The project is independent and is not affiliated with or endorsed by Apple Inc.

Tessl scores, security status, version numbers, policy dates, and other volatile proof must come from a checked-in value that has been verified for the release. They must include provider, version, observation date, and scope. If current evidence cannot be verified, omit the value rather than displaying a stale or context-free number.

The page must not claim an approval rate, knowledge of Apple’s internal review process, detection of AI-written code, automatic review certainty, or official Apple affiliation.

## Goals

1. Make a visitor arriving from the ad understand the product and the next action within five seconds.
2. Make the real report and its evidence contract more visually important than decorative CGI.
3. Turn install/preflight into the single primary conversion path.
4. Build a distinctive visual system from the product’s actual mechanism: evidence crossing a review gate.
5. Preserve the project’s rigorous claim discipline, accessibility, static architecture, and GitHub Pages reliability.
6. Recompose the mobile experience rather than stacking a desktop layout.

## Non-goals

- Changing the skill’s behavior, scanner, report schema, or review methodology.
- Redesigning the generated report itself. The landing page must use the currently shipped report as truth unless a separate report redesign is approved and merged.
- Adding a JavaScript framework, build system, analytics provider, account integration, or runtime dependency.
- Adding Apple logos, App Store badges, proprietary Apple interface chrome, or visual treatment that implies endorsement.
- Publishing, deploying, merging, buying a commercial font, or activating advertising as part of this design phase.
- Copying COLLINS layouts, identities, typography, or motion. The reference is a standard of authorship and narrative coherence, not a template.

## Audience and decision

The primary visitor is an iOS maker or product team using an AI coding agent. They may be preparing a first submission, responding to a rejection, or worrying that a technically working app still feels unfinished.

Their decision is simple: “Is this credible and useful enough to run in my repository?” The page therefore needs to answer, in order:

1. What does it do?
2. What will it inspect?
3. What will I get?
4. Can I verify the result?
5. How do I run it?
6. What does it not promise or change?

## Core proposition and voice

### Hero copy

**Headline**

> Find the risk.<br>
> Prove the fix.

**Supporting line**

> A read-only preflight that traces App Store review risks to the files, rules, and checks behind them.

**Primary action**

> Run the preflight

The primary action scrolls to the install section. The install command remains visible in the first viewport so a returning visitor can copy it immediately. The button must not imply that the site itself executes code.

**Secondary action**

> Inspect the sample report

**First-viewport reassurance**

> First pass: read-only · Xcode, Expo, React Native, and Flutter

### Voice rules

- Write short, concrete sentences in plain language.
- Prefer verbs such as inspect, trace, verify, run, and prove.
- Keep evidence, inference, manual checks, and unknowns distinct.
- Avoid generic claims such as “AI-powered,” “next generation,” “supercharge,” “seamless,” “world-class,” or “revolutionary.”
- Avoid slogans about founders, magic, certainty, or guaranteed acceptance.
- Use sentence case. Tracked uppercase is reserved for literal report statuses or compact metadata, not section decoration.
- No emoji, faux quotes, fabricated testimonials, or invented usage counts.

## Narrative architecture

The page follows one continuous sequence. Each section resolves the question raised by the previous one.

| Act | Visitor question | Content | Dominant visual |
| --- | --- | --- | --- |
| Alarm + transformation | “What catches the risk before Apple does?” | Proposition, install command, gate transformation | Evidence fragment crossing the CGI gate into a report sheet |
| Proof | “What do I actually receive?” | Real ParcelTrack report, verdict, source JSON | Large report crop on warm paper |
| Method | “Can I trust the reasoning?” | What / where / why / how-to-verify contract | One continuous evidence trace, not four cards |
| Action | “How do I use it?” | Recommended install, prompt, alternate methods | Command rail with one dominant copy action |
| Reassurance | “Will it fit my situation, and what are its limits?” | Three modes, independently scoped evaluation, policy guide, FAQ | Editorial sequence with restrained diagrams and rules |
| Close | “What should I do now?” | Final command, read-only reminder, disclosure | Quiet high-contrast closing field |

## Page composition

### 1. Header

The header contains the original review-gate mark, the product name, and three destinations: Report, Install, and GitHub. Install is the visually emphasized navigation action. GitHub remains a text link with an external-link indicator; no star count or star button appears in the header.

On narrow screens, retain the product mark/name, Install, and GitHub. Report remains reachable through the hero’s secondary action. The header must not hide every internal route.

### 2. Hero: alarm becomes evidence

The hero is a full-bleed stage rather than a text card beside an image card. Its composition has three depth planes:

1. **Rear plane — alarm:** a tightly cropped, responsive derivative of the existing review-gate CGI. The red gate is recognizable, but the image never carries the message by itself.
2. **Middle plane — evidence path:** a blue repository-evidence strip grounded in the fictional ParcelTrack sample: `app.json:18`, followed by the missing `NSCameraUsageDescription` signal, a red risk checkpoint, and a green verification marker. Every state includes a text or shape cue so meaning does not depend on color.
3. **Front plane — proof:** a warm-paper crop from the actual ParcelTrack report, including the visible “NOT READY” verdict and “Camera flow has no purpose string” finding. It overlaps the gate and visually resolves the transition.

The headline occupies the left/top of the stage and is allowed to break the conventional column grid. The command dock sits directly below the proposition and remains visible at 1440×900 and 390×844. The page does not place Tessl scores, security badges, or a four-item metric rail in the hero.

The first viewport should be remembered as “evidence crossing a gate and becoming a report,” not as “a glowing cyber image.”

### 3. Proof: the report is the product artifact

The next section moves from night to report paper without a card container. The real ParcelTrack report occupies at least half the desktop viewport width and becomes the largest body visual. Use a sharply legible crop rather than shrinking an entire long page into a thumbnail.

Adjacent copy states:

- the release verdict;
- the distinction between blockers and manual checks;
- that the report arrives before proposed fixes;
- that its evidence is fictional sample data;
- links to the complete HTML report; the source JSON remains published and discoverable from the README rather than adding another landing-page action.

The report image is not treated as decorative. It needs descriptive alt text, explicit dimensions, and a direct link to the accessible HTML report.

### 4. Method: every claim has a return address

Keep the useful evidence contract, but render it as a single trace running from finding to verification:

1. What was found.
2. Where it lives.
3. Why it matters.
4. How to prove the fix.

The four steps share a continuous rule or path. They must not become four equal rounded cards. Use the existing fictional camera finding throughout: the camera permission request in `src/features/scan/LabelScanner.tsx:42`; the missing purpose string in `app.json:18`; the published Guideline 5.1.1(ii) relevance; and the instruction to build the release archive, inspect the merged `Info.plist`, and retest the label scanner on a clean device. This section demonstrates the method instead of only describing it.

### 5. Action: install and run

This section follows proof and method immediately. The Skills CLI route is dominant:

```text
npx skills add ElxMaj/app-store-review-skill
```

The copy control is at least 44×44 CSS pixels, announces success without relying on color, and degrades to selectable text if the Clipboard API is unavailable.

The next line supplies the first prompt:

> Audit this iOS app before submission. Report first and do not edit files.

Tessl and Claude Code remain available as quieter alternate routes under “Other install methods.” They do not receive equal visual weight. A link to `INSTALL.md` covers all supported methods.

### 6. Reassurance

#### Review modes

Present the three modes as positions along one release journey rather than three product cards:

- Before upload — pre-submission audit.
- After rejection — rejection recovery.
- Before it feels done — human-craft audit.

Each mode includes one sentence about the evidence produced. Numbering is valid here because the visual is an ordered journey, not arbitrary decoration.

#### Independent evaluation

Replace the hero metric strip with a smaller, self-contained evidence note. Every displayed evaluation includes:

- provider name and destination link;
- evaluated skill version;
- date observed;
- score label and value exactly as provided;
- a one-sentence scope or limitation.

“Security scan passed” may appear only if the current provider result and finding scope support that exact phrase. A score must never be presented as an approval-rate claim.

#### Policy guide and FAQ

Keep the source-based AI-built-app guide and the three existing limits:

- no guaranteed App Store approval;
- no AI-code detector claim;
- no edits on the first pass.

The policy guide is supporting content, not an interruption between the report and install path.

### 7. Closing field

End on the primary install command, one direct sentence, and the independence disclosure. Do not introduce a new CTA, testimonial, badge row, or feature list at the close.

Proposed closing sentence:

> See the evidence before the reviewer sees the gap.

## Visual system

### Color

The palette is inherited from the ad but made semantic:

| Token | Value | Meaning |
| --- | --- | --- |
| Night | `#070A10` | Alarm field and closing field |
| Ink | `#111318` | Primary text on paper |
| Report paper | `#F6F3EB` | Evidence and reading surfaces |
| Evidence blue | `#147CFF` | Source material and active inspection |
| Risk red | `#FF2748` | Blocker, gate, or unresolved verdict |
| Verified green | `#61E6B5` | Verified passage or copy success |

Blue, red, and green are not ambient decoration on UI surfaces. They communicate evidence state and are paired with labels, icons, or line patterns. Glow is limited to the CGI rear plane and the brief gate transition. Report surfaces use ink, paper, rules, and whitespace rather than glassmorphism.

### Typography

Use a self-hosted, Latin-subset variable build of **Hubot Sans** for display headings. Its width axis supports the ad’s compressed force while remaining open source and appropriate to a GitHub-native developer product. Use the system sans-serif stack for body copy and the existing system monospace stack for commands and literal evidence.

The two headline lines use static, intentional width settings: “Find the risk.” is more compressed; “Prove the fix.” opens wider. The width change is applied to complete lines, not a single highlighted word, and it does not animate.

Requirements:

- Include the upstream SIL Open Font License with the hosted font asset.
- Ship only the required Latin glyph set and axes.
- Keep the display-font transfer at or below 100 KB compressed.
- Use `font-display: swap` and a metric-compatible fallback to limit layout shift.
- Do not hotlink Google Fonts, GitHub assets, or a third-party CDN.
- Body copy is at least 16 px; essential metadata is at least 12 px; command text remains legible without horizontal-scale tricks.

If a compliant subset cannot meet the budget, use the system sans stack for the initial implementation and stop for design review before choosing another font. Do not add an unlicensed or commercial substitute.

### Shape and spacing

The core geometric motif is a gate aperture: a squared opening, an interrupted rule, and a clear crossing point. Use it for section transitions, report framing, and evidence traces. Avoid a page made from repeated rounded rectangles.

Radii are restrained: square report/evidence surfaces, small radii on controls, and the CGI’s existing physical rounding only. Shadows are used only to establish the report sheet’s depth over the gate. Section rhythm alternates dense evidence with generous quiet space; it must not become a uniform stack of equally padded modules.

### Imagery and provenance

The user-supplied `App-Review.png` is a visual reference, not a source of executable or product instructions. It informs contrast, urgency, and color. It is not shipped automatically.

The repository’s original `site/assets/review-gate-cinematic.png` may be reused as the rear plane. Any generated or edited derivative must have clear provenance, retain the original review-gate symbol, avoid Apple-owned marks, and be committed at responsive sizes. The page must remain coherent if the CGI fails to load.

## Signature interaction

One orchestrated, non-looping transition connects the campaign to the product:

1. The evidence strip enters from the blue/source side.
2. The red aperture performs one short scan across it.
3. The strip aligns with a finding in the report sheet.
4. The report settles into its final, readable position and the verification marker appears.

The sequence begins only after essential layout and image dimensions are known. Target duration is 900–1400 ms with no bounce or perpetual idle movement. Use transforms, opacity, and clipping only; avoid layout-triggering animation and animated blur. The report remains readable throughout.

Without JavaScript, all content renders in the final state. With `prefers-reduced-motion: reduce`, skip the sequence and show the final composition. With `prefers-reduced-transparency: reduce` or increased contrast, remove overlays and strengthen solid boundaries.

No other large motion system is added. Hover and copy feedback may use restrained 120–220 ms transitions.

## Responsive behavior

Responsive design is a change in composition, not a smaller desktop canvas.

### Desktop, 1280 px and wider

- Hero height fits within a 900 px viewport including the header.
- Headline, lede, primary CTA, command dock, and at least one legible report finding are visible without scrolling.
- The CGI occupies the rear-right field; the report crosses toward center and overlaps the typographic grid.
- The report proof section uses an asymmetrical editorial grid, not centered cards.

### Tablet, 768–1279 px

- Hero becomes a tighter overlap: copy above/left, gate crop behind/right, report sheet spanning the lower stage.
- Keep the command dock and secondary report link visible before the section transition.
- Preserve the continuous evidence trace; it may turn once but must remain ordered.

### Mobile, 320–767 px

- Hero is rebuilt as a compact poster: headline, lede, command, and a cropped gate-to-report composite within the first 844 px at 390 px width.
- Do not load the 1536×1024 PNG as the only source. Serve a purpose-cropped AVIF/WebP mobile derivative with a PNG fallback.
- The CGI is subordinate and may be partially hidden; the report verdict and one evidence row remain legible.
- Primary controls are full-width or comfortably thumb-sized. Minimum target size is 44×44 CSS pixels.
- Navigation retains Install and GitHub.
- Commands may scroll inside a labeled code region, but the page itself must have no horizontal overflow at 320 px.

## Accessibility requirements

- One descriptive `h1`; semantic `h2` section hierarchy; landmarks and skip link retained.
- Keyboard focus is visible against both night and paper surfaces.
- The hero transformation is decorative duplication and is hidden from assistive technology; equivalent product meaning is present in text.
- The linked report crop has useful alt text and an accessible HTML destination.
- Statuses never rely on color alone.
- Text and essential UI meet WCAG 2.2 AA contrast.
- Controls meet a 44×44 CSS-pixel target unless an inline text-link exception is justified.
- Copy success is exposed as a polite live-region message, not only a color change.
- At 200% zoom, reading order and controls remain usable without two-dimensional scrolling.
- Reduced motion, reduced transparency, high contrast, and forced-colors states receive explicit verification.

## Performance budget

The production page remains static HTML, CSS, and vanilla JavaScript.

| Resource | Budget |
| --- | --- |
| Critical HTML + CSS + JS, transferred | ≤ 120 KB excluding fonts and images |
| Display font, transferred | ≤ 100 KB |
| Mobile hero imagery, transferred | ≤ 450 KB total |
| Desktop hero imagery, transferred | ≤ 900 KB total |
| Initial JavaScript, minified | ≤ 12 KB |

Additional requirements:

- Use explicit image width and height or `aspect-ratio` to prevent layout shift.
- Use AVIF/WebP sources with a PNG fallback where browser support requires it.
- Preload only the true LCP image and the display font if measurement supports it.
- Lazy-load below-fold imagery.
- No autoplay video, canvas particle field, WebGL, scroll-polling loop, or third-party script.
- Target Lighthouse mobile scores of at least 95 for Performance, Accessibility, Best Practices, and SEO under the project’s reproducible test conditions.
- Target LCP ≤ 2.5 s, CLS ≤ 0.05, and INP ≤ 200 ms in the same controlled run. These are acceptance targets, not public product claims.

## Metadata and discovery

Update page title, description, Open Graph copy, Twitter copy, image alt text, and visible `h1` together so they describe the same proposition. Preserve canonical URL, crawl files, JSON-LD types, version sourcing, guide URL, and report URL.

Proposed metadata:

- **Title:** `App Store Review Skill — Find the risk. Prove the fix.`
- **Description:** `Run a read-only App Store review preflight in Codex or Claude Code. Trace iOS submission risks to project evidence, published guidance, and verification steps.`
- **Social headline:** `Find the risk. Prove the fix.`
- **Social supporting line:** `A read-only App Store review preflight for Codex and Claude Code.`

The social card should echo the landing composition at 1200×630, with the report artifact more prominent than the CGI. It must not imply Apple endorsement.

## Implementation boundaries

The later implementation is expected to modify:

- `site/index.html`
- `site/styles.css`
- `site/site.js`
- `scripts/tests/test_pages_site.py`
- responsive assets under `site/assets/`
- font and license files under `site/assets/fonts/`
- `site/assets/review-gate-social.png` if the social composition changes

The Pages workflow already publishes the sample report and copies `assets/visual-report-example.png` into the built site. Do not duplicate that source asset under `site/assets/` unless the workflow contract is intentionally changed and tested.

README art, the generated report, skill packages, manifests, versions, registry publishing, and launch campaign files are outside scope unless implementation reveals a direct broken reference. Any such expansion requires a separate decision.

## Implementation approach

1. Add or update page-contract tests first so they fail on the old hierarchy and pass only with the approved narrative, command priority, truth labels, assets, and accessibility hooks.
2. Build the semantic HTML in static final-state order.
3. Establish typography, color, and responsive composition in CSS without motion.
4. Produce and optimize responsive image/font assets with licenses and provenance.
5. Add the single progressive-enhancement transition and copy feedback.
6. Verify content truth, keyboard behavior, responsive layouts, reduced modes, asset budgets, and real browser output.
7. Run the deterministic anti-slop detector once on the final candidate, then conduct independent desktop/mobile visual critique.

## Verification matrix

### Automated

- `python3 -m unittest discover -s scripts/tests -p 'test_pages_site.py' -v`
- `python3 -m unittest discover -s scripts/tests -v`
- `python3 scripts/app_store_review_scan.py . --format json | python3 -m json.tool >/dev/null`
- `git diff --check`
- Validate all local links and published asset paths in the built `_site` artifact.
- Assert no horizontal overflow at the target viewport widths.
- Assert motion/transparency/contrast media queries, live-region feedback, heading hierarchy, and required claim/disclosure text.
- Measure transferred asset sizes against the budgets above.

### Browser and visual

Capture and inspect the complete page at:

- 1440×900
- 1280×800
- 768×1024
- 390×844
- 320×568

For each relevant viewport, verify:

- first meaningful action and report evidence placement;
- no horizontal overflow or clipped focus rings;
- readable command and report crop;
- correct source order with CSS disabled;
- keyboard-only flow and copy fallback;
- 200% zoom;
- reduced motion, reduced transparency, increased contrast, and forced colors;
- slow-network behavior and image fallback;
- final-state rendering with JavaScript disabled.

Run Lighthouse mobile under recorded, repeatable conditions. Record the environment and measurements rather than reporting an unexplained score.

### Independent review

The final candidate receives two independent reviews:

1. A design critique asking whether the page has a specific authorship, a coherent ad-to-page handoff, and an obvious conversion path.
2. A skeptical detector review looking for generic AI/security tropes, repetitive card grids, unsupported proof, mobile stacking, decorative glow, and accessibility regressions.

Actionable findings are fixed and the affected checks rerun before completion is claimed.

## Acceptance criteria

The redesign is accepted when all of the following are true:

- A first-time visitor can state what the skill does and how to try it from the first viewport.
- “Run the preflight” is the only dominant CTA; the install command is directly accessible; GitHub is tertiary.
- The hero visibly transforms evidence into the actual report and does not read as a generic cybersecurity or AI-tool landing page.
- The report is the largest body proof and appears before modes, policy content, or general reassurance.
- The order is Alarm/Transformation → Proof → Method → Action → Reassurance → Close.
- The current ParcelTrack example is clearly labeled fictional and links to the complete HTML report; its source JSON remains published and linked from the README.
- Any evaluation score includes provider, version, observation date, and scope, or is omitted.
- No Apple-owned mark, affiliation implication, guaranteed-approval claim, invented user proof, or unsupported metric is introduced.
- The 390×844 composition includes the proposition, command/action, and meaningful report evidence without horizontal page overflow.
- The page works in its final state without JavaScript and respects every specified accessibility preference.
- Asset and performance budgets pass in the built output.
- Existing site, discovery, report-publication, and full Python test contracts pass after intentional copy assertions are updated.
- Independent critiques have no unresolved high-severity finding.

## Failure and rollback rules

- If the signature transition harms readability, accessibility, or performance, ship the same composition in its static final state.
- If the CGI prevents the mobile budget from passing, reduce or remove it on mobile before reducing report legibility.
- If a volatile proof cannot be tied to a current provider/version/date/scope, remove it.
- If font licensing or subsetting cannot be verified, stop and use the system stack pending review.
- If the redesign breaks report or guide routes, do not merge.
- The implementation stays on an isolated `codex/` branch. Reverting the page commit restores the current `e4c78ff` design; publication and merge remain explicit follow-up actions.

## Source and reference notes

- Campaign reference supplied by the user: `App-Review.png` (off-repository visual reference; not shipped).
- Existing original gate art: `site/assets/review-gate-cinematic.png`.
- Existing report proof: `assets/visual-report-example.png`, `examples/parceltrack-report.html`, and `examples/parceltrack-report.json`.
- Hubot Sans source and SIL OFL license: <https://github.com/github/hubot-sans>.
- COLLINS “101 Design Rules” reference for coherent, opinionated design practice: <https://wearecollins.com/story/101-design-rules/>.

These references inform the standard and constraints. The shipped identity remains original to App Store Review Skill.
