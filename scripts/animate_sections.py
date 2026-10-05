"""Render profile cards with stationary copy and looping workflow accents."""
from pathlib import Path
from math import sin, pi

from PIL import Image, ImageDraw, ImageFont, ImageOps

if __package__:
    from .render_sections import PROJECTS
    from .visual_tokens import (
        ACCENT, BG, BORDER, DOT, MUTED, ON_ACCENT, PANEL, SURFACE, TEXT, mix, rgb,
    )
else:
    from render_sections import PROJECTS
    from visual_tokens import (
        ACCENT, BG, BORDER, DOT, MUTED, ON_ACCENT, PANEL, SURFACE, TEXT, mix, rgb,
    )

FRAMES = 60
WIDTH = 960
FONTS = Path("C:/Windows/Fonts")


def label(draw, xy, value, size=17, color=TEXT, bold=False, mono=False, anchor="ls"):
    name = "consola.ttf" if mono else "segoeuib.ttf" if bold else "segoeui.ttf"
    draw.text(xy, value, font=ImageFont.truetype(str(FONTS / name), size),
              fill=color, anchor=anchor)


def card(height, accent):
    image = Image.new("RGBA", (WIDTH, height))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, WIDTH-2, height-2), 26, fill=BG, outline=BORDER)
    grid = Image.new("RGBA", image.size)
    gd = ImageDraw.Draw(grid)
    # A faint accent grid; on white it needs more alpha than on black to register.
    color = rgb(accent) + (14,)
    for x in range(48, WIDTH-24, 48):
        gd.line((x, 26, x, height-26), fill=color)
    for y in range(48, height-24, 48):
        gd.line((26, y, WIDTH-26, y), fill=color)
    image.alpha_composite(grid)
    return image


def edge(draw, frame, accent, height):
    x = 28 + int(frame / FRAMES * (WIDTH-56))
    # The comet tail fades into the page background, not toward black.
    for offset in range(50):
        if x-offset >= 28:
            draw.point((x-offset, 2), fill=mix(accent, BG, offset/50))


def project_frame(project, frame):
    _, number, name, description, metadata, labels, accent = project
    image = card(460, accent)
    draw = ImageDraw.Draw(image)
    label(draw, (32, 54), "SELECTED WORK", 15, accent, mono=True)
    label(draw, (32, 113), name, 40, bold=True)
    lines = wrap_description(draw, description, width=300, size=26)
    for index, line in enumerate(lines):
        label(draw, (32, 165+index*35), line, 26, MUTED)
    for index, tag in enumerate(metadata.split(" · ")):
        label(draw, (32, 325+index*25), tag, 17, accent, mono=True)
    label(draw, (32, 423), "VIEW PROJECT  /", 19, TEXT, mono=True)
    add_preview(image, project[0], accent)
    edge(ImageDraw.Draw(image), frame, accent, 460)
    return image


def add_preview(image, filename, accent):
    source_name = filename.replace("project-", "").replace(".svg", ".png")
    path = Path(__file__).resolve().parents[1] / "assets" / "previews" / source_name
    with Image.open(path) as source:
        preview = ImageOps.contain(source.convert("RGB"), (550, 354), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((374, 30, 934, 430), 18, fill=PANEL, outline=BORDER)
    for x in (391, 405, 419):
        draw.ellipse((x, 47, x+6, 53), fill=accent if x == 391 else DOT)
    label(draw, (916, 55), "PRODUCT PREVIEW", 13, MUTED, mono=True, anchor="rs")
    # Contain rather than crop: retain subtitles and dashboard labels in full.
    left = 379 + (550-preview.width)//2
    top = 67 + (354-preview.height)//2
    image.paste(preview, (left, top))
    # Light screenshots need a hairline to separate them from the light frame.
    draw.rectangle((left-1, top-1, left+preview.width, top+preview.height), outline=BORDER)


def wrap_description(draw, description, width=780, size=28):
    font = ImageFont.truetype(str(FONTS / "segoeui.ttf"), size)
    lines, line = [], ""
    for word in description.split():
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=font) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    return lines + [line]


def stack_frame(frame):
    image = card(290, ACCENT)
    draw = ImageDraw.Draw(image)
    label(draw, (40, 63), "Focused tools.", 36, bold=True)
    label(draw, (40, 98), "The stack behind the systems.", 23, MUTED)
    names = ("TypeScript", "JavaScript", "Java", "Spring Boot",
             "Vue", "MySQL", "AI APIs", "Automation")
    for i, name in enumerate(names):
        x = 40 + (i % 4)*225
        y = 127 + (i // 4)*75
        active = int(frame / FRAMES * len(names)) == i
        draw.rounded_rectangle((x, y, x+205, y+56), 18, fill=SURFACE,
                               outline=ACCENT if active else BORDER, width=2 if active else 1)
        label(draw, (x+102, y+36), name, 22, ACCENT if active else TEXT,
              mono=True, anchor="ms")
    edge(draw, frame, ACCENT, 290)
    return image


def contact_frame(frame):
    image = card(220, ACCENT)
    draw = ImageDraw.Draw(image)
    label(draw, (40, 63), "Have an idea worth automating?", 36, bold=True)
    label(draw, (40, 108), "Let's build something useful.", 25, MUTED)
    label(draw, (40, 176), "AUCKLAND, NEW ZEALAND", 19, MUTED, mono=True)
    pulse = (1+sin(frame / FRAMES * 2*pi))/2
    draw.rounded_rectangle((695, 129, 925, 197), 28,
                           outline=mix(ACCENT, BG, .7 - .55*pulse), width=2)
    draw.rounded_rectangle((700, 134, 920, 192), 24, fill=ACCENT)
    label(draw, (810, 172), "LET'S TALK", 24, ON_ACCENT, mono=True, anchor="ms")
    edge(draw, frame, ACCENT, 220)
    return image


def export(name, renderer, directory):
    frames = [renderer(i) for i in range(FRAMES)]
    palette = frames[0].convert("RGB").quantize(colors=192 if name.startswith("project-") else 96)
    encoded = []
    for frame in frames:
        indexed = frame.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
        indexed.paste(255, mask=frame.getchannel("A").point(lambda a: 255 if a == 0 else 0))
        encoded.append(indexed)
    path = directory / name
    encoded[0].save(path, save_all=True, append_images=encoded[1:], duration=80,
                    loop=0, transparency=255, disposal=1, optimize=True)
    print(f"{name}: {path.stat().st_size:,} bytes")


def render(directory):
    directory.mkdir(parents=True, exist_ok=True)
    for project in PROJECTS:
        export(project[0].replace(".svg", ".gif"),
               lambda frame, item=project: project_frame(item, frame), directory)
    export("stack.gif", stack_frame, directory)
    export("contact.gif", contact_frame, directory)


if __name__ == "__main__":
    render(Path("assets"))
