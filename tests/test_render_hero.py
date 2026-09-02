import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.render_hero import FPS, FRAME_COUNT, render_assets


class RenderHeroTests(unittest.TestCase):
    def test_rendered_assets_match_profile_constraints(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            gif_path, png_path = render_assets(Path(directory))

            self.assertTrue(gif_path.exists())
            self.assertTrue(png_path.exists())
            self.assertLessEqual(gif_path.stat().st_size, 5 * 1024 * 1024)

            with Image.open(gif_path) as animation:
                self.assertEqual(animation.size, (1280, 360))
                self.assertEqual(animation.n_frames, FRAME_COUNT)
                self.assertEqual(animation.info["duration"], 1000 // FPS)

            with Image.open(png_path) as still:
                self.assertEqual(still.size, (1280, 360))


if __name__ == "__main__":
    unittest.main()
