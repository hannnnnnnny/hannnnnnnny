import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.render_hero import FPS, FRAME_COUNT, make_frame, render_assets


class RenderHeroTests(unittest.TestCase):
    def test_prompt_never_enters_manifesto_safe_area(self) -> None:
        prompt_fill = (17, 19, 19)
        for frame_number in range(FRAME_COUNT):
            frame = make_frame(frame_number)
            safe_area = frame.crop((40, 80, 720, 330))
            prompt_pixels = sum(
                pixel == prompt_fill for pixel in safe_area.get_flattened_data()
            )
            self.assertEqual(prompt_pixels, 0, f"overlap at frame {frame_number}")

    def test_right_status_area_has_visual_content(self) -> None:
        frame = make_frame(55)
        right_area = frame.crop((760, 55, 1230, 330))
        background = (8, 9, 9)
        content_pixels = sum(
            pixel != background for pixel in right_area.get_flattened_data()
        )
        self.assertGreater(content_pixels, 15_000)

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
