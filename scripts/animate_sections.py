"""Render profile cards with stationary copy and looping workflow accents."""
from pathlib import Path
from math import sin, pi

from PIL import Image, ImageDraw, ImageFont, ImageColor

if __package__:
    from .render_sections import PROJECTS
    from .visual_tokens import BG, BORDER, SURFACE, TEXT, MUTED, MINT
else:
    from render_sections import PROJECTS
    from visual_tokens import BG, BORDER, SURFACE, TEXT, MUTED, MINT

FRAMES = 60
WIDTH = 1280
FONTS = Path("C:/Windows/Fonts")


def label(draw, xy, value, size=17, color=TEXT, bold=False, mono=False, anchor="ls"):
    name = "consola.ttf" if mono else "segoeuib.ttf" if bold else "segoeui.ttf"
    draw.text(xy, value, font=ImageFont.truetype(str(FONTS / name), size),
              fill=color, anchor=anchor)


def card(height, accent):
    image = Image.new("RGBA", (WIDTH, height))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, 1278, height-2), 18, fill=BG, outline=BORDER)
    grid = Image.new("RGBA", image.size)
    gd = ImageDraw.Draw(grid)
    color = ImageColor.getrgb(accent) + (10,)
    for x in range(36, 1278, 36):
        gd.line((x, 3, x, height-4), fill=color)
    for y in range(36, height-4, 36):
        gd.line((3, y, 1276, y), fill=color)
    image.alpha_composite(grid)
    return image


def edge(draw, frame, accent, height):
    x = 22 + int(frame / FRAMES * 1234)
    rgb = ImageColor.getrgb(accent)
    for offset in range(50):
        shade = tuple(int(v * (1-offset/50)) for v in rgb)
        if x-offset >= 22:
            draw.point((x-offset, 2), fill=shade)


def project_frame(project, frame):
    _, number, name, description, metadata, labels, accent = project
    image = card(168, accent)
    draw = ImageDraw.Draw(image)
    for x in (112, 860):
        draw.line((x, 2, x, 165), fill=BORDER)
    label(draw, (56, 91), number, 13, MUTED, mono=True, anchor="ms")
    label(draw, (153, 61), name, 27, bold=True)
    label(draw, (153, 94), description, 17, MUTED)
    label(draw, (153, 128), metadata, 12, accent, mono=True)
    draw.line((948, 84, 1188, 84), fill=BORDER)
    phase = frame / FRAMES * 3
    for i, value in enumerate(labels):
        x = 900 + i * 120
        active = int(phase) == i
        draw.rounded_rectangle((x, 60, x+96, 108), 10, fill=SURFACE,
                               outline=accent if active else BORDER, width=2 if active else 1)
        label(draw, (x+48, 88), value, 11, accent if active else MUTED,
              mono=True, anchor="ms")
        if i < 2:
            progress = (phase % 1)
            if active:
                dot = x + 99 + int(progress * 18)
                draw.ellipse((dot-2, 82, dot+2, 86), fill=accent)
    edge(draw, frame, accent, 168)
    return image


def stack_frame(frame):
    image = card(128, MINT)
    draw = ImageDraw.Draw(image)
    label(draw, (38, 48), "BUILDING WITH", 12, MUTED, mono=True)
    label(draw, (38, 85), "Focused tools.", 26, bold=True)
    draw.line((285, 2, 285, 126), fill=BORDER)
    names = ("TypeScript", "JavaScript", "Java", "Spring Boot",
             "Vue", "MySQL", "AI APIs", "Automation")
    x = 328
    for i, name in enumerate(names):
        width = 50 + len(name)*7
        active = int(frame / FRAMES * len(names)) == i
        draw.rounded_rectangle((x, 46, x+width, 80), 17, fill=SURFACE,
                               outline=MINT if active else BORDER)
        label(draw, (x+width/2, 68), name, 13, MINT if active else TEXT,
              mono=True, anchor="ms")
        x += width+10
    edge(draw, frame, MINT, 128)
    return image


def contact_frame(frame):
    image = card(126, MINT)
    draw = ImageDraw.Draw(image)
    label(draw, (38, 55), "Have an idea worth automating?", 24, bold=True)
    label(draw, (38, 87), "BUILDING FROM AUCKLAND, NEW ZEALAND", 12, MUTED, mono=True)
    pulse = (1+sin(frame / FRAMES * 2*pi))/2
    outline = tuple(int(v*(.4+.5*pulse)) for v in ImageColor.getrgb(MINT))
    draw.rounded_rectangle((1075, 32, 1238, 94), 31, outline=outline)
    draw.rounded_rectangle((1080, 37, 1233, 89), 26, fill=MINT)
    label(draw, (1156, 69), "LET'S TALK", 14, "#08100D", mono=True, anchor="ms")
    edge(draw, frame, MINT, 126)
    return image


def export(name, renderer, directory):
    frames = [renderer(i) for i in range(FRAMES)]
    palette = frames[0].convert("RGB").quantize(colors=96)
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
