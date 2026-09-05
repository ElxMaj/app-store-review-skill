import gzip
import json
import re
import struct
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
SITE_URL = "https://elxmaj.github.io/app-store-review-skill/"
GUIDE_PATH = "guides/will-apple-reject-ai-built-apps/"
X_CAMPAIGN = ROOT / "docs" / "launch" / "2026-09-03-x-app-review-campaign.json"
X_CAMPAIGN_DOC = ROOT / "docs" / "launch" / "2026-09-03-x-app-review-campaign.md"
X_CREATIVE_FILENAME = "x-app-review-preflight-v3.png"
X_CREATIVE_WEB_PATH = f"/app-store-review-skill/assets/{X_CREATIVE_FILENAME}"
X_CREATIVE_ALT = (
    "3D App Store Review graphic reading ‘REJECTED? Find risks first,’ with a "
    "blue checklist tile colliding with a red warning symbol among privacy and "
    "purchase icons, leading toward a green check"
)
X_CREATIVE = SITE / "assets" / X_CREATIVE_FILENAME
SOCIAL_CARD_FILENAME = "review-gate-social.png"
SOCIAL_CARD_WEB_PATH = f"/app-store-review-skill/assets/{SOCIAL_CARD_FILENAME}"
SOCIAL_CARD_ALT = (
    "A luminous review gate turning iOS project evidence into an inspectable "
    "App Store review report"
)
SOCIAL_CARD = SITE / "assets" / SOCIAL_CARD_FILENAME
README_HERO = ROOT / "assets" / "review-gate-hero.png"
CINEMATIC_ART = SITE / "assets" / "review-gate-cinematic.png"
SITE_MARK = SITE / "assets" / "review-gate-mark.svg"
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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def json_ld_documents(html: str) -> list[dict]:
    blocks = re.findall(
        r'<script\s+type="application/ld\+json">(.*?)</script>',
        html,
        flags=re.DOTALL,
    )
    return [json.loads(block) for block in blocks]


def graph_nodes(documents: list[dict]) -> list[dict]:
    nodes: list[dict] = []
    for document in documents:
        if "@graph" in document:
            nodes.extend(document["@graph"])
        else:
            nodes.append(document)
    return nodes


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"{path} is not a valid PNG")
    return struct.unpack(">II", data[16:24])


def assert_asset_signature(testcase, path: Path, signature: bytes) -> None:
    data = path.read_bytes()[:16]
    if signature == b"WEBP":
        testcase.assertEqual(b"RIFF", data[:4])
        testcase.assertEqual(b"WEBP", data[8:12])
    elif signature == b"ftypavif":
        testcase.assertIn(data[4:12], (b"ftypavif", b"ftypavis"))
    else:
        testcase.assertTrue(data.startswith(signature))


def gzip_size(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), compresslevel=9, mtime=0))


class PagesSiteTests(unittest.TestCase):
    def test_landing_page_has_indexable_product_contract(self):
        landing_path = SITE / "index.html"
        self.assertTrue(landing_path.is_file(), "site/index.html is missing")
        landing = read(landing_path)

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
        for property_name in ("og:title", "og:description", "og:url", "og:image"):
            with self.subTest(property_name=property_name):
                self.assertIn(f'<meta property="{property_name}"', landing)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', landing)
        social_image = f"{SITE_URL}assets/{SOCIAL_CARD_FILENAME}"
        self.assertIn(f'<meta property="og:image" content="{social_image}">', landing)
        self.assertIn(f'<meta name="twitter:image" content="{social_image}">', landing)
        self.assertIn(
            f'<meta name="twitter:image:alt" content="{SOCIAL_CARD_ALT}">',
            landing,
        )

        visible_text = re.sub(r"<[^>]+>", " ", landing)
        visible_text = re.sub(r"\s+", " ", visible_text)
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
                self.assertIn(visible_claim, visible_text)

        self.assertEqual(1, landing.count('class="button button-primary"'))
        self.assertIn(
            'class="button button-primary" href="#install">Run the preflight</a>',
            landing,
        )
        self.assertNotIn("Star on GitHub", landing)
        self.assertNotIn("Security scan passed", landing)
        self.assertNotIn('class="hero-proof"', landing)
        self.assertNotIn("98% impact", landing)
        self.assertNotIn("low-severity W011", landing)

        section_order = (
            "report",
            "method",
            "install",
            "modes",
            "evaluation",
            "policy",
            "faq",
            "close",
        )
        positions = [landing.index(f'id="{section_id}"') for section_id in section_order]
        self.assertEqual(sorted(positions), positions)

        self.assertIn("Tessl evaluation · v1.2.2", landing)
        self.assertIn(
            '<time datetime="2026-09-03">Last scored 3 September 2026</time>',
            landing,
        )
        self.assertNotIn("aggregateRating", landing)
        self.assertNotIn("approval rate</strong>", landing)

        self.assertIn('href="https://github.com/ElxMaj/app-store-review-skill"', landing)
        self.assertIn(f'href="/app-store-review-skill/{GUIDE_PATH}"', landing)
        self.assertIn('href="/app-store-review-skill/report/"', landing)
        self.assertIn(
            "Apple’s published guidelines do not name AI-written code as a rejection category",
            landing,
        )
        self.assertNotIn("AI code is not the review category", landing)

    def test_landing_json_ld_uses_supported_source_truth(self):
        landing = read(SITE / "index.html")
        nodes = graph_nodes(json_ld_documents(landing))
        by_type = {node["@type"]: node for node in nodes}

        self.assertEqual({"WebSite", "SoftwareSourceCode", "FAQPage"}, set(by_type))
        software = by_type["SoftwareSourceCode"]
        self.assertEqual("App Store Review Skill", software["name"])
        self.assertEqual("1.2.2", software["version"])
        self.assertEqual(
            "https://github.com/ElxMaj/app-store-review-skill",
            software["codeRepository"],
        )
        self.assertEqual(
            "https://github.com/ElxMaj/app-store-review-skill/blob/main/LICENSE",
            software["license"],
        )
        serialized = json.dumps(nodes)
        self.assertNotIn("aggregateRating", serialized)
        self.assertNotIn('"review"', serialized)

        visible_text = re.sub(r"<[^>]+>", " ", landing)
        visible_text = re.sub(r"\s+", " ", visible_text)
        for item in by_type["FAQPage"]["mainEntity"]:
            with self.subTest(question=item["name"]):
                self.assertIn(item["name"], visible_text)
                self.assertIn(item["acceptedAnswer"]["text"], visible_text)

    def test_ai_built_app_guide_states_apple_policy_without_inventing_a_ban(self):
        guide_path = SITE / GUIDE_PATH / "index.html"
        self.assertTrue(guide_path.is_file(), f"{guide_path.relative_to(ROOT)} is missing")
        guide = read(guide_path)

        expected_url = f"{SITE_URL}{GUIDE_PATH}"
        self.assertEqual(1, len(re.findall(r"<h1(?:\s|>)", guide)))
        self.assertIn("<h1>Will Apple reject an AI-built app?</h1>", guide)
        self.assertIn(f'<link rel="canonical" href="{expected_url}">', guide)
        social_image = f"{SITE_URL}assets/{SOCIAL_CARD_FILENAME}"
        self.assertIn(f'<meta property="og:image" content="{social_image}">', guide)
        self.assertIn(f'<meta name="twitter:image" content="{social_image}">', guide)
        self.assertIn(
            f'<meta name="twitter:image:alt" content="{SOCIAL_CARD_ALT}">',
            guide,
        )
        self.assertIn("AI-generated code is not a named rejection category", guide)
        for topic in ("Guideline 4.2.6", "Guideline 4.3(a)", "Guideline 4.3(b)"):
            with self.subTest(topic=topic):
                self.assertIn(topic, guide)
        self.assertIn(
            'href="https://developer.apple.com/app-store/review/guidelines/#minimum-functionality"',
            guide,
        )
        self.assertIn(
            'href="https://developer.apple.com/app-store/review/guidelines/#spam"',
            guide,
        )
        self.assertIn("Last checked against Apple’s guidelines: September 2, 2026", guide)
        self.assertIn("does not guarantee approval", guide)
        self.assertNotIn("Not because a coding assistant wrote the source", guide)
        self.assertIn(
            '<meta property="article:modified_time" content="2026-09-04">',
            guide,
        )

        nodes = graph_nodes(json_ld_documents(guide))
        article = next(node for node in nodes if node["@type"] == "Article")
        self.assertEqual("2026-09-02", article["datePublished"])
        self.assertEqual("2026-09-04", article["dateModified"])
        self.assertEqual(expected_url, article["mainEntityOfPage"])

    def test_review_gate_assets_and_install_interaction_are_publishable(self):
        landing = read(SITE / "index.html")
        guide = read(SITE / GUIDE_PATH / "index.html")
        readme = read(ROOT / "README.md")

        self.assertTrue(README_HERO.is_file(), "README review-gate hero is missing")
        self.assertEqual((1440, 760), png_dimensions(README_HERO))
        self.assertIn("assets/review-gate-hero.png", readme)

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
        self.assertNotIn("38 CHECKS", landing)

        self.assertTrue(SOCIAL_CARD.is_file(), "social preview card is missing")
        self.assertEqual((1200, 630), png_dimensions(SOCIAL_CARD))
        self.assertIn(SOCIAL_CARD_WEB_PATH, landing)

        self.assertTrue(SITE_MARK.is_file(), "review-gate site mark is missing")
        mark_root = ET.parse(SITE_MARK).getroot()
        self.assertEqual("0 0 64 64", mark_root.attrib.get("viewBox"))
        mark_path = "/app-store-review-skill/assets/review-gate-mark.svg"
        for page in (landing, guide):
            self.assertIn(f'<link rel="icon" href="{mark_path}" type="image/svg+xml">', page)

        script_path = SITE / "site.js"
        self.assertTrue(script_path.is_file(), "progressive install interaction is missing")
        self.assertIn(
            '<script src="/app-store-review-skill/site.js" defer></script>',
            landing,
        )
        copy_target = re.search(r'<button[^>]+data-copy-target="([^"]+)"', landing)
        self.assertIsNotNone(copy_target, "install command has no copy control")
        self.assertIn(f'id="{copy_target.group(1)}"', landing)

    def test_review_gate_motion_and_accessibility_contract(self):
        landing = read(SITE / "index.html")

        self.assertIn('class="gate-sequence" aria-hidden="true"', landing)
        self.assertIn("data-gate-sequence", landing)
        self.assertIn('class="evidence-packet"', landing)
        self.assertIn('class="hero-report-sheet"', landing)
        self.assertIn("Camera flow has no purpose string", landing)
        self.assertIn("app.json:18", landing)
        self.assertIn('aria-live="polite"', landing)
        self.assertIn('href="#install"', landing)
        for section_id in (
            "report",
            "method",
            "install",
            "modes",
            "evaluation",
            "policy",
            "faq",
            "close",
        ):
            with self.subTest(section_id=section_id):
                self.assertIn(f'id="{section_id}"', landing)

        shared_css = read(SITE / "styles.css")
        home_css = read(HOME_CSS)

        self.assertIn('href="/app-store-review-skill/home.css"', landing)
        self.assertIn("@font-face", home_css)
        self.assertIn('font-family: "Hubot Sans"', home_css)
        self.assertIn("font-stretch: 75% 125%", home_css)
        self.assertIn("font-stretch: 78%", home_css)
        self.assertIn("font-stretch: 112%", home_css)
        self.assertIn("@media (max-width: 1279px)", home_css)
        self.assertIn("@media (max-width: 767px)", home_css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", home_css)
        self.assertIn("@media (prefers-reduced-transparency: reduce)", home_css)
        self.assertIn("@media (prefers-contrast: more)", home_css)
        self.assertIn("@media (forced-colors: active)", home_css)
        self.assertNotIn("transition: all", shared_css + home_css)
        self.assertNotIn("backdrop-filter", home_css)
        self.assertNotIn(".hero-proof", home_css)
        self.assertIn(".article-shell", shared_css)
        self.assertNotIn(".hero-surface", shared_css)

        site_js = read(SITE / "site.js")
        self.assertIn('document.documentElement.classList.add("has-js")', landing)
        self.assertIn("@keyframes evidence-enter", home_css)
        self.assertIn("@keyframes gate-scan", home_css)
        self.assertIn("@keyframes report-resolve", home_css)
        self.assertNotIn("infinite", home_css)
        self.assertIn('data-copy-status="hero-copy-status"', landing)
        self.assertIn('data-copy-status="install-copy-status"', landing)
        self.assertIn('data-copy-status="close-copy-status"', landing)
        self.assertIn('status.textContent = "Install command copied."', site_js)
        self.assertIn(
            'status.textContent = "Command selected. Press Command-C or Control-C."',
            site_js,
        )
        self.assertNotIn("setInterval", site_js)
        self.assertNotIn('addEventListener("scroll"', site_js)

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

    def test_crawl_and_llm_discovery_files_use_canonical_urls(self):
        robots = read(SITE / "robots.txt")
        self.assertIn("User-agent: *", robots)
        self.assertIn(f"Sitemap: {SITE_URL}sitemap.xml", robots)
        self.assertNotIn("Disallow: /", robots)

        sitemap_root = ET.fromstring(read(SITE / "sitemap.xml"))
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = {node.text for node in sitemap_root.findall("sm:url/sm:loc", namespace)}
        self.assertEqual(
            {
                SITE_URL,
                f"{SITE_URL}{GUIDE_PATH}",
                f"{SITE_URL}report/",
            },
            urls,
        )

        llms = read(SITE / "llms.txt")
        self.assertIn("# App Store Review Skill", llms)
        self.assertIn("Pre-submission audit", llms)
        self.assertIn("Rejection recovery", llms)
        self.assertIn("Human-craft audit", llms)
        self.assertIn("https://github.com/ElxMaj/app-store-review-skill/blob/main/SKILL.md", llms)
        self.assertIn(f"{SITE_URL}{GUIDE_PATH}", llms)

    def test_pages_workflow_publishes_site_and_moves_report_below_root(self):
        workflow = read(ROOT / ".github" / "workflows" / "pages.yml")

        self.assertIn('- "site/**"', workflow)
        self.assertIn("cp -R site/. _site/", workflow)
        self.assertIn("mkdir -p _site/report", workflow)
        self.assertIn("cp examples/parceltrack-report.html _site/report/index.html", workflow)
        self.assertIn(
            "cp examples/parceltrack-report.json _site/report/parceltrack-report.json",
            workflow,
        )
        self.assertIn(
            "cp examples/parceltrack-report.json _site/parceltrack-report.json",
            workflow,
        )
        self.assertIn(
            "cp assets/visual-report-example.png _site/assets/visual-report-example.png",
            workflow,
        )
        self.assertNotIn("cp examples/parceltrack-report.html _site/index.html", workflow)
        focused_test = "python3 -m unittest discover -s scripts/tests -p 'test_pages_site.py' -v"
        self.assertIn(focused_test, workflow)
        self.assertLess(workflow.index(focused_test), workflow.index("actions/upload-pages-artifact"))

    def test_readme_routes_people_to_product_page_and_report(self):
        readme = read(ROOT / "README.md")

        self.assertLessEqual(len(readme.splitlines()), 130)
        self.assertIn("[Product page](https://elxmaj.github.io/app-store-review-skill/)", readme)
        self.assertIn(
            "[Open the complete sample report](https://elxmaj.github.io/app-store-review-skill/report/)",
            readme,
        )
        self.assertIn(
            "[Inspect its source JSON](https://elxmaj.github.io/app-store-review-skill/report/parceltrack-report.json)",
            readme,
        )
        self.assertIn("[Star on GitHub](https://github.com/ElxMaj/app-store-review-skill)", readme)

    def test_growth_launch_package_is_draft_only_and_measurable(self):
        launch_path = ROOT / "docs" / "launch" / "2026-09-02-growth-launch.md"
        self.assertTrue(launch_path.is_file(), f"{launch_path.relative_to(ROOT)} is missing")
        launch = read(launch_path)

        for required in (
            "Draft only. Do not publish without action-time approval.",
            "10 genuine GitHub stars",
            "GitHub unique visitors",
            "Skills.sh installs",
            "ClaudePluginHub copy clicks",
            "W011",
            "r/ClaudeCode weekly showcase",
            "Product Hunt",
            "LinkedIn",
            "X",
            "Show HN",
        ):
            with self.subTest(required=required):
                self.assertIn(required, launch)
        self.assertNotRegex(launch.lower(), r"ask for (an |your )?(upvote|vote)s?")

        channel_sections = {
            heading: re.split(r"\n#{2,3} ", launch.split(heading, 1)[1], maxsplit=1)[0]
            for heading in (
                "### r/ClaudeCode weekly showcase comment",
                "### Product Hunt package",
                "### LinkedIn post",
                "### X post",
            )
        }
        for heading, section in channel_sections.items():
            with self.subTest(heading=heading):
                self.assertIn("not affiliated with Apple", section)

        x_post = channel_sections["### X post"].strip()
        self.assertLessEqual(len(x_post), 280)

    def test_x_campaign_payload_is_publishable_and_fail_closed(self):
        self.assertTrue(X_CAMPAIGN.is_file(), f"{X_CAMPAIGN.relative_to(ROOT)} is missing")
        payload = json.loads(read(X_CAMPAIGN))

        self.assertEqual("draft_only", payload["state"])
        self.assertFalse(payload["activation"]["authorized"])
        self.assertEqual(0, payload["activation"]["authorized_spend_eur"])
        self.assertTrue(payload["activation"]["requires_final_preview"])
        self.assertTrue(
            {
                "account_eligibility",
                "advertiser_handle",
                "funding_source",
                "start_at",
                "final_payload_confirmation",
            }.issubset(payload["activation"]["required_before_activation"])
        )

        campaign = payload["campaign"]
        self.assertEqual("website_traffic", campaign["objective"])
        self.assertEqual("link_clicks", campaign["optimization_goal"])
        self.assertEqual("link_clicks", campaign["pay_by"])
        self.assertEqual("autobid", campaign["bid_strategy"])
        self.assertEqual(15, campaign["daily_budget_eur"])
        self.assertEqual(7, campaign["duration_days"])
        self.assertEqual(105, campaign["planned_cap_eur"])

        audience = payload["audience"]
        keywords = audience["include_keywords"]
        self.assertGreaterEqual(len(keywords), 25)
        self.assertLessEqual(len(keywords), 50)
        self.assertEqual(len(keywords), len({keyword.casefold() for keyword in keywords}))
        self.assertFalse(audience["optimized_targeting"])
        self.assertFalse(
            {"ai", "codex", "claude code"}
            & {keyword.casefold() for keyword in keywords},
            "paid targeting must stay focused on App Store Review intent",
        )

        creatives = payload["creatives"]
        self.assertEqual(
            {"preflight", "rejection_recovery", "product_depth"},
            {creative["id"] for creative in creatives},
        )
        self.assertEqual(3, len(creatives))
        for creative in creatives:
            with self.subTest(creative=creative["id"]):
                copy = creative["post_copy"]
                self.assertLessEqual(len(copy), 257)
                self.assertIn("not affiliated with Apple", copy)
                self.assertNotRegex(
                    copy.casefold(),
                    r"guarantee(?:d)? approval|approval rate|detect(?:s|ion)? ai-written code",
                )
                self.assertLessEqual(len(creative["card_headline"]), 50)
                self.assertEqual(X_CREATIVE_WEB_PATH, creative["image_path"])
                self.assertEqual(X_CREATIVE_ALT, creative["alt_text"])

                destination = urlparse(creative["destination_url"])
                self.assertEqual("https", destination.scheme)
                self.assertEqual("elxmaj.github.io", destination.netloc)
                self.assertEqual("/app-store-review-skill/", destination.path)
                query = parse_qs(destination.query)
                self.assertEqual(["x"], query.get("utm_source"))
                self.assertEqual(["paid_social"], query.get("utm_medium"))
                self.assertEqual(["app_store_review_preflight"], query.get("utm_campaign"))
                self.assertEqual([creative["id"]], query.get("utm_content"))

        measurement = payload["measurement"]
        self.assertFalse(measurement["x_pixel_enabled"])
        self.assertEqual(50, measurement["review_after_spend_eur"])
        self.assertEqual(25, measurement["minimum_clicks_at_review"])
        self.assertEqual(3, measurement["minimum_adoption_signals_at_completion"])

    def test_x_campaign_creative_matches_declared_png_contract(self):
        self.assertTrue(X_CREATIVE.is_file(), f"{X_CREATIVE.relative_to(ROOT)} is missing")
        dimensions = png_dimensions(X_CREATIVE)
        self.assertEqual((1200, 628), dimensions)
        self.assertLessEqual(X_CREATIVE.stat().st_size, 5_000_000)
        xmp_height = re.search(
            rb"<exif:PixelYDimension>(\d+)</exif:PixelYDimension>",
            X_CREATIVE.read_bytes(),
        )
        if xmp_height:
            self.assertEqual(str(dimensions[1]).encode(), xmp_height.group(1))

    def test_x_campaign_markdown_matches_json_source_of_truth(self):
        payload = json.loads(read(X_CAMPAIGN))
        campaign_doc = read(X_CAMPAIGN_DOC)

        self.assertIn(
            "The JSON campaign file is the source of truth for every exact payload value.",
            campaign_doc,
        )
        self.assertNotIn("Rotate all three creatives evenly", campaign_doc)
        self.assertIn("Launch all three creatives together", campaign_doc)
        self.assertIn("delivery is algorithmic", campaign_doc)

        campaign = payload["campaign"]
        for expected_setting in (
            f"| Daily budget | EUR {campaign['daily_budget_eur']} |",
            f"| Duration | {campaign['duration_days']} days |",
            f"| Planned maximum | EUR {campaign['planned_cap_eur']} |",
        ):
            with self.subTest(expected_setting=expected_setting):
                self.assertIn(expected_setting, campaign_doc)

        for creative in payload["creatives"]:
            with self.subTest(creative=creative["id"]):
                self.assertIn(f"> {creative['post_copy']}", campaign_doc)
                self.assertIn(
                    f"**Card headline:** {creative['card_headline']}",
                    campaign_doc,
                )
                self.assertIn(
                    f"**Destination:** `{creative['destination_url']}`",
                    campaign_doc,
                )
                self.assertIn(creative["alt_text"], campaign_doc)

        for keyword in (
            payload["audience"]["include_keywords"]
            + payload["audience"]["exclude_keywords"]
        ):
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, campaign_doc)


if __name__ == "__main__":
    unittest.main()
