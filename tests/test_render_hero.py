import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import render_hero
from scripts.render_hero import DURATION_MS, FRAME_COUNT, make_frame, render_assets


class RenderHeroTests(unittest.TestCase):
    def test_left_action_uses_supported_ascii_glyphs(self) -> None:
        action = getattr(render_hero, "LEFT_ACTION", None)

        self.assertEqual(action, "VIEW SELECTED WORK")
        self.assertTrue(action.isascii())

    def test_split_hero_uses_approved_canvas(self) -> None:
        frame = make_frame(25)

        self.assertEqual(frame.size, (1280, 720))
        self.assertEqual(frame.mode, "RGBA")

    def test_frame_has_transparent_rounded_corners(self) -> None:
        frame = make_frame(0)

        self.assertEqual(frame.mode, "RGBA")
        self.assertEqual(frame.getpixel((0, 0))[3], 0)
        self.assertEqual(frame.getpixel((22, 22))[3], 255)

    def test_signals_stay_above_portrait_headline(self) -> None:
        mint_mask = getattr(render_hero, "mint_signal_mask", None)
        violet_mask = getattr(render_hero, "violet_signal_mask", None)
        self.assertTrue(callable(mint_mask))
        self.assertTrue(callable(violet_mask))
        headline_box = (790, 330, 1185, 515)

        for frame_number in range(FRAME_COUNT):
            self.assertIsNone(mint_mask(frame_number).crop(headline_box).getbbox())
            self.assertIsNone(violet_mask(frame_number).crop(headline_box).getbbox())

    def test_violet_signal_is_visible_in_portrait_card(self) -> None:
        frame = make_frame(25)
        violet_mask = getattr(render_hero, "violet_signal_mask", None)
        self.assertTrue(callable(violet_mask))
        mask = violet_mask(25)
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
            self.assertEqual(gif_path.name, "hero-split.gif")
            self.assertEqual(png_path.name, "hero-split-static.png")
            self.assertLessEqual(gif_path.stat().st_size, 5 * 1024 * 1024)

            with Image.open(gif_path) as animation:
                self.assertEqual(animation.size, (1280, 720))
                self.assertEqual(animation.n_frames, FRAME_COUNT)
                self.assertEqual(animation.info["duration"], DURATION_MS)
                self.assertEqual(animation.convert("RGBA").getpixel((0, 0))[3], 0)

            with Image.open(png_path) as still:
                self.assertEqual(still.size, (1280, 720))
                self.assertEqual(still.getpixel((0, 0))[3], 0)


if __name__ == "__main__":
    unittest.main()
