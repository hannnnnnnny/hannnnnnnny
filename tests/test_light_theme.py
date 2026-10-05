"""The profile must read as a light theme with accessible contrast."""
import re
import unittest
from pathlib import Path

from PIL import Image, ImageColor

from scripts import visual_tokens as tokens

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PUBLISHED_RENDERERS = (
    "render_hero.py",
    "render_sections.py",
    "animate_sections.py",
    "render_project_previews.py",
)
PUBLISHED_RASTERS = (
    "hero-split-static.png",
    "project-kiwicue-hd.png",
    "project-pansub-hd.png",
    "project-renova-hd.png",
    "stack.gif",
    "contact.gif",
)


def luminance(color: str | tuple[int, int, int]) -> float:
    rgb = ImageColor.getrgb(color) if isinstance(color, str) else color
    channels = []
    for value in rgb[:3]:
        c = value / 255
        channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(first: str, second: str) -> float:
    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


class LightThemeTests(unittest.TestCase):
    def test_backgrounds_are_light_not_black(self) -> None:
        for name in ("BG", "SURFACE", "PANEL"):
            self.assertGreater(luminance(getattr(tokens, name)), 0.85, name)

    def test_text_tokens_meet_wcag_aa_on_light_surfaces(self) -> None:
        for name in ("TEXT", "MUTED", "ACCENT", "VIOLET", "CORAL"):
            for surface in ("BG", "SURFACE"):
                ratio = contrast(getattr(tokens, name), getattr(tokens, surface))
                self.assertGreaterEqual(ratio, 4.5, f"{name} on {surface}: {ratio:.2f}")

    def test_accent_button_label_is_readable(self) -> None:
        self.assertGreaterEqual(contrast(tokens.ON_ACCENT, tokens.ACCENT), 4.5)

    def test_published_renderers_take_colours_from_tokens(self) -> None:
        for name in PUBLISHED_RENDERERS:
            source = (ROOT / "scripts" / name).read_text(encoding="utf-8")
            self.assertEqual(re.findall(r"#[0-9A-Fa-f]{6}\b", source), [], name)

    def test_published_images_have_light_dominant_background(self) -> None:
        for name in PUBLISHED_RASTERS:
            with self.subTest(asset=name), Image.open(ASSETS / name) as image:
                rgba = image.convert("RGBA")
                opaque = [
                    (count, pixel) for count, pixel
                    in rgba.getcolors(rgba.width * rgba.height)
                    if pixel[3] == 255
                ]
                _, dominant = max(opaque)
                self.assertGreater(luminance(dominant), 0.85, dominant)


if __name__ == "__main__":
    unittest.main()
