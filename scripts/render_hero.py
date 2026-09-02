from __future__ import annotations

from functools import cache
from math import pi, sin
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

WIDTH = 1280
HEIGHT = 720
FPS = 20
FRAME_COUNT = FPS * 5
DURATION_MS = 1000 // FPS

BG = "#0A0E13"
CARD = "#0C1116"
ART = "#060A09"
OFF_WHITE = "#F4F3ED"
MUTED = "#79837F"
MINT = "#71F6C6"
VIOLET = "#8E7CFF"
CORAL = "#FF6B4A"
BORDER = "#27332F"

CARD_BOX = (760, 35, 1240, 685)
ART_BOX = (780, 55, 1220, 515)
FONT_ROOT = Path("C:/Windows/Fonts")
DISPLAY_FONT = FONT_ROOT / "segoeuib.ttf"
REGULAR_FONT = FONT_ROOT / "segoeui.ttf"
MONO_FONT = FONT_ROOT / "consola.ttf"
LEFT_COPY = (
    "I design and build AI-assisted products that turn\n"
    "repetitive workflows into reliable systems."
)


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


@cache
def art_mask() -> Image.Image:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(mask).rounded_rectangle(ART_BOX, radius=22, fill=255)
    return mask


def signal_y(x: int, frame: int, lane: int) -> int:
    progress = (x - ART_BOX[0]) / (ART_BOX[2] - ART_BOX[0])
    time = frame / FRAME_COUNT * 2 * pi
    if lane == 0:
        base = 214 - 56 * progress - 24 * sin(progress * pi)
        motion = 5 * sin(time + progress * 2 * pi)
    else:
        base = 282 - 48 * progress - 18 * sin(progress * pi)
        motion = 6 * sin(time * 1.15 + progress * 2.3 * pi)
    return int(base + motion)


def signal_mask(frame: int, lane: int) -> Image.Image:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    points = [
        (x, signal_y(x, frame, lane))
        for x in range(ART_BOX[0], ART_BOX[2] + 1, 3)
    ]
    width = 8 if lane == 0 else 10
    ImageDraw.Draw(mask).line(points, fill=255, width=width, joint="curve")
    return ImageChops.multiply(mask, art_mask())


def mint_signal_mask(frame: int) -> Image.Image:
    return signal_mask(frame, 0)


def violet_signal_mask(frame: int) -> Image.Image:
    return signal_mask(frame, 1)


def draw_background(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((0, 0, WIDTH - 1, HEIGHT - 1), 22, fill=BG)
    for x in range(0, 720, 72):
        draw.line((x, 0, x, HEIGHT), fill=(21, 31, 29, 38))
    draw.ellipse((-190, 60, 620, 870), fill=(20, 64, 50, 22))


def draw_left_intro(draw: ImageDraw.ImageDraw) -> None:
    draw.text(
        (70, 90), "AI & AUTOMATION / AUCKLAND, NZ",
        font=font(MONO_FONT, 17), fill=MINT,
    )
    draw.text((68, 212), "Hi, I'm", font=font(DISPLAY_FONT, 78), fill=OFF_WHITE)
    draw.text((68, 298), "Yi Han.", font=font(DISPLAY_FONT, 78), fill=MINT)
    draw.multiline_text(
        (72, 424), LEFT_COPY, font=font(REGULAR_FONT, 24),
        fill=MUTED, spacing=11,
    )
    draw.text(
        (72, 560), "VIEW SELECTED WORK ↘",
        font=font(MONO_FONT, 16), fill=OFF_WHITE,
    )
    draw.line((72, 598, 232, 598), fill=MINT, width=2)


def draw_card_art(image: Image.Image) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.rectangle(ART_BOX, fill=ART)
    for x in range(ART_BOX[0], ART_BOX[2] + 1, 40):
        draw.line((x, ART_BOX[1], x, ART_BOX[3]), fill=(29, 48, 41, 105))
    for y in range(ART_BOX[1], ART_BOX[3] + 1, 40):
        draw.line((ART_BOX[0], y, ART_BOX[2], y), fill=(29, 48, 41, 105))
    layer.putalpha(art_mask())
    image.alpha_composite(layer)


def draw_signal(image: Image.Image, mask: Image.Image, color: tuple[int, int, int]) -> None:
    glow_alpha = mask.filter(ImageFilter.GaussianBlur(18)).point(
        lambda value: value // 2
    )
    glow_alpha = ImageChops.multiply(glow_alpha, art_mask())
    glow = Image.new("RGBA", image.size, color + (0,))
    glow.putalpha(glow_alpha)
    image.alpha_composite(glow)
    core = Image.new("RGBA", image.size, color + (255,))
    core.putalpha(mask)
    image.alpha_composite(core)


def draw_coral_tail(image: Image.Image, frame: int) -> None:
    mask = violet_signal_mask(frame)
    fade = Image.new("L", image.size, 0)
    pixels = fade.load()
    for x in range(1050, ART_BOX[2] + 1):
        alpha = int(255 * (x - 1050) / (ART_BOX[2] - 1050))
        ImageDraw.Draw(fade).line((x, 190, x, 310), fill=alpha)
    tail = ImageChops.multiply(mask, fade)
    layer = Image.new("RGBA", image.size, (255, 107, 74, 0))
    layer.putalpha(tail)
    image.alpha_composite(layer)


def draw_particle(image: Image.Image, frame: int) -> None:
    progress = frame / (FRAME_COUNT - 1)
    x = ART_BOX[0] + int(progress * (ART_BOX[2] - ART_BOX[0]))
    y = signal_y(x, frame, 0)
    opacity = int(255 * sin(progress * pi) ** 0.4)
    particle = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(particle, "RGBA")
    draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(113, 246, 198, opacity // 4))
    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(244, 243, 237, opacity))
    image.alpha_composite(particle.filter(ImageFilter.GaussianBlur(2)))


def draw_card_headline(draw: ImageDraw.ImageDraw) -> None:
    display = font(DISPLAY_FONT, 43)
    draw.text((806, 350), "TURN FRICTION", font=display, fill=OFF_WHITE)
    draw.text((806, 396), "INTO", font=display, fill=OFF_WHITE)
    draw.text((806, 442), "FLOW.", font=display, fill=MINT)


def draw_card_caption(draw: ImageDraw.ImageDraw) -> None:
    draw.text(
        (786, 548), "P1-A · LIQUID SIGNAL RIBBON",
        font=font(DISPLAY_FONT, 19), fill=OFF_WHITE,
    )
    draw.text(
        (786, 588), "A luminous data stream in motion — restrained, fluid, and alive.",
        font=font(REGULAR_FONT, 13), fill=MUTED,
    )
    draw.rounded_rectangle((786, 626, 970, 660), radius=17, outline=BORDER, width=2)
    draw.text((807, 635), "LIGHT · TECH · FLUID", font=font(MONO_FONT, 11), fill=MUTED)


def draw_portrait_card(image: Image.Image, frame: int) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle(
        CARD_BOX, radius=29, fill=CARD, outline=(67, 129, 111, 255), width=2
    )
    draw_card_art(image)
    draw_signal(image, mint_signal_mask(frame), (113, 246, 198))
    draw_signal(image, violet_signal_mask(frame), (142, 124, 255))
    draw_coral_tail(image, frame)
    draw_particle(image, frame)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.text((806, 78), "YI HAN / AI AUTOMATION ENGINEER", font=font(MONO_FONT, 11), fill=MUTED)
    draw_card_headline(draw)
    draw_card_caption(draw)


def make_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw_background(image)
    draw_left_intro(ImageDraw.Draw(image, "RGBA"))
    draw_portrait_card(image, frame)
    image.putalpha(rounded_alpha())
    return image


def quantize(image: Image.Image) -> Image.Image:
    opaque = Image.new("RGB", image.size, BG)
    opaque.paste(image.convert("RGB"), mask=image.getchannel("A"))
    palette_image = opaque.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
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
    make_frame(6).save(png_path, optimize=True)
    return gif_path, png_path


if __name__ == "__main__":
    gif, still = render_assets(Path("assets"))
    print(f"Rendered {gif} and {still}")
