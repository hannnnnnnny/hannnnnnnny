# Premium GitHub Profile README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Replace the Markdown-heavy GitHub profile with the approved P1-A Obsidian Editorial system: a rounded animated liquid-ribbon hero and six rounded SVG modules.

**Architecture:** Python generates every styled asset locally and deterministically. Pillow renders the transparent-corner GIF; standard-library string templates render self-contained SVG modules with title and description metadata. README.md becomes a small link-and-image composition, and tests validate rendering, accessibility, links, mobile legibility, and GitHub-safe markup.

**Tech Stack:** Python 3.14, Pillow 12.3, SVG 1.1, XML ElementTree, unittest, Markdown, Git, GitHub CLI

## Global Constraints

- Visual direction: P1-A Obsidian Editorial with Liquid Signal Ribbon.
- Content modules use 18px rounded corners; overall visual language uses 22px rounded corners.
- Every source asset is 1280px wide and displays at 100% README width.
- The hero is a five-second, 20 FPS loop under 5 MB.
- The ribbon never intersects text-safe regions.
- Primary text remains readable at a 375px viewport.
- All SVGs include title and description elements.
- All assets are local and contain no scripts, external fonts, remote images, tracking, statistics, counters, or badge services.
- README.md contains no Markdown tables or blockquotes.
- Project posters remain separately clickable.
- Publishing targets origin/master without force push.

---

## File Map

- Create scripts/visual_tokens.py — shared colors, dimensions, escaping, SVG shell, and rounded-card helpers.
- Create scripts/render_sections.py — deterministic identity, project, stack, and contact SVG renderer.
- Modify scripts/render_hero.py — replace the current status-panel animation with the liquid signal ribbon and transparent rounded corners.
- Create tests/test_sections.py — SVG structure, metadata, dimensions, and rounded-corner tests.
- Modify tests/test_render_hero.py — transparent corner, timing, file-size, and ribbon safe-zone tests.
- Modify tests/test_readme.py — image-led composition, exact links, alt text, and forbidden Markdown tests.
- Modify README.md — linked asset sequence with concise fallback copy.
- Create assets/identity.svg, assets/project-kiwicue.svg, assets/project-pansub.svg, assets/project-till-tally.svg, assets/stack.svg, and assets/contact.svg.
- Regenerate assets/hero.gif and assets/hero-static.png.

### Task 1: Shared SVG system and rounded static modules

**Files:**

- Create: scripts/visual_tokens.py
- Create: scripts/render_sections.py
- Create: tests/test_sections.py
- Create: assets/identity.svg
- Create: assets/project-kiwicue.svg
- Create: assets/project-pansub.svg
- Create: assets/project-till-tally.svg
- Create: assets/stack.svg
- Create: assets/contact.svg

**Interfaces:**

- Produces svg_document(title: str, description: str, height: int, body: str, accent: str) -> str.
- Produces render_sections(output_dir: pathlib.Path) -> list[pathlib.Path].
- Produces six 1280px-wide SVG files consumed by README.md.

- [ ] **Step 1: Add the failing SVG asset tests**

Create tests/test_sections.py:

    import tempfile
    import unittest
    import xml.etree.ElementTree as ET
    from pathlib import Path

    from scripts.render_sections import OUTPUTS, render_sections

    SVG = "{http://www.w3.org/2000/svg}"


    class SectionAssetTests(unittest.TestCase):
        def test_renderer_creates_every_approved_asset(self) -> None:
            with tempfile.TemporaryDirectory() as directory:
                paths = render_sections(Path(directory))
                self.assertEqual({path.name for path in paths}, set(OUTPUTS))

        def test_assets_have_metadata_and_rounded_outer_card(self) -> None:
            with tempfile.TemporaryDirectory() as directory:
                for path in render_sections(Path(directory)):
                    root = ET.parse(path).getroot()
                    self.assertEqual(root.attrib["width"], "1280")
                    self.assertTrue(root.attrib["viewBox"].startswith("0 0 1280 "))
                    self.assertIsNotNone(root.find(f"{SVG}title"))
                    self.assertIsNotNone(root.find(f"{SVG}desc"))
                    outer = root.find(f"{SVG}rect")
                    self.assertEqual(outer.attrib["rx"], "18")


    if __name__ == "__main__":
        unittest.main()

- [ ] **Step 2: Run the SVG tests and verify RED**

Run:

    python -m unittest tests.test_sections -v

Expected: FAIL with ModuleNotFoundError for scripts.render_sections.

- [ ] **Step 3: Add shared SVG tokens and helpers**

Create scripts/visual_tokens.py:

    from __future__ import annotations

    from html import escape

    WIDTH = 1280
    BG = "#080A0A"
    SURFACE = "#0D1110"
    BORDER = "#29312F"
    TEXT = "#F2F2EB"
    MUTED = "#84908A"
    MINT = "#7CF6CE"
    VIOLET = "#9F91FF"
    CORAL = "#FF7054"


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
              <path d="M36 0H0V36" fill="none" stroke="{accent}" stroke-opacity=".06"/>
            </pattern>
          </defs>
          <rect x="1" y="1" width="1278" height="{height - 2}" rx="18"
            fill="{BG}" stroke="{BORDER}"/>
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
    ) -> str:
        safe = escape(value)
        return (
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" font-family="{family}">{safe}</text>'
        )


    def pill(x: int, y: int, width: int, value: str, accent: str) -> str:
        return (
            f'<rect x="{x}" y="{y}" width="{width}" height="34" rx="17" '
            f'fill="{SURFACE}" stroke="{BORDER}"/>'
            + text(x + 17, y + 22, value, 13, accent, 600, "Consolas,monospace")
        )

- [ ] **Step 4: Implement the deterministic section renderer**

Create scripts/render_sections.py with these complete public structures and functions:

    from __future__ import annotations

    from pathlib import Path

    from scripts.visual_tokens import (
        BORDER,
        CORAL,
        MINT,
        MUTED,
        SURFACE,
        TEXT,
        VIOLET,
        pill,
        svg_document,
        text,
    )

    OUTPUTS = (
        "identity.svg",
        "project-kiwicue.svg",
        "project-pansub.svg",
        "project-till-tally.svg",
        "stack.svg",
        "contact.svg",
    )

    PROJECTS = (
        ("project-kiwicue.svg", "01 / 03", "KiwiCue",
         "Bilingual Auckland event discovery with smart reminders.",
         "DISCOVERY · AUTOMATION · TYPESCRIPT", ("EVENT", "MATCH", "REMIND"), MINT),
        ("project-pansub.svg", "02 / 03", "PanSub",
         "Real-time AI Chinese subtitles for lecture recordings.",
         "AI · ACCESSIBILITY · JAVASCRIPT", ("AUDIO", "AI", "SUBTITLE"), VIOLET),
        ("project-till-tally.svg", "03 / 03", "Till Tally",
         "Retail analytics that turns sales data into useful decisions.",
         "DATA · INTELLIGENCE · TYPESCRIPT", ("SALES", "SIGNAL", "DECIDE"), CORAL),
    )


    def identity_svg() -> str:
        body = (
            '<line x1="330" y1="1" x2="330" y2="188" stroke="' + BORDER + '"/>'
            + text(42, 48, "PROFILE / 001", 13, MUTED, 600, "Consolas,monospace")
            + text(42, 101, "Yi Han.", 43, TEXT, 800)
            + text(42, 135, "FULL-STACK × AI", 14, MINT, 600, "Consolas,monospace")
            + text(372, 67, "I design and build AI-assisted products that turn repetitive", 21)
            + text(372, 99, "workflows into reliable systems people can actually use.", 21)
            + pill(372, 126, 120, "PORTFOLIO ↗", MINT)
            + pill(506, 126, 112, "LINKEDIN ↗", TEXT)
            + pill(632, 126, 91, "EMAIL ↗", TEXT)
        )
        return svg_document("Yi Han profile", "Full-stack and AI product builder.", 190, body)


    def system_diagram(labels: tuple[str, str, str], accent: str) -> str:
        parts = ['<line x1="1000" y1="76" x2="1190" y2="76" stroke="#46544F"/>']
        for index, label in enumerate(labels):
            x = 920 + index * 120
            color = accent if index == 2 else BORDER
            parts.append(f'<rect x="{x}" y="54" width="92" height="44" rx="9" fill="{SURFACE}" stroke="{color}"/>')
            parts.append(text(x + 46, 81, label, 11, accent if index == 2 else MUTED, 600, "Consolas,monospace"))
        return "".join(parts)


    def project_svg(project: tuple[str, str, str, str, str, tuple[str, str, str], str]) -> str:
        _, number, name, description, metadata, labels, accent = project
        body = (
            '<line x1="112" y1="1" x2="112" y2="166" stroke="' + BORDER + '"/>'
            '<line x1="875" y1="1" x2="875" y2="166" stroke="' + BORDER + '"/>'
            + text(42, 91, number, 13, MUTED, 600, "Consolas,monospace")
            + text(153, 61, name + " ↗", 27, TEXT, 750)
            + text(153, 94, description, 17, MUTED, 400)
            + text(153, 128, metadata, 12, accent, 600, "Consolas,monospace")
            + system_diagram(labels, accent)
        )
        return svg_document(name, description, 168, body, accent)


    def stack_svg() -> str:
        names = ("TypeScript", "JavaScript", "Java", "Spring Boot",
                 "Vue", "MySQL", "AI APIs", "Automation")
        parts = [text(38, 48, "BUILDING WITH", 12, MUTED, 600, "Consolas,monospace"),
                 text(38, 85, "Focused tools.", 26, TEXT, 750),
                 '<line x1="285" y1="1" x2="285" y2="126" stroke="' + BORDER + '"/>']
        x = 328
        for index, name in enumerate(names):
            width = 58 + len(name) * 7
            parts.append(pill(x, 46, width, name, MINT if index % 3 == 0 else TEXT))
            x += width + 12
        return svg_document("Technology stack", ", ".join(names), 128, "".join(parts))


    def contact_svg() -> str:
        body = (
            text(38, 55, "Have an idea worth automating?", 24, TEXT, 750)
            + text(38, 87, "BUILDING FROM AUCKLAND, NEW ZEALAND", 12, MUTED, 600, "Consolas,monospace")
            + '<rect x="1080" y="37" width="153" height="52" rx="26" fill="' + MINT + '"/>'
            + text(1105, 69, "LET'S TALK ↗", 14, "#08100D", 800, "Consolas,monospace")
        )
        return svg_document("Contact Yi Han", "Have an idea worth automating? Let's talk.", 126, body)


    def render_sections(output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        documents = {"identity.svg": identity_svg(), "stack.svg": stack_svg(),
                     "contact.svg": contact_svg()}
        documents.update({project[0]: project_svg(project) for project in PROJECTS})
        paths = []
        for name in OUTPUTS:
            path = output_dir / name
            path.write_text(documents[name], encoding="utf-8")
            paths.append(path)
        return paths


    if __name__ == "__main__":
        for rendered in render_sections(Path("assets")):
            print(f"Rendered {rendered}")

- [ ] **Step 5: Generate and test all SVG modules**

Run:

    python scripts/render_sections.py
    python -m unittest tests.test_sections -v

Expected: six Rendered lines and two passing tests.

- [ ] **Step 6: Commit the static visual system**

Run:

    git add scripts/visual_tokens.py scripts/render_sections.py tests/test_sections.py assets/*.svg
    git commit -m "feat: add premium profile visual modules"

### Task 2: Rounded liquid-ribbon hero

**Files:**

- Modify: scripts/render_hero.py
- Modify: tests/test_render_hero.py
- Regenerate: assets/hero.gif
- Regenerate: assets/hero-static.png

**Interfaces:**

- Keeps render_assets(output_dir: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path].
- Adds TEXT_SAFE_BOXES as immutable rectangles used by tests.

- [ ] **Step 1: Replace status-panel tests with failing P1-A tests**

In tests/test_render_hero.py, remove the status-panel density test and add:

    def test_gif_has_transparent_rounded_corners(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            gif_path, _ = render_assets(Path(directory))
            with Image.open(gif_path) as animation:
                transparency = animation.info.get("transparency")
                self.assertIsNotNone(transparency)
                self.assertEqual(animation.getpixel((0, 0)), transparency)

    def test_ribbon_never_enters_text_safe_boxes(self) -> None:
        from scripts.render_hero import TEXT_SAFE_BOXES, ribbon_mask

        for frame_number in range(FRAME_COUNT):
            mask = ribbon_mask(frame_number)
            for safe_box in TEXT_SAFE_BOXES:
                self.assertIsNone(mask.crop(safe_box).getbbox())

Run:

    python -m unittest tests.test_render_hero -v

Expected: FAIL because TEXT_SAFE_BOXES and ribbon_mask do not exist and the current GIF corner is opaque.

- [ ] **Step 2: Implement the approved hero behavior**

Update scripts/render_hero.py so it retains WIDTH=1280, HEIGHT=360, FPS=20, FRAME_COUNT=100, DURATION_MS=50 and exposes:

    TEXT_SAFE_BOXES = ((50, 22, 680, 86), (50, 238, 740, 345))


    def rounded_alpha() -> Image.Image:
        mask = Image.new("L", (WIDTH, HEIGHT), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, WIDTH - 1, HEIGHT - 1),
            radius=22,
            fill=255,
        )
        return mask


    def ribbon_mask(frame: int) -> Image.Image:
        mask = Image.new("L", (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(mask)
        phase_value = frame / FRAME_COUNT * math.tau
        points = []
        for x in range(-80, WIDTH + 81, 16):
            y = 158 + math.sin(x / 155 + phase_value) * 28
            points.append((x, int(y)))
        draw.line(points, fill=205, width=34, joint="curve")
        return mask


    def draw_ribbon(image: Image.Image, frame: int) -> None:
        mask = ribbon_mask(frame)
        gradient = Image.new("RGBA", image.size)
        pixels = gradient.load()
        for x in range(WIDTH):
            mix = x / WIDTH
            color = (
                int(124 + 35 * mix),
                int(246 - 95 * mix),
                int(206 + 25 * mix),
                210,
            )
            for y in range(HEIGHT):
                pixels[x, y] = color
        image.alpha_composite(Image.composite(gradient, Image.new("RGBA", image.size), mask))

Place the ribbon only through the center band. Draw the eyebrow at (52, 36), the white line “TURN FRICTION INTO” at (52, 245), the mint “FLOW.” at (52, 316), and right-aligned metadata above the ribbon. Apply rounded_alpha before quantization. Reserve palette index 0 for transparency, encode a seven-pixel frame marker at the bottom edge, and save with transparency=0, disposal=2, optimize=True.

- [ ] **Step 3: Generate and verify the hero**

Run:

    python scripts/render_hero.py
    python -m unittest tests.test_render_hero -v

Expected: all hero tests pass; the GIF has 100 frames, 50ms duration, transparent corner pixels, and size at most 5 MB.

- [ ] **Step 4: Commit the hero redesign**

Run:

    git add scripts/render_hero.py tests/test_render_hero.py assets/hero.gif assets/hero-static.png
    git commit -m "feat: redesign profile hero with liquid motion"

### Task 3: Image-led README composition

**Files:**

- Modify: README.md
- Modify: tests/test_readme.py

**Interfaces:**

- Consumes all seven generated image assets.
- Produces exact clickable destinations for identity, project, and contact modules.

- [ ] **Step 1: Add failing README composition tests**

Replace the structured-table test with:

    def test_readme_uses_only_approved_visual_modules(self) -> None:
        expected = [
            "assets/hero.gif",
            "assets/identity.svg",
            "assets/project-kiwicue.svg",
            "assets/project-pansub.svg",
            "assets/project-till-tally.svg",
            "assets/stack.svg",
            "assets/contact.svg",
        ]
        for path in expected:
            self.assertEqual(self.text.count(path), 1)
        self.assertNotIn("<table>", self.text)
        self.assertNotIn("> **", self.text)

Run:

    python -m unittest tests.test_readme -v

Expected: FAIL because the six SVG assets are absent from README.md and the existing table and blockquote remain.

- [ ] **Step 2: Replace README.md with the approved image sequence**

Use this complete README.md:

    ![Animated liquid signal ribbon introducing Yi Han, an AI automation engineer.](assets/hero.gif)

    <a href="https://hannnnnnnny.github.io/yi-han-software-engineer/">
      <img src="assets/identity.svg" width="100%" alt="Yi Han, a full-stack developer building practical AI automation." />
    </a>

    <a href="https://github.com/hannnnnnnny/kiwicue">
      <img src="assets/project-kiwicue.svg" width="100%" alt="KiwiCue: bilingual Auckland event discovery with smart reminders." />
    </a>

    <a href="https://github.com/hannnnnnnny/pansub">
      <img src="assets/project-pansub.svg" width="100%" alt="PanSub: real-time AI Chinese subtitles for lecture recordings." />
    </a>

    <a href="https://github.com/hannnnnnnny/till-tally">
      <img src="assets/project-till-tally.svg" width="100%" alt="Till Tally: retail analytics that turns sales data into useful decisions." />
    </a>

    ![Focused tools: TypeScript, JavaScript, Java, Spring Boot, Vue, MySQL, AI APIs, and automation.](assets/stack.svg)

    <a href="mailto:harryhaber606@gmail.com">
      <img src="assets/contact.svg" width="100%" alt="Have an idea worth automating? Contact Yi Han." />
    </a>

    <p align="center">
      <a href="https://hannnnnnnny.github.io/yi-han-software-engineer/">Portfolio</a>
      · <a href="https://www.linkedin.com/in/yi-han-29ab28323/">LinkedIn</a>
      · <a href="mailto:harryhaber606@gmail.com">Email</a>
    </p>

- [ ] **Step 3: Run the full suite and commit**

Run:

    python -m unittest discover -s tests -v
    git diff --check

Expected: all tests pass and no whitespace errors.

Run:

    git add README.md tests/test_readme.py
    git commit -m "feat: compose image-led profile README"

### Task 4: Visual QA and live publication

**Files:**

- Modify only if QA finds defects: generated assets, their renderers, tests, or README.md.

**Interfaces:**

- Consumes the completed local branch.
- Produces verified origin/master and live profile presentation.

- [ ] **Step 1: Create local contact sheets**

Render hero-static.png and all SVG assets to a single desktop review image and a 375px-wide review image using Pillow with CairoSVG if already available. If CairoSVG is unavailable, use the installed browser screenshot tooling against a local HTML file containing the exact README image sequence.

Expected: all seven modules appear with visible 18px rounded corners and consistent gaps.

- [ ] **Step 2: Inspect desktop and mobile reviews**

Check:

- No text intersects the liquid ribbon.
- No text is clipped.
- Primary hero copy is readable at 375px.
- All three projects remain distinguishable.
- Rounded corners are visible against GitHub dark background.
- Fine metadata is secondary to titles and descriptions.

- [ ] **Step 3: Run final verification**

Run:

    python -m unittest discover -s tests -v
    git diff --check
    git status --short

Expected: all tests pass, no whitespace errors, and no uncommitted diagnostic files.

- [ ] **Step 4: Push explicitly to the profile default branch**

Run:

    git push origin HEAD:master

Expected: origin/master advances without force.

- [ ] **Step 5: Verify remote identity**

Run:

    git rev-parse HEAD
    gh api repos/hannnnnnnny/hannnnnnnny/commits/master --jq .sha
    git hash-object assets/hero.gif
    gh api "repos/hannnnnnnny/hannnnnnnny/contents/assets/hero.gif?ref=master" --jq .sha

Expected: local and remote commit hashes match; local and remote hero blob hashes match.

- [ ] **Step 6: Inspect the live GitHub profile**

Open https://github.com/hannnnnnnny with a commit-based cache-busting query. Confirm the seven modules render, the GIF moves, rounded corners are visible, all links navigate correctly, and the old table and blockquote are absent.

