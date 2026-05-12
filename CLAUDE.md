# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Douban Poster Wall (豆瓣观影海报墙) — a Python scraper that fetches movie posters from Douban and displays them in two HTML pages: a responsive grid wall and a 3D mosaic screensaver.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper (generates posters/ and poster_paths.json)
python -m scraper.douban_spider

# Serve locally
python -m http.server 8000
```

## Architecture

- **No build system or framework** — pure vanilla HTML/CSS/JS and Python. Files are served as-is.
- **Data flow**: `scraper/douban_spider.py` writes `posters/*.jpg` + `poster_paths.json` → `index.html` and `screensaver.html` read `poster_paths.json` via `fetch()` at runtime.

### Directory Structure

```
├── scraper/            # Python scraper module
│   ├── config.py       # Env vars, constants (DOUBAN_ID, MAX_PAGES, etc.)
│   ├── utils.py        # Logging setup
│   └── douban_spider.py # Main scraper logic
├── static/
│   ├── css/            # reset.css, common.css, poster-wall.css, screensaver.css
│   ├── js/             # poster-wall.js, screensaver.js
│   └── favicon.ico
├── docs/               # design.md (design system), prd.md (requirements)
├── index.html          # Poster wall page
├── screensaver.html    # 3D screensaver page
├── posters/            # Auto-generated poster images (gitignored)
└── poster_paths.json   # Auto-generated JSON index (gitignored)
```

### CSS Architecture

- `reset.css` — shared box-sizing reset
- `common.css` — CSS custom properties (colors, typography, spacing, Apple spring curves), shared animations
- `poster-wall.css` / `screensaver.css` — page-specific styles using `var()` tokens

### Key Details

- Configuration via `.env`: `DOUBAN_ID` (required), `DOUBAN_COOKIE` (optional for authenticated access).
- `.env` contains a real Douban user ID — do not commit changes to it. Use `.env.example` as template.
- `posters/` and `poster_paths.json` are auto-generated; clear `posters/` before re-running for a fresh set.
- Screensaver has click-to-exit, ESC-to-exit, and auto-hiding cursor after 3s inactivity.
- All animations use Apple spring curve: `cubic-bezier(0.16, 1, 0.3, 1)`.
- Project UI and comments are in Chinese.
- No test suite, linting, or CI/CD configured.
