from __future__ import annotations

from html import escape

from PIL import ImageColor

WIDTH = 1280

# Light theme: the single source of colour for every published renderer.
# Text-bearing colours (TEXT, MUTED, ACCENT, VIOLET, CORAL) keep WCAG AA
# (>= 4.5:1) on BG and SURFACE; MINT and SIGNAL are decorative only.
BG = "#FBFCFB"
SURFACE = "#FFFFFF"
PANEL = "#F3F6F5"
BORDER = "#E3E8E6"
HAIRLINE = "#ECF1EF"
CARD_EDGE = "#BFDDD2"
DOT = "#C9D3CF"
TEXT = "#0E1512"
MUTED = "#5E6B66"
ACCENT = "#0A7C5C"
ON_ACCENT = "#FFFFFF"
MINT = "#7CF6CE"
SIGNAL = "#12B886"
VIOLET = "#6C5CE7"
CORAL = "#C2410C"
SHADOW = "#0E1512"


def rgb(color: str) -> tuple[int, int, int]:
    return ImageColor.getrgb(color)[:3]


def mix(first: str, second: str, amount: float) -> tuple[int, int, int]:
    """Blend `first` toward `second`; amount 0 keeps first, 1 returns second."""
    a, b = rgb(first), rgb(second)
    return tuple(round(x + (y - x) * amount) for x, y in zip(a, b))


def svg_document(
    title: str,
    description: str,
    height: int,
    body: str,
    accent: str = MINT,
) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}"
  height="{height}" viewBox="0 0 {WIDTH} {height}" role="img"
  aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M36 0H0V36" fill="none" stroke="{accent}" stroke-opacity=".055"/>
    </pattern>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="{accent}" stop-opacity=".16"/>
      <stop offset=".55" stop-color="{accent}" stop-opacity=".035"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="1278" height="{height - 2}" rx="18"
    fill="{BG}" stroke="{BORDER}"/>
  <rect x="2" y="2" width="1276" height="{height - 4}" rx="17"
    fill="url(#grid)" opacity=".72"/>
  <rect x="2" y="2" width="1276" height="3" rx="1.5" fill="url(#fade)"/>
  {body}
</svg>"""


def text(
    x: int,
    y: int,
    value: str,
    size: int,
    fill: str = TEXT,
    weight: int = 600,
    family: str = "Segoe UI,Arial,sans-serif",
    anchor: str = "start",
) -> str:
    safe = escape(value)
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
        f'font-weight="{weight}" font-family="{family}" '
        f'text-anchor="{anchor}">{safe}</text>'
    )


def pill(x: int, y: int, width: int, value: str, accent: str) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="34" rx="17" '
        f'fill="{SURFACE}" stroke="{BORDER}"/>'
        + text(x + width // 2, y + 22, value, 13, accent, 600,
               "Consolas,monospace", "middle")
    )
