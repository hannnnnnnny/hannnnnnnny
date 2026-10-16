# Cursor walkthrough sources

Captured on 2026-10-16 with Playwright CLI video recording (`--cursor`, 1280 × 800, 15 fps). Web and CLI GIFs are 1100 px wide at 10 fps; the game replay is 960 px wide at 8 fps to keep the download small. All use a shared 256-colour palette. The cursor records actual browser actions, including clicks; it is not pasted over a static screenshot. Gray recording padding is removed.

Source revisions: PanSub `6f06b469d9fdfbd502600ced1cf1f091ef1783b3`; GuardRun `728022cfa7c5c992f0133ac71938170b70b444fb`.

| Preview | Source | What the mouse does |
| --- | --- | --- |
| KiwiCue | https://kiwicue.nz | Selects weekend and market filters; opens Ask KiwiCue. No microphone access or model request. |
| ReNova | https://renova-marketplace.vercel.app | Opens a real bicycle listing from search results; scrolls through the detail page. No account or transaction. |
| PanSub | https://github.com/hannnnnnnny/pansub | Operates the actual `options.html` UI locally: style presets and bilingual/translation-only display. Uses the project's storage mock pattern, not a private lecture or an installed extension session. |
| GuardRun | https://github.com/hannnnnnnny/GuardRun/blob/main/examples/offline_demo.py | Clicks through a labelled replay of stdout from an actual local offline run: normal read, blocked `.env` read, and unapproved shell command. The model provider is scripted; the safety checks are real. The replay viewer is recording infrastructure, not a GuardRun product UI. |
| Ashen Depths | https://github.com/hannnnnnnny/ARPG-CX/tree/main/docs/media | Switches a replay viewer between the project's original `desktop_play_en.gif` and `desktop_menus_en.gif`. Gameplay itself is prerecorded; the cursor controls playback, not the game. |

## Reproduction

Run commands from the repository root. Keep cloned source, raw videos and local fixture data under `output/playwright/`; these are not published assets.

1. Clone PanSub to `output/playwright/sources/pansub` and GuardRun to `output/playwright/sources/guardrun`.
2. Create `output/playwright/guardrun-env`, install the cloned GuardRun package there, and run `python scripts/demos/prepare_local_demos.py`.
3. Download the two English game GIFs above to `output/playwright/recordings/gameplay-source.gif` and `menus-source.gif`.
4. Serve the root with `python -m http.server 64363 --bind 127.0.0.1`.
5. Use `npx --yes --package @playwright/cli playwright-cli` with named sessions at 1280 × 800. Observe a current snapshot before replaying locator-based actions.
6. Start recordings with `video-start output/playwright/recordings/<name>.webm --size=1280x800 --fps=15 --cursor`, execute the corresponding `scripts/demos/*.js` with `run-code --filename`, then `video-stop`.
7. For PanSub, run `pansub-setup.js` before starting its recording. For GuardRun and the game, open `scripts/demos/viewer.html` (append `?project=game` for the game).
8. Match recording filenames to `TAKES` in `scripts/encode_previews.py`, then run that script. It requires Pillow, NumPy and imageio-ffmpeg in the local capture environment.

README structure was informed by https://github.com/DeryFerd/DeryFerd . Personal details, project claims and stack entries describe Harry Han's own work.
