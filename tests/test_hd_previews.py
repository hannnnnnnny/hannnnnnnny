import unittest
from PIL import Image
from scripts.render_project_previews import ROOT, PROJECTS


class HDPreviewTests(unittest.TestCase):
    def test_published_cards_are_retina_full_colour_pngs(self):
        for project in PROJECTS:
            path = ROOT / "assets" / project[0].replace(".svg", "-hd.png")
            with self.subTest(project=project[2]), Image.open(path) as image:
                self.assertEqual(image.size, (1920, 920))
                self.assertEqual(image.mode, "RGBA")
                self.assertEqual(image.format, "PNG")
                self.assertEqual(image.getpixel((0, 0))[3], 0)
                self.assertGreater(len(image.getcolors(1920*920)), 256)
