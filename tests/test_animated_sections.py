"""Check the published animations, not just their source renderers."""
import unittest
from pathlib import Path

from PIL import Image, ImageChops


ASSETS = Path(__file__).resolve().parents[1] / "assets"


class AnimatedSectionTests(unittest.TestCase):
    def test_animations_keep_copy_stable_and_corners_transparent(self):
        for name, height in (("project-kiwicue", 460), ("project-pansub", 460),
                             ("project-till-tally", 460), ("stack", 290),
                             ("contact", 220)):
            with self.subTest(name=name), Image.open(ASSETS / f"{name}.gif") as gif:
                self.assertEqual(gif.size, (960, height))
                self.assertEqual(gif.n_frames, 60)
                self.assertEqual(gif.info["loop"], 0)
                first = gif.convert("RGBA")
                for index in (20, 40, 59):
                    gif.seek(index)
                    frame = gif.convert("RGBA")
                    self.assertEqual(frame.getpixel((0, 0))[3], 0)
                    diff = ImageChops.difference(first.convert("RGB"), frame.convert("RGB"))
                    self.assertIsNotNone(diff.getbbox())
                    # Headings and descriptions must not blink or accumulate GIF trails.
                    self.assertIsNone(diff.crop((30, 25, 930, 120)).getbbox())


if __name__ == "__main__":
    unittest.main()
