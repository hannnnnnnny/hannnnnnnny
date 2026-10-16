"""Render the README through GitHub's Markdown API for local browser review."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def render():
    result = subprocess.run(['gh', 'api', 'markdown', '-F', 'text=@README.md',
                             '-f', 'mode=gfm'], cwd=ROOT, capture_output=True,
                            text=True, encoding='utf-8', check=True, timeout=30)
    body = result.stdout.replace('src="assets/', 'src="/assets/')
    css = ('*{box-sizing:border-box}body{margin:0;background:#f6f8fa;color:#1f2328;'
           'font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}'
           'article{max-width:920px;margin:32px auto;padding:30px;background:white;'
           'border:1px solid #d1d9e0;border-radius:10px}img{max-width:100%;height:auto}'
           'a{color:#0969da;overflow-wrap:anywhere}h3{font-size:21px;margin-top:28px}'
           'hr{border:0;border-top:1px solid #d1d9e0;margin:30px 0}'
           'li{margin:7px 0}p{overflow-wrap:anywhere}'
           '@media(max-width:600px){article{margin:0;padding:18px;border:0}}')
    html = ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Harry Han — README preview</title>'
            f'<style>{css}</style><article>{body}</article></html>')
    path = ROOT / 'output/playwright/profile-preview.html'
    path.write_text(html, encoding='utf-8')
    print(path.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    render()
