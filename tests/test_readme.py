import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


class ReadmeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = README.read_text(encoding="utf-8")

    def test_required_identity_and_projects_are_present(self) -> None:
        required = [
            "Hey, I'm Yi Han.",
            "AI-assisted products",
            "KiwiCue",
            "PanSub",
            "Till Tally",
        ]
        for value in required:
            self.assertIn(value, self.text)

    def test_local_images_exist_and_have_alt_text(self) -> None:
        images = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", self.text)
        self.assertGreaterEqual(len(images), 1)
        for alt, relative_path in images:
            self.assertTrue(alt.strip())
            self.assertTrue((ROOT / relative_path).exists())

    def test_approved_links_are_exact(self) -> None:
        links = [
            "https://github.com/hannnnnnnny/kiwicue",
            "https://github.com/hannnnnnnny/pansub",
            "https://github.com/hannnnnnnny/till-tally",
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

    def test_projects_use_a_structured_visual_table(self) -> None:
        self.assertIn("<table>", self.text)
        self.assertEqual(self.text.count("<tr>"), 3)
        for number in ("01", "02", "03"):
            self.assertIn(f"<strong>{number}</strong>", self.text)


if __name__ == "__main__":
    unittest.main()
