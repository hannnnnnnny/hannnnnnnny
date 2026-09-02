from __future__ import annotations

from functools import cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1280
HEIGHT = 360
FPS = 20
FRAME_COUNT = FPS * 5
DURATION_MS = 1000 // FPS

BG = "#080909"
OFF_WHITE = "#F4F3ED"
MUTED = "#747A76"
MINT = "#7CF6CE"
CORAL = "#FF5A3C"
BORDER = "#2C3030"

FONT_ROOT = Path("C:/Windows/Fonts")
DISPLAY_FONT = FONT_ROOT / "segoeuib.ttf"
MONO_FONT = FONT_ROOT / "consola.ttf"


@cache
def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise FileNotFoundError(f"Required font is missing: {path}")
    return ImageFont.truetype(str(path), size)


def ease(value: float) -> float:
    clamped = max(0.0, min(1.0, value))
    return clamped * clamped * (3 - 2 * clamped)


def phase(frame: int, start: int, end: int) -> float:
    return ease((frame - start) / max(1, end - start))


def draw_header(draw: ImageDraw.ImageDraw) -> None:
    draw.text(
        (58, 38),
        "YI HAN / CURRENT MODE: BUILDING",
        font=font(MONO_FONT, 19),
        fill=MUTED,
    )


def draw_prompt(draw: ImageDraw.ImageDraw, frame: int) -> None:
    mono = font(MONO_FONT, 20)
    draw.rounded_rectangle(
        (58, 286, 462, 329),
        radius=9,
        fill="#111313",
        outline=BORDER,
    )
    draw.text((77, 297), "→", font=mono, fill=MINT)
    draw.text((105, 297), "turning friction into flow", font=mono, fill=MUTED)
    if (frame // 10) % 2 == 0:
        draw.rectangle((432, 300, 439, 318), fill=MINT)


def draw_scanline(draw: ImageDraw.ImageDraw, frame: int) -> None:
    progress = frame / (FRAME_COUNT - 1)
    y = int(progress * (HEIGHT + 30)) - 15
    fade = min(1.0, min(progress, 1 - progress) * 14)
    color = (124, 246, 206, int(100 * fade))
    draw.line((0, y, WIDTH, y), fill=color, width=2)


def mark_frame(draw: ImageDraw.ImageDraw, frame: int) -> None:
    for bit in range(7):
        color = MINT if frame & (1 << bit) else BG
        draw.point((WIDTH - bit - 1, HEIGHT - 1), fill=color)


def draw_statement(draw: ImageDraw.ImageDraw, frame: int) -> None:
    display = font(DISPLAY_FONT, 68)
    x, y = 58, 98
    old_text = "Repetitive work."
    draw.text((x, y), old_text, font=display, fill=MUTED)

    old_box = draw.textbbox((x, y), old_text, font=display)
    strike_progress = phase(frame, 10, 27)
    strike_end = x + int((old_box[2] - x) * strike_progress)
    draw.rounded_rectangle(
        (x, y + 43, strike_end, y + 50),
        radius=3,
        fill=CORAL,
    )

    enter = phase(frame, 28, 45)
    exit_progress = phase(frame, 74, 89)
    visible = max(0.0, enter - exit_progress)
    new_y = 193 + int((1 - visible) * 45)
    draw.text(
        (x, new_y),
        "Reliable systems.",
        font=display,
        fill=(124, 246, 206, int(255 * visible)),
    )


def make_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_header(draw)
    draw_statement(draw, frame)
    draw_prompt(draw, frame)
    draw_scanline(draw, frame)
    mark_frame(draw, frame)
    return image.convert("RGB")


def quantize(image: Image.Image) -> Image.Image:
    return image.quantize(colors=64, method=Image.Quantize.MEDIANCUT)


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
    )
    make_frame(55).save(png_path, optimize=True)
    return gif_path, png_path


if __name__ == "__main__":
    gif, still = render_assets(Path("assets"))
    print(f"Rendered {gif} and {still}")
