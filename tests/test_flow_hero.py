import unittest
from PIL import Image, ImageChops
from scripts.render_flow_hero import ROOT, FRAMES, frame_at


class FlowHeroTests(unittest.TestCase):
    def test_animation_preserves_type_and_full_colour(self):
        path = ROOT / 'assets/hero-flow-motion.png'
        self.assertLess(path.stat().st_size, 8_000_000)
        with Image.open(path) as animation, Image.open(ROOT / 'assets/hero-flow-source.png') as original:
            source = original.convert('RGB')
            self.assertEqual(animation.n_frames, FRAMES)
            self.assertEqual(animation.info['loop'], 0)
            for index in (0, 15, 30, 45, 59):
                animation.seek(index)
                decoded = animation.convert('RGB')
                self.assertIsNone(ImageChops.difference(decoded, frame_at(source,index/FRAMES)).getbbox())
                self.assertIsNone(ImageChops.difference(decoded,source).crop((0,0,1050,source.height)).getbbox())
            self.assertIsNone(ImageChops.difference(frame_at(source,0),frame_at(source,1)).getbbox())
