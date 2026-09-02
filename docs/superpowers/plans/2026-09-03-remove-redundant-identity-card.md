# Remove Redundant Identity Card Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the repeated Yi Han identity card from the profile README so the split hero flows directly into the selected projects.

**Architecture:** This is a README composition change only. A regression test defines the exact six-image sequence, then the single linked identity image is removed without deleting its reusable SVG asset.

**Tech Stack:** GitHub Markdown, Python unittest, Git/GitHub CLI.

## Global Constraints

- Keep `assets/hero-split.gif?v=split-poster-20260903` as the first image.
- Do not reference `assets/identity.svg` from `README.md`.
- Keep KiwiCue, PanSub, Till Tally, stack, contact, and native text links unchanged.
- Preserve non-empty alt text and valid local image paths.

---

### Task 1: Remove the identity card safely

**Files:**
- Modify: `tests/test_readme.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: the existing README text loaded by `ReadmeTests.setUp`.
- Produces: a six-image README sequence with no `assets/identity.svg` reference.

- [ ] **Step 1: Write the failing regression test**

```python
def test_identity_card_is_not_repeated_below_hero(self) -> None:
    self.assertNotIn("assets/identity.svg", self.text)
    expected = [
        "assets/hero-split.gif",
        "assets/project-kiwicue.svg",
        "assets/project-pansub.svg",
        "assets/project-till-tally.svg",
        "assets/stack.svg",
        "assets/contact.svg",
    ]
    for asset in expected:
        self.assertEqual(self.text.count(asset), 1)
```

- [ ] **Step 2: Verify the test fails**

Run: `python -m unittest tests.test_readme.ReadmeTests.test_identity_card_is_not_repeated_below_hero -v`

Expected: FAIL because `README.md` still contains `assets/identity.svg`.

- [ ] **Step 3: Remove only the linked identity image**

Delete this block from `README.md`:

```markdown
[![About Yi Han: full-stack developer building AI-assisted products and practical automation in Auckland, New Zealand.](assets/identity.svg)](https://hannnnnnnny.github.io/yi-han-software-engineer/)
```

- [ ] **Step 4: Verify and commit**

Run: `python -m unittest discover -s tests -v`

Expected: all tests pass.

```bash
git add README.md tests/test_readme.py
git commit -m "refactor: remove redundant profile identity card"
```

### Task 2: Publish and verify the profile

**Files:**
- Verify: `README.md`

**Interfaces:**
- Consumes: the committed six-image README sequence.
- Produces: verified GitHub profile on `master`.

- [ ] **Step 1: Run completion checks**

Run: `python -m unittest discover -s tests -v`

Run: `git diff --check`

Expected: zero failures and zero whitespace errors.

- [ ] **Step 2: Publish**

```bash
git push origin HEAD:master
```

- [ ] **Step 3: Verify the live page**

Open `https://github.com/hannnnnnnny` with the new commit as a query parameter.
Confirm the README contains the split hero followed immediately by KiwiCue and
that every visible README image loads successfully.
