import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import render_hero
from scripts.render_hero import FPS, FRAME_COUNT, make_frame, render_assets


class RenderHeroTests(unittest.TestCase):
    def test_frame_has_transparent_rounded_corners(self) -> None:
        frame = make_frame(0)

        self.assertEqual(frame.mode, "RGBA")
        self.assertEqual(frame.getpixel((0, 0))[3], 0)
        self.assertEqual(frame.getpixel((22, 22))[3], 255)

    def test_liquid_ribbon_stays_between_text_safe_areas(self) -> None:
        ribbon_mask = getattr(render_hero, "ribbon_mask", None)
        self.assertIsNotNone(ribbon_mask)
        safe_boxes = ((40, 18, 760, 96), (40, 238, 780, 345))

        for frame_number in range(FRAME_COUNT):
            mask = ribbon_mask(frame_number)
            self.assertIsNotNone(mask.getbbox())
            for safe_box in safe_boxes:
                self.assertIsNone(
                    mask.crop(safe_box).getbbox(),
                    f"ribbon overlap at frame {frame_number}",
                )

    def test_liquid_ribbon_is_visible_in_frame(self) -> None:
        frame = make_frame(25)
        mask = render_hero.ribbon_mask(25)
        pixels = zip(frame.get_flattened_data(), mask.get_flattened_data())
        violet_pixels = sum(
            alpha > 0 and blue - red > 45
            for (red, _green, blue, _alpha), alpha in pixels
        )

        self.assertGreater(violet_pixels, 2_000)

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
                self.assertEqual(animation.convert("RGBA").getpixel((0, 0))[3], 0)

            with Image.open(png_path) as still:
                self.assertEqual(still.size, (1280, 360))
                self.assertEqual(still.getpixel((0, 0))[3], 0)


if __name__ == "__main__":
    unittest.main()
