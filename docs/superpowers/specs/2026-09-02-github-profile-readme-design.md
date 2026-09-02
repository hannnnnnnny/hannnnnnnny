# GitHub Profile README Design

## 1. Objective

Create an English-language profile README for github.com/hannnnnnnny that presents Yi Han as an AI and automation-focused full-stack product builder. The page should feel like a restrained, high-quality product landing page rather than a generic badge dashboard.

The primary message is:

> Repetitive work. → Reliable systems.

The README should make this positioning understandable within a few seconds, then support it with real projects.

## 2. Creative Direction

The selected visual direction is **“Rewriting Manifesto.”** It takes inspiration from the polished component composition and gradient restraint seen in 21st.dev, together with the strong typography and motion-led presentation associated with Anton Skvortsov's portfolio. It must remain an original design rather than reproducing either source.

The visual system uses:

- Near-black background matching GitHub dark mode.
- Warm off-white primary type.
- Mint green for the successful rewritten state.
- Coral red for the strikethrough action.
- Monospace microcopy paired with bold sans-serif display type.
- Subtle borders and rounded corners consistent with GitHub's surrounding interface.

The animation is purposeful: “Repetitive work.” is struck through and replaced by “Reliable systems.” A scanning line and terminal-style caret add restrained secondary movement. The loop must remain calm and readable.

## 3. Content Structure

The README contains five sections in this order:

1. **Animated manifesto banner**
2. **Short introduction**
3. **Selected systems**
4. **Focused technology stack**
5. **Contact links**

GitHub contribution statistics, streak cards, trophies, visitor counters, and large badge collections are excluded because they compete with the project narrative and rely on external services.

## 4. Approved Copy

### Banner

- Eyebrow: “YI HAN / CURRENT MODE: BUILDING”
- Initial statement: “Repetitive work.”
- Rewritten statement: “Reliable systems.”
- Supporting line: “turning friction into flow”

### Introduction

Heading:

> Hey, I'm Yi Han.

Body:

> A full-stack developer in Auckland building AI-assisted products and practical automation. I turn messy, repetitive workflows into reliable systems people can actually use.

### Selected systems

1. **KiwiCue** — Bilingual Auckland event discovery with smart reminders.
2. **PanSub** — Real-time AI Chinese subtitles for lecture recordings.
3. **Till Tally** — Retail analytics that turns sales data into useful decisions.

Each project links directly to its GitHub repository and names only its most relevant technology or capability.

### Contact links

- Portfolio: https://hannnnnnnny.github.io/yi-han-software-engineer/
- LinkedIn: https://www.linkedin.com/in/yi-han-29ab28323/
- Email: mailto:harryhaber606@gmail.com

## 5. Assets and Implementation Constraints

The README is implemented with native Markdown and conservative GitHub-compatible HTML only.

- README.md is the entry point.
- assets/hero.gif is a self-contained animated banner.
- assets/hero-static.png is a still frame for documentation and quality review.
- Project content remains real text and links, not text baked into one large image, so it stays accessible, selectable, and maintainable.
- The hero target size is 1280 × 360 pixels with a displayed width of 100%.
- The animation target is a five-second seamless loop at 18–24 FPS and no more than 5 MB.
- No remote scripts, tracking pixels, visitor counters, or runtime dependencies are used.
- No secrets or private data are included.

GitHub Markdown does not support arbitrary CSS or JavaScript. Motion therefore lives only in the animated image; the document structure uses portable Markdown.

## 6. Responsive and Accessibility Requirements

- The banner text and focal action must remain legible when scaled to a 375-pixel viewport.
- Project entries stack vertically, avoiding a three-column table that becomes cramped on mobile.
- The banner has descriptive alt text: “Repetitive work transforms into reliable systems.”
- Motion avoids flashes, rapid zooms, and abrupt cuts.
- Body copy maintains strong contrast in both GitHub light and dark themes by relying on native Markdown colors.
- Link text describes the destination and does not rely on color alone.

## 7. Repository and Publishing Model

For GitHub to display the README on the profile, the target repository must be public and named exactly hannnnnnnny, matching the GitHub username. The local repository currently has no remote and no existing commits.

Publishing consists of:

1. Creating the README and local assets.
2. Rendering and visually checking the animation and static frame.
3. Validating all links and checking the README at desktop and 375-pixel widths.
4. Committing the implementation with a clear commit message.
5. Creating or connecting the hannnnnnnny GitHub repository.
6. Pushing the default branch and confirming the profile renders correctly.

Creating the remote repository or pushing to GitHub may require authenticated GitHub CLI access. No repository will be overwritten.

## 8. Verification

Completion requires all of the following:

- The GIF loops without a visible jump and stays within the file-size budget.
- The static frame and animation contain no clipped text.
- All three repository links resolve.
- Portfolio, LinkedIn, and email links are correct.
- The README remains readable at 375 pixels wide.
- git status contains only intentional files before commit.
- The public GitHub profile displays the README after publication.

