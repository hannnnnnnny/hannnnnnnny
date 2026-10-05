import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
VERSION = "?v=light-20261005"

# Published modules in reading order: hero, then three project cards.
SEQUENCE = [
    "assets/hero-split.gif",
    "assets/project-kiwicue-hd.png",
    "assets/project-pansub-hd.png",
    "assets/project-renova-hd.png",
]


class ReadmeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = README.read_text(encoding="utf-8")

    def test_full_light_sequence_appears_once_in_order(self) -> None:
        positions = []
        for asset in SEQUENCE:
            self.assertEqual(self.text.count(asset), 1, asset)
            self.assertIn(asset + VERSION, self.text, asset)
            positions.append(self.text.index(asset))
        self.assertEqual(positions, sorted(positions))

    def test_till_tally_is_not_featured(self) -> None:
        self.assertNotIn("till-tally", self.text.lower())

    def test_identity_card_is_not_repeated_below_hero(self) -> None:
        self.assertNotIn("assets/identity.svg", self.text)

    def test_project_cards_link_to_their_destinations(self) -> None:
        destinations = {
            "assets/project-kiwicue-hd.png": "https://kiwicue.nz",
            "assets/project-pansub-hd.png": "https://github.com/hannnnnnnny/pansub",
            "assets/project-renova-hd.png": "https://renova-marketplace.vercel.app",
        }
        for asset, href in destinations.items():
            pattern = rf"\[!\[[^\]]+\]\({re.escape(asset)}[^)]*\)\]\({re.escape(href)}\)"
            self.assertRegex(self.text, pattern, asset)

    def test_stack_and_contact_cards_are_removed(self) -> None:
        self.assertNotIn("assets/stack.gif", self.text)
        self.assertNotIn("assets/contact.gif", self.text)

    def test_local_images_exist_and_have_alt_text(self) -> None:
        images = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", self.text)
        self.assertEqual(len(images), len(SEQUENCE))
        for alt, relative_path in images:
            self.assertTrue(alt.strip())
            local_path = relative_path.split("?", 1)[0]
            self.assertTrue((ROOT / local_path).exists(), local_path)

    def test_old_dark_hero_version_is_gone(self) -> None:
        self.assertNotIn("neural-motion-20260905", self.text)
        self.assertNotIn("assets/hero-minimal.gif", self.text)
        self.assertNotIn("assets/hero-flow-motion.png", self.text)

    def test_approved_links_are_exact(self) -> None:
        links = [
            "https://hannnnnnnny.github.io/yi-han-software-engineer/",
            "https://www.linkedin.com/in/yi-han-29ab28323/",
            "mailto:harryhaber606@gmail.com",
            "https://github.com/hannnnnnnny/kiwicue",
            "https://github.com/hannnnnnnny/ReNova-Second-Hand-C2C-Marketplace",
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
