"""Typography-first profile hero with a single animated mint full stop."""
from pathlib import Path
from math import sin, tau
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SIZE = (1600, 660)
FRAMES = 48


def text(draw, xy, value, size, fill='#F4F5F0', bold=False):
    font = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold
                              else 'C:/Windows/Fonts/segoeui.ttf', size)
    draw.text(xy, value, font=font, fill=fill, anchor='ls')


def frame_at(index):
    image = Image.new('RGB', SIZE, '#0D1117')
    draw = ImageDraw.Draw(image)
    text(draw, (70, 160), "Hi, I'm", 88)
    text(draw, (62, 377), 'Yi Han', 216, bold=True)
    # Only this punctuation moves; name and supporting copy stay pixel-identical.
    radius = 14 + 3*sin(index/FRAMES*tau)
    draw.ellipse((785-radius, 356-radius, 785+radius, 356+radius), fill='#7CF6CE')
    text(draw, (76, 479), 'AI & Automation · Full-stack Development', 40)
    text(draw, (76, 540), 'Building useful products and simplifying repetitive work.', 33, '#A8B3B0')
    text(draw, (76, 612), 'Auckland, New Zealand', 25, '#A8B3B0')
    return image


if __name__ == '__main__':
    frames = [frame_at(i) for i in range(FRAMES)]
    palette = frames[0].quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    target = ROOT / 'assets/hero-minimal.gif'
    indexed[0].save(target, save_all=True, append_images=indexed[1:],
                    duration=100, loop=0, disposal=1, optimize=True)
    frames[0].save(ROOT / 'output/minimal-hero-preview.png')
    print(f'{target.name}: {target.stat().st_size:,} bytes')
