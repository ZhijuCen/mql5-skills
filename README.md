# mql5-skills

MQL5 Agent Skill for MetaTrader 5 development. Conforms to the
[AgentSkills.io Specification](https://agentskills.io/specification).

## What's Inside

An AI agent skill (`skills/mql5/SKILL.md`) that gives an LLM agent working
knowledge of MQL5 development — positions, orders, indicators, risk management,
backtesting — backed by the full MQL5 programming book and API reference
extracted to Markdown.

```
skills/mql5/
├── SKILL.md                      # The agent skill (agentskills.io spec)
├── scripts/
│   ├── verify_sl_tp_formulas.py  # Python SL/TP risk formula verification
│   └── ...
└── references/
    ├── book/                     # MQL5 Programming Book (581 pages)
    ├── docs/                     # MQL5 API Reference (4135 pages)
    └── symbol-spec/              # Broker symbol specifications (CSV)
```

## Quick Start

### Use the Skill

Point your AI agent at `skills/mql5/SKILL.md`. The skill covers:

- **Trading operations**: CTrade class, OrderSend, position management
- **Indicators**: built-in handles, multi-timeframe, custom indicators
- **Risk management**: PointValue-based SL/TP calculation, lot sizing,
  currency conversion for cross-pair profit currencies
- **Backtesting**: Strategy Tester, OnTester custom criteria, optimization
- **Pitfalls**: 16 documented pitfalls including SL/TP-specific issues

### Extract References (Development)

The `references/book/` and `references/docs/` directories are generated from
mql5.com sitemaps via a two-phase pipeline:

```bash
# Phase 1: Download HTML (needs network)
uv run scripts/extract.py download --all

# Phase 2: Convert to Markdown (offline)
uv run scripts/extract.py convert --all
```

See `docs-dev/extraction.md` for the full pipeline design.

### Verify Risk Formulas

```bash
python skills/mql5/scripts/verify_sl_tp_formulas.py
```

Tests SL/TP calculation against real symbol specs (XAUUSD, USDJPY) with
verified PointValue-based formulas.

## Symbol Specs

Broker-specific symbol specifications live in `skills/mql5/references/symbol-spec/`:

| File | Symbol | Calc Mode | Contract Size | Digits |
|------|--------|-----------|---------------|--------|
| `specs-XAUUSD.csv` | XAUUSD | CFD Leverage | 100 | 2 |
| `specs-USDJPY.csv` | USDJPY | Forex | 100,000 | 3 |

These are used by the verification script and can be extended for additional
symbols.

## Project Structure

```
mql5-skills/
├── AGENTS.md                     # Project conventions for AI agents
├── LICENSE                       # MIT
├── README.md                     # This file
├── pyproject.toml                # uv project config (Python 3.14)
├── sitemaps/                     # Source sitemaps from mql5.com
│   ├── sitemap_book_en.xml       #   581 URLs → programming book
│   └── sitemap_docs_en.xml       #   4135 URLs → API reference docs
├── scripts/                      # Extraction pipeline
│   └── extract.py                #   XML → HTML → Markdown
├── skills/mql5/                  # The MQL5 agent skill
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── docs-dev/                     # Development documentation
│   ├── extraction.md             #   Extraction pipeline design
│   ├── naming.md                 #   File/folder naming conventions
│   ├── skill-design.md           #   SKILL.md content plan
│   └── symbol-spec.md            #   Symbol spec workflow
└── html_cache/                   # Downloaded HTML (gitignored)
```

## Development

```bash
# Setup
uv sync

# Run extraction
uv run scripts/extract.py download --all
uv run scripts/extract.py convert --all

# Verify formulas
python skills/mql5/scripts/verify_sl_tp_formulas.py
```

## License

MIT
