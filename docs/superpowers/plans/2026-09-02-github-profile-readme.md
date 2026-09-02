# GitHub Profile README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Build, verify, and publish an English GitHub profile README for hannnnnnnny with a lightweight animated “Repetitive work. → Reliable systems.” hero.

**Architecture:** A deterministic Pillow script generates a self-contained GIF and PNG from local fonts and a fixed visual specification. README.md uses only native Markdown and conservative GitHub HTML, while standard-library tests validate asset limits, required content, link targets, and excluded dashboard clutter. Publishing connects this local repository to the public GitHub profile repository without overwriting an existing remote.

**Tech Stack:** Python 3.14, Pillow 12.3, unittest, Markdown, Git, GitHub CLI

## Global Constraints

- README copy is English only.
- The banner is 1280 × 360 pixels and displays at 100% width.
- The GIF is a seamless five-second loop at 18 FPS and no more than 5 MB.
- The banner uses near-black, warm off-white, mint green, and coral red.
- Motion must avoid flashes, rapid zooms, and abrupt cuts.
- The banner remains legible at a 375-pixel viewport.
- Project entries stack vertically.
- No remote scripts, tracking pixels, visitor counters, runtime dependencies, secrets, or private data.
- Do not add GitHub statistics, streak cards, trophies, or large badge collections.
- The target public GitHub repository is named exactly hannnnnnnny.

---

## File Map

- Create scripts/render_hero.py — deterministic renderer for the animated GIF and static PNG.
- Create tests/test_render_hero.py — validates dimensions, duration, frame count, and file-size budget.
- Create assets/hero.gif — generated animated manifesto.
- Create assets/hero-static.png — generated review frame.
- Create tests/test_readme.py — validates README content, local assets, links, and excluded widgets.
- Create README.md — GitHub profile content and links.
- Modify .gitignore — keep Python cache files out of the profile repository.

### Task 1: Deterministic animated hero

**Files:**

- Create: scripts/render_hero.py
- Create: tests/test_render_hero.py
- Create: assets/hero.gif
- Create: assets/hero-static.png
- Modify: .gitignore

**Interfaces:**

- Produces: render_assets(output_dir: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]
- Produces: assets/hero.gif and assets/hero-static.png for README.md
- Consumes: C:/Windows/Fonts/segoeuib.ttf and C:/Windows/Fonts/consola.ttf

- [ ] **Step 1: Add the failing renderer test**

Create tests/test_render_hero.py:

    import tempfile
    import unittest
    from pathlib import Path

    from PIL import Image

    from scripts.render_hero import FPS, FRAME_COUNT, render_assets


    class RenderHeroTests(unittest.TestCase):
        def test_rendered_assets_match_profile_constraints(self) -> None:
            with tempfile.TemporaryDirectory() as directory:
                gif_path, png_path = render_assets(Path(directory))

                self.assertTrue(gif_path.exists())
                self.assertTrue(png_path.exists())
                self.assertLessEqual(gif_path.stat().st_size, 5 * 1024 * 1024)

                with Image.open(gif_path) as animation:
                    self.assertEqual(animation.size, (1280, 360))
                    self.assertEqual(animation.n_frames, FRAME_COUNT)
                    self.assertEqual(animation.info["duration"], 1000 // FPS)

                with Image.open(png_path) as still:
                    self.assertEqual(still.size, (1280, 360))


    if __name__ == "__main__":
        unittest.main()

- [ ] **Step 2: Run the renderer test and verify it fails**

Run:

    python -m unittest tests.test_render_hero -v

Expected: FAIL with ModuleNotFoundError for scripts.render_hero.

- [ ] **Step 3: Implement the renderer**

Create scripts/render_hero.py:

    from __future__ import annotations

    import math
    from pathlib import Path

    from PIL import Image, ImageDraw, ImageFont

    WIDTH = 1280
    HEIGHT = 360
    FPS = 20
    FRAME_COUNT = FPS * 5
    DURATION_MS = 1000 // FPS

    BG = "#080909"
    OFF_WHITE = "#F4F3ED"
    MUTED = "#747A76"
    MINT = "#7CF6CE"
    CORAL = "#FF5A3C"
    BORDER = "#2C3030"

    FONT_ROOT = Path("C:/Windows/Fonts")
    DISPLAY_FONT = FONT_ROOT / "segoeuib.ttf"
    MONO_FONT = FONT_ROOT / "consola.ttf"


    def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
        if not path.exists():
            raise FileNotFoundError(f"Required font is missing: {path}")
        return ImageFont.truetype(str(path), size)


    def ease(value: float) -> float:
        clamped = max(0.0, min(1.0, value))
        return clamped * clamped * (3 - 2 * clamped)


    def phase(frame: int, start: int, end: int) -> float:
        return ease((frame - start) / max(1, end - start))


    def draw_header(draw: ImageDraw.ImageDraw) -> None:
        mono = font(MONO_FONT, 19)
        draw.text(
            (58, 38),
            "YI HAN / CURRENT MODE: BUILDING",
            font=mono,
            fill=MUTED,
        )


    def draw_prompt(draw: ImageDraw.ImageDraw, frame: int) -> None:
        mono = font(MONO_FONT, 20)
        box = (58, 286, 462, 329)
        draw.rounded_rectangle(box, radius=9, fill="#111313", outline=BORDER)
        draw.text((77, 297), "→", font=mono, fill=MINT)
        draw.text((105, 297), "turning friction into flow", font=mono, fill=MUTED)
        if (frame // 9) % 2 == 0:
            draw.rectangle((432, 300, 439, 318), fill=MINT)


    def draw_scanline(draw: ImageDraw.ImageDraw, frame: int) -> None:
        progress = frame / (FRAME_COUNT - 1)
        y = int(progress * (HEIGHT + 30)) - 15
        fade = min(1.0, min(progress, 1 - progress) * 14)
        color = (124, 246, 206, int(100 * fade))
        draw.line((0, y, WIDTH, y), fill=color, width=2)


    def draw_statement(draw: ImageDraw.ImageDraw, frame: int) -> None:
        display = font(DISPLAY_FONT, 68)
        x, y = 58, 98
        old_text = "Repetitive work."
        draw.text((x, y), old_text, font=display, fill=MUTED)

        old_box = draw.textbbox((x, y), old_text, font=display)
        strike_progress = phase(frame, 10, 27)
        strike_end = x + int((old_box[2] - x) * strike_progress)
        draw.rounded_rectangle(
            (x, y + 43, strike_end, y + 50),
            radius=3,
            fill=CORAL,
        )

        enter = phase(frame, 28, 45)
        exit_progress = phase(frame, 74, 89)
        visible = max(0.0, enter - exit_progress)
        new_y = 193 + int((1 - visible) * 45)
        draw.text(
            (x, new_y),
            "Reliable systems.",
            font=display,
            fill=(124, 246, 206, int(255 * visible)),
        )


    def make_frame(frame: int) -> Image.Image:
        image = Image.new("RGBA", (WIDTH, HEIGHT), BG)
        draw = ImageDraw.Draw(image, "RGBA")
        draw_header(draw)
        draw_statement(draw, frame)
        draw_prompt(draw, frame)
        draw_scanline(draw, frame)
        return image.convert("RGB")


    def quantize(image: Image.Image) -> Image.Image:
        return image.quantize(colors=64, method=Image.Quantize.MEDIANCUT)


    def render_assets(output_dir: Path) -> tuple[Path, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        frames = [quantize(make_frame(index)) for index in range(FRAME_COUNT)]
        gif_path = output_dir / "hero.gif"
        png_path = output_dir / "hero-static.png"
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=DURATION_MS,
            loop=0,
            optimize=True,
            disposal=2,
        )
        make_frame(55).save(png_path, optimize=True)
        return gif_path, png_path


    if __name__ == "__main__":
        gif, still = render_assets(Path("assets"))
        print(f"Rendered {gif} and {still}")

- [ ] **Step 4: Ignore local Python cache files**

Append to .gitignore:

    __pycache__/
    *.py[cod]

- [ ] **Step 5: Generate the assets**

Run:

    python scripts/render_hero.py

Expected:

    Rendered assets\hero.gif and assets\hero-static.png

- [ ] **Step 6: Run the renderer test**

Run:

    python -m unittest tests.test_render_hero -v

Expected: one test passes and the generated GIF is at most 5 MB.

- [ ] **Step 7: Inspect the generated still frame and animation metadata**

Run:

    python -c "from PIL import Image; from pathlib import Path; p=Path('assets/hero.gif'); im=Image.open(p); print(im.size, im.n_frames, im.info.get('duration'), p.stat().st_size)"

Expected: (1280, 360), 100 frames, 50 milliseconds per frame, and a byte size no greater than 5,242,880.

Open assets/hero-static.png with the local image viewer. Confirm the eyebrow, both manifesto lines, coral strike, prompt, and caret are inside the frame.

- [ ] **Step 8: Commit the animated hero**

Run:

    git add .gitignore scripts/render_hero.py tests/test_render_hero.py assets/hero.gif assets/hero-static.png
    git commit -m "feat: add animated profile hero"

Expected: a commit containing only the renderer, its tests, generated assets, and cache ignore rules.

### Task 2: Accessible profile README

**Files:**

- Create: README.md
- Create: tests/test_readme.py

**Interfaces:**

- Consumes: assets/hero.gif from Task 1
- Produces: README.md as the GitHub profile entry point
- Produces: a standard-library validation suite runnable with python -m unittest

- [ ] **Step 1: Add the failing README test**

Create tests/test_readme.py:

    import re
    import unittest
    from pathlib import Path


    ROOT = Path(__file__).resolve().parents[1]
    README = ROOT / "README.md"


    class ReadmeTests(unittest.TestCase):
        def setUp(self) -> None:
            self.text = README.read_text(encoding="utf-8")

        def test_required_identity_and_projects_are_present(self) -> None:
            required = [
                "Hey, I'm Yi Han.",
                "AI-assisted products",
                "KiwiCue",
                "PanSub",
                "Till Tally",
            ]
            for value in required:
                self.assertIn(value, self.text)

        def test_local_images_exist_and_have_alt_text(self) -> None:
            images = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", self.text)
            self.assertGreaterEqual(len(images), 1)
            for alt, relative_path in images:
                self.assertTrue(alt.strip())
                self.assertTrue((ROOT / relative_path).exists())

        def test_approved_links_are_exact(self) -> None:
            links = [
                "https://github.com/hannnnnnnny/kiwicue",
                "https://github.com/hannnnnnnny/pansub",
                "https://github.com/hannnnnnnny/till-tally",
                "https://hannnnnnnny.github.io/yi-han-software-engineer/",
                "https://www.linkedin.com/in/yi-han-29ab28323/",
                "mailto:harryhaber606@gmail.com",
            ]
            for link in links:
                self.assertIn(link, self.text)

        def test_dashboard_clutter_is_absent(self) -> None:
            banned = ["github-readme-stats", "streak-stats", "visitor-badge"]
            lowered = self.text.lower()
            for value in banned:
                self.assertNotIn(value, lowered)


    if __name__ == "__main__":
        unittest.main()

- [ ] **Step 2: Run the README test and verify it fails**

Run:

    python -m unittest tests.test_readme -v

Expected: ERROR because README.md does not exist.

- [ ] **Step 3: Create the README**

Create README.md:

    <p align="center">
      <img
        src="assets/hero.gif"
        width="100%"
        alt="Repetitive work transforms into reliable systems."
      />
    </p>

    # Hey, I'm Yi Han.

    A full-stack developer in Auckland building **AI-assisted products and practical automation**. I turn messy, repetitive workflows into reliable systems people can actually use.

    [View my portfolio](https://hannnnnnnny.github.io/yi-han-software-engineer/) · [Connect on LinkedIn](https://www.linkedin.com/in/yi-han-29ab28323/) · [Email me](mailto:harryhaber606@gmail.com)

    ## Selected systems

    ### [01 · KiwiCue](https://github.com/hannnnnnnny/kiwicue)

    Bilingual Auckland event discovery with smart reminders.

    TypeScript · Product discovery · Automation

    ---

    ### [02 · PanSub](https://github.com/hannnnnnnny/pansub)

    Real-time AI Chinese subtitles for lecture recordings.

    JavaScript · AI integration · Accessibility

    ---

    ### [03 · Till Tally](https://github.com/hannnnnnnny/till-tally)

    Retail analytics that turns sales data into useful decisions.

    TypeScript · Data visualization · Business intelligence

    ## Working with

    TypeScript · JavaScript · Java · Spring Boot · Vue · MySQL · AI integrations · Workflow automation

    ---

    Building from Auckland, New Zealand — always interested in useful software, thoughtful automation, and the problems between them.

- [ ] **Step 4: Run the full local test suite**

Run:

    python -m unittest discover -s tests -v

Expected: all renderer and README tests pass.

- [ ] **Step 5: Check formatting and repository scope**

Run:

    git diff --check
    git status --short

Expected: no whitespace errors; only README.md and tests/test_readme.py are uncommitted.

- [ ] **Step 6: Commit the profile README**

Run:

    git add README.md tests/test_readme.py
    git commit -m "feat: create GitHub profile README"

Expected: a commit containing only README.md and its content validation tests.

### Task 3: Visual and responsive quality review

**Files:**

- Modify if defects are found: scripts/render_hero.py
- Regenerate if defects are found: assets/hero.gif
- Regenerate if defects are found: assets/hero-static.png
- Modify if defects are found: README.md

**Interfaces:**

- Consumes: completed assets and README from Tasks 1–2
- Produces: visually approved desktop and 375-pixel presentation

- [ ] **Step 1: Inspect the full-resolution still**

Open assets/hero-static.png with the local image viewer at original resolution.

Expected: no clipped text; the coral line cleanly crosses “Repetitive work.”; mint text is readable; the prompt remains secondary.

- [ ] **Step 2: Inspect a 375-pixel simulation**

Run:

    python -c "from PIL import Image; im=Image.open('assets/hero-static.png'); im.resize((375, 105), Image.Resampling.LANCZOS).save('assets/hero-mobile-review.png')"

Open assets/hero-mobile-review.png with the local image viewer.

Expected: the core manifesto remains readable and no focal text is cropped.

- [ ] **Step 3: Remove the temporary review image**

Run:

    Remove-Item -LiteralPath "assets/hero-mobile-review.png"

Expected: the temporary image is removed and will not be committed.

- [ ] **Step 4: Re-run all checks**

Run:

    python -m unittest discover -s tests -v
    git diff --check
    git status --short

Expected: all tests pass, no whitespace errors, and the worktree is clean. If visual changes were required, commit only the corrected files with:

    git add scripts/render_hero.py assets/hero.gif assets/hero-static.png README.md
    git commit -m "fix: refine profile README presentation"

### Task 4: Publish and verify the GitHub profile

**Files:**

- No local file changes expected.

**Interfaces:**

- Consumes: clean local master branch
- Produces: public repository https://github.com/hannnnnnnny/hannnnnnnny and rendered profile README

- [ ] **Step 1: Authenticate GitHub CLI**

Run:

    gh auth status

Current expected result: the stored token for hannnnnnnny is invalid.

Run:

    gh auth login -h github.com -p https -w

Expected: browser authentication completes for account hannnnnnnny. Stop and request user action if GitHub displays an authorization code or approval page.

- [ ] **Step 2: Check whether the profile repository already exists**

Run:

    gh repo view hannnnnnnny/hannnnnnnny --json nameWithOwner,visibility,url,defaultBranchRef

Expected: either metadata for an existing public repository or a clear “repository not found” error. Do not create a duplicate or overwrite an existing repository.

- [ ] **Step 3: Connect or create the remote safely**

If the repository exists and has no conflicting history, run:

    git remote add origin https://github.com/hannnnnnnny/hannnnnnnny.git
    git fetch origin

Inspect:

    git log --oneline --decorate --all -10

If the repository does not exist, run:

    gh repo create hannnnnnnny --public --source=. --remote=origin

Expected: origin points to https://github.com/hannnnnnnny/hannnnnnnny.git.

- [ ] **Step 4: Push the profile branch**

Run:

    git push -u origin master

Expected: master is pushed without force and tracks origin/master.

- [ ] **Step 5: Verify the public files and profile**

Run:

    Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/hannnnnnnny/hannnnnnnny/master/README.md" | Select-Object StatusCode
    Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/hannnnnnnny/hannnnnnnny/master/assets/hero.gif" | Select-Object StatusCode
    Invoke-WebRequest -UseBasicParsing "https://github.com/hannnnnnnny" | Select-Object StatusCode

Expected: all three requests return StatusCode 200.

Open https://github.com/hannnnnnnny in a browser and confirm:

- The animation plays.
- The text is not clipped.
- The three projects and contact links are visible.
- The README appears in the profile overview.

- [ ] **Step 6: Report publication**

Run:

    git status --short
    git log --oneline -5

Expected: clean worktree with the implementation commits visible. Report the live profile URL and any authentication step the user completed.
