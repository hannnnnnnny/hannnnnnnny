"""Animate localized highlights over approved artwork without quantizing its colours."""
from pathlib import Path
from math import cos, sin, tau

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FRAMES = 60


def frame_at(source, phase):
    image = source.copy()
    width, height = source.size
    cx = int(width * (.81 + .135*cos(phase*tau)))
    cy = int(height * (.44 + .25*sin(phase*tau)))
    radius = 65
    box = (max(0, cx-radius), max(0, cy-radius),
           min(width, cx+radius), min(height, cy+radius))
    patch = np.asarray(source.crop(box)).astype(np.float32)
    yy, xx = np.mgrid[box[1]:box[3], box[0]:box[2]]
    distance = ((xx-cx)**2 + (yy-cy)**2) / radius**2
    envelope = np.maximum(0, 1-distance)**3
    rgb = patch[:, :, :3]
    # Light follows existing coloured filaments, not black space or white typography.
    saturation = (rgb.max(axis=2)-rgb.min(axis=2))/255
    strength = envelope * np.clip(saturation*3, 0, 1) * .7
    rgb += (255-rgb)*strength[:, :, None]
    image.paste(Image.fromarray(np.clip(patch, 0, 255).astype('uint8')), box[:2])
    return image


def render():
    with Image.open(ROOT / 'assets/hero-flow-source.png') as original:
        source = original.convert('RGB')
    frames = [frame_at(source, i/FRAMES) for i in range(FRAMES)]
    output = ROOT / 'assets/hero-flow-motion.png'
    frames[0].save(output, save_all=True, append_images=frames[1:],
                   duration=80, loop=0, disposal=0, blend=0, optimize=True)
    print(f'{output.name}: {output.stat().st_size:,} bytes; {FRAMES} frames')


if __name__ == '__main__':
    render()
