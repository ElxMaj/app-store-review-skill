import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
SITE_URL = "https://elxmaj.github.io/app-store-review-skill/"
GUIDE_PATH = "guides/will-apple-reject-ai-built-apps/"


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


class PagesSiteTests(unittest.TestCase):
    def test_landing_page_has_indexable_product_contract(self):
        landing_path = SITE / "index.html"
        self.assertTrue(landing_path.is_file(), "site/index.html is missing")
        landing = read(landing_path)

        self.assertEqual(1, len(re.findall(r"<h1(?:\s|>)", landing)))
        self.assertIn("<h1>App Store review for Codex and Claude Code</h1>", landing)
        self.assertIn(f'<link rel="canonical" href="{SITE_URL}">', landing)
        self.assertRegex(landing, r'<meta name="description" content="[^\"]{140,180}">')
        for property_name in ("og:title", "og:description", "og:url", "og:image"):
            with self.subTest(property_name=property_name):
                self.assertIn(f'<meta property="{property_name}"', landing)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', landing)

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


if __name__ == "__main__":
    unittest.main()
