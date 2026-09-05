"""Full-colour, 2x project cards: preserve screenshot detail without GIF quantization."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

try:
    from .animate_sections import label, wrap_description, PROJECTS, BG, BORDER, TEXT
except ImportError:
    from animate_sections import label, wrap_description, PROJECTS, BG, BORDER, TEXT

ROOT = Path(__file__).resolve().parents[1]


def preview(image, filename, accent):
    name = filename.replace("project-", "").replace(".svg", ".png")
    with Image.open(ROOT / "assets" / "previews" / name) as source:
        shot = ImageOps.contain(source.convert("RGB"), (1100, 708), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((748, 60, 1868, 860), 36, fill="#151B1D", outline=BORDER, width=2)
    for x in (782, 810, 838):
        draw.ellipse((x, 94, x+12, 106), fill=accent if x == 782 else "#52625C")
    label(draw, (1832, 110), "PRODUCT PREVIEW", 26, "#BCC8C2", mono=True, anchor="rs")
    image.paste(shot, (758+(1100-shot.width)//2, 134+(708-shot.height)//2))


def render_project(project):
    filename, _, name, description, metadata, _, accent = project
    image = Image.new("RGBA", (1920, 920))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((2, 2, 1916, 916), 52, fill=BG, outline=BORDER, width=2)
    label(draw, (64, 108), "SELECTED WORK", 30, accent, mono=True)
    label(draw, (64, 226), name, 80, bold=True)
    lines = wrap_description(draw, description, width=600, size=52)
    for i, line in enumerate(lines):
        label(draw, (64, 330+i*70), line, 52, "#BCC8C2")
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
