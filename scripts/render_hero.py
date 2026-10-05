from __future__ import annotations

from functools import cache
from math import pi, sin
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

if __package__:
    from .visual_tokens import (
        ACCENT, BG, BORDER, CARD_EDGE, CORAL, HAIRLINE, MINT, MUTED, PANEL,
        SHADOW, SIGNAL, SURFACE, TEXT, VIOLET, mix, rgb,
    )
else:
    from visual_tokens import (
        ACCENT, BG, BORDER, CARD_EDGE, CORAL, HAIRLINE, MINT, MUTED, PANEL,
        SHADOW, SIGNAL, SURFACE, TEXT, VIOLET, mix, rgb,
    )

WIDTH = 1280
HEIGHT = 720
FPS = 20
FRAME_COUNT = FPS * 5
DURATION_MS = 1000 // FPS

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
LEFT_ACTION = "VIEW SELECTED WORK"


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
        motion = 14 * sin(time + progress * 2 * pi)
    else:
        base = 282 - 48 * progress - 18 * sin(progress * pi)
        motion = 12 * sin(time + progress * 2.3 * pi)
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


def soft_layer(
    size: tuple[int, int], color: tuple[int, int, int], alpha: Image.Image, blur: int
) -> Image.Image:
    # Blur only the alpha: blurring an RGBA layer whose clear pixels are black
    # bleeds grey into the soft edge, which shows as a smudge on a light page.
    layer = Image.new("RGBA", size, color + (0,))
    layer.putalpha(alpha.filter(ImageFilter.GaussianBlur(blur)))
    return layer


def draw_background(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((0, 0, WIDTH - 1, HEIGHT - 1), 22, fill=BG)
    for x in range(0, 720, 72):
        draw.line((x, 0, x, HEIGHT), fill=HAIRLINE)
    haze = Image.new("L", image.size, 0)
    ImageDraw.Draw(haze).ellipse((-120, 140, 520, 640), fill=70)
    image.alpha_composite(soft_layer(image.size, rgb(MINT), haze, 100))


def draw_left_intro(draw: ImageDraw.ImageDraw) -> None:
    draw.text(
        (70, 90), "AI & AUTOMATION / AUCKLAND, NZ",
        font=font(MONO_FONT, 17), fill=ACCENT,
    )
    draw.text((68, 212), "Hi, I'm", font=font(DISPLAY_FONT, 78), fill=TEXT)
    draw.text((68, 298), "Yi Han.", font=font(DISPLAY_FONT, 78), fill=ACCENT)
    draw.multiline_text(
        (72, 424), LEFT_COPY, font=font(REGULAR_FONT, 24),
        fill=MUTED, spacing=11,
    )
    draw.text(
        (72, 560), LEFT_ACTION,
        font=font(MONO_FONT, 16), fill=TEXT,
    )
    draw.line((72, 598, 232, 598), fill=ACCENT, width=2)


def draw_card_art(image: Image.Image) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.rectangle(ART_BOX, fill=PANEL)
    for x in range(ART_BOX[0], ART_BOX[2] + 1, 40):
        draw.line((x, ART_BOX[1], x, ART_BOX[3]), fill=BORDER)
    for y in range(ART_BOX[1], ART_BOX[3] + 1, 40):
        draw.line((ART_BOX[0], y, ART_BOX[2], y), fill=BORDER)
    layer.putalpha(art_mask())
    image.alpha_composite(layer)


def draw_signal(image: Image.Image, mask: Image.Image, color: tuple[int, int, int]) -> None:
    # On a light panel a softer glow keeps the ribbon crisp instead of muddy.
    glow_alpha = mask.filter(ImageFilter.GaussianBlur(16)).point(
        lambda value: min(110, value * 3)
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
    for x in range(1050, ART_BOX[2] + 1):
        alpha = int(255 * (x - 1050) / (ART_BOX[2] - 1050))
        ImageDraw.Draw(fade).line((x, 190, x, 310), fill=alpha)
    tail = ImageChops.multiply(mask, fade)
    layer = Image.new("RGBA", image.size, rgb(CORAL) + (0,))
    layer.putalpha(tail)
    image.alpha_composite(layer)


def packet_alpha(frame: int, lane: int) -> Image.Image:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(mask)
    for packet in range(3):
        progress = (frame / FRAME_COUNT * 2 + packet / 3 + lane * .17) % 1
        for trail in range(18):
            position = progress - trail * .007
            if not 0 <= position <= 1:
                continue
            x = 780 + int(position * 440)
            y = signal_y(x, frame, lane)
            alpha = int(255 * (1 - trail / 18))
            draw.ellipse((x-3, y-3, x+3, y+3), fill=alpha)
    return ImageChops.multiply(mask, art_mask())


def draw_particle(image: Image.Image, frame: int) -> None:
    # Pale, lane-tinted packets read as light travelling along each signal.
    lane_colors = (mix(SIGNAL, SURFACE, .6), mix(VIOLET, SURFACE, .55))
    for lane, color in enumerate(lane_colors):
        alpha = packet_alpha(frame, lane)
        image.alpha_composite(soft_layer(image.size, color, alpha, 4))
        crisp = Image.new("RGBA", image.size, color + (0,))
        crisp.putalpha(alpha)
        image.alpha_composite(crisp)


def draw_telemetry(image: Image.Image, frame: int) -> None:
    layer = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(layer, "RGBA")
    phase = frame / FRAME_COUNT
    scan = 115 + int(phase * 205)
    draw.line((795, scan, 1205, scan), fill=rgb(SIGNAL) + (60,), width=1)
    for index in range(30):
        x = 800 + index * 14
        height = 4 + int(16 * (1 + sin(index * .6 - phase * 4 * pi)) / 2)
        draw.line((x, 323, x, 323-height), fill=rgb(SIGNAL) + (150,), width=3)
    for index in range(8):
        x = 830 + index * 47
        y = 130 + int((index * 29 - phase * 100) % 160)
        draw.point((x, y), fill=rgb(ACCENT) + (180,))
    x = 72 + int(phase * 160)
    draw.line((72, 598, 232, 598), fill=mix(ACCENT, BG, .75) + (255,), width=2)
    draw.line((max(72, x-35), 598, x, 598), fill=rgb(ACCENT) + (255,), width=3)
    image.alpha_composite(layer)


def draw_card_headline(draw: ImageDraw.ImageDraw) -> None:
    display = font(DISPLAY_FONT, 43)
    draw.text((806, 350), "TURN FRICTION", font=display, fill=TEXT)
    draw.text((806, 396), "INTO", font=display, fill=TEXT)
    draw.text((806, 442), "FLOW.", font=display, fill=ACCENT)


def draw_card_caption(draw: ImageDraw.ImageDraw) -> None:
    draw.text(
        (786, 548), "INTELLIGENCE IN MOTION",
        font=font(DISPLAY_FONT, 19), fill=TEXT,
    )
    draw.text(
        (786, 588), "From context to decisions. From decisions to action.",
        font=font(REGULAR_FONT, 13), fill=MUTED,
    )
    draw.rounded_rectangle((786, 626, 970, 660), radius=17, outline=BORDER, width=2)
    draw.text((807, 635), "AI / SYSTEMS / BUILD", font=font(MONO_FONT, 11), fill=MUTED)


def draw_card_shadow(image: Image.Image) -> None:
    # A white card on a white page needs a soft shadow to read as raised.
    alpha = Image.new("L", image.size, 0)
    x0, y0, x1, y1 = CARD_BOX
    ImageDraw.Draw(alpha).rounded_rectangle((x0, y0 + 12, x1, y1 + 8), radius=29, fill=30)
    image.alpha_composite(soft_layer(image.size, rgb(SHADOW), alpha, 20))


def draw_portrait_card(image: Image.Image, frame: int) -> None:
    draw_card_shadow(image)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle(CARD_BOX, radius=29, fill=SURFACE, outline=CARD_EDGE, width=2)
    draw_card_art(image)
    draw_signal(image, mint_signal_mask(frame), rgb(SIGNAL))
    draw_signal(image, violet_signal_mask(frame), rgb(VIOLET))
    draw_coral_tail(image, frame)
    draw_particle(image, frame)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.text((806, 78), "NEURAL SIGNAL / ACTIVE", font=font(MONO_FONT, 11), fill=MUTED)
    draw_card_headline(draw)
    draw_card_caption(draw)


def make_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw_background(image)
    draw_left_intro(ImageDraw.Draw(image, "RGBA"))
    draw_portrait_card(image, frame)
    draw_telemetry(image, frame)
    image.putalpha(rounded_alpha())
    return image


PALETTE_FRAMES = (0, 25, 50, 75)


@cache
def animation_palette() -> Image.Image:
    # Light gradients band badly with a small single-frame palette, so sample
    # several frames (every signal position and the coral tail) and spend all
    # 255 slots; index 255 stays free for transparency.
    samples = [make_frame(index).convert("RGB") for index in PALETTE_FRAMES]
    strip = Image.new("RGB", (WIDTH, HEIGHT * len(samples)))
    for row, sample in enumerate(samples):
        strip.paste(sample, (0, row * HEIGHT))
    return strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT)


# Only these regions change between frames: the signal panel and the underline.
DYNAMIC_BOXES = ((780, 55, 1221, 516), (70, 595, 236, 602))


def quantize(image: Image.Image, base: Image.Image | None = None) -> Image.Image:
    """Index a frame against the shared palette.

    Without `base`, the whole frame is dithered: near-white haze and shadow
    gradients otherwise band into visible rings. With `base` (the dithered
    static frame), only the animated boxes are re-quantized, undithered, so
    stationary pixels stay identical and GIF delta encoding keeps files small.
    """
    opaque = Image.new("RGB", image.size, BG)
    opaque.paste(image.convert("RGB"), mask=image.getchannel("A"))
    dither = Image.Dither.FLOYDSTEINBERG if base is None else Image.Dither.NONE
    palette_image = opaque.quantize(palette=animation_palette(), dither=dither)
    if base is not None:
        merged = base.copy()
        for box in DYNAMIC_BOXES:
            merged.paste(palette_image.crop(box), box[:2])
        palette_image = merged
    transparent = image.getchannel("A").point(lambda value: 255 if value == 0 else 0)
    palette_image.paste(255, mask=transparent)
    return palette_image


def render_assets(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    base = quantize(make_frame(0))
    frames = [quantize(make_frame(index), base) for index in range(FRAME_COUNT)]
    gif_path = output_dir / "hero-split.gif"
    png_path = output_dir / "hero-split-static.png"
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
        transparency=255,
    )
    make_frame(6).save(png_path, optimize=True)
    return gif_path, png_path


if __name__ == "__main__":
    gif, still = render_assets(Path("assets"))
    print(f"Rendered {gif} and {still}")
