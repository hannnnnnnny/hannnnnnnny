# Premium GitHub Profile README Redesign

## Objective

Replace the current Markdown-heavy profile README with an original, image-led portfolio system that GitHub renders consistently. The result presents Yi Han as a full-stack builder focused on AI-assisted products and practical automation.

## Approved Direction

The approved direction is **P1-A: Obsidian Editorial with a Liquid Signal Ribbon**.

- Near-black surfaces with subtle mint grid lines.
- Warm off-white display typography.
- Mint as the primary active color.
- Violet and coral used only to distinguish selected projects.
- Soft rounded corners: 18px for content modules and 22px for the overall visual language.
- A restrained animated ribbon is the only large motion element.
- Original composition inspired by the polish of 21st.dev and Anton Skvortsov's motion-led work without copying either source.

## GitHub-Compatible Architecture

GitHub does not support custom README CSS or JavaScript. Every styled module is therefore rendered locally as a self-contained image:

1. assets/hero.gif — animated hero with rounded transparent corners.
2. assets/hero-static.png — review frame and fallback reference.
3. assets/identity.svg — name, positioning statement, and contact labels.
4. assets/project-kiwicue.svg — linked KiwiCue project poster.
5. assets/project-pansub.svg — linked PanSub project poster.
6. assets/project-till-tally.svg — linked Till Tally project poster.
7. assets/stack.svg — focused technology strip.
8. assets/contact.svg — final contact call-to-action.

README.md contains the image sequence, descriptive alt text, and individual links. It does not use Markdown tables, blockquotes, statistics widgets, visitor counters, trophies, or external badge services.

## Content

### Hero

- Eyebrow: “YI HAN / AI AUTOMATION ENGINEER”
- Primary line: “TURN FRICTION INTO”
- Accent line: “FLOW.”
- Supporting metadata: “FULL-STACK PRODUCTS / AUCKLAND, NEW ZEALAND”

The liquid signal ribbon moves horizontally with a slow vertical wave. It must not cross or obscure any text.

### Identity

- Name: “Yi Han.”
- Label: “FULL-STACK × AI”
- Copy: “I design and build AI-assisted products that turn repetitive workflows into reliable systems people can actually use.”
- Destinations: Portfolio, LinkedIn, and email.

### Selected Systems

Each project is a separate full-width rounded poster wrapped in its repository link.

1. KiwiCue — “Bilingual Auckland event discovery with smart reminders.” Metadata: “DISCOVERY · AUTOMATION · TYPESCRIPT”.
2. PanSub — “Real-time AI Chinese subtitles for lecture recordings.” Metadata: “AI · ACCESSIBILITY · JAVASCRIPT”.
3. Till Tally — “Retail analytics that turns sales data into useful decisions.” Metadata: “DATA · INTELLIGENCE · TYPESCRIPT”.

Each poster contains a small three-stage system diagram. KiwiCue uses mint, PanSub uses violet, and Till Tally uses coral.

### Stack and Contact

The stack strip lists TypeScript, JavaScript, Java, Spring Boot, Vue, MySQL, AI APIs, and Automation.

The final call-to-action reads:

- “Have an idea worth automating?”
- “BUILDING FROM AUCKLAND, NEW ZEALAND”
- “LET'S TALK ↗”

The contact image links to mailto:harryhaber606@gmail.com.

## Exact Links

- KiwiCue: https://github.com/hannnnnnnny/kiwicue
- PanSub: https://github.com/hannnnnnnny/pansub
- Till Tally: https://github.com/hannnnnnnny/till-tally
- Portfolio: https://hannnnnnnny.github.io/yi-han-software-engineer/
- LinkedIn: https://www.linkedin.com/in/yi-han-29ab28323/
- Email: mailto:harryhaber606@gmail.com

## Responsive and Accessibility Requirements

- All modules use a 1280px source width and scale to 100% of the README width.
- Primary text remains readable when scaled to a 375px viewport.
- Fine metadata may simplify on mobile but cannot become the only source of meaning.
- Every image has descriptive alt text.
- Each image alt attribute contains the essential identity or project description, while each SVG also includes matching title and description elements.
- The animation runs for five seconds at 20 FPS, loops smoothly, stays under 5 MB, and contains no flashes.
- Rounded corners are baked into each image using transparent pixels, so GitHub cannot remove them.
- SVGs use local shapes and text only: no scripts, remote fonts, external images, or embedded tracking.

## Verification

- Automated tests validate every asset exists and every destination link is exact.
- SVG parsing validates 1280px width, viewBox, rounded outer rectangle, title, and description.
- Animation tests validate 1280px width, 20 FPS, five-second duration, frame count, and file-size limit.
- A pixel-based test confirms the moving ribbon never intersects the text-safe regions.
- Desktop and 375px previews are inspected before publishing.
- The live GitHub page is inspected after push to confirm rounded corners, link behavior, animation playback, and absence of Markdown tables.

## Publishing

Implementation remains on codex/profile-readme until tests and visual review pass. The verified commit is pushed explicitly to origin/master, then the live profile and asset hashes are checked. No force push is used.
