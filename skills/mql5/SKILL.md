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

# MQL5 Development Skill

Expert development skill for MetaTrader 5. Covers EA, Indicator, Script, and
Service creation with emphasis on trading operations, technical indicators,
multi-timeframe analysis, risk management, and backtesting workflows.

## 1. MQL5 Fundamentals

### Language and File Types

- MQL5 syntax is similar to C++ but with domain-specific additions
- Source files: `*.mq5` (programs), `*.mqh` (headers)
- Compiled output: `*.ex5` (same name as source)
- Compiler: built into MetaEditor IDE

### Program Types

| Type | Purpose | Key Handler | Directory |
|------|---------|-------------|-----------|
| Expert Advisor | Automated trading | `OnTick()` | `MQL5/Experts/` |
| Indicator | Technical analysis | `OnCalculate()` | `MQL5/Indicators/` |
| Script | One-shot execution | `OnStart()` | `MQL5/Scripts/` |
| Service | Background task | `OnStart()` + `OnTimer()` | `MQL5/Services/` |

### MQL5 Directory Structure

Default locations per platform:

| Platform | Path |
|----------|------|
| Windows 10+ | `$env:USERPROFILE\AppData\Roaming\MetaQuotes\Terminal\$INSTANT_HEX\MQL5` |
| Linux (Wine) | `~/.wine/drive_c/Program Files/MetaTrader 5/MQL5/` |
| macOS | Unknown — verify per installation |

Key subdirectories:
```
MQL5/
├── Experts/          # EA source files (.mq5)
│   ├── Examples/     # Built-in example EAs
│   └── Free Robots/  # Downloaded EAs
├── Indicators/       # Indicator source files
├── Scripts/          # Script source files
├── Services/         # Service source files
├── Include/          # Header files (.mqh)
│   ├── Trade/        # Trading classes (Trade.mqh, PositionInfo.mqh, etc.)
│   ├── Indicators/   # Indicator helpers
│   ├── Expert/       # Expert base classes
│   └── Generic/      # Generic collections
├── Files/            # File I/O sandbox
├── Images/           # Image resources
├── Libraries/        # DLL/shared libraries
├── Profiles/         # Chart profiles
└── Logs/             # Log files
```

### Multi-Instance MT5

Multiple MT5 instances can run simultaneously for different accounts:

1. Install MT5 to separate target paths (e.g. `MT5_BrokerA/`, `MT5_BrokerB/`)
2. Each instance has its own `MQL5/` directory
3. To identify which account an instance is logged into:
   - `AccountInfoInteger(ACCOUNT_LOGIN)` — account number
   - `AccountInfoString(ACCOUNT_NAME)` — account name
   - `AccountInfoString(ACCOUNT_SERVER)` — broker server
4. Each instance runs as a separate process — use `Magic Number` to distinguish
   EA trades across instances on the same symbol

## 2. Trading Operations

### Core Concepts

- **Order**: instruction to buy/sell (Market or Pending)
- **Deal**: executed exchange (buy at Ask, sell at Bid)
- **Position**: current obligation (long or short)

### CTrade Class (Standard Library)

```mql5
#include <Trade\Trade.mqh>

CTrade trade;

// Setup in OnInit()
trade.SetExpertMagicNumber(EA_MAGIC);
trade.SetMarginMode();
trade.SetTypeFillingBySymbol(Symbol());
trade.SetDeviationInPoints(Slippage);
```

Key methods:

| Method | Purpose |
|--------|---------|
| `PositionOpen(symbol, type, volume, price, sl, tp)` | Open a position |
| `PositionClose(symbol, deviation)` | Close a position |
| `PositionModify(symbol, sl, tp)` | Modify SL/TP |
| `PositionClosePartial(symbol, volume)` | Partial close |
| `Buy(volume, price, sl, tp, comment)` | Shortcut for buy |
| `Sell(volume, price, sl, tp, comment)` | Shortcut for sell |
| `BuyLimit/BuyStop/SellLimit/SellStop(...)` | Pending orders |
| `ResultRetcode()` | Check trade server return code |
| `ResultDeal()` | Get deal ticket after execution |

### Position Queries

```mql5
// Iterate open positions (Hedging account)
uint total = PositionsTotal();
for (uint i = 0; i < total; i++) {
    string sym = PositionGetSymbol(i);
    if (sym == _Symbol && PositionGetInteger(POSITION_MAGIC) == EA_MAGIC) {
        double vol = PositionGetDouble(POSITION_VOLUME);
        double sl  = PositionGetDouble(POSITION_SL);
        double tp  = PositionGetDouble(POSITION_TP);
        long   type = PositionGetInteger(POSITION_TYPE);
    }
}

// Netting account — simpler
if (PositionSelect(_Symbol)) {
    // position is selected
}
```

### Order Execution Pattern

```mql5
// Calculate price
double price = (signal == ORDER_TYPE_BUY)
    ? SymbolInfoDouble(_Symbol, SYMBOL_ASK)
    : SymbolInfoDouble(_Symbol, SYMBOL_BID);

// Open with SL/TP
trade.PositionOpen(_Symbol, signal, lotSize, price, sl, tp, "EA Signal");

// Always check result
if (trade.ResultRetcode() != TRADE_RETCODE_DONE) {
    Print("Trade failed: ", trade.ResultRetcode());
}
```

### Hedging vs Netting

```mql5
bool IsHedging = ((ENUM_ACCOUNT_MARGIN_MODE)
    AccountInfoInteger(ACCOUNT_MARGIN_MODE) == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
```

- **Hedging**: multiple positions per symbol, must iterate and match Magic Number
- **Netting**: one position per symbol, use `PositionSelect()`

## 3. Indicators and Multi-Timeframe

### Built-in Indicator Handles

```mql5
// Moving Average
int handle = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_SMA, PRICE_CLOSE);

// RSI
int handle = iRSI(_Symbol, PERIOD_H1, 14, PRICE_CLOSE);

// MACD
int handle = iMACD(_Symbol, PERIOD_H1, 12, 26, 9, PRICE_CLOSE);

// Bollinger Bands
int handle = iBands(_Symbol, PERIOD_H1, 20, 0, 2.0, PRICE_CLOSE);
```

### Reading Indicator Values

```mql5
double buffer[];
ArraySetAsSeries(buffer, true);
if (CopyBuffer(handle, 0, 0, 3, buffer) != 3) {
    Print("No indicator data");
    return;
}
// buffer[0] = current bar value
// buffer[1] = previous bar value
```

### Multi-Timeframe Analysis

```mql5
// Higher timeframe trend
int h4_ma = iMA(_Symbol, PERIOD_H4, 50, 0, MODE_SMA, PRICE_CLOSE);

// Entry timeframe signal
int h1_rsi = iRSI(_Symbol, PERIOD_H1, 14, PRICE_CLOSE);

// In OnTick():
double h4_val[], h1_val[];
CopyBuffer(h4_ma, 0, 0, 1, h4_val);
CopyBuffer(h1_rsi, 0, 0, 1, h1_val);

bool bullish = (SymbolInfoDouble(_Symbol, SYMBOL_BID) > h4_val[0]);
bool oversold = (h1_val[0] < 30);
```

### New Bar Detection

```mql5
datetime lastBarTime = 0;

void OnTick() {
    datetime currentBarTime = iTime(_Symbol, _Period, 0);
    if (currentBarTime == lastBarTime) return;  // not a new bar
    lastBarTime = currentBarTime;
    // New bar — run analysis here
}
```

## 4. Ticks and Bars

### Timeseries Access

Index 0 = current (unfinished) bar. Array is reverse-ordered.

```mql5
MqlRates rates[];
ArraySetAsSeries(rates, true);
CopyRates(_Symbol, _Period, 0, 100, rates);

// rates[0] = current bar
// rates[1] = previous bar
// rates[0].open, .high, .low, .close, .tick_volume, .time
```

### Tick Data

```mql5
MqlTick tick;
SymbolInfoTick(_Symbol, tick);
// tick.bid, tick.ask, tick.last, tick.volume, tick.time
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `CopyRates()` | Bulk OHLCV data |
| `CopyOpen/High/Low/Close()` | Individual price arrays |
| `CopyTime()` | Bar open times |
| `CopyBuffer()` | Indicator buffer values |
| `iBars()` | Bar count for symbol/period |
| `iBarShift()` | Bar index by time |
| `iTime()` | Bar open time by shift |
| `SymbolInfoTick()` | Current tick data |

## 5. Risk Management and Lot Sizing

### Fixed Percentage Risk

```mql5
double CalculateLotSize(double riskPercent, double slPoints) {
    double accountBalance = AccountInfoDouble(ACCOUNT_BALANCE);
    double riskAmount = accountBalance * riskPercent / 100.0;

    double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
    double tickSize  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
    double point     = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

    if (tickValue == 0 || tickSize == 0 || slPoints == 0) return 0;

    double slMoneyPerLot = (slPoints * point / tickSize) * tickValue;
    double lot = riskAmount / slMoneyPerLot;

    // Normalize to broker constraints
    double minLot  = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double maxLot  = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
    double lotStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);

    lot = MathFloor(lot / lotStep) * lotStep;
    lot = MathMax(lot, minLot);
    lot = MathMin(lot, maxLot);

    return NormalizeDouble(lot, 2);
}
```

### Risk-to-Reward Ratio

```mql5
// Minimum 1:2 RR
double slDistance = MathAbs(price - sl);
double tpDistance = slDistance * 2;  // 1:2 minimum
double tp = (orderType == ORDER_TYPE_BUY) ? price + tpDistance : price - tpDistance;
```

### Position Sizing Rules

1. Never risk more than 1-2% per trade
2. Calculate lot size from risk amount and SL distance
3. Normalize to broker's lot step and min/max constraints
4. Account for spread when calculating SL distance

## 6. Backtesting and Optimization

### Strategy Tester

The Strategy Tester is built into MT5. Key concepts:

1. **Single Test**: run EA once with fixed parameters
2. **Optimization**: genetic algorithm searches parameter space
3. **Custom Criterion**: `OnTester()` returns optimization value

### OnTester Handler

```mql5
double OnTester() {
    // Called after each test pass
    // Return value used as "Custom max" optimization criterion

    double profit   = TesterStatistics(STAT_PROFIT);
    double dd       = TesterStatistics(STAT_BALANCE_DDREL_PERCENT);
    double trades   = TesterStatistics(STAT_TRADES);
    double pf       = TesterStatistics(STAT_PROFIT_FACTOR);
    double sharpe   = TesterStatistics(STAT_SHARPE_RATIO);

    // Minimum trade count filter
    if (trades < 50) return 0;

    // Custom criterion: profit factor * (1 - max drawdown%)
    return pf * (1.0 - dd / 100.0);
}
```

### Key Statistics

| Stat | Description |
|------|-------------|
| `STAT_PROFIT` | Net profit/loss |
| `STAT_PROFIT_FACTOR` | Gross profit / gross loss |
| `STAT_BALANCE_DDREL_PERCENT` | Max balance drawdown % |
| `STAT_SHARPE_RATIO` | Sharpe ratio |
| `STAT_TRADES` | Number of trades |
| `STAT_PROFIT_TRADES` | Winning trades |
| `STAT_LOSS_TRADES` | Losing trades |
| `STAT_EXPECTED_PAYOFF` | Average profit per trade |
| `STAT_RECOVERY_FACTOR` | Profit / max drawdown |

### Backtesting Workflow

1. Code the EA with `OnTick()`, `OnInit()`, `OnDeinit()`
2. Add `OnTester()` for custom optimization criterion
3. In MT5: Strategy Tester → select EA → set symbol/timeframe/period
4. Choose "Open prices only" for speed, "Every tick" for accuracy
5. Run single test → check results
6. Run optimization → find best parameters
7. Validate with out-of-sample data

### Automated Backtesting Loop

```
EA Development Cycle:
  Code → Compile → Single Test → Check Results
       ↓
  If promising → Optimize → Analyze Results
       ↓
  If validated → Forward Test → Deploy
       ↓
  Monitor → Collect Data → Refine → Repeat
```

## 7. Event Handlers Reference

| Handler | When Called | Use Case |
|---------|-----------|----------|
| `OnInit()` | EA/indicator starts | Initialize handles, variables |
| `OnDeinit()` | EA/indicator stops | Cleanup, release handles |
| `OnTick()` | New tick received | EA main logic |
| `OnTimer()` | Timer event | Periodic operations |
| `OnTrade()` | Trade event | React to trade changes |
| `OnTradeTransaction()` | Trade transaction | Detailed trade tracking |
| `OnChartEvent()` | Chart interaction | GUI buttons, objects |
| `OnCalculate()` | Indicator calculation | Indicator main logic |
| `OnTester()` | Test complete | Custom optimization criterion |
| `OnTesterInit()` | Optimization start | Setup for optimization |
| `OnTesterPass()` | Each optimization pass | Log intermediate results |

## 8. Common Pitfalls

1. **Always check `ResultRetcode()`** after `PositionOpen()` — success != execution
2. **Use `SetExpertMagicNumber()`** to distinguish your EA's trades
3. **Normalize prices** with `SymbolInfoInteger(_Symbol, SYMBOL_DIGITS)`
4. **Check `Bars() > N`** before trading to ensure enough history
5. **Use `ArraySetAsSeries(true)`** for timeseries arrays (index 0 = latest)
6. **Release indicator handles** in `OnDeinit()` with `IndicatorRelease()`
7. **Don't trade on `OnInit()`** — wait for first `OnTick()`
8. **Account type matters**: Hedging requires iterating positions, Netting uses select
9. **Spread varies**: use `SymbolInfoInteger(_Symbol, SYMBOL_SPREAD)` for live spread
10. **Timer in tester**: use `EventSetTimer()` in `OnInit()`, not hardcoded delays

## 9. Quick Reference — EA Skeleton

```mql5
//+------------------------------------------------------------------+
//|                                            MyExpertAdvisor.mq5   |
//+------------------------------------------------------------------+
#property copyright "Your Name"
#property link      ""
#property version   "1.00"

#include <Trade\Trade.mqh>

input double RiskPercent   = 1.0;    // Risk % per trade
input int    Slippage      = 10;     // Max slippage in points
input int    MagicNumber   = 12345;  // EA magic number

#define EA_MAGIC MagicNumber

CTrade trade;
bool   IsHedging;
datetime lastBarTime = 0;

//+------------------------------------------------------------------+
int OnInit() {
    IsHedging = ((ENUM_ACCOUNT_MARGIN_MODE)
        AccountInfoInteger(ACCOUNT_MARGIN_MODE) == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);

    trade.SetExpertMagicNumber(EA_MAGIC);
    trade.SetMarginMode();
    trade.SetTypeFillingBySymbol(Symbol());
    trade.SetDeviationInPoints(Slippage);

    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
void OnDeinit(const int reason) {
    // Cleanup
}

//+------------------------------------------------------------------+
void OnTick() {
    // New bar check
    datetime barTime = iTime(_Symbol, _Period, 0);
    if (barTime == lastBarTime) return;
    lastBarTime = barTime;

    // Analysis and trading logic here
    // ...
}

//+------------------------------------------------------------------+
double OnTester() {
    // Custom optimization criterion
    double trades = TesterStatistics(STAT_TRADES);
    if (trades < 30) return 0;
    return TesterStatistics(STAT_PROFIT_FACTOR);
}
```

## 10. References

### In this skill

- `references/book/` — Programming book (learning path, 581 pages)
  - `00-intro/` — Introduction and IDE
  - `01-basis/` — Language fundamentals
  - `02-oop/` — Object-oriented programming
  - `03-common/` — Common functions (strings, files, math)
  - `04-applications/` — Charts, indicators, objects, events
  - `05-automation/` — Trading, symbols, tester
  - `06-advanced/` — Resources, SQLite, Python, OpenCL
- `references/docs/` — API reference (4135 pages)
  - `19-trading/` — Trading functions (OrderSend, PositionGet, etc.)
  - `16-series/` — Timeseries access (CopyRates, CopyBuffer, etc.)
  - `26-indicators/` — Built-in indicators (iMA, iRSI, iMACD, etc.)
  - `24-customind/` — Custom indicator creation
  - `13-event-handlers/` — Event handlers (OnTick, OnTester, etc.)
  - `34-standardlibrary/` — Standard library (CTrade, CPositionInfo, etc.)

### External

- [MQL5 Reference](https://www.mql5.com/en/docs)
- [MQL5 Book](https://www.mql5.com/en/book)
- [Strategy Tester Guide](https://www.mql5.com/en/terminal/strategytester)
