import tempfile
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.render_sections import OUTPUTS, render_sections

SVG = "{http://www.w3.org/2000/svg}"


class SectionAssetTests(unittest.TestCase):
    def test_renderer_cli_runs_from_project_root(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "scripts/render_sections.py"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Rendered assets", result.stdout)

    def test_renderer_creates_every_approved_asset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            paths = render_sections(Path(directory))
            self.assertEqual({path.name for path in paths}, set(OUTPUTS))

    def test_assets_have_metadata_and_rounded_outer_card(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            for path in render_sections(Path(directory)):
                root = ET.parse(path).getroot()
                self.assertEqual(root.attrib["width"], "1280")
                self.assertTrue(root.attrib["viewBox"].startswith("0 0 1280 "))
                self.assertIsNotNone(root.find(f"{SVG}title"))
                self.assertIsNotNone(root.find(f"{SVG}desc"))
                outer = root.find(f"{SVG}rect")
                self.assertEqual(outer.attrib["rx"], "18")


if __name__ == "__main__":
    unittest.main()
