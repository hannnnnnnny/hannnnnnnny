# Split Poster Profile Hero Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish one 1280 × 720 animated GitHub hero with a calm Yi Han introduction on the left and the approved P1-A portrait signal card on the right.

**Architecture:** Keep the hero deterministic and self-contained in Pillow. Geometry helpers produce separate mint and violet signal masks, the frame renderer composites those masks into a fixed split composition, and the README consumes the versioned GIF as one image so GitHub cannot disturb the layout.

**Tech Stack:** Python 3, Pillow, unittest, GitHub Markdown, Git/GitHub CLI.

## Global Constraints

- Output is `assets/hero-split.gif` at 1280 × 720, 100 frames, 20 FPS, and no more than 5 MB.
- Output includes a matching `assets/hero-split-static.png` representative still.
- Right card keeps the supplied 373:506 proportion, nested rounded borders, two separate luminous lines, and fixed three-line headline.
- Left copy is English and begins `Hi, I'm` / `Yi Han.`.
- Motion never enters either text safe area.
- Existing identity, project, stack, and contact assets remain unchanged.

---

### Task 1: Lock the split-poster geometry

**Files:**
- Modify: `tests/test_render_hero.py`
- Modify: `scripts/render_hero.py`

**Interfaces:**
- Produces: `mint_signal_mask(frame: int) -> Image.Image`
- Produces: `violet_signal_mask(frame: int) -> Image.Image`
- Produces: `make_frame(frame: int) -> Image.Image`
- Produces: `render_assets(output_dir: Path) -> tuple[Path, Path]`

- [ ] **Step 1: Write failing geometry tests**

```python
def test_split_hero_dimensions_and_copy_regions(self) -> None:
    frame = make_frame(25)
    self.assertEqual(frame.size, (1280, 720))
    self.assertEqual(frame.mode, "RGBA")

def test_signals_stay_above_portrait_headline(self) -> None:
    headline_box = (790, 330, 1185, 515)
    for frame in range(FRAME_COUNT):
        self.assertIsNone(mint_signal_mask(frame).crop(headline_box).getbbox())
        self.assertIsNone(violet_signal_mask(frame).crop(headline_box).getbbox())
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `python -m unittest tests.test_render_hero -v`

Expected: FAIL because the old frame is 1280 × 360 and the two signal-mask functions do not exist.

- [ ] **Step 3: Implement the fixed geometry and two independent signals**

```python
WIDTH, HEIGHT = 1280, 720
CARD_BOX = (760, 35, 1240, 685)
ART_BOX = (780, 55, 1220, 515)
PORTRAIT_HEADLINE_SAFE_BOX = (790, 330, 1185, 515)
REGULAR_FONT = FONT_ROOT / "segoeui.ttf"
LEFT_COPY = "I design and build AI-assisted products that turn\nrepetitive workflows into reliable systems."

def signal_y(x: int, frame: int, lane: int) -> int:
    time = frame / FRAME_COUNT * 2 * pi
    base_y = 180 if lane == 0 else 255
    amplitude = 24 if lane == 0 else 20
    return int(base_y + sin(x / 145 + time * (1.0 + lane * .2)) * amplitude)

def signal_mask(frame: int, lane: int) -> Image.Image:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    thickness = 7 if lane == 0 else 9
    points = [(x, signal_y(x, frame, lane)) for x in range(780, 1221, 4)]
    ImageDraw.Draw(mask).line(points, fill=255, width=thickness, joint="curve")
    return mask

def mint_signal_mask(frame: int) -> Image.Image:
    return signal_mask(frame, 0)

def violet_signal_mask(frame: int) -> Image.Image:
    return signal_mask(frame, 1)
```

- [ ] **Step 4: Render the left editorial introduction and right portrait card**

```python
def draw_left_intro(draw: ImageDraw.ImageDraw) -> None:
    draw.text((70, 92), "AI & AUTOMATION / AUCKLAND, NZ", font=font(MONO_FONT, 17), fill=MINT)
    draw.text((70, 220), "Hi, I'm", font=font(DISPLAY_FONT, 78), fill=OFF_WHITE)
    draw.text((70, 302), "Yi Han.", font=font(DISPLAY_FONT, 78), fill=MINT)
    draw.multiline_text((72, 420), LEFT_COPY, font=font(REGULAR_FONT, 24), fill=MUTED, spacing=10)
    draw.text((72, 555), "VIEW SELECTED WORK ↘", font=font(MONO_FONT, 16), fill=OFF_WHITE)

def draw_signal(image: Image.Image, mask: Image.Image, color: tuple[int, int, int]) -> None:
    glow = Image.new("RGBA", image.size, color + (0,))
    glow.putalpha(mask.filter(ImageFilter.GaussianBlur(18)).point(lambda value: value // 2))
    image.alpha_composite(glow)
    core = Image.new("RGBA", image.size, color + (255,))
    core.putalpha(mask)
    image.alpha_composite(core)

def draw_particle(image: Image.Image, frame: int) -> None:
    progress = frame / FRAME_COUNT
    x = 782 + int(progress * 438)
    y = signal_y(x, frame, 0)
    particle = Image.new("RGBA", image.size)
    dot = ImageDraw.Draw(particle, "RGBA")
    dot.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(113, 246, 198, 45))
    dot.ellipse((x - 5, y - 5, x + 5, y + 5), fill=OFF_WHITE)
    image.alpha_composite(particle.filter(ImageFilter.GaussianBlur(2)))

def draw_card_grid(draw: ImageDraw.ImageDraw) -> None:
    for x in range(820, 1220, 40):
        draw.line((x, 55, x, 515), fill=(28, 44, 38, 80))
    for y in range(95, 515, 40):
        draw.line((780, y, 1220, y), fill=(28, 44, 38, 80))

def draw_card_headline(draw: ImageDraw.ImageDraw) -> None:
    display = font(DISPLAY_FONT, 42)
    draw.text((808, 354), "TURN FRICTION", font=display, fill=OFF_WHITE)
    draw.text((808, 400), "INTO", font=display, fill=OFF_WHITE)
    draw.text((808, 446), "FLOW.", font=display, fill=MINT)

def draw_card_caption(draw: ImageDraw.ImageDraw) -> None:
    draw.text((790, 548), "P1-A · LIQUID SIGNAL RIBBON", font=font(DISPLAY_FONT, 19), fill=OFF_WHITE)
    draw.text((790, 588), "A luminous data stream in motion — restrained, fluid, and alive.", font=font(REGULAR_FONT, 13), fill=MUTED)
    draw.rounded_rectangle((790, 624, 970, 656), radius=16, outline=BORDER)
    draw.text((810, 633), "LIGHT · TECH · FLUID", font=font(MONO_FONT, 11), fill=MUTED)

def draw_portrait_card(image: Image.Image, frame: int) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle(CARD_BOX, radius=28, fill="#0C1110", outline="#3A7567", width=2)
    draw.rounded_rectangle(ART_BOX, radius=22, fill="#070A09", outline=BORDER, width=2)
    draw_card_grid(draw)
    draw_signal(image, mint_signal_mask(frame), (113, 246, 198))
    draw_signal(image, violet_signal_mask(frame), (142, 124, 255))
    draw_particle(image, frame)
    draw_card_headline(draw)
    draw_card_caption(draw)
```

The left headline uses two lines and the right headline uses exactly
`TURN FRICTION`, `INTO`, and `FLOW.`. Keep every helper under 40 lines.

- [ ] **Step 5: Run tests and commit**

Run: `python -m unittest tests.test_render_hero -v`

Expected: all hero tests pass.

```bash
git add scripts/render_hero.py tests/test_render_hero.py
git commit -m "feat: build split poster profile hero"
```

### Task 2: Export and wire the new hero

**Files:**
- Modify: `scripts/render_hero.py`
- Modify: `tests/test_readme.py`
- Modify: `README.md`
- Create: `assets/hero-split.gif`
- Create: `assets/hero-split-static.png`

**Interfaces:**
- Consumes: `render_assets(output_dir: Path) -> tuple[Path, Path]`
- Produces: README reference `assets/hero-split.gif?v=split-poster-20260903`

- [ ] **Step 1: Write failing README and output tests**

```python
def test_split_poster_hero_is_versioned(self) -> None:
    self.assertIn(
        "assets/hero-split.gif?v=split-poster-20260903",
        self.text,
    )
    self.assertNotIn("assets/hero.gif?v=", self.text)
```

```python
with Image.open(gif_path) as animation:
    self.assertEqual(animation.size, (1280, 720))
    self.assertEqual(animation.n_frames, FRAME_COUNT)
    self.assertEqual(animation.info["duration"], DURATION_MS)
    self.assertEqual(animation.convert("RGBA").getpixel((0, 0))[3], 0)
self.assertLessEqual(gif_path.stat().st_size, 5 * 1024 * 1024)
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m unittest tests.test_readme tests.test_render_hero -v`

Expected: FAIL because the README still references `assets/hero.gif` and the new files do not exist.

- [ ] **Step 3: Export and reference the split poster**

```python
gif_path = output_dir / "hero-split.gif"
png_path = output_dir / "hero-split-static.png"
```

Replace only the first README image path with
`assets/hero-split.gif?v=split-poster-20260903`; keep the remaining module order unchanged.

- [ ] **Step 4: Generate, test, and commit**

Run: `python scripts/render_hero.py`

Run: `python -m unittest discover -s tests -v`

Expected: all tests pass and the GIF is no more than 5 MB.

```bash
git add README.md assets/hero-split.gif assets/hero-split-static.png scripts/render_hero.py tests/test_readme.py tests/test_render_hero.py
git commit -m "feat: publish split poster hero assets"
```

### Task 3: Visual QA and GitHub publication

**Files:**
- Verify: `assets/hero-split-static.png`
- Verify: `README.md`

**Interfaces:**
- Consumes: the committed split-poster assets and README.
- Produces: verified GitHub profile on `master`.

- [ ] **Step 1: Inspect the still at native resolution**

Confirm the right card matches the supplied reference structure: outer teal
border, inner rounded art panel, thin separate signal lines, three-line lower-left
headline, English card caption, and pill. Confirm the left side reads cleanly.

- [ ] **Step 2: Preview desktop and 375px widths**

Render a temporary local README preview. Confirm all images load, the page has no
horizontal overflow, and the hero remains readable and balanced.

- [ ] **Step 3: Run final verification**

Run: `python -m unittest discover -s tests -v`

Run: `git diff --check && git status --short --branch`

Expected: zero failing tests, no whitespace errors, and a clean branch ahead of `origin/master`.

- [ ] **Step 4: Publish and verify GitHub**

```bash
git push origin HEAD:master
gh api repos/hannnnnnnny/hannnnnnnny/commits/master --jq .sha
```

Open `https://github.com/hannnnnnnny` with a commit query parameter and confirm
the new `hero-split.gif` is loaded with no broken README images.
