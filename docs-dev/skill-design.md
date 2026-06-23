# SKILL.md Design — skills/mql5

This document describes the content and structure of `skills/mql5/SKILL.md`,
conforming to the [AgentSkills.io Specification](https://agentskills.io/specification).

## Frontmatter

```yaml
---
name: mql5
description: >
  MQL5 development skill for MetaTrader 5. Covers Expert Advisors, Indicators,
  Scripts, and Services. Focus on positions, orders, indicators, ticks, and bars.
  Includes programming book and API reference documentation.
version: "0.1"
license: MIT
compatibility: >
  Target: MetaTrader 5 platform. Language: MQL5 (C++-like syntax).
  File extensions: *.mq5 (source), *.mqh (headers).
  References: mql5.com/en/book (programming), mql5.com/en/docs (API).
metadata:
  project-version: "0.1.0"
  sources:
    book: sitemaps/sitemap_book_en.xml (581 URLs)
    docs: sitemaps/sitemap_docs_en.xml (4135 URLs)
  focus-areas:
    - positions
    - orders
    - indicators
    - ticks
    - bars
---
```

## Body Content Structure

The body should be structured as follows:

### 1. Overview

Brief description of MQL5 and MetaTrader 5:
- MQL5 is the programming language for MetaTrader 5
- Syntax similar to C++
- File types: `.mq5` (source), `.mqh` (headers)
- Program types: Expert Advisors, Indicators, Scripts, Services

### 2. Quick Reference — Key Operations

Focus areas with concise API patterns:

#### Positions
- `CTrade` class for position management
- `PositionGetSymbol()`, `PositionSelect()`, `PositionGetDouble()`
- `CTrade::PositionOpen()`, `CTrade::PositionClose()`

#### Orders
- `CTrade::OrderSend()` for pending orders
- `ORDER_TYPE_BUY_LIMIT`, `ORDER_TYPE_SELL_LIMIT`, etc.
- `OrderGetTicket()`, `OrderSelect()`

#### Indicators
- `iMA()`, `iRSI()`, `iMACD()`, `iBands()` — built-in indicators
- `CopyBuffer()` to read indicator values
- `IndicatorCreate()` for custom indicators

#### Ticks
- `SymbolInfoTick()` — current tick data
- `MqlTick` structure: `bid`, `ask`, `last`, `volume`, `time`
- `OnTick()` handler for Expert Advisors

#### Bars
- `Bars()`, `BarsCalculated()` — bar count
- `CopyOpen()`, `CopyHigh()`, `CopyLow()`, `CopyClose()`, `CopyVolume()`
- `CopyRates()`, `CopyTime()`
- `CTerminalInfo`, `CSymbolInfo` for symbol/bar info

### 3. Program Types

| Type | Purpose | Key Handler |
|------|---------|-------------|
| Expert Advisor | Automated trading | `OnTick()`, `OnInit()`, `OnDeinit()` |
| Indicator | Technical analysis | `OnCalculate()` |
| Script | One-shot execution | `OnStart()` |
| Service | Background task | `OnStart()`, `OnTimer()` |

### 4. Common Patterns

- Trade execution with error handling
- Indicator buffer management
- Timer-based operations
- Chart object manipulation
- File I/O for logging/data

### 5. References

Point to the extracted documentation:
- `references/book/` — Programming book (learning path)
- `references/docs/` — API reference (function/type lookup)

### 6. Pitfalls & Best Practices

- `RefreshRates()` before trading operations
- `NormalizeDouble()` for price comparisons
- Check `Retcode()` after trade operations
- Use `CTrade` class over raw `OrderSend()`
- Handle `OnTimer()` for periodic operations
- Test with Strategy Tester before live deployment

## Implementation Notes

- The SKILL.md should be concise (< 1024 chars for description, body can be longer)
- Body is loaded as context by AI agents — prioritize actionable patterns
- Reference files provide depth; SKILL.md provides the "what to do"
- Version 0.1: initial content, will expand as extraction completes
