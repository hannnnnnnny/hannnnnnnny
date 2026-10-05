# Light Profile README with Real Project Previews

## Objective

Re-theme the image-led GitHub profile README from the near-black "Obsidian"
palette to a **light (white) palette with green/cyan accents**, expand the
README from hero-only back to the **full section sequence**, and replace the
abstract project posters with **light "browser-frame" cards that embed real
application screenshots**.

Featured projects this version: **KiwiCue, PanSub, ReNova**. TillTally is
dropped for now because it has no live deployment to screenshot.

## Approved Direction

Approach A (approved): re-theme the whole generated-image system to light and
composite real screenshots into light project cards, keeping the existing
image-led, self-contained-module architecture so GitHub renders it
consistently in both light and dark UI themes.

Not doing: Markdown-based project sections, external badge/stat/trophy widgets,
Markdown tables, visitor counters (keeps the current image-led philosophy).

## Palette (light tokens)

Replaces the dark tokens in `scripts/visual_tokens.py`. Accent colours are
deepened where needed so lines and labels keep AA contrast on white.

| Token | Old (dark) | New (light) | Use |
|-------|-----------|-------------|-----|
| `BG` | `#080A0A` | `#FBFCFB` | page / card backdrop |
| `SURFACE` | `#0D1110` | `#FFFFFF` | raised panels, pills |
| `BORDER` | `#29312F` | `#E3E8E6` | hairlines, card edges |
| `TEXT` | `#F2F2EB` | `#0E1512` | primary text |
| `MUTED` | `#84908A` | `#5E6B66` | secondary text |
| `ACCENT` (new) | — | `#0FB886` | deep teal: lines, accent labels on white |
| `MINT` | `#7CF6CE` | `#7CF6CE` (kept) | glows / fills only, not text on white |
| `VIOLET` | `#9F91FF` | `#6C5CE7` | project accent (deepened) |
| `CORAL` | `#FF7054` | `#E8603C` | project accent (deepened) |

Grid lines and the signal ribbon use `ACCENT`/`MINT` at low opacity on white.

## GitHub-Compatible Architecture

Unchanged principle: GitHub supports no README CSS/JS, so every styled module
is a self-contained local image referenced from `README.md`. Rounded corners
are baked with transparent pixels. All modules use a 1280px source width and
scale to 100% of the README column; text stays readable at a 375px viewport.

## README Section Sequence

1. **Hero** (`assets/hero-*`): eyebrow "YI HAN / AI AUTOMATION ENGINEER",
   primary line "TURN FRICTION INTO", accent line "FLOW.", metadata
   "FULL-STACK PRODUCTS / AUCKLAND, NEW ZEALAND". Light background; signal
   ribbon in teal/mint; ribbon must never cross or obscure text.
2. **Identity** (`assets/identity.svg`): "Yi Han.", label "FULL-STACK × AI",
   copy "I design and build AI-assisted products that turn repetitive
   workflows into reliable systems people can actually use.", and the three
   destination labels.
3. **Selected work** — one light browser-frame card per project, each wrapped
   in its link, each embedding a real screenshot:
   - **KiwiCue** — screenshot of https://kiwicue.nz — "Bilingual Auckland
     event discovery with smart reminders." — `DISCOVERY · AUTOMATION ·
     TYPESCRIPT` — accent teal/mint.
   - **PanSub** — the repo store screenshot
     (`pansub/assets/store/screenshot-main-1280x800.png`) — "Real-time AI
     Chinese subtitles for lecture recordings." — `AI · ACCESSIBILITY ·
     JAVASCRIPT` — accent violet.
   - **ReNova** — screenshot of https://renova-marketplace.vercel.app —
     "Second-hand C2C marketplace: listings, offers, orders, reviews." —
     `FULL-STACK · MARKETPLACE · VUE` — accent coral.
4. **Tech stack** (`assets/stack.*`): TypeScript, JavaScript, Java, Spring
   Boot, Vue, MySQL, AI APIs, Automation — light strip.
5. **Contact** (`assets/contact.*`): "Have an idea worth automating?" /
   "BUILDING FROM AUCKLAND, NEW ZEALAND" / "LET'S TALK ↗" → mailto.

## Production Method

1. **Centralise the palette.** Today only `render_sections.py` imports
   `visual_tokens`; `render_hero.py`, `render_project_previews.py`,
   `render_flow_hero.py`, `render_minimal_hero.py`, `animate_sections.py`
   hardcode colours. Move all colours to `visual_tokens.py` (add `ACCENT`) and
   make every script import from it, so the theme has one source of truth.
2. **Capture real screenshots** headless (puppeteer-core + local Chrome) at
   1280px, saved under `assets/screens/`:
   - `kiwicue.png` from https://kiwicue.nz
   - `renova.png` from https://renova-marketplace.vercel.app
   - `pansub.png` copied from the PanSub repo store screenshot
   Each is verified to be non-blank before use (no login/error page).
3. **Adapt `render_project_previews.py`** to composite a given screenshot into
   a light rounded browser-frame card (dot bar + title + one-liner + stack
   chips baked in), 1280px, rounded transparent corners, per-project accent.
4. **Re-render** hero, identity, stack, contact in the light theme via their
   scripts, preserving animation constraints: 5s at 20fps, loops smoothly,
   < 5 MB, no flashes, ribbon never crosses text-safe regions.
5. **Rewrite `README.md`** to the full light sequence: each image on its own
   line, descriptive alt text, individual links.

## Exact Links

- KiwiCue: site https://kiwicue.nz · repo https://github.com/hannnnnnnny/kiwicue
- PanSub: repo https://github.com/hannnnnnnny/pansub
- ReNova: live https://renova-marketplace.vercel.app · repo https://github.com/hannnnnnnny/ReNova-Second-Hand-C2C-Marketplace
- Portfolio: https://hannnnnnnny.github.io/yi-han-software-engineer/ (verify current during implementation)
- LinkedIn: https://www.linkedin.com/in/yi-han-29ab28323/
- Email: mailto:harryhaber606@gmail.com

## Testing (TDD)

- Update existing tests for the light palette: remove/adjust any assertion
  tied to dark hex values; keep structural assertions (1280px width, viewBox,
  rounded outer rect, title/desc, ribbon never intersecting text-safe boxes,
  signal visibility).
- New tests for project cards: asset exists, 1280px width, rounded transparent
  corners, embeds a non-empty screenshot region, file-size limit.
- Screenshot capture is a committed-fixture step (not run in CI); tests assert
  the committed screenshots and composed cards exist and meet dimension/size
  specs.
- Verify light cards render correctly on both GitHub light and dark UI themes
  (baked transparent rounded corners).

## Verification

- `python -m pytest tests/` (or the repo's runner) passes.
- Re-render all assets; inspect desktop and 375px widths.
- Push to `feat/light-profile-readme`; after merge to `master`, inspect the
  live profile for rounded corners, link behaviour, animation playback, light
  theme in both GitHub UI modes, and absence of Markdown tables/widgets.
- No force push.

## Non-Goals

- TillTally (no live screenshot this version).
- Any external widget/badge/stat service or Markdown tables.
- Re-positioning the identity copy (kept as "FULL-STACK × AI / AI AUTOMATION
  ENGINEER"); adjustable later if desired.
