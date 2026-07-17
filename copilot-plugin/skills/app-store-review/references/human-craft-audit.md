# Human-craft audit

Use this audit for Guideline 4.3(b), low-effort concerns, template similarity, or a product that feels generic. The goal is to make the app genuinely more specific, useful, and complete. It is not an AI detector or camouflage guide.

## Core position

`OFFICIAL`: Apple does not publish a rule rejecting apps because AI helped write them. Apple reviews the submitted product under rules covering completeness, minimum functionality, templates, spam, dynamic code, privacy, metadata, and other observable behavior.

`OFFICIAL`: The June 8, 2026 wording of 4.3(b) rejects new submissions in mature categories unless they provide a meaningfully different or improved experience, and describes some low-effort categories as adding no value.

Audit the symptoms. Do not label an app AI-generated from visual style, code style, or copy.

When only a product description is supplied, complete the audit instead of stopping for files. Grade claims supported by that description conservatively, grade every screen, provenance, accessibility, and product-page dimension without evidence as `UNVERIFIED`, and make each intervention conditional on the missing evidence it addresses.

## Evidence grades

Grade every dimension:

- `DISTINCT`: specific, coherent evidence makes the product hard to confuse with a generic category entry.
- `CREDIBLE`: complete and intentional, with some generic surfaces that do not erase the product's value.
- `GENERIC`: several important surfaces could belong to many apps and do not make the product's specific value legible.
- `HIGH RISK`: confirmed thinness, duplication, template provenance, or incomplete execution directly supports a 4.2 or 4.3 concern.
- `UNVERIFIED`: the required build, screens, metadata, or provenance was not supplied.

Grades summarize inspected evidence. They are not approval probabilities.

## 1. Product distinction

Inspect:

- one-sentence purpose
- specific user and job
- first useful outcome
- core loop and repeat value
- capability that requires domain knowledge
- differentiation from sibling apps and obvious category comparators

`DISTINCT` evidence:

- The app solves a narrow problem with a workflow or insight that generic competitors do not provide.
- Distinction appears in the first session and does not depend on marketing copy.
- Product depth exists in data handling, interaction, offline behavior, integrations, or domain logic.

`GENERIC` or `HIGH RISK` evidence:

- The pitch is only "AI for X", "a better timer", "all-in-one", or another category label.
- The app wraps one API call or website without meaningful mobile value.
- Most navigation leads to static, placeholder, or paywalled screens.
- Differentiation consists only of colors, layout, or a renamed template.

Ask: what can this app demonstrate in three minutes that a thin clone cannot?

## 2. Binary and asset provenance

Inspect:

- starter kits, commercial templates, generators, and upstream repositories
- inherited module names, namespaces, copyright headers, and package URLs
- icon, illustration, sound, Lottie, and launch assets
- reuse across the developer's portfolio or prior rejected builds
- assistant files or internal notes included in the archive
- framework-common code versus app-specific behavior

Evidence rules:

- Template provenance is a policy issue under 4.2.6 only when the facts match the guideline.
- Exact asset reuse is reportable evidence. It does not prove Apple's internal matching method.
- A framework such as Flutter, React Native, Capacitor, Godot, or Unity is not a defect.
- `DOCUMENTED CASE`: an icon change was decisive in one published 4.3 recovery. Use it to justify comparison, not an icon-change ritual.

Under-a-day improvements:

- remove shipped internal artifacts
- replace genuinely reused primary assets
- clean inherited names that misstate ownership
- document licenses and transformation
- trim unused dependencies and sample resources

Do not recommend code obfuscation.

## 3. Visual identity and accessibility

Inspect screenshots or run the app. Do not grade from source filenames alone.

### Icon

- recognizable at small size
- distinct silhouette and purpose
- no unreadable generated lettering or irrelevant stock symbol
- works in the supported appearance modes

### Typography and hierarchy

- consistent text roles and labels
- Dynamic Type without clipping
- custom typography, if used, serves a deliberate role
- one primary action per state

### Color and materials

- semantic palette and sufficient contrast
- translucency and materials preserve hierarchy
- Reduce Transparency is respected where relevant
- state is not communicated by color alone

### Motion and haptics

- feedback marks meaningful state changes
- motion explains hierarchy or progress
- Reduce Motion is respected
- haptics are not attached indiscriminately to every tap

### iPad execution

- layout uses the available space intentionally
- popovers, sheets, keyboard, rotation, split views, and pointer interactions behave coherently
- the app does not look like a stretched phone screen unless the product justifies it

Evidence of craft is coherence, not decoration. Native controls can be distinctive when the product's content, hierarchy, and interaction are specific.

## 4. Microcopy and interaction states

Inspect every primary flow for:

- onboarding
- permission explanation
- empty state
- loading state
- error and recovery
- destructive confirmation
- purchase and trial terms
- account deletion
- success feedback

Flag:

- "Welcome to MyApp"
- "No data"
- "Something went wrong. Please try again."
- "Unlock the power of"
- "Manage your X"
- mixed tone from screen to screen
- permissions that repeat the system prompt without explaining the feature
- error messages with no next action

Rewrite formula:

1. name the object or problem
2. state the consequence or benefit
3. give the next action

Examples:

| Generic | Specific |
|---|---|
| No data | No shipments yet. Add one to start tracking delivery changes. |
| Something went wrong | The receipt could not be verified. Check your connection, then try Restore Purchases. |
| Camera access needed | Scan a shipping label to fill in the tracking number automatically. |
| Manage your documents | Turn case files into a searchable timeline. |

Specific copy must describe a feature that exists.

## 5. App Store product page

Inspect:

- name and subtitle
- first description sentence
- audience and core outcome
- screenshot sequence and captions
- keywords and categories
- privacy, support, and terms pages
- What's New history

`DISTINCT` evidence:

- The first sentence names a specific outcome and audience.
- Screenshots show real flows in a clear order.
- Each caption states a concrete benefit visible in the frame.
- Claims are supported by the build.
- The support page has a working contact and product-specific help.

`GENERIC` or `HIGH RISK` evidence:

- The copy could describe hundreds of apps.
- The name is a keyword chain.
- Screenshots are mostly marketing art or show UI absent from the build.
- Description and screenshots lead with a saturated category rather than distinct value.
- Repeated What's New entries say only "bug fixes and improvements."

## Output

```text
# Human-craft audit: <app>

Product distinction: <GRADE>
Provenance: <GRADE>
Visual identity: <GRADE>
Microcopy and states: <GRADE>
Product page: <GRADE>

## Why these grades
<path, screen, metadata, or supplied evidence for each>

## Top five interventions
1. <intervention>
   Evidence: <location>
   Why it matters: <specific 4.2, 4.3, completeness, or reviewer-legibility reason>
   Effort: <S | M | L>
   Verify: <observable outcome>

## Unverified surfaces
<screens, archive, metadata, provenance, or comparisons still needed>
```

If product distinction is `HIGH RISK`, lead with the product change required. Do not bury it beneath icon, color, copy, or animation suggestions.
