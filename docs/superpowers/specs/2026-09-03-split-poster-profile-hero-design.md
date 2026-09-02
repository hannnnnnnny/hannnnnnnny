# Split Poster Profile Hero Design

## Objective

Replace the current horizontal ribbon hero with one wide animated image that
recreates the approved P1-A portrait card on the right and introduces Yi Han on
the left. The composition must render consistently on GitHub without relying on
HTML columns, CSS, or theme-dependent table styling.

## Output

- `assets/hero-split.gif`: 1280 × 720 animated GitHub hero.
- `assets/hero-split-static.png`: matching representative still.
- The README references the GIF with a cache-busting query parameter.
- The existing identity, project, stack, and contact modules remain unchanged.

## Composition

The hero is a single canvas with two visually distinct zones and no divider.

### Left introduction

- Occupies approximately 54% of the canvas.
- Eyebrow: `AI & AUTOMATION / AUCKLAND, NZ`.
- Headline: `Hi, I'm` on the first line and `Yi Han.` on the second.
- Supporting copy: `I design and build AI-assisted products that turn
  repetitive workflows into reliable systems.`
- One restrained action label: `VIEW SELECTED WORK ↘`.
- Large negative space; no stats, badges, or dashboard decoration.

### Right P1-A portrait card

- Recreates the supplied reference at the same 373:506 proportion.
- Outer card uses a thin desaturated mint stroke and a 22px-equivalent radius.
- Inner artwork panel uses a dark fill, subtle grid, and a 16px-equivalent radius.
- Two separate luminous signal lines cross the upper half:
  - mint line above;
  - violet line below with a restrained coral tail/glow.
- A small glowing particle travels along the mint signal line.
- Headline is fixed at the inner panel's lower-left in three lines:
  `TURN FRICTION` / `INTO` / `FLOW.`.
- The headline never overlaps either signal line.
- The lower card copy is English:
  - `P1-A · LIQUID SIGNAL RIBBON`
  - `A luminous data stream in motion — restrained, fluid, and alive.`
  - pill: `LIGHT · TECH · FLUID`

## Art direction

- Canvas: near-black `#090D0C` with a subtle green-black atmospheric gradient.
- Primary text: warm white `#F4F3ED`.
- Secondary text: cool grey `#7A8681`.
- Accents: mint `#71F6C6`, violet `#8E7CFF`, restrained coral `#FF6B4A`.
- Typography: bold Segoe UI display face and Consolas metadata.
- The right card is the visual object; the left side remains editorial and calm.

## Motion

- Five-second seamless loop at 20 FPS.
- Both signal lines drift independently with low-amplitude wave motion.
- The mint particle travels left-to-right and fades near the loop boundary.
- Glow breathes subtly; text and card geometry remain stationary.
- Motion stays within the upper signal region and never crosses the headline.

## GitHub constraints

- One image prevents GitHub from changing the two-column relationship.
- The GIF must remain below 5 MB.
- The composition must remain readable when scaled to GitHub's profile width.
- A 375px viewport may scale the entire composition, but must not overflow.
- Transparent rounded outer canvas corners are retained.
- The static PNG provides deterministic visual QA and repository fallback.

## Verification

- Unit tests lock dimensions, frame count, duration, transparency, and file size.
- Geometry tests prove signal masks do not enter text safe areas.
- README tests require the new asset and cache-busting query.
- Visual QA compares the generated still with the supplied reference structure at
  desktop width and confirms no horizontal overflow at 375px.
- The live GitHub profile is checked after publishing for asset load and cache
  freshness.
