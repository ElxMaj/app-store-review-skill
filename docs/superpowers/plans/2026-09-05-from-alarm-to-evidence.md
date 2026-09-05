# From Alarm to Evidence Landing Page Implementation Plan

> **Status note (2026-09-05):** The landing-page composition and typography in this plan were superseded after visual review by the campaign-poster refactor in `site/index.html` and `site/home.css`. `site/assets/fonts/README.md` is the canonical, reproducible record for the fonts that now ship. The product-truth, accessibility, route, and publication gates below remain active; this document is retained as the historical implementation plan for the previous composition.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recompose the App Store Review Skill landing page so an ad visitor moves from rejection anxiety to a credible, report-backed install action in the first viewport.

**Architecture:** Keep GitHub Pages static and dependency-free at runtime. Split shared/guide CSS from landing-only CSS, render the gate-to-report sequence as semantic HTML plus one decorative responsive CGI plate, keep the real ParcelTrack report as the main proof, and progressively enhance copy feedback and a single non-looping intro transition.

**Tech Stack:** Static HTML5, CSS custom properties and media queries, vanilla JavaScript, Python 3.11 `unittest`, Hubot Sans variable WOFF2, AVIF/WebP assets, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-05-from-alarm-to-evidence-design.md`

## Global Constraints

- Preserve the narrative order exactly: Alarm/Transformation → Proof → Method → Action → Reassurance → Close.
- Use exactly one dominant CTA, “Run the preflight,” linking to `#install`; keep the sample report secondary and GitHub tertiary.
- Use the exact hero headline “Find the risk. Prove the fix.” and the approved 159-character metadata description from the spec.
- Preserve the canonical URL, report route, policy-guide route, JSON-LD types, FAQ truth, and version `1.2.2` unless source manifests change first.
- Keep the first pass described as read-only; never claim guaranteed approval, an approval rate, AI-code detection, Apple affiliation, or Apple-internal review knowledge.
- Do not introduce Apple-owned logos, badges, interface chrome, fabricated testimonials, or invented usage metrics.
- Display Tessl evidence as `97% quality`, `99% impact`, `v1.2.2`, and `Last scored 3 September 2026`; state that this evaluates the skill package and is not an App Store approval rate. These values were read from the v1.2.2 API response on 2026-09-05, whose `scores.lastScoredAt` is `2026-09-03T14:45:15.705Z`.
- Use `#070A10`, `#111318`, `#F6F3EB`, `#147CFF`, `#FF2748`, and `#61E6B5` for night, ink, report paper, evidence, risk, and verification respectively.
- Blue, red, and green must carry semantic state and have a non-color label or shape cue; glow stays inside the CGI plate and one gate scan.
- Use self-hosted Hubot Sans only for display; system sans for body; system monospace for commands and literal evidence.
- Use no eyebrow/kicker labels above headings. The approved ad-handoff `h1` is the only display size allowed above 6rem; keep its tracking at the `-0.04em` floor and keep every body heading at or below 6rem.
- Keep runtime dependencies at zero. Pinned `uvx` and `npx` tooling is allowed only to produce committed assets.
- Keep compressed critical HTML + CSS + JS ≤ 120 KB, font ≤ 100 KB, mobile hero imagery ≤ 450 KB, desktop hero imagery ≤ 900 KB, and minified/production JavaScript ≤ 12 KB.
- Preserve no-JavaScript readability, WCAG 2.2 AA contrast, 44×44 CSS-pixel primary controls, visible focus, 200% zoom usability, and explicit reduced-motion/transparency/contrast/forced-colors states.
- Do not change `SKILL.md`, manifests, scanner/report behavior, report schema, generated report files, README art, campaign files, or registry state.
- Work only in `/Users/eliemajorel/.codex/worktrees/app-store-review-alarm-evidence` on `codex/from-alarm-to-evidence`.
- Run the Impeccable context command once and load `reference/craft-floor.md` immediately before the first UI edit. Do not enable repository hooks. Run the manual detector once, after the full candidate is built.
- Publication, deployment, and merge remain separate actions after the implementation and hosted checks are reviewed.

---

## File Map

| File | Responsibility |
| --- | --- |
| `site/index.html` | Landing semantics, exact copy, metadata, JSON-LD, section order, gate/report DOM, install controls |
| `site/styles.css` | Shared reset, tokens, header/footer, long-form guide styling; no landing composition |
| `site/home.css` | Landing-only art direction, layout, responsive recomposition, interaction states, preference modes |
| `site/site.js` | Clipboard enhancement, selectable fallback, accessible status reset; no scroll loop or business logic |
| `scripts/tests/test_pages_site.py` | Static product truth, narrative order, asset integrity/budgets, accessibility and enhancement contracts |
| `site/assets/fonts/Hubot-Sans-display.woff2` | Upright `wdth`/`wght` display subset |
| `site/assets/fonts/OFL.txt` | Upstream SIL Open Font License 1.1 |
| `site/assets/fonts/README.md` | Font and responsive-image provenance, pinned inputs, exact generation commands and hashes |
| `site/assets/review-gate-cinematic-{768,1440}.{avif,webp}` | Responsive derivatives of the existing original CGI gate; no semantic text |
| `scripts/assets/review-gate-social.html` | Reproducible 1200×630 social-card source using exact HTML text and repository assets |
| `site/assets/review-gate-social.png` | Rendered social preview with report proof dominant over CGI |

`site/assets/review-gate-cinematic.png`, `assets/visual-report-example.png`, `examples/parceltrack-report.html`, and `examples/parceltrack-report.json` remain source truth and are not rewritten.

---

### Task 1: Produce Licensed, Responsive Visual Assets

**Files:**
- Create: `site/assets/fonts/Hubot-Sans-display.woff2`
- Create: `site/assets/fonts/OFL.txt`
- Create: `site/assets/fonts/README.md`
- Create: `site/assets/review-gate-cinematic-768.avif`
- Create: `site/assets/review-gate-cinematic-768.webp`
- Create: `site/assets/review-gate-cinematic-1440.avif`
- Create: `site/assets/review-gate-cinematic-1440.webp`
- Modify: `scripts/tests/test_pages_site.py:9-65`
- Modify: `scripts/tests/test_pages_site.py:188-227`

**Interfaces:**
- Consumes: `site/assets/review-gate-cinematic.png`; GitHub Hubot Sans release `v1.0.1`; `uvx`; `npx`.
- Produces: `HUBOT_FONT`, `HUBOT_LICENSE`, `HUBOT_PROVENANCE`, and `RESPONSIVE_GATE_ART` test constants; four browser-selectable gate derivatives and one licensed display font used by Tasks 2–5.

- [ ] **Step 1: Add failing asset integrity and budget tests**

Add these constants below `SITE_MARK`:

```python
HOME_CSS = SITE / "home.css"
HUBOT_FONT = SITE / "assets" / "fonts" / "Hubot-Sans-display.woff2"
HUBOT_LICENSE = SITE / "assets" / "fonts" / "OFL.txt"
HUBOT_PROVENANCE = SITE / "assets" / "fonts" / "README.md"
RESPONSIVE_GATE_ART = (
    (SITE / "assets" / "review-gate-cinematic-768.avif", b"ftypavif", 100_000),
    (SITE / "assets" / "review-gate-cinematic-768.webp", b"WEBP", 120_000),
    (SITE / "assets" / "review-gate-cinematic-1440.avif", b"ftypavif", 180_000),
    (SITE / "assets" / "review-gate-cinematic-1440.webp", b"WEBP", 220_000),
)
```

Add helpers below `png_dimensions`:

```python
def assert_asset_signature(testcase, path: Path, signature: bytes) -> None:
    data = path.read_bytes()[:16]
    if signature == b"WEBP":
        testcase.assertEqual(b"RIFF", data[:4])
        testcase.assertEqual(b"WEBP", data[8:12])
    elif signature == b"ftypavif":
        testcase.assertIn(data[4:12], (b"ftypavif", b"ftypavis"))
    else:
        testcase.assertTrue(data.startswith(signature))
```

Replace the current single-CGI assertions inside `test_review_gate_assets_and_install_interaction_are_publishable` with:

```python
self.assertTrue(CINEMATIC_ART.is_file(), "source cinematic gate art is missing")
self.assertEqual((1536, 1024), png_dimensions(CINEMATIC_ART))

for asset, signature, maximum_bytes in RESPONSIVE_GATE_ART:
    with self.subTest(asset=asset.name):
        self.assertTrue(asset.is_file(), f"{asset.name} is missing")
        assert_asset_signature(self, asset, signature)
        self.assertLessEqual(asset.stat().st_size, maximum_bytes)

self.assertTrue(HUBOT_FONT.is_file(), "Hubot Sans display subset is missing")
self.assertEqual(b"wOF2", HUBOT_FONT.read_bytes()[:4])
self.assertLessEqual(HUBOT_FONT.stat().st_size, 100_000)
self.assertIn("SIL OPEN FONT LICENSE Version 1.1", read(HUBOT_LICENSE))
provenance = read(HUBOT_PROVENANCE)
self.assertIn("github/hubot-sans", provenance)
self.assertIn("v1.0.1", provenance)
self.assertIn("fonttools[woff]==4.64.0", provenance)
self.assertIn("sharp-cli@5.2.0", provenance)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python3 -m unittest scripts.tests.test_pages_site.PagesSiteTests.test_review_gate_assets_and_install_interaction_are_publishable -v
```

Expected: FAIL because `review-gate-cinematic-768.avif` and the Hubot Sans files do not exist.

- [ ] **Step 3: Generate the pinned Hubot Sans subset**

Run exactly:

```bash
landing_font_tmp=$(mktemp -d /private/tmp/app-review-hubot.XXXXXX)
curl --fail --silent --show-error --location \
  https://github.com/github/hubot-sans/releases/download/v1.0.1/Hubot-Sans.zip \
  -o "$landing_font_tmp/Hubot-Sans.zip"
printf '%s  %s\n' \
  b460d36097a5c9a3e45710cbe1554589eaa5765d7c2c88df364516f3e27159b1 \
  "$landing_font_tmp/Hubot-Sans.zip" | shasum -a 256 -c -
unzip -p "$landing_font_tmp/Hubot-Sans.zip" 'Hubot Sans/Hubot-Sans.woff2' \
  > "$landing_font_tmp/Hubot-Sans.woff2"
unzip -p "$landing_font_tmp/Hubot-Sans.zip" 'Hubot Sans/LICENSE' \
  > "$landing_font_tmp/OFL.txt"
uvx --from 'fonttools[woff]==4.64.0' fonttools varLib.instancer \
  --no-recalc-timestamp \
  "$landing_font_tmp/Hubot-Sans.woff2" slnt=0 \
  --output="$landing_font_tmp/Hubot-Sans-upright.woff2"
uvx --from 'fonttools[woff]==4.64.0' pyftsubset \
  "$landing_font_tmp/Hubot-Sans-upright.woff2" \
  --output-file="$landing_font_tmp/Hubot-Sans-display.woff2" \
  --flavor=woff2 \
  --unicodes='U+0020-007E,U+00A0-00FF,U+2010-205E,U+20AC,U+2190-2199,U+21A5,U+2212,U+2264-2265,U+2713' \
  --layout-features='kern,liga' \
  --name-IDs='0,1,2,3,4,5,6,13,14' \
  --name-languages='*' \
  --notdef-glyph \
  --recommended-glyphs \
  --no-recalc-timestamp
mkdir -p site/assets/fonts
install -m 0644 "$landing_font_tmp/Hubot-Sans-display.woff2" \
  site/assets/fonts/Hubot-Sans-display.woff2
install -m 0644 "$landing_font_tmp/OFL.txt" site/assets/fonts/OFL.txt
```

Expected source ZIP SHA-256: `b460d36097a5c9a3e45710cbe1554589eaa5765d7c2c88df364516f3e27159b1`. Expected deterministic subset size with the pinned toolchain: 62,376 bytes, below the 100 KB gate.

- [ ] **Step 4: Generate responsive CGI derivatives**

Run exactly:

```bash
landing_image_tmp=$(mktemp -d /private/tmp/app-review-gate.XXXXXX)
npx --yes sharp-cli@5.2.0 \
  -i site/assets/review-gate-cinematic.png \
  -o "$landing_image_tmp/review-gate-cinematic-1440.avif" \
  -f avif -q 55 --effort 6 \
  resize 1440 960 --fit cover --position east
npx --yes sharp-cli@5.2.0 \
  -i site/assets/review-gate-cinematic.png \
  -o "$landing_image_tmp/review-gate-cinematic-1440.webp" \
  -f webp -q 72 --effort 6 \
  resize 1440 960 --fit cover --position east
npx --yes sharp-cli@5.2.0 \
  -i site/assets/review-gate-cinematic.png \
  -o "$landing_image_tmp/review-gate-cinematic-768.avif" \
  -f avif -q 50 --effort 6 \
  resize 768 640 --fit cover --position east
npx --yes sharp-cli@5.2.0 \
  -i site/assets/review-gate-cinematic.png \
  -o "$landing_image_tmp/review-gate-cinematic-768.webp" \
  -f webp -q 68 --effort 6 \
  resize 768 640 --fit cover --position east
install -m 0644 "$landing_image_tmp"/review-gate-cinematic-* site/assets/
```

Inspect both WebP outputs before continuing:

```bash
open "$landing_image_tmp/review-gate-cinematic-1440.webp"
open "$landing_image_tmp/review-gate-cinematic-768.webp"
```

Reject the derivatives if the complete red aperture, blue evidence tile, or green exit marker is lost. Re-run only by changing crop position; do not repaint or synthesize product evidence.

- [ ] **Step 5: Add the exact provenance record**

Create `site/assets/fonts/README.md` with:

```markdown
# Landing asset provenance

## Hubot Sans display subset

- Upstream: https://github.com/github/hubot-sans
- Release: v1.0.1
- Release asset: Hubot-Sans.zip
- Source ZIP SHA-256: `b460d36097a5c9a3e45710cbe1554589eaa5765d7c2c88df364516f3e27159b1`
- License: SIL Open Font License 1.1; copied as `OFL.txt`
- Toolchain: `fonttools[woff]==4.64.0`
- Transformation: remove the unused slant axis, retain variable weight and width, subset to the Latin and interface characters listed in the implementation plan.
- Output SHA-256: `d48383a1e421d6bec4b5e7a578ede43398047c637fa1311e5a9558e35e2dd9ee`

## Review-gate responsive derivatives

- Source: `../review-gate-cinematic.png`, the repository's original 1536×1024 artwork.
- Toolchain: `sharp-cli@5.2.0`
- Transformation: responsive east-weighted crop and AVIF/WebP encoding only.
- Semantic text and report evidence remain HTML; these files are decorative plates.
- `review-gate-cinematic-768.avif` SHA-256: `28adf780f1cd63d72ddd0d255a14f0e6eccec77b7ce19c96ff21b2582cff1650`
- `review-gate-cinematic-768.webp` SHA-256: `e5231eadea8ce2e9b9bfee7473de5ea21b570b76cfc05626343fddc225170292`
- `review-gate-cinematic-1440.avif` SHA-256: `748343a6187cec1179c7b357a3f19fcec34b2a519f5fe47d257e69b94a3b5763`
- `review-gate-cinematic-1440.webp` SHA-256: `3534d149c5f84e41ed0efe4db4fde17fd1c538b354ee0b7c60e5a009d9d1961b`

The exact commands and output budgets are recorded in `docs/superpowers/plans/2026-09-05-from-alarm-to-evidence.md`.
```

- [ ] **Step 6: Run asset and full site tests**

Run:

```bash
python3 -m unittest scripts.tests.test_pages_site.PagesSiteTests.test_review_gate_assets_and_install_interaction_are_publishable -v
python3 -m unittest discover -s scripts/tests -p 'test_pages_site.py' -v
git diff --check
```

Expected: PASS; all four responsive images have valid signatures and remain below their individual gates; the font is valid WOFF2 below 100 KB; existing page tests remain green.

- [ ] **Step 7: Commit the asset foundation**

```bash
git add scripts/tests/test_pages_site.py site/assets/fonts \
  site/assets/review-gate-cinematic-768.avif \
  site/assets/review-gate-cinematic-768.webp \
  site/assets/review-gate-cinematic-1440.avif \
  site/assets/review-gate-cinematic-1440.webp
git commit -m "feat: add licensed landing visual assets"
```

---

### Task 2: Recompose the Narrative and Semantic HTML

**Files:**
- Modify: `scripts/tests/test_pages_site.py:67-145`
- Modify: `scripts/tests/test_pages_site.py:188-242`
- Modify: `site/index.html:1-282`

**Interfaces:**
- Consumes: responsive gate assets from Task 1; current report routes and ParcelTrack sample values.
- Produces: ordered section IDs `report`, `method`, `install`, `modes`, `evaluation`, `policy`, `faq`, `close`; unique `hero-install-command`, `install-command`, and `close-install-command` copy targets; landing DOM consumed by `home.css` and `site.js`.

- [ ] **Step 1: Replace old hero assertions with the approved product contract**

In `test_landing_page_has_indexable_product_contract`, replace the old title/headline and visible-claim assertions with:

```python
self.assertEqual(1, len(re.findall(r"<h1(?:\s|>)", landing)))
self.assertIn(
    "<title>App Store Review Skill — Find the risk. Prove the fix.</title>",
    landing,
)
self.assertIn('<span class="headline-risk">Find the risk.</span>', landing)
self.assertIn('<span class="headline-proof">Prove the fix.</span>', landing)
self.assertIn(
    "A read-only preflight that traces App Store review risks to the files, "
    "rules, and checks behind them.",
    landing,
)
self.assertIn(f'<link rel="canonical" href="{SITE_URL}">', landing)
self.assertRegex(landing, r'<meta name="description" content="[^\"]{140,180}">')

for visible_claim in (
    "npx skills add ElxMaj/app-store-review-skill",
    "Pre-submission audit",
    "Rejection recovery",
    "Human-craft audit",
    "97% quality",
    "99% impact",
    "Tessl evaluates the skill package. It is not an App Store approval rate.",
    "Fictional ParcelTrack evidence",
):
    with self.subTest(visible_claim=visible_claim):
        self.assertIn(visible_claim, landing)

self.assertEqual(1, landing.count('class="button button-primary"'))
self.assertIn('class="button button-primary" href="#install">Run the preflight</a>', landing)
self.assertNotIn("Star on GitHub", landing)
self.assertNotIn("Security scan passed", landing)
self.assertNotIn('class="hero-proof"', landing)
```

Add an order assertion:

```python
section_order = ("report", "method", "install", "modes", "evaluation", "policy", "faq", "close")
positions = [landing.index(f'id="{section_id}"') for section_id in section_order]
self.assertEqual(sorted(positions), positions)
```

Add exact evaluation scope assertions:

```python
self.assertIn("Tessl evaluation · v1.2.2", landing)
self.assertIn('<time datetime="2026-09-03">Last scored 3 September 2026</time>', landing)
self.assertNotIn("aggregateRating", landing)
self.assertNotIn("approval rate</strong>", landing)
```

- [ ] **Step 2: Add failing hierarchy and progressive-markup tests**

Replace `test_review_gate_motion_and_accessibility_contract` with the semantic assertions below. Task 3 adds stylesheet assertions after `home.css` exists:

```python
def test_review_gate_motion_and_accessibility_contract(self):
    landing = read(SITE / "index.html")

    self.assertIn('class="gate-sequence" aria-hidden="true"', landing)
    self.assertIn('data-gate-sequence', landing)
    self.assertIn('class="evidence-packet"', landing)
    self.assertIn('class="hero-report-sheet"', landing)
    self.assertIn("Camera flow has no purpose string", landing)
    self.assertIn("app.json:18", landing)
    self.assertIn('aria-live="polite"', landing)
    self.assertIn('href="#install"', landing)
    for section_id in ("report", "method", "install", "modes", "evaluation", "policy", "faq", "close"):
        with self.subTest(section_id=section_id):
            self.assertIn(f'id="{section_id}"', landing)
```

Run:

```bash
python3 -m unittest \
  scripts.tests.test_pages_site.PagesSiteTests.test_landing_page_has_indexable_product_contract \
  scripts.tests.test_pages_site.PagesSiteTests.test_review_gate_motion_and_accessibility_contract \
  -v
```

Expected: FAIL on the old title/headline, dominant GitHub CTA, old section order, and missing evidence/report DOM.

- [ ] **Step 3: Update head metadata and resource declarations**

Use this head contract in `site/index.html` while preserving the canonical, favicon, sitemap, robots, JSON-LD graph, and current social-image URL:

```html
<title>App Store Review Skill — Find the risk. Prove the fix.</title>
<meta name="description" content="Run a read-only App Store review preflight in Codex or Claude Code. Trace iOS submission risks to project evidence, published guidance, and verification steps.">
<meta name="theme-color" content="#070a10">
<meta property="og:title" content="Find the risk. Prove the fix.">
<meta property="og:description" content="A read-only App Store review preflight for Codex and Claude Code.">
<meta name="twitter:title" content="Find the risk. Prove the fix.">
<meta name="twitter:description" content="A read-only App Store review preflight for Codex and Claude Code.">
<link rel="preload" href="/app-store-review-skill/assets/fonts/Hubot-Sans-display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/app-store-review-skill/styles.css">
<script>document.documentElement.classList.add("has-js");</script>
<script src="/app-store-review-skill/site.js" defer></script>
```

Update the `WebSite` description to the same read-only preflight proposition. Keep `SoftwareSourceCode.version` sourced as `1.2.2`; do not add ratings or reviews to JSON-LD.

- [ ] **Step 4: Replace the header and hero with the exact conversion hierarchy**

Use this semantic structure and copy:

```html
<header class="site-header site-header-dark">
  <a class="brand" href="/app-store-review-skill/" aria-label="App Store Review Skill home">
    <span class="brand-mark" aria-hidden="true"><i></i><i></i></span>
    <span>App Store Review</span>
  </a>
  <nav class="site-nav" aria-label="Primary navigation">
    <a href="#report">Report</a>
    <a class="nav-install" href="#install">Install</a>
    <a class="nav-github" href="https://github.com/ElxMaj/app-store-review-skill">GitHub <span aria-hidden="true">↗</span></a>
  </nav>
</header>

<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-copy">
      <h1 id="hero-title">
        <span class="headline-risk">Find the risk.</span>
        <span class="headline-proof">Prove the fix.</span>
      </h1>
      <p class="hero-lede">A read-only preflight that traces App Store review risks to the files, rules, and checks behind them.</p>
      <div class="hero-actions">
        <a class="button button-primary" href="#install">Run the preflight</a>
        <a class="button button-secondary" href="/app-store-review-skill/report/">Inspect the sample report</a>
      </div>
      <div class="command-dock" role="group" aria-label="Install with Skills CLI">
        <code id="hero-install-command">npx skills add ElxMaj/app-store-review-skill</code>
        <button class="copy-button" type="button" data-copy-target="hero-install-command" data-copy-status="hero-copy-status" aria-label="Copy install command"><span aria-hidden="true">Copy</span></button>
        <span class="sr-only" id="hero-copy-status" aria-live="polite"></span>
      </div>
      <p class="hero-reassurance">First pass: read-only <span aria-hidden="true">·</span> Codex + Claude Code <span aria-hidden="true">·</span> Xcode, Expo, React Native, and Flutter</p>
    </div>

    <div class="gate-sequence" aria-hidden="true" data-gate-sequence>
      <picture class="gate-machine">
        <source media="(max-width: 767px)" type="image/avif" srcset="/app-store-review-skill/assets/review-gate-cinematic-768.avif">
        <source media="(max-width: 767px)" type="image/webp" srcset="/app-store-review-skill/assets/review-gate-cinematic-768.webp">
        <source type="image/avif" srcset="/app-store-review-skill/assets/review-gate-cinematic-1440.avif">
        <source type="image/webp" srcset="/app-store-review-skill/assets/review-gate-cinematic-1440.webp">
        <img src="/app-store-review-skill/assets/review-gate-cinematic.png" width="1536" height="1024" alt="" fetchpriority="high">
      </picture>
      <div class="evidence-packet">
        <span>Source evidence</span>
        <code>app.json:18</code>
        <strong>NSCameraUsageDescription missing</strong>
      </div>
      <div class="gate-aperture"><span>Review gate</span><i></i></div>
      <article class="hero-report-sheet">
        <div class="hero-report-meta"><span>ParcelTrack</span><span>Sample report</span></div>
        <div class="hero-report-verdict"><span>Release verdict</span><strong>NOT READY</strong></div>
        <p>Camera flow has no purpose string</p>
        <code>app.json:18 · Guideline 5.1.1(ii)</code>
        <div class="hero-report-check"><i></i><span>Verify in merged release Info.plist</span></div>
      </article>
    </div>
  </section>
```

The complete decorative sequence remains `aria-hidden="true"`; the headline, lede, proof section, and method section provide equivalent meaning in the accessibility tree.

- [ ] **Step 5: Reorder and rewrite the body acts**

After the hero, implement these sections in this exact DOM order:

```html
<section class="report-proof" id="report" aria-labelledby="report-title">
  <div class="report-proof-copy">
    <h2 id="report-title">The report arrives before the fix.</h2>
    <p>See the verdict, confirmed blockers, manual checks, App Review Notes draft, and approval-gated fix groups before a project file changes.</p>
    <div class="report-actions">
      <a class="button button-paper" href="/app-store-review-skill/report/">Open the complete report</a>
      <a class="text-link" href="/app-store-review-skill/report/parceltrack-report.json">Inspect source JSON <span aria-hidden="true">↗</span></a>
    </div>
    <p class="sample-note">Fictional ParcelTrack evidence · No private project data</p>
  </div>
  <figure class="report-figure">
    <a href="/app-store-review-skill/report/" aria-label="Open the complete ParcelTrack sample report">
      <img src="/app-store-review-skill/assets/visual-report-example.png" width="1440" height="1500" loading="lazy" decoding="async" alt="ParcelTrack sample review report marked Not Ready with one blocker and three manual checks">
    </a>
    <figcaption><span>NOT READY</span><span>1 blocker · 3 manual checks</span></figcaption>
  </figure>
</section>

<section class="method" id="method" aria-labelledby="method-title">
  <div class="section-intro">
    <h2 id="method-title">Every claim has a return address.</h2>
    <p>Confirmed evidence stays separate from inference and checks that still need a person or release build.</p>
  </div>
  <ol class="evidence-trace">
    <li><span>01</span><div><strong>What was found</strong><p>The camera permission is requested in <code>src/features/scan/LabelScanner.tsx:42</code>.</p></div></li>
    <li><span>02</span><div><strong>Where the gap lives</strong><p><code>app.json:18</code> has no <code>NSCameraUsageDescription</code>.</p></div></li>
    <li><span>03</span><div><strong>Why it matters</strong><p>The sample maps the missing explanation to published Guideline 5.1.1(ii).</p></div></li>
    <li><span>04</span><div><strong>How to prove the fix</strong><p>Build the release archive, inspect the merged <code>Info.plist</code>, then retest the scanner on a clean device.</p></div></li>
  </ol>
  <a class="text-link" href="https://github.com/ElxMaj/app-store-review-skill/blob/main/SKILL.md">Read the review contract <span aria-hidden="true">↗</span></a>
</section>

<section class="install" id="install" aria-labelledby="install-title">
  <div class="install-copy">
    <h2 id="install-title">Install once. Ask in plain language.</h2>
    <p>The recommended Skills CLI route works with Codex and agents that support the open skills format.</p>
  </div>
  <div class="install-primary">
    <div class="command-dock command-dock-light" role="group" aria-label="Recommended install command">
      <code id="install-command">npx skills add ElxMaj/app-store-review-skill</code>
      <button class="copy-button" type="button" data-copy-target="install-command" data-copy-status="install-copy-status" aria-label="Copy recommended install command"><span aria-hidden="true">Copy</span></button>
      <span class="sr-only" id="install-copy-status" aria-live="polite"></span>
    </div>
    <blockquote>Audit this iOS app before submission. Report first and do not edit files.</blockquote>
  </div>
  <details class="alternate-installs">
    <summary>Other install methods</summary>
    <div><strong>Tessl</strong><code>npx tessl install maj-labs/app-store-review</code></div>
    <div><strong>Claude Code</strong><code>/plugin marketplace add ElxMaj/app-store-review-skill</code></div>
    <a href="https://github.com/ElxMaj/app-store-review-skill/blob/main/INSTALL.md">See every install method <span aria-hidden="true">↗</span></a>
  </details>
</section>

<section class="modes" id="modes" aria-labelledby="modes-title">
  <div class="section-intro">
    <h2 id="modes-title">Meet the review where you are.</h2>
  </div>
  <ol class="mode-path">
    <li><span>01 / Before upload</span><h3>Pre-submission audit</h3><p>Produces an evidence-ranked verdict across permissions, privacy, purchases, metadata, reviewer access, and release paths.</p></li>
    <li><span>02 / After rejection</span><h3>Rejection recovery</h3><p>Preserves Apple’s exact message and produces a sourced next move: fix, clarify, appeal, or ask.</p></li>
    <li><span>03 / Before it feels done</span><h3>Human-craft audit</h3><p>Produces a specific refinement plan for distinction, provenance, visual identity, microcopy, accessibility, and missing states.</p></li>
  </ol>
</section>

<section class="evaluation" id="evaluation" aria-labelledby="evaluation-title">
  <div>
    <h2 id="evaluation-title">Proof with a date and a boundary.</h2>
  </div>
  <a class="evaluation-record" href="https://tessl.io/registry/maj-labs/app-store-review">
    <span>Tessl evaluation · v1.2.2</span>
    <strong><b>97%</b> quality <i></i> <b>99%</b> impact</strong>
    <time datetime="2026-09-03">Last scored 3 September 2026</time>
    <p>Tessl evaluates the skill package. It is not an App Store approval rate.</p>
  </a>
</section>

<section class="policy" id="policy" aria-labelledby="policy-title">
  <span class="policy-number" aria-hidden="true">4.3</span>
  <div>
    <h2 id="policy-title">Apple’s published guidelines do not name AI-written code as a rejection category.</h2>
    <p>The rules focus on the product that ships: useful functionality, distinct value, truthful metadata, privacy, safety, and who submits template-generated work.</p>
    <a class="text-link" href="/app-store-review-skill/guides/will-apple-reject-ai-built-apps/">Read the source-based guide to 4.2.6 and 4.3 <span aria-hidden="true">→</span></a>
  </div>
</section>

<section class="faq" id="faq" aria-labelledby="faq-title">
  <div class="section-intro">
    <h2 id="faq-title">A useful review keeps its limits visible.</h2>
  </div>
  <div class="faq-list">
    <div><h3>Does it guarantee App Store approval?</h3><p>No. It finds evidence and prepares review work, but Apple makes the decision.</p></div>
    <div><h3>Does it detect AI-written code?</h3><p>No. It reviews product evidence, policy risks, and app quality. It does not claim to detect AI-written code.</p></div>
    <div><h3>Does it edit my project?</h3><p>The first pass is read-only. You see the report before any proposed fix group is applied.</p></div>
  </div>
</section>

<section class="closing-field" id="close" aria-labelledby="close-title">
  <h2 id="close-title">See the evidence before the reviewer sees the gap.</h2>
  <div class="command-dock" role="group" aria-label="Install App Store Review Skill">
    <code id="close-install-command">npx skills add ElxMaj/app-store-review-skill</code>
    <button class="copy-button" type="button" data-copy-target="close-install-command" data-copy-status="close-copy-status" aria-label="Copy install command"><span aria-hidden="true">Copy</span></button>
    <span class="sr-only" id="close-copy-status" aria-live="polite"></span>
  </div>
  <p>Open source · First pass read-only · Independent and not affiliated with Apple Inc.</p>
</section>
```

Close `main` after `#close`. Keep the footer concise with MIT license, maker links, and the existing non-affiliation disclosure.

- [ ] **Step 6: Run the focused contract tests and verify GREEN**

Run:

```bash
python3 -m unittest \
  scripts.tests.test_pages_site.PagesSiteTests.test_landing_page_has_indexable_product_contract \
  scripts.tests.test_pages_site.PagesSiteTests.test_landing_json_ld_uses_supported_source_truth \
  scripts.tests.test_pages_site.PagesSiteTests.test_review_gate_motion_and_accessibility_contract \
  scripts.tests.test_pages_site.PagesSiteTests.test_ai_built_app_guide_states_apple_policy_without_inventing_a_ban \
  -v
git diff --check
```

Expected: PASS. Confirm `site/guides/will-apple-reject-ai-built-apps/index.html` was not modified.

- [ ] **Step 7: Commit the narrative recompose**

```bash
git add site/index.html scripts/tests/test_pages_site.py
git commit -m "feat: turn landing alarm into evidence"
```

---

### Task 3: Build the Static Editorial Visual System

**Files:**
- Create: `site/home.css`
- Modify: `site/styles.css:1-1594`
- Modify: `scripts/tests/test_pages_site.py:228-243`

**Interfaces:**
- Consumes: Task 2 class names and section IDs; Hubot Sans and responsive images from Task 1.
- Produces: a shared `styles.css` safe for the guide plus a landing-scoped `home.css` with static final-state layout; motion selectors consumed by Task 4.

- [ ] **Step 1: Add failing style-architecture and preference tests**

Extend `test_review_gate_motion_and_accessibility_contract` after its HTML assertions:

```python
shared_css = read(SITE / "styles.css")
home_css = read(HOME_CSS)

self.assertIn('href="/app-store-review-skill/home.css"', landing)
self.assertIn('@font-face', home_css)
self.assertIn('font-family: "Hubot Sans"', home_css)
self.assertIn('font-stretch: 75% 125%', home_css)
self.assertIn('font-stretch: 78%', home_css)
self.assertIn('font-stretch: 112%', home_css)
self.assertIn('@media (max-width: 1279px)', home_css)
self.assertIn('@media (max-width: 767px)', home_css)
self.assertIn('@media (prefers-reduced-motion: reduce)', home_css)
self.assertIn('@media (prefers-reduced-transparency: reduce)', home_css)
self.assertIn('@media (prefers-contrast: more)', home_css)
self.assertIn('@media (forced-colors: active)', home_css)
self.assertNotIn('transition: all', shared_css + home_css)
self.assertNotIn('backdrop-filter', home_css)
self.assertNotIn('.hero-proof', home_css)
self.assertIn('.article-shell', shared_css)
self.assertNotIn('.hero-surface', shared_css)
```

Add a compressed critical-resource budget helper and test:

```python
import gzip


def gzip_size(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), compresslevel=9, mtime=0))


def test_landing_critical_resources_stay_within_budget(self):
    critical = (
        SITE / "index.html",
        SITE / "styles.css",
        SITE / "home.css",
        SITE / "site.js",
    )
    self.assertLessEqual(sum(gzip_size(path) for path in critical), 120_000)
    self.assertLessEqual((SITE / "site.js").stat().st_size, 12_000)
    report_image = ROOT / "assets" / "visual-report-example.png"
    mobile_gate = SITE / "assets" / "review-gate-cinematic-768.avif"
    desktop_gate = SITE / "assets" / "review-gate-cinematic-1440.avif"
    self.assertLessEqual(mobile_gate.stat().st_size + report_image.stat().st_size, 450_000)
    self.assertLessEqual(desktop_gate.stat().st_size + report_image.stat().st_size, 900_000)
```

- [ ] **Step 2: Run the style tests and verify RED**

Run:

```bash
python3 -m unittest \
  scripts.tests.test_pages_site.PagesSiteTests.test_review_gate_motion_and_accessibility_contract \
  scripts.tests.test_pages_site.PagesSiteTests.test_landing_critical_resources_stay_within_budget \
  -v
```

Expected: FAIL because `site/home.css` does not exist and landing rules still occupy `styles.css`.

- [ ] **Step 3: Refactor `styles.css` into the shared/guide layer**

Keep these responsibilities in `site/styles.css`:

- `:root` tokens used by both pages;
- reset, body, links, focus, media, `figure`, `code`/`pre`, heading wrapping;
- `.skip-link`, `.site-header`, `.site-footer`, `.brand`, `.brand-mark`, `.site-nav`, `.page-shell`, shared `.text-link` and `.button` primitives;
- the complete current long-form-guide rules from `.article-shell` through `.article-note`;
- guide-specific responsive and print rules.

Remove obsolete landing selectors including `.hero-surface`, `.hero-grid`, `.review-gate`, `.hero-proof`, `.manifesto`, `.mode-journey`, `.evidence-section`, `.report-section`, `.policy-section`, `.install-grid`, `.prompt-example`, and `.faq-section`. Do not copy them into `home.css`; build the new class system from Task 2.

The shared token/base opening must remain equivalent to:

```css
:root {
  color-scheme: light;
  --night: #070a10;
  --night-raised: #0d111b;
  --ink: #111318;
  --paper: #f6f3eb;
  --paper-raised: #fffdf7;
  --muted: #62656c;
  --quiet: #61646b;
  --rule: rgb(17 19 24 / 16%);
  --rule-strong: rgb(17 19 24 / 42%);
  --blue: #3559d8;
  --blue-bright: #87a1ff;
  --evidence: #147cff;
  --risk: #ff2748;
  --verified: #61e6b5;
  --cobalt: var(--evidence);
  --ruby: var(--risk);
  --coral: #ff654f;
  --mint: var(--verified);
  --gold: #eadb93;
  --max: 1320px;
  --copy: 1180px;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; background: var(--night); }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
```

- [ ] **Step 4: Create the landing-only font, tokens, and layout foundation**

Start `site/home.css` with:

```css
@font-face {
  font-family: "Hubot Sans";
  src: url("/app-store-review-skill/assets/fonts/Hubot-Sans-display.woff2") format("woff2-variations");
  font-display: swap;
  font-style: normal;
  font-weight: 200 900;
  font-stretch: 75% 125%;
}

.home-page {
  --gutter: clamp(18px, 3.4vw, 52px);
  --section-space: clamp(92px, 12vw, 180px);
  background: var(--paper);
  scrollbar-color: var(--risk) var(--night);
}

.home-page ::selection { background: var(--evidence); color: #fff; }
.home-page main { overflow-x: clip; }
.home-page .site-header-dark {
  width: 100%;
  padding-inline: max(var(--gutter), calc((100% - var(--max)) / 2));
  border-color: rgb(255 255 255 / 16%);
  background: var(--night);
  color: #f8f7f3;
}

.home-page .nav-install {
  border-bottom: 2px solid var(--verified);
  color: #fff;
}

.home-page .copy-button:disabled {
  cursor: wait;
  opacity: 0.82;
}

.hero {
  position: relative;
  display: grid;
  min-height: calc(100svh - 82px);
  max-height: 880px;
  padding: clamp(56px, 7vh, 92px) max(var(--gutter), calc((100% - var(--max)) / 2));
  overflow: hidden;
  background: var(--night);
  color: #f8f7f3;
  isolation: isolate;
}

.hero-copy {
  z-index: 4;
  width: min(700px, 58vw);
  align-self: center;
}

.hero h1 {
  margin: 0;
  font-family: "Hubot Sans", sans-serif;
  font-size: clamp(68px, 8vw, 124px);
  font-weight: 850;
  letter-spacing: -0.04em;
  line-height: 0.82;
}

.hero h1 span { display: block; white-space: nowrap; }
.headline-risk { font-stretch: 78%; color: #fff; }
.headline-proof { font-stretch: 112%; color: #fff; }

.hero-lede {
  max-width: 610px;
  margin: 30px 0 0;
  color: rgb(248 247 243 / 78%);
  font-size: clamp(18px, 1.5vw, 23px);
  letter-spacing: -0.018em;
  line-height: 1.45;
}

.gate-sequence {
  position: absolute;
  z-index: 1;
  top: 0;
  right: max(-130px, calc((100vw - var(--max)) / -2));
  bottom: 0;
  width: min(68vw, 980px);
}

.gate-machine,
.gate-machine img {
  width: 100%;
  height: 100%;
}

.gate-machine img {
  object-fit: cover;
  object-position: 70% center;
  opacity: 0.78;
}
```

At the same time, add this immediately after the shared stylesheet in `site/index.html`:

```html
<link rel="stylesheet" href="/app-store-review-skill/home.css">
```

Use a solid night overlay at the left edge, not a decorative glow field. Position `.evidence-packet` before the aperture and `.hero-report-sheet` over the aperture so the visual reads left/source → red/gate → paper/report. Keep all hero visual states inside the first viewport.

- [ ] **Step 5: Implement report, method, action, reassurance, and close as continuous fields**

Use the following composition rules rather than a card grid:

```css
.report-proof,
.method,
.install,
.modes,
.evaluation,
.policy,
.faq,
.closing-field {
  width: min(var(--max), calc(100% - (2 * var(--gutter))));
  margin-inline: auto;
}

.report-proof {
  display: grid;
  grid-template-columns: minmax(270px, 0.68fr) minmax(560px, 1.32fr);
  gap: clamp(48px, 8vw, 120px);
  align-items: center;
  padding-block: var(--section-space);
}

.report-figure {
  position: relative;
  border-top: 4px solid var(--risk);
  background: #ece9e1;
  box-shadow: 0 32px 80px rgb(17 19 24 / 18%);
  transform: rotate(0.65deg);
}

.report-figure img { width: 100%; height: auto; }

.method {
  display: grid;
  grid-template-columns: minmax(280px, 0.78fr) minmax(0, 1.22fr);
  gap: clamp(54px, 9vw, 140px);
  padding-block: var(--section-space);
  border-top: 1px solid var(--rule-strong);
}

.evidence-trace {
  position: relative;
  margin: 0;
  padding: 0;
  list-style: none;
}

.evidence-trace::before {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 19px;
  width: 2px;
  background: var(--evidence);
  content: "";
}

.evidence-trace li {
  position: relative;
  display: grid;
  grid-template-columns: 40px minmax(0, 1fr);
  gap: 25px;
  padding: 0 0 44px;
}

.install {
  display: grid;
  grid-template-columns: minmax(280px, 0.72fr) minmax(520px, 1.28fr);
  gap: clamp(50px, 8vw, 120px);
  padding: clamp(70px, 9vw, 120px);
  background: var(--evidence);
  color: #fff;
}

.mode-path {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin: 64px 0 0;
  padding: 0;
  border-top: 1px solid var(--rule-strong);
  list-style: none;
}

.mode-path li {
  min-height: 330px;
  padding: 28px 36px 32px 0;
  border-bottom: 1px solid var(--rule-strong);
}

.mode-path li + li {
  padding-left: 36px;
  border-left: 1px solid var(--rule);
}

.evaluation {
  display: grid;
  grid-template-columns: 0.8fr 1.2fr;
  gap: clamp(44px, 8vw, 120px);
  padding-block: var(--section-space);
  border-top: 1px solid var(--rule-strong);
}

.evaluation-record {
  display: grid;
  gap: 18px;
  padding: 28px 0;
  border-block: 4px solid var(--ink);
  text-decoration: none;
}

.policy {
  display: grid;
  grid-template-columns: minmax(190px, 0.42fr) minmax(0, 1.58fr);
  gap: clamp(42px, 7vw, 100px);
  padding-block: var(--section-space);
}

.faq-list > div {
  display: grid;
  grid-template-columns: minmax(220px, 0.8fr) minmax(0, 1.2fr);
  gap: 48px;
  padding: 28px 0;
  border-top: 1px solid var(--rule-strong);
}

.closing-field {
  width: 100%;
  padding: clamp(88px, 11vw, 160px) max(var(--gutter), calc((100% - var(--max)) / 2));
  background: var(--night);
  color: #fff;
}
```

Only `.command-dock`, buttons, and the disclosure `details` may use a small radius. Do not add equal rounded wrappers around the report, method steps, modes, evaluation, policy, or FAQ.

- [ ] **Step 6: Recompose tablet and mobile explicitly**

Add these breakpoints and behaviors:

```css
@media (max-width: 1279px) {
  .hero-copy { width: min(660px, 66vw); }
  .gate-sequence { right: -210px; width: 78vw; }
  .report-proof { grid-template-columns: 0.75fr 1.25fr; }
  .install { grid-template-columns: 1fr; }
}

@media (max-width: 767px) {
  .home-page { --gutter: 16px; --section-space: 92px; }
  .home-page .site-header { min-height: 64px; }
  .home-page .site-nav { gap: 14px; }
  .home-page .site-nav a:first-child { display: none; }

  .hero {
    min-height: calc(100svh - 64px);
    max-height: none;
    padding-top: 36px;
    padding-bottom: 300px;
  }

  .hero-copy { width: 100%; align-self: start; }
  .hero h1 { font-size: clamp(53px, 16.2vw, 68px); line-height: 0.84; }
  .hero-lede { max-width: 35ch; margin-top: 22px; font-size: 17px; }
  .hero-actions { margin-top: 24px; }
  .button { min-height: 48px; }
  .command-dock { grid-template-columns: minmax(0, 1fr) 48px; }
  .command-dock code { min-width: 0; overflow-x: auto; font-size: 11px; }
  .copy-button { min-width: 48px; min-height: 48px; }

  .gate-sequence {
    top: auto;
    right: -82px;
    bottom: 0;
    width: 125vw;
    height: 310px;
  }

  .gate-machine img { object-position: 72% center; }
  .evidence-packet { left: 5%; bottom: 76px; transform: scale(0.72); transform-origin: left bottom; }
  .gate-aperture { right: 35%; bottom: 40px; }
  .hero-report-sheet { right: 7%; bottom: 26px; width: min(52vw, 205px); }

  .report-proof,
  .method,
  .evaluation,
  .policy,
  .faq-list > div {
    grid-template-columns: 1fr;
  }

  .report-proof { gap: 48px; }
  .report-figure { width: calc(100% + 8px); margin-left: -4px; }
  .method { gap: 48px; }
  .install { width: 100%; padding: 72px var(--gutter); }
  .mode-path { grid-template-columns: 1fr; }
  .mode-path li { min-height: 0; padding: 28px 0 44px; }
  .mode-path li + li { padding-left: 0; border-left: 0; }
  .policy-number { font-size: 88px; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .home-page *, .home-page *::before, .home-page *::after {
    animation-duration: 0.01ms !important;
    animation-delay: 0ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

@media (prefers-reduced-transparency: reduce) {
  .gate-machine img { opacity: 1; }
  .gate-sequence::after { display: none; }
}

@media (prefers-contrast: more) {
  .home-page { --muted: #44464b; --rule: rgb(17 19 24 / 48%); }
  .hero, .closing-field { background: #000; }
  .hero-lede, .hero-reassurance { color: #fff; }
}

@media (forced-colors: active) {
  .evidence-trace::before, .gate-aperture i { background: CanvasText; }
  .button, .command-dock, .evaluation-record { border: 2px solid CanvasText; }
}
```

At 390×844, tune only vertical spacing and visual positions until the headline, lede, primary CTA, command dock, and a readable `NOT READY` report fragment fit before 844 CSS pixels. Do not solve overflow by reducing command text below 11 px or hiding the report fragment.

- [ ] **Step 7: Run tests and inspect the guide before committing**

Run:

```bash
python3 -m unittest discover -s scripts/tests -p 'test_pages_site.py' -v
git diff --check
```

Then render both `/app-store-review-skill/` and `/app-store-review-skill/guides/will-apple-reject-ai-built-apps/` locally. Confirm the guide header, body measure, policy table, footer, and mobile layout remain unchanged in meaning and usable after the CSS split.

- [ ] **Step 8: Commit the static visual system**

```bash
git add site/styles.css site/home.css scripts/tests/test_pages_site.py
git commit -m "feat: build the evidence-gate visual system"
```

---

### Task 4: Add the One-Shot Transition and Accessible Copy Feedback

**Files:**
- Modify: `site/index.html:1-40`
- Modify: `site/index.html` command docks from Task 2
- Modify: `site/home.css`
- Modify: `site/site.js:1-52`
- Modify: `scripts/tests/test_pages_site.py`

**Interfaces:**
- Consumes: `data-gate-sequence`, `.evidence-packet`, `.gate-aperture`, `.hero-report-sheet`; copy target/status ID pairs from Task 2.
- Produces: `.has-js` one-shot CSS intro; `copyText(text): Promise<void>`; per-button polite status feedback and selection fallback.

- [ ] **Step 1: Add failing enhancement tests**

Append these assertions to `test_review_gate_motion_and_accessibility_contract`:

```python
site_js = read(SITE / "site.js")
home_css = read(HOME_CSS)

self.assertIn('document.documentElement.classList.add("has-js")', landing)
self.assertIn("@keyframes evidence-enter", home_css)
self.assertIn("@keyframes gate-scan", home_css)
self.assertIn("@keyframes report-resolve", home_css)
self.assertNotIn("infinite", home_css)
self.assertIn('data-copy-status="hero-copy-status"', landing)
self.assertIn('data-copy-status="install-copy-status"', landing)
self.assertIn('data-copy-status="close-copy-status"', landing)
self.assertIn('status.textContent = "Install command copied."', site_js)
self.assertIn('status.textContent = "Command selected. Press Command-C or Control-C."', site_js)
self.assertNotIn("setInterval", site_js)
self.assertNotIn('addEventListener("scroll"', site_js)
```

Run the single test. Expected: FAIL because the keyframes and accessible status strings do not yet exist.

- [ ] **Step 2: Add the bounded gate transition in CSS**

Add exactly three animations, all under motion permission:

```css
@media (prefers-reduced-motion: no-preference) {
  .has-js .evidence-packet {
    animation: evidence-enter 1100ms var(--ease-out) 180ms both;
  }

  .has-js .gate-aperture i {
    animation: gate-scan 760ms var(--ease-out) 520ms both;
  }

  .has-js .hero-report-sheet {
    animation: report-resolve 980ms var(--ease-out) 620ms both;
  }
}

@keyframes evidence-enter {
  from { opacity: 0; transform: translate3d(-72px, 0, 0); }
  to { opacity: 1; transform: translate3d(0, 0, 0); }
}

@keyframes gate-scan {
  0% { opacity: 0; transform: scaleY(0.2) translateY(-70%); }
  35%, 75% { opacity: 1; }
  100% { opacity: 0.72; transform: scaleY(1) translateY(70%); }
}

@keyframes report-resolve {
  from { opacity: 0; transform: translate3d(56px, 8px, 0) rotate(1.8deg); }
  to { opacity: 1; transform: translate3d(0, 0, 0) rotate(-0.6deg); }
}
```

All default, no-JavaScript selectors must describe the final state. The animation affects only decorative duplicated content. Do not animate blur, font axes, layout properties, or the report proof section.

- [ ] **Step 3: Replace `site/site.js` with the complete copy enhancement**

Use:

```javascript
(() => {
  const copyText = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    const helper = document.createElement("textarea");
    helper.value = text;
    helper.setAttribute("readonly", "");
    helper.style.position = "fixed";
    helper.style.opacity = "0";
    document.body.appendChild(helper);
    helper.select();
    const copied = document.execCommand("copy");
    helper.remove();

    if (!copied) throw new Error("Copy command was unavailable");
  };

  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    button.addEventListener("click", async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      const status = document.getElementById(button.dataset.copyStatus);
      const label = button.querySelector("span");
      if (!target || !status || !label || button.disabled) return;

      const originalLabel = label.textContent;
      button.disabled = true;

      try {
        await copyText(target.textContent.trim());
        label.textContent = "Copied";
        status.textContent = "Install command copied.";
        button.classList.add("is-copied");
      } catch {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(target);
        selection.removeAllRanges();
        selection.addRange(range);
        label.textContent = "Selected";
        status.textContent = "Command selected. Press Command-C or Control-C.";
      }

      window.setTimeout(() => {
        label.textContent = originalLabel;
        status.textContent = "";
        button.classList.remove("is-copied");
        button.disabled = false;
      }, 1800);
    });
  });
})();
```

- [ ] **Step 4: Run source and browser interaction checks**

Run:

```bash
python3 -m unittest \
  scripts.tests.test_pages_site.PagesSiteTests.test_review_gate_motion_and_accessibility_contract \
  scripts.tests.test_pages_site.PagesSiteTests.test_landing_critical_resources_stay_within_budget \
  -v
```

In a secure local browser context, activate each of the three copy buttons by keyboard and pointer. Confirm the matching live region announces success. Force Clipboard API failure and confirm the command is selected and the fallback message is announced. Disable JavaScript and confirm all copy text and the final gate/report composition remain visible.

- [ ] **Step 5: Commit the progressive enhancement**

```bash
git add site/index.html site/home.css site/site.js scripts/tests/test_pages_site.py
git commit -m "feat: add accessible evidence-gate motion"
```

---

### Task 5: Render the Report-Led Social Card

**Files:**
- Create: `scripts/assets/review-gate-social.html`
- Modify: `site/assets/review-gate-social.png`
- Modify: `site/index.html:13-26`
- Modify: `site/guides/will-apple-reject-ai-built-apps/index.html:13-27`
- Modify: `scripts/tests/test_pages_site.py:24-30`
- Modify: `scripts/tests/test_pages_site.py:146-160`

**Interfaces:**
- Consumes: Hubot Sans subset, responsive gate plate, report visual, exact proposition.
- Produces: a deterministic 1200×630 PNG and one shared `SOCIAL_CARD_ALT` string used by landing and guide metadata.

- [ ] **Step 1: Add failing social-card source and truth assertions**

Set:

```python
SOCIAL_CARD_ALT = (
    "App Store Review Skill evidence crossing a red review gate into a "
    "ParcelTrack report marked Not Ready"
)
SOCIAL_CARD_SOURCE = ROOT / "scripts" / "assets" / "review-gate-social.html"
```

Extend the social asset test:

```python
self.assertTrue(SOCIAL_CARD_SOURCE.is_file(), "social-card source is missing")
social_source = read(SOCIAL_CARD_SOURCE)
self.assertIn("Find the risk.", social_source)
self.assertIn("Prove the fix.", social_source)
self.assertIn("Camera flow has no purpose string", social_source)
self.assertIn("NOT READY", social_source)
self.assertNotIn("97%", social_source)
self.assertNotIn("99%", social_source)
self.assertNotIn("Apple logo", social_source)
self.assertLessEqual(SOCIAL_CARD.stat().st_size, 650_000)
```

Run the focused test. Expected: FAIL because the source file does not exist and current social metadata still uses the old alt text.

- [ ] **Step 2: Create the deterministic 1200×630 source**

Create `scripts/assets/review-gate-social.html` as a fixed canvas with no external network calls. It must use:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1200, initial-scale=1">
  <style>
    @font-face {
      font-family: "Hubot Sans";
      src: url("../../site/assets/fonts/Hubot-Sans-display.woff2") format("woff2-variations");
      font-weight: 200 900;
      font-stretch: 75% 125%;
    }
    * { box-sizing: border-box; }
    html, body { width: 1200px; height: 630px; margin: 0; overflow: hidden; }
    body { position: relative; background: #070a10; color: #fff; font-family: Arial, sans-serif; }
    .machine { position: absolute; inset: 0 0 0 430px; width: 770px; height: 630px; object-fit: cover; object-position: 72% center; opacity: 0.72; }
    .wordmark { position: absolute; top: 50px; left: 56px; font-size: 14px; font-weight: 700; letter-spacing: 0.08em; }
    h1 { position: absolute; top: 142px; left: 56px; z-index: 2; margin: 0; font-family: "Hubot Sans", sans-serif; font-size: 82px; font-weight: 850; letter-spacing: -0.04em; line-height: 0.82; }
    h1 span { display: block; white-space: nowrap; }
    h1 span:first-child { font-stretch: 78%; }
    h1 span:last-child { font-stretch: 112%; }
    .report { position: absolute; z-index: 3; right: 64px; bottom: 54px; width: 420px; padding: 28px; border-top: 7px solid #ff2748; background: #f6f3eb; color: #111318; box-shadow: 0 24px 70px rgb(0 0 0 / 42%); transform: rotate(-1deg); }
    .report-meta { display: flex; justify-content: space-between; font-size: 12px; text-transform: uppercase; }
    .verdict { display: flex; justify-content: space-between; gap: 20px; margin-top: 34px; padding-block: 20px; border-block: 1px solid rgb(17 19 24 / 28%); }
    .verdict strong { color: #c92d24; }
    .finding { margin: 22px 0 6px; font-size: 27px; font-weight: 700; line-height: 1.05; }
    .path { color: #62656c; font: 13px ui-monospace, monospace; }
    .tagline { position: absolute; left: 56px; bottom: 62px; width: 390px; color: rgb(255 255 255 / 72%); font-size: 18px; }
  </style>
</head>
<body>
  <img class="machine" src="../../site/assets/review-gate-cinematic-1440.webp" alt="">
  <div class="wordmark">APP STORE REVIEW SKILL</div>
  <h1><span>Find the risk.</span><span>Prove the fix.</span></h1>
  <p class="tagline">A read-only preflight for Codex and Claude Code.</p>
  <article class="report">
    <div class="report-meta"><span>ParcelTrack</span><span>Sample report</span></div>
    <div class="verdict"><span>Release verdict</span><strong>NOT READY</strong></div>
    <p class="finding">Camera flow has no purpose string</p>
    <p class="path">app.json:18 · Guideline 5.1.1(ii)</p>
  </article>
</body>
</html>
```

- [ ] **Step 3: Render and visually inspect the PNG**

Run from repository root:

```bash
npx --yes playwright@1.63.0 screenshot \
  --channel chrome \
  --viewport-size "1200,630" \
  "file://$PWD/scripts/assets/review-gate-social.html" \
  site/assets/review-gate-social.png
```

Inspect the resulting PNG at original size. Require all exact text to be sharp, the report to remain more prominent than the CGI checklist tile, and no crop through the red gate or report. If the render fails to load local assets, serve the repository root with `python3 -m http.server 4173` and capture `http://127.0.0.1:4173/scripts/assets/review-gate-social.html` instead; do not replace text with generated raster lettering.

- [ ] **Step 4: Synchronize social metadata**

In both the landing and guide, set `og:image:alt` and `twitter:image:alt` to:

```html
content="App Store Review Skill evidence crossing a red review gate into a ParcelTrack report marked Not Ready"
```

Keep the 1200×630 declarations and canonical social image URL unchanged.

- [ ] **Step 5: Verify and commit the social handoff**

Run:

```bash
python3 -m unittest \
  scripts.tests.test_pages_site.PagesSiteTests.test_review_gate_assets_and_install_interaction_are_publishable \
  scripts.tests.test_pages_site.PagesSiteTests.test_landing_page_has_indexable_product_contract \
  scripts.tests.test_pages_site.PagesSiteTests.test_ai_built_app_guide_states_apple_policy_without_inventing_a_ban \
  -v
git diff --check
```

Commit:

```bash
git add scripts/assets/review-gate-social.html \
  site/assets/review-gate-social.png \
  site/index.html \
  site/guides/will-apple-reject-ai-built-apps/index.html \
  scripts/tests/test_pages_site.py
git commit -m "feat: align social preview with the evidence gate"
```

---

### Task 6: Verify the Complete Experience and Close Review Findings

**Files:**
- Modify only when a verified defect requires it: `site/index.html`, `site/styles.css`, `site/home.css`, `site/site.js`, responsive/social assets, `scripts/tests/test_pages_site.py`
- Do not commit: `_site/`, Lighthouse JSON/HTML, screenshots, detector output, browser profiles, or temporary asset directories

**Interfaces:**
- Consumes: complete candidate from Tasks 1–5.
- Produces: fresh automated results, built-site route proof, desktop/mobile screenshots, performance/a11y measurements, deterministic detector result, and two independent visual reviews.

- [ ] **Step 1: Run the full local functional gate**

Run:

```bash
python3 -m unittest discover -s scripts/tests -v
python3 scripts/app_store_review_scan.py . --format json | python3 -m json.tool >/dev/null
git diff --check origin/main...HEAD
```

Expected: 67 or more tests PASS, scanner pipeline exits `0`, and diff check prints nothing. A lower test count requires investigation; do not describe it as complete.

- [ ] **Step 2: Assemble the exact Pages artifact outside the worktree**

Run:

```bash
landing_build_dir=$(mktemp -d /private/tmp/app-review-pages.XXXXXX)
mkdir -p "$landing_build_dir/app-store-review-skill/report" "$landing_build_dir/app-store-review-skill/assets"
cp -R site/. "$landing_build_dir/app-store-review-skill/"
cp examples/parceltrack-report.html "$landing_build_dir/app-store-review-skill/report/index.html"
cp examples/parceltrack-report.json "$landing_build_dir/app-store-review-skill/report/parceltrack-report.json"
cp examples/parceltrack-report.json "$landing_build_dir/app-store-review-skill/parceltrack-report.json"
cp assets/visual-report-example.png "$landing_build_dir/app-store-review-skill/assets/visual-report-example.png"
python3 -m http.server 4173 --bind 127.0.0.1 --directory "$landing_build_dir"
```

Run the server in a recorded terminal/session so it can be stopped after browser verification. Verify HTTP 200 for landing, report HTML, report JSON, policy guide, CSS, font, AVIF, WebP, and social PNG.

- [ ] **Step 3: Capture the bounded viewport matrix in one pass**

Create a temporary screenshot directory and run:

```bash
landing_shots_dir=$(mktemp -d /private/tmp/app-review-landing-shots.XXXXXX)
npx --yes playwright@1.63.0 screenshot --channel chrome --viewport-size "1440,900" --full-page \
  http://127.0.0.1:4173/app-store-review-skill/ "$landing_shots_dir/1440x900.png"
npx --yes playwright@1.63.0 screenshot --channel chrome --viewport-size "1280,800" --full-page \
  http://127.0.0.1:4173/app-store-review-skill/ "$landing_shots_dir/1280x800.png"
npx --yes playwright@1.63.0 screenshot --channel chrome --viewport-size "768,1024" --full-page \
  http://127.0.0.1:4173/app-store-review-skill/ "$landing_shots_dir/768x1024.png"
npx --yes playwright@1.63.0 screenshot --channel chrome --viewport-size "390,844" --full-page \
  http://127.0.0.1:4173/app-store-review-skill/ "$landing_shots_dir/390x844.png"
npx --yes playwright@1.63.0 screenshot --channel chrome --viewport-size "320,568" --full-page \
  http://127.0.0.1:4173/app-store-review-skill/ "$landing_shots_dir/320x568.png"
```

Inspect all five together. Check first-viewport action/proof placement, report legibility, section rhythm, nav persistence, focus-ring room, and absence of accidental card grids or ambient glow. Make one batched correction for every defect found, then repeat only the affected screenshots once.

- [ ] **Step 4: Run browser behavior and accessibility checks**

Use the browser-verification skill against the same local server and evaluate at 1440×900, 768×1024, 390×844, and 320×568:

```javascript
({
  viewport: [window.innerWidth, window.innerHeight],
  noHorizontalOverflow:
    document.documentElement.scrollWidth <= document.documentElement.clientWidth,
  primaryCtaCount: document.querySelectorAll(".button-primary").length,
  firstActionBottom: document.querySelector(".command-dock").getBoundingClientRect().bottom,
  reportFragmentBottom: document.querySelector(".hero-report-sheet").getBoundingClientRect().bottom,
  heroBottom: document.querySelector(".hero").getBoundingClientRect().bottom,
})
```

Require `noHorizontalOverflow: true`, `primaryCtaCount: 1`, and at 390×844 both `firstActionBottom` and `reportFragmentBottom` ≤ `844`.

Also verify:

- complete keyboard order and visible focus on both color fields;
- all three copy controls at ≥44×44 pixels with live-region feedback;
- 200% zoom without two-dimensional page scrolling;
- JavaScript disabled shows the final visual state and readable commands;
- reduced motion shows no entrance travel;
- reduced transparency removes overlays;
- increased contrast and forced colors keep states and focus visible;
- missing AVIF falls back to WebP; missing WebP falls back to PNG;
- image failure leaves the proposition, evidence packet, and report sheet understandable.

- [ ] **Step 5: Measure performance with recorded conditions**

Run Lighthouse against the local production-shaped artifact:

```bash
landing_lighthouse_dir=$(mktemp -d /private/tmp/app-review-lighthouse.XXXXXX)
npx --yes lighthouse@12.8.2 \
  http://127.0.0.1:4173/app-store-review-skill/ \
  --only-categories=performance,accessibility,best-practices,seo \
  --form-factor=mobile \
  --screenEmulation.mobile=true \
  --screenEmulation.width=390 \
  --screenEmulation.height=844 \
  --screenEmulation.deviceScaleFactor=1 \
  --chrome-flags="--headless --no-sandbox" \
  --output=json \
  --output-path="$landing_lighthouse_dir/report.json"
jq '{categories: (.categories | map_values(.score)), metrics: {
  lcp: .audits["largest-contentful-paint"].numericValue,
  cls: .audits["cumulative-layout-shift"].numericValue,
  tbt: .audits["total-blocking-time"].numericValue
}}' "$landing_lighthouse_dir/report.json"
```

Require all four category scores ≥0.95, LCP ≤2500 ms, and CLS ≤0.05 under this recorded run. Lighthouse lab output does not directly prove field INP; report INP as unmeasured rather than substituting TBT.

- [ ] **Step 6: Run the one allowed deterministic anti-slop scan**

Run exactly once on the final candidate:

```bash
/Users/eliemajorel/.codex/skills/impeccable/scripts/impeccable detect --json \
  --viewport 390x844 \
  http://127.0.0.1:4173/app-store-review-skill/ site/site.js
```

The URL target resolves the root-absolute stylesheets against the assembled site, avoiding the known local-file false-positive path. Classify every finding against rendered computed styles and source. Fix all actionable high-severity findings in the same batched correction used for visual review. Do not add blanket detector ignores or rerun the detector; record the initial result and verify corrections with the affected source/browser checks.

- [ ] **Step 7: Complete the two approved independent reviews**

Dispatch the approved final reviews independently:

1. Design review: judge specificity, ad-to-page handoff, evidence dominance, conversion hierarchy, and desktop/mobile composition without seeing detector findings first.
2. Skeptical review: inspect source, live browser evidence, performance/accessibility results, truth labels, overflow, and generic AI/security tropes.

Synthesize disagreements. Fix every validated high-severity issue and rerun only the affected automated/browser checks. The final branch cannot carry an unresolved high-severity finding.

- [ ] **Step 8: Run the final immutable gate and commit only verified corrections**

After all corrections, run fresh:

```bash
python3 -m unittest discover -s scripts/tests -v
python3 scripts/app_store_review_scan.py . --format json | python3 -m json.tool >/dev/null
git diff --check
git diff --cached --check
git diff --check origin/main...HEAD
git status --short --branch
```

If verification corrections changed tracked files, commit them as one bounded finish commit:

```bash
git add site scripts/tests/test_pages_site.py
git diff --cached --check
git commit -m "fix: close landing verification findings"
git status --short --branch
```

If there is no tracked correction, do not create an empty commit. Stop the local HTTP server. Confirm no `_site`, screenshot, Lighthouse, detector, browser-profile, or temporary-generation artifact is present in `git status`.

Do not merge or deploy in this task. Hand off the exact branch head, commits, test counts, scanner result, Lighthouse environment/results, screenshot paths, detector findings, independent-review verdicts, and any remaining unknowns for the explicit merge decision.

---

## Plan Acceptance Checklist

- [ ] Task 1 supplies licensed assets and enforces the font/image budgets.
- [ ] Task 2 implements every narrative act, approved copy block, claim boundary, and exact section order.
- [ ] Task 3 makes the report the dominant body artifact, splits shared and landing CSS, and recomposes mobile rather than stacking it.
- [ ] Task 4 implements one non-looping transformation, no-JavaScript final state, and accessible clipboard feedback.
- [ ] Task 5 aligns the social handoff without generated text, Apple marks, or context-free metrics.
- [ ] Task 6 covers routes, automated tests, real browser sizes, zoom/preferences, performance, anti-slop detection, and two independent critiques.
- [ ] No task changes the skill, scanner, report schema/output, registry state, campaign, README art, or deployment state.
