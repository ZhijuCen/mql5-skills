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
│       │   ├── parse_optimizer_report.py # Optimization report parser + analysis
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

#### `windows` subcommand

Splits a backtest into N equal time windows and computes the same 7
core metrics (Profit, Expected Payoff, Profit Factor, Recovery Factor,
Balance DD Rel%, Trades, Sharpe Ratio) per window. Use to detect
over-fitting / regime change.

```
# N=1: validation — should match the full report within tolerance
python skills/mql5/scripts/parse_tester_report.py <report.html> windows --count 1

# N=4: typical analysis (quarterly for a 1.5y backtest)
python skills/mql5/scripts/parse_tester_report.py <report.html> windows --count 4

# JSON output for further processing
python skills/mql5/scripts/parse_tester_report.py <report.html> windows --count 6 --json
```

**Conventions:**
- Time boundaries are equal-length `[t_start, t_end)` slices,
  left-closed right-open. Window 0 starts at the backtest start;
  window N-1 ends at the backtest end. Adjacent windows do not overlap.
- A trade is assigned to the window where it OPENS (entry time).
  Its P&L lands at exit time, which may fall in a later window — we
  attribute the P&L to the opening window because that is the
  "decision moment" the user cares about.
- Balance DD Rel% computes MT5's STAT_BALANCE_DDREL_PERCENT (maximum
  relative drawdown, i.e. the largest (peak - trough) / peak % across
  the balance curve). For the full report this matches the HTML's
  Balance Drawdown Relative field exactly (44.60% vs 44.63% on
  246753; the 0.03% gap is from intra-trade floating P&L not in HTML).
  Per the user's rule "如 Equity DD % 不可用，则以 Balance DD % 代替",
  the script's `bal_dd_rel_pct` field is this balance-based relative
  DD.
- Gross Profit / Gross Loss use MT5's split: each trade's exit-leg
  P&L goes to GP if positive or GL if non-positive; entry costs always
  go to GL. Matches the report exactly for window=1.
- Sharpe Ratio uses the standard per-trade HPR formula
  (mean/std × sqrt(N_per_year)). MT5's reported value uses a
  different (undocumented) annualization; the value differs from the
  report for window=1, but the formula is consistent across all
  sub-windows, so the relative ranking is still meaningful.

**Outlier flags per window (z-score vs window mean):**
- `▲2σ` — at least one metric has |z| ≥ 2 (值得关注 — this
  window's value is far from the rest of the windows).
- `■EXT` — at least one metric has |z| ≥ 5 (极端 — extreme outlier).
- The marker is followed by `k=N` (count of outlier metrics) and
  the metric abbreviations with their signed z (e.g.
  `prof(+2.3σ),reco(+2.3σ)`).

z = (this window's value − mean across all windows) / std.
Direction is sign-bearing (+/-); the threshold is on |z|.
Lower-is-better metrics (bal_dd_rel_pct) are NOT inverted — a
negative z means "this window's DD is unusually low" (good for
safety, neutral for consistency), a positive z means "unusually
high DD" (a red flag). For all other metrics, the natural sign
applies (high profit, high PF, etc. = good).

A single window with a strong outlier is a regime signal.
Multiple windows each with their own outliers point to a
high-variance strategy — harder to predict live performance.

**Tolerances (N=1 vs report):**
- 4 of 7 metrics are **exact**: Profit, Expected Payoff, Profit
  Factor, Trades.
- 3 are documented approximations:
  - **Balance DD Rel%** — MT5's STAT_BALANCE_DDREL_PERCENT (max
    relative drawdown). Our value matches the HTML's Balance
    Drawdown Relative field within 0.03%. Per the user's rule
    "如 Equity DD % 不可用，则以 Balance DD % 代替" — this is what
    we do.
  - **Recovery Factor** — downstream of bal_dd_rel_abs.
  - **Sharpe Ratio** — MT5's reported value is inconsistent with the
    textbook formula `(AHPR - 1) / std_HPR × sqrt(N/year)` that the
    MQL5 community reverse-engineers agree on (forum thread 337071).
    For 246753 the textbook formula gives 2.49 vs the report's
    22.92 — a 9.2× gap. MT5 does not publish the actual computation.
    The per-trade Sharpe (`sharpe_ratio_raw` in the JSON output) is
    still a useful per-window signal.

### parse_optimizer_report.py

Parses MT5 Strategy Tester Optimization XML reports (SpreadsheetML format
— XML-tagged Excel workbook, also openable in LibreOffice Calc). Companion
to `parse_tester_report.py`; same three output modes:

```
python skills/mql5/scripts/parse_optimizer_report.py <ReportOptimizer-*.xml>
python skills/mql5/scripts/parse_optimizer_report.py <report.xml> --json
python skills/mql5/scripts/parse_optimizer_report.py <report.xml> --analyze
```

Reads `<DocumentProperties>` for the strategy environment card
(EA / Symbol / Period / Date range from `Title`, plus Deposit / Leverage /
Server / MT5 build / run timestamp) and the single "Tester Optimizator
Results" worksheet for one row per parameter pass. `--analyze` adds:

- **Orthogonality**: actual pass count vs expected cartesian product
- **Parameter effect**: which Inp* parameters actually move the result
  (vs. dead parameters that should be removed from optimization)
- **Dead boolean parameters**: bit-for-bit identical true/false groups
  on key metrics — cleanest signal of a parameter not wired into the EA
- **Duplicate metric vectors**: high count (>30%) usually points to a
  dead parameter
- **Best passes** by Profit / Profit Factor / Recovery Factor / Custom
- **Trade count distribution** with daily rate and correlations vs
  profit / drawdown (overtrading detection)

Use alongside `parse_tester_report.py` for the same EA: the latter
explains *why* a specific pass performs, the former explains *which*
pass performs and *which* parameters are even worth tuning.

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
