# SKILL.md Design — skills/mql5

This document describes the content and structure of `skills/mql5/SKILL.md`,
conforming to the [AgentSkills.io Specification](https://agentskills.io/specification).

## Frontmatter

```yaml
---
name: mql5
description: >
  MQL5 development skill for MetaTrader 5 Expert Advisors, Indicators, Scripts,
  and Services. Focus on positions, orders, indicators, ticks, bars, risk
  management, backtesting, and multi-instance MT5 operations. Includes
  programming book and API reference documentation.
version: "0.1"
license: MIT
compatibility: >
  Target: MetaTrader 5 platform. Language: MQL5 (C++-like syntax).
  File extensions: *.mq5 (source), *.mqh (headers).
  Run time: Windows native, Linux via Wine, macOS via Wine.
metadata:
  project-version: "0.1.0"
  focus-areas:
    - positions
    - orders
    - indicators
    - ticks
    - bars
    - risk-management
    - backtesting
---
```

## Body Content Structure

### 1. MQL5 Fundamentals
- Language and file types (.mq5, .mqh, .ex5)
- Program types: EA, Indicator, Script, Service
- MQL5 directory structure (Windows, Linux/Wine)
- Multi-instance MT5 operations

### 2. Trading Operations
- Core concepts: Order, Deal, Position
- CTrade class usage patterns
- Position queries (Hedging vs Netting)
- Order execution pattern with error handling

### 3. Indicators and Multi-Timeframe
- Built-in indicator handles (iMA, iRSI, iMACD, iBands)
- Reading indicator values via CopyBuffer
- Multi-timeframe analysis pattern
- New bar detection

### 4. Ticks and Bars
- Timeseries access (MqlRates, ArraySetAsSeries)
- Tick data (MqlTick, SymbolInfoTick)
- Key functions table

### 5. Risk Management and Lot Sizing
- **PointValue concept**: profit-currency per 1-point move for 1 lot
  - Forex/CFD: `point × ContractSize`
  - Futures: `point × TickValue / TickSize`
- **Direction A**: SL distance points → SL price
- **Direction B**: Risk% + fixed lots → SL price (with currency conversion)
- **Direction C**: SL price + risk% → lot size
- **Profit verification**: OrderCalcProfit + manual formula
- Risk-to-Reward ratio
- Position sizing rules (7 rules)

### 6. Backtesting and Optimization
- Strategy Tester concepts
- OnTester custom optimization criterion
- Key statistics table
- Backtesting workflow

### 7. Event Handlers Reference
- Handler table (OnInit through OnTesterPass)

### 8. Common Pitfalls
- **General** (10 items): ResultRetcode, MagicNumber, NormalizeDouble, etc.
- **SL/TP and Risk Calculation** (6 items): PointValue vs TICK_VALUE,
  TickSize vs Point, currency conversion, NormalizeDouble rounding,
  lot step quantization, STOPS_LEVEL check

### 9. Quick Reference — EA Skeleton
- Complete EA template with inline risk functions:
  - `PointValue()`, `FindFXRate()`, `CalcSLFromRisk()`, `CalcLotsFromSL()`
  - OnTick example with SL calculation and loss verification

### 10. References
- In-skill references (book/, docs/, symbol-spec/, scripts/)
- External links (MQL5 Reference, MQL5 Book, Strategy Tester Guide)

## Implementation Notes

- Body is loaded as context by AI agents — prioritize actionable patterns
- Reference files provide depth; SKILL.md provides the "what to do"
- Risk formulas verified against real symbol specs (XAUUSD, USDJPY)
  via `scripts/verify_sl_tp_formulas.py`
- Version 0.1: initial content, will expand as extraction completes
