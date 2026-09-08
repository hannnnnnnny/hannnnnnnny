import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


class ReadmeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = README.read_text(encoding="utf-8")

    def test_approved_visual_assets_appear_once(self) -> None:
        assets = [
            "assets/hero-flow-motion.png",
        ]
        for asset in assets:
            self.assertEqual(self.text.count(asset), 1, asset)

    def test_identity_card_is_not_repeated_below_hero(self) -> None:
        self.assertNotIn("assets/identity.svg", self.text)

    def test_project_showcase_is_removed(self) -> None:
        self.assertNotIn("assets/project-", self.text)

    def test_old_stack_and_contact_cards_are_removed(self) -> None:
        self.assertNotIn("assets/stack.gif", self.text)
        self.assertNotIn("assets/contact.gif", self.text)

    def test_local_images_exist_and_have_alt_text(self) -> None:
        images = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", self.text)
        self.assertGreaterEqual(len(images), 1)
        for alt, relative_path in images:
            self.assertTrue(alt.strip())
            local_path = relative_path.split("?", 1)[0]
            self.assertTrue((ROOT / local_path).exists())

    def test_flow_hero_replaces_split_poster(self) -> None:
        self.assertIn(
            "assets/hero-flow-motion.png",
            self.text,
        )
        self.assertNotIn("assets/hero-split.gif", self.text)

    def test_approved_links_are_exact(self) -> None:
        links = [
            "https://hannnnnnnny.github.io/yi-han-software-engineer/",
            "https://www.linkedin.com/in/yi-han-29ab28323/",
            "mailto:harryhaber606@gmail.com",
        ]
        for link in links:
            self.assertIn(link, self.text)

    def test_dashboard_clutter_is_absent(self) -> None:
        banned = ["github-readme-stats", "streak-stats", "visitor-badge"]
        lowered = self.text.lower()
        for value in banned:
            self.assertNotIn(value, lowered)

    def test_layout_avoids_markdown_heavy_components(self) -> None:
        self.assertNotIn("<table", self.text.lower())
        self.assertNotIn("> **", self.text)


if __name__ == "__main__":
    unittest.main()
