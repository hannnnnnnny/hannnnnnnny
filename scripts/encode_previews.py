"""Encode real browser recordings, including their captured cursor, for GitHub."""
from pathlib import Path
import subprocess
from io import BytesIO

from PIL import Image, ImageChops

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
TAKES = {
    'kiwicue': ('kiwicue-final.webm', 16),
    'renova': ('renova-detail-1.webm', 12),
    'pansub': ('pansub-cursor.webm', 18),
    'guardrun': ('guardrun-final.webm', 14),
    'ashen-depths': ('game-final.webm', 13),
}


def content_box(source):
    result = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error',
                             '-ss', '1', '-i', str(source), '-frames:v', '1',
                             '-f', 'image2pipe', '-vcodec', 'png', '-'],
                            capture_output=True, check=True, timeout=30)
    image = Image.open(BytesIO(result.stdout)).convert('RGB')
    # CLI videos pad small viewports with gray; remove that recording-only padding.
    mask = ImageChops.difference(image, Image.new('RGB', image.size, (128,128,128)))
    box = mask.point(lambda value: 255 if value > 5 else 0).getbbox()
    if box is None:
        raise ValueError('Recording contains no visible page')
    return f'crop={box[2]-box[0]}:{box[3]-box[1]}:{box[0]}:{box[1]}'


def encode(name, recording, seconds):
    source = ROOT / 'output/playwright/recordings' / recording
    if not source.is_file():
        raise FileNotFoundError(source)
    output = ROOT / 'assets/demos' / f'{name}-cursor.gif'
    size, fps = (960, 8) if name == 'ashen-depths' else (1100, 10)
    dither = 'none' if name == 'ashen-depths' else 'bayer:bayer_scale=3'
    filters = (content_box(source) + f',fps={fps},scale={size}:-1:flags=lanczos,split[a][b];'
               '[a]palettegen=stats_mode=diff:max_colors=256[p];'
               f'[b][p]paletteuse=dither={dither}:diff_mode=rectangle')
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-hide_banner',
                    '-loglevel', 'error', '-ss', '0.7', '-i', str(source),
                    '-t', str(seconds), '-filter_complex', filters,
                    '-loop', '0', str(output)], check=True, timeout=120)
    if output.stat().st_size > 9_000_000:
        raise ValueError(f'{output.name} exceeds the 9 MB preview budget')
    print(f'{output.name}: {output.stat().st_size:,} bytes')


if __name__ == '__main__':
    import sys
    names = sys.argv[1:] or list(TAKES)
    for name in names:
        if name not in TAKES:
            raise ValueError(f'Unknown preview: {name}')
        encode(name, *TAKES[name])
