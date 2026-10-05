"""Full-colour, 2x project cards: preserve screenshot detail without GIF quantization."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps

try:
    from .animate_sections import label, wrap_description, PROJECTS
    from .visual_tokens import BG, BORDER, DOT, MUTED, PANEL, SHADOW, TEXT, rgb
except ImportError:
    from animate_sections import label, wrap_description, PROJECTS
    from visual_tokens import BG, BORDER, DOT, MUTED, PANEL, SHADOW, TEXT, rgb

ROOT = Path(__file__).resolve().parents[1]
FRAME_BOX = (748, 60, 1868, 860)


def frame_shadow(image):
    # A soft drop shadow lifts the light browser frame off the light card.
    alpha = Image.new("L", image.size, 0)
    x0, y0, x1, y1 = FRAME_BOX
    ImageDraw.Draw(alpha).rounded_rectangle((x0, y0+14, x1, y1+14), 36, fill=26)
    # Blur only the alpha so the soft edge never picks up stray grey.
    layer = Image.new("RGBA", image.size, rgb(SHADOW) + (0,))
    layer.putalpha(alpha.filter(ImageFilter.GaussianBlur(22)))
    image.alpha_composite(layer)


def preview(image, filename, accent):
    name = filename.replace("project-", "").replace(".svg", ".png")
    with Image.open(ROOT / "assets" / "previews" / name) as source:
        shot = ImageOps.contain(source.convert("RGB"), (1100, 708), Image.Resampling.LANCZOS)
    frame_shadow(image)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(FRAME_BOX, 36, fill=PANEL, outline=BORDER, width=2)
    for x in (782, 810, 838):
        draw.ellipse((x, 94, x+12, 106), fill=accent if x == 782 else DOT)
    label(draw, (1832, 110), "PRODUCT PREVIEW", 26, MUTED, mono=True, anchor="rs")
    left = 758 + (1100-shot.width)//2
    top = 134 + (708-shot.height)//2
    image.paste(shot, (left, top))
    draw.rectangle((left-1, top-1, left+shot.width, top+shot.height), outline=BORDER, width=2)


def render_project(project):
    filename, _, name, description, metadata, _, accent = project
    image = Image.new("RGBA", (1920, 920))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((2, 2, 1916, 916), 52, fill=BG, outline=BORDER, width=2)
    label(draw, (64, 108), "SELECTED WORK", 30, accent, mono=True)
    label(draw, (64, 226), name, 80, bold=True)
    lines = wrap_description(draw, description, width=600, size=52)
    for i, line in enumerate(lines):
        label(draw, (64, 330+i*70), line, 52, MUTED)
    for i, tag in enumerate(metadata.split(" · ")):
        label(draw, (64, 650+i*50), tag, 34, accent, mono=True)
    label(draw, (64, 846), "VIEW PROJECT  /", 38, TEXT, mono=True)
    preview(image, filename, accent)
    return image


if __name__ == "__main__":
    for project in PROJECTS:
        path = ROOT / "assets" / project[0].replace(".svg", "-hd.png")
        render_project(project).save(path, optimize=True)
        print(f"{path.name}: {path.stat().st_size:,} bytes")
