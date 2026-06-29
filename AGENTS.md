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
├── LICENSE                # MIT license
├── README.md              # Public readme
├── pyproject.toml         # uv project config
├── .python-version        # Pins Python 3.14
├── uv.lock                # Locked dependencies
├── sitemaps/              # Source sitemaps from mql5.com
│   ├── sitemap_book_en.xml   # 581 URLs → programming book
│   └── sitemap_docs_en.xml   # 4135 URLs → API reference docs
├── html_cache/            # Downloaded HTML (lossless, gitignored)
│   ├── book/              #   581 .html files
│   └── docs/              #   4135 .html files
├── scripts/               # Extraction scripts (Python)
│   └── extract.py         # Main extraction: XML → HTML → Markdown
├── resources/             # Static resources
│   └── random-user-agents.csv
├── skills/
│   └── mql5/              # The MQL5 development skill
│       ├── SKILL.md       # Skill definition (agentskills.io spec)
│       ├── scripts/
│       │   ├── mql5_helper.py            # Compile/deploy/status via Wine
│       │   ├── parse_tester_report.py    # Backtest report parser + analysis
│       │   └── verify_sl_tp_formulas.py  # SL/TP risk formula verification
│       └── references/
│           ├── book/      # Programming book markdown (from sitemap_book_en.xml)
│           │   ├── 0000-book.md
│           │   ├── 00-intro/
│           │   │   ├── 0001-intro.md
│           │   │   └── pics/
│           │   └── ...
│           ├── docs/      # API reference markdown (from sitemap_docs_en.xml)
│           │   ├── 0000-docs.md
│           │   ├── 01-basis/
│           │   │   ├── 0001-basis.md
│           │   │   └── pics/
│           │   └── ...
│           └── symbol-spec/  # Broker symbol specifications (CSV)
│               ├── specs-XAUUSD.csv
│               └── specs-USDJPY.csv
├── jobs/                  # Backtest job folders
│   ├── 250013-job.md      # Job specification
│   └── ReportTester-250013/
│       ├── ReportTester-600xxxxx.html   # MT5 Strategy Tester HTML report
│       └── ReportTester-600xxxxx*.png   # Screenshots (equity, holding, MFE/MAE)
└── docs-dev/              # Development documentation
    ├── extraction.md      # Extraction workflow and script design
    ├── naming.md          # Folder/file naming conventions
    ├── skill-design.md    # SKILL.md content plan
    └── symbol-spec.md     # Symbol spec workflow
```

## SKILL.md Convention (skills/mql5/)

Per agentskills.io spec:
- Frontmatter: `name` (required, max 64 chars, lowercase+hyphens), `description` (required, max 1024 chars)
- Body: Markdown instructions for the agent
- Optional dirs: `scripts/`, `references/`, `assets/`
- Focus areas: positions, orders, indicators, ticks, bars

## Scripts

### parse_tester_report.py

Parses MT5 Strategy Tester HTML reports. Supports three output modes:

```
# Text report (default)
python skills/mql5/scripts/parse_tester_report.py <report.html>

# JSON dump (raw parsed data)
python skills/mql5/scripts/parse_tester_report.py <report.html> --json

# JSON with trade analysis (--analyze includes idle_time, monthly breakdown, etc.)
python skills/mql5/scripts/parse_tester_report.py <report.html> --analyze
```

Key analysis fields: `idle_time` (HH:MM:SS flat duration across backtest period),
`win_loss_ratio`, `breakeven_win_rate`, `monthly`, `reentries`, `lot_pattern`.

### mql5_helper.py

MT5 development helper for compile/deploy/status via Wine:

```
python skills/mql5/scripts/mql5_helper.py compile FILE.mq5
python skills/mql5/scripts/mql5_helper.py check FILE.mq5     # syntax only (/s flag)
python skills/mql5/scripts/mql5_helper.py deploy FILE.mq5
python skills/mql5/scripts/mql5_helper.py status
python skills/mql5/scripts/mql5_helper.py list
```

MT5 paths resolved in order: `$MQL5_DIR` env → cwd walk-up → Program Files scan → Wine fallback.

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

## Ad-hoc Verification

No formal test suite. Scripts are verified via temporary scripts under `/tmp` with
`hermes-verify-` filename prefix. Pattern:

1. Write a focused verification script to `/tmp/hermes-verify-<topic>.py`
2. Import the changed functions, exercise them with known inputs
3. Run via `uv run python /tmp/hermes-verify-<topic>.py` (requires project venv for deps)
4. Clean up the temp file after passing

Example (from `parse_tester_report.py` changes):
```bash
# Create /tmp/hermes-verify-parse-tester.py with test cases
# Run:
uv run python /tmp/hermes-verify-parse-tester.py
# Clean up:
rm /tmp/hermes-verify-parse-tester.py
```

## Git Workflow

- Conventional commits
- Do not commit .venv, __pycache__
- Tag releases per semver
