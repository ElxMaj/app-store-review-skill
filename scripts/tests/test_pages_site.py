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
X_CREATIVE = SITE / "assets" / "x-app-review-preflight.png"


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


class PagesSiteTests(unittest.TestCase):
    def test_landing_page_has_indexable_product_contract(self):
        landing_path = SITE / "index.html"
        self.assertTrue(landing_path.is_file(), "site/index.html is missing")
        landing = read(landing_path)

        self.assertEqual(1, len(re.findall(r"<h1(?:\s|>)", landing)))
        self.assertIn("<title>App Store Review preflight for iOS apps</title>", landing)
        self.assertIn("<h1>Find App Store Review risks before submission</h1>", landing)
        self.assertIn("Runs in Codex and Claude Code", landing)
        self.assertIn(f'<link rel="canonical" href="{SITE_URL}">', landing)
        self.assertRegex(landing, r'<meta name="description" content="[^\"]{140,180}">')
        for property_name in ("og:title", "og:description", "og:url", "og:image"):
            with self.subTest(property_name=property_name):
                self.assertIn(f'<meta property="{property_name}"', landing)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', landing)
        social_image = f"{SITE_URL}assets/x-app-review-preflight.png"
        social_image_alt = "App Store Review preflight with evidence-led release findings"
        self.assertIn(f'<meta property="og:image" content="{social_image}">', landing)
        self.assertIn(f'<meta name="twitter:image" content="{social_image}">', landing)
        self.assertIn(
            f'<meta name="twitter:image:alt" content="{social_image_alt}">',
            landing,
        )

        for visible_claim in (
            "npx skills add ElxMaj/app-store-review-skill",
            "Pre-submission audit",
            "Rejection recovery",
            "Human-craft audit",
            "97% quality",
            "98% impact",
            "low-severity W011",
            "Star on GitHub",
        ):
            with self.subTest(visible_claim=visible_claim):
                self.assertIn(visible_claim, landing)

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
        self.assertEqual("1.2.1", software["version"])
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
        social_image = f"{SITE_URL}assets/x-app-review-preflight.png"
        social_image_alt = "App Store Review preflight with evidence-led release findings"
        self.assertIn(f'<meta property="og:image" content="{social_image}">', guide)
        self.assertIn(f'<meta name="twitter:image" content="{social_image}">', guide)
        self.assertIn(
            f'<meta name="twitter:image:alt" content="{social_image_alt}">',
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

        nodes = graph_nodes(json_ld_documents(guide))
        article = next(node for node in nodes if node["@type"] == "Article")
        self.assertEqual("2026-09-02", article["datePublished"])
        self.assertEqual("2026-09-02", article["dateModified"])
        self.assertEqual(expected_url, article["mainEntityOfPage"])

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
                self.assertEqual(
                    "/app-store-review-skill/assets/x-app-review-preflight.png",
                    creative["image_path"],
                )
                self.assertTrue(creative["alt_text"].strip())

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
        self.assertEqual((1200, 628), png_dimensions(X_CREATIVE))
        self.assertLessEqual(X_CREATIVE.stat().st_size, 5_000_000)

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
