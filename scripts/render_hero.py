from __future__ import annotations

from functools import cache
from math import pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

WIDTH = 1280
HEIGHT = 360
FPS = 20
FRAME_COUNT = FPS * 5
DURATION_MS = 1000 // FPS

BG = "#070A09"
OFF_WHITE = "#F4F3ED"
MUTED = "#7A8681"
MINT = "#71F6C6"
VIOLET = "#8E7CFF"
CORAL = "#FF6B4A"
BORDER = "#25302C"

FONT_ROOT = Path("C:/Windows/Fonts")
DISPLAY_FONT = FONT_ROOT / "segoeuib.ttf"
MONO_FONT = FONT_ROOT / "consola.ttf"


@cache
def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise FileNotFoundError(f"Required font is missing: {path}")
    return ImageFont.truetype(str(path), size)


@cache
def rounded_alpha() -> Image.Image:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, WIDTH - 1, HEIGHT - 1), radius=22, fill=255
    )
    return mask


def ribbon_mask(frame: int) -> Image.Image:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    upper = []
    lower = []
    time = frame / FRAME_COUNT * 2 * pi
    for x in range(0, WIDTH + 1, 8):
        wave = sin(x / 118 + time) * 11 + sin(x / 51 - time * 1.3) * 5
        thickness = 34 + sin(x / 83 + time * 0.7) * 5
        center = 166 + wave
        upper.append((x, int(center - thickness)))
        lower.append((x, int(center + thickness)))
    ImageDraw.Draw(mask).polygon(upper + list(reversed(lower)), fill=255)
    return mask


@cache
def ribbon_gradient() -> Image.Image:
    colors = ((113, 246, 198), (142, 124, 255), (255, 107, 74))
    strip = Image.new("RGBA", (WIDTH, 1))
    pixels = strip.load()
    for x in range(WIDTH):
        position = x / (WIDTH - 1) * 2
        index = min(1, int(position))
        mix = position - index
        start, end = colors[index], colors[index + 1]
        pixels[x, 0] = tuple(
            int(a + (b - a) * mix) for a, b in zip(start, end)
        ) + (255,)
    return strip.resize((WIDTH, HEIGHT))


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    for x in range(0, WIDTH, 64):
        draw.line((x, 0, x, HEIGHT), fill=(25, 34, 31, 90), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line((0, y, WIDTH, y), fill=(25, 34, 31, 90), width=1)


def draw_ribbon(image: Image.Image, frame: int) -> None:
    mask = ribbon_mask(frame)
    glow_alpha = mask.filter(ImageFilter.GaussianBlur(22)).point(
        lambda value: value // 4
    )
    glow = Image.new("RGBA", image.size, (113, 246, 198, 0))
    glow.putalpha(glow_alpha)
    image.alpha_composite(glow)
    signal = ribbon_gradient().copy()
    signal.putalpha(mask)
    image.alpha_composite(signal)


def draw_top_copy(draw: ImageDraw.ImageDraw) -> None:
    mono = font(MONO_FONT, 17)
    draw.text((52, 34), "YI HAN / AI AUTOMATION ENGINEER", font=mono, fill=MINT)
    draw.text((1228, 34), "AUCKLAND · NZ", font=mono, fill=MUTED, anchor="ra")
    draw.line((52, 72, 1228, 72), fill=BORDER, width=1)


def draw_bottom_copy(draw: ImageDraw.ImageDraw) -> None:
    display = font(DISPLAY_FONT, 49)
    mono = font(MONO_FONT, 15)
    draw.text((52, 252), "TURN FRICTION INTO", font=display, fill=OFF_WHITE)
    prefix_width = draw.textlength("TURN FRICTION INTO ", font=display)
    draw.text((52 + prefix_width, 252), "FLOW.", font=display, fill=MINT)
    draw.text(
        (1228, 258), "AI → SYSTEMS → ACTION", font=mono, fill=OFF_WHITE, anchor="ra"
    )
    draw.text(
        (1228, 286), "CURRENT MODE / BUILDING", font=mono, fill=MUTED, anchor="ra"
    )
    draw.line((52, 328, 1228, 328), fill=BORDER, width=1)


def make_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_grid(draw)
    draw_ribbon(image, frame)
    draw_top_copy(draw)
    draw_bottom_copy(draw)
    image.putalpha(rounded_alpha())
    return image


def quantize(image: Image.Image) -> Image.Image:
    opaque = Image.new("RGB", image.size, BG)
    opaque.paste(image.convert("RGB"), mask=image.getchannel("A"))
    palette_image = opaque.quantize(colors=96, method=Image.Quantize.MEDIANCUT)
    transparent = image.getchannel("A").point(lambda value: 255 if value == 0 else 0)
    palette_image.paste(255, mask=transparent)
    return palette_image


def render_assets(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = [quantize(make_frame(index)) for index in range(FRAME_COUNT)]
    gif_path = output_dir / "hero.gif"
    png_path = output_dir / "hero-static.png"
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
        transparency=255,
    )
    make_frame(25).save(png_path, optimize=True)
    return gif_path, png_path


if __name__ == "__main__":
    gif, still = render_assets(Path("assets"))
    print(f"Rendered {gif} and {still}")
