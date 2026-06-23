# AGENTS.md — mql5-skills Project

## Overview

MQL5 Agent Skills project. Creates and publishes Agent Skills conforming to the
[AgentSkills.io Specification](https://agentskills.io/specification).

- **Project version**: 0.1.0 (pinned during initial phase, not incremented per change)
- **SKILL.md version**: 0.1 (per-document, pinned during initial phase)
- **Language**: Python 3.14, uv-managed
- **Dependencies**: beautifulsoup4, requests

## Directory Structure

```
mql5-skills/
├── AGENTS.md              # This file — project conventions
├── README.md              # Public readme
├── pyproject.toml         # uv project config
├── sitemaps/              # Source sitemaps from mql5.com
│   ├── sitemap_book_en.xml   # 581 URLs → programming book
│   └── sitemap_docs_en.xml   # 4135 URLs → API reference docs
├── html_cache/            # Downloaded HTML (lossless, gitignored)
│   ├── book/              #   581 .html files
│   └── docs/              #   4135 .html files
├── scripts/               # Extraction scripts (Python)
│   └── extract.py         # Main extraction: XML → HTML → Markdown
├── skills/
│   └── mql5/              # The MQL5 development skill
│       ├── SKILL.md       # Skill definition (agentskills.io spec)
│       └── references/
│           ├── book/      # Programming book markdown (from sitemap_book_en.xml)
│           │   ├── 0000-book.md
│           │   ├── 00-intro/
│           │   │   ├── 0001-intro.md
│           │   │   └── pics/
│           │   └── ...
│           └── docs/      # API reference markdown (from sitemap_docs_en.xml)
│               ├── 0000-docs.md
│               ├── 01-basis/
│               │   ├── 0001-basis.md
│               │   └── pics/
│               └── ...
└── docs-dev/              # Development documentation
    ├── extraction.md      # Extraction workflow and script design
    ├── naming.md          # Folder/file naming conventions
    └── skill-design.md    # SKILL.md content plan
```

## SKILL.md Convention (skills/mql5/)

Per agentskills.io spec:
- Frontmatter: `name` (required, max 64 chars, lowercase+hyphens), `description` (required, max 1024 chars)
- Body: Markdown instructions for the agent
- Optional dirs: `scripts/`, `references/`, `assets/`
- Focus areas: positions, orders, indicators, ticks, bars

## Extraction Workflow

Two-phase pipeline (network only needed for Phase 1):

```
Phase 1: download  — sitemap → fetch HTML → html_cache/
Phase 2: convert   — html_cache/ → parse HTML → download images → .md files
```

- Script: `scripts/extract.py` with `download`, `convert`, `debug` subcommands
- HTML cache: `html_cache/book/`, `html_cache/docs/` (lossless, gitignored)
- Output: `skills/mql5/references/book/`, `skills/mql5/references/docs/`
- Each sitemap URL → one .md file + corresponding .html in cache
- Images → `pics/` subfolder within chapter dir
- Debug target: TesterStatistics page (mixed content: tables, images, code, console output)

## Naming Convention

See `docs-dev/naming.md` for full specification. Key rules:
- 4-digit sequential prefix per file within a chapter folder
- 2-digit prefix on chapter folder names
- Chapter folder names derived from URL path segments
- Max one level of subfolder under `book/` or `docs/`
- Each chapter folder contains a `pics/` subfolder

## Git Workflow

- Conventional commits
- Do not commit .venv, __pycache__
- Tag releases per semver
