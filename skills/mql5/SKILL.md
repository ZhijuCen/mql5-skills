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

**How to look up any trading function**: Full API docs are in
`references/docs/19-trading/` (34 files). Filename pattern:
`0801-trading-ordercalcprofit.md`. Each file contains parameters, return
values, and usage notes. For functions not listed below, read the
corresponding doc file.

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

// ADX (trend strength)
int handle = iADX(_Symbol, PERIOD_H4, 14);
```

**How to look up any indicator**: Full API docs are in
`references/docs/26-indicators/` (41 files). Filename pattern:
`0969-indicators-i<name>.md` (e.g. `iadx`, `iatr`, `ifractals`).
Each file contains: function signature, parameters, return value,
buffer indices, and usage examples. For indicators not listed in §3,
read the corresponding doc file rather than guessing the API.

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

### Core Concept: PointValue

`PointValue` = profit/loss in profit-currency for a 1-point price move on 1 lot.
This is the foundation for all risk calculations.

```mql5
double PointValue(string symbol) {
    double point    = SymbolInfoDouble(symbol, SYMBOL_POINT);
    double contract = SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE);
    ENUM_SYMBOL_CALC_MODE mode =
        (ENUM_SYMBOL_CALC_MODE)SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE);

    switch (mode) {
        case SYMBOL_CALC_MODE_FOREX:
        case SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE:
        case SYMBOL_CALC_MODE_CFD:
        case SYMBOL_CALC_MODE_CFDINDEX:
        case SYMBOL_CALC_MODE_CFDLEVERAGE:
        case SYMBOL_CALC_MODE_EXCH_STOCKS:
        case SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX:
            return point * contract;

        case SYMBOL_CALC_MODE_FUTURES:
        case SYMBOL_CALC_MODE_EXCH_FUTURES:
        case SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS:
            return point * SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
                                / SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
    }
    return 0;
}
```

Key distinction:
- `SYMBOL_TRADE_TICK_VALUE` = profit-currency per tick for **1 lot** (broker-supplied)
- `PointValue` = profit-currency per **1 point** for **1 lot** (computed)
- `loss = points × PointValue × Lots`

### Direction A: SL Distance Points → SL Price

Given a stop loss distance in points, compute the SL price level.

```mql5
double CalcSLFromPoints(string symbol, double openPrice, int slPoints,
                        bool isBuy) {
    double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
    double slDistPrice = slPoints * point;

    if (isBuy)
        return NormalizeDouble(openPrice - slDistPrice,
                              (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS));
    else
        return NormalizeDouble(openPrice + slDistPrice,
                              (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS));
}
```

### Direction B: Risk % → SL Price (fixed lot size)

Given account balance, risk %, and lot size, compute where SL must be placed.

**CRITICAL**: When profit_currency ≠ account_currency, convert risk amount first.

```mql5
double CalcSLFromRisk(string symbol, double balance, double riskPct,
                      double lots, double openPrice, bool isBuy) {
    double pv = PointValue(symbol);
    if (pv == 0 || lots == 0) return 0;

    double riskAmount = balance * riskPct / 100.0;

    // If profit currency differs from account currency, convert.
    // Example: USDJPY → profit=JPY, account=USD → multiply by USDJPY bid
    string profCy  = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
    string accCy   = AccountInfoString(ACCOUNT_CURRENCY);
    if (profCy != accCy) {
        // Find exchange rate pair: look for a Forex symbol with
        // base=accCy, profit=profCy (or reverse)
        string rateSym = "";
        int dir = FindFXRate(accCy, profCy, rateSym);
        if (dir == 0) { Print("Cannot convert ", profCy, "→", accCy); return 0; }
        MqlTick tick;
        SymbolInfoTick(rateSym, tick);
        double rate = (dir > 0) ? tick.bid : 1.0 / tick.ask;
        riskAmount *= rate;  // risk in profit currency
    }

    double points  = riskAmount / (pv * lots);
    double slPrice = points * SymbolInfoDouble(symbol, SYMBOL_POINT);

    if (isBuy)
        return NormalizeDouble(openPrice - slPrice,
                              (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS));
    else
        return NormalizeDouble(openPrice + slPrice,
                              (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS));
}

// Helper: find a Forex pair that converts from→to
// Returns +1 if pair is from/to, -1 if to/from, 0 if not found
int FindFXRate(string from, string to, string &result) {
    for (int i = 0; i < SymbolsTotal(true); i++) {
        string sym = SymbolName(i, true);
        ENUM_SYMBOL_CALC_MODE m =
            (ENUM_SYMBOL_CALC_MODE)SymbolInfoInteger(sym, SYMBOL_TRADE_CALC_MODE);
        if (m != SYMBOL_CALC_MODE_FOREX &&
            m != SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE) continue;
        string base  = SymbolInfoString(sym, SYMBOL_CURRENCY_BASE);
        string profit = SymbolInfoString(sym, SYMBOL_CURRENCY_PROFIT);
        if (base == from && profit == to) { result = sym; return +1; }
        if (base == to   && profit == from) { result = sym; return -1; }
    }
    return 0;
}
```

### Direction C: SL Price → Lot Size (risk-based sizing)

Given a fixed SL price, compute the lot size so loss matches the risk budget.

```mql5
double CalcLotsFromSL(string symbol, double balance, double riskPct,
                      double openPrice, double slPrice) {
    double pv = PointValue(symbol);
    if (pv == 0) return 0;

    double riskAmount = balance * riskPct / 100.0;

    // Currency conversion (same as Direction B above)
    string profCy = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
    string accCy  = AccountInfoString(ACCOUNT_CURRENCY);
    if (profCy != accCy) {
        string rateSym = "";
        int dir = FindFXRate(accCy, profCy, rateSym);
        if (dir == 0) return 0;
        MqlTick tick;
        SymbolInfoTick(rateSym, tick);
        double rate = (dir > 0) ? tick.bid : 1.0 / tick.ask;
        riskAmount *= rate;
    }

    double slDistPrice = MathAbs(openPrice - slPrice);
    if (slDistPrice == 0) return 0;

    double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
    double points = slDistPrice / point;
    double rawLots = riskAmount / (pv * points);

    // Normalize to broker constraints
    double minLot  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
    double maxLot  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
    double lotStep = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);

    double lot = MathFloor(rawLots / lotStep) * lotStep;
    lot = MathMax(lot, minLot);
    lot = MathMin(lot, maxLot);
    return NormalizeDouble(lot, 2);
}
```

### Profit Verification

Use `OrderCalcProfit` (EA/scripts only) or manual formula to verify:

```mql5
// Using OrderCalcProfit
double profit;
OrderCalcProfit(ORDER_TYPE_BUY, symbol, lots, openPrice, closePrice, profit);
// profit is in profit currency

// Manual formula (Forex/CFD)
double profit = (closePrice - openPrice) * ContractSize * Lots;

// Manual formula (Futures)
double profit = (closePrice - openPrice) * TickValue / TickSize * Lots;
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
2. Calculate SL price from risk% and lot size (Direction B), OR
   calculate lot size from SL price and risk% (Direction C)
3. **Always verify with `OrderCalcProfit`** — compute actual loss for the
   lot you're about to open and confirm it doesn't exceed risk budget
4. Normalize SL with `NormalizeDouble(price, SYMBOL_DIGITS)`
5. Check SL distance ≥ `SYMBOL_TRADE_STOPS_LEVEL × Point`
6. Normalize lots to `SYMBOL_VOLUME_STEP`, clamp to `[VOLUME_MIN, VOLUME_MAX]`.
   If `rawLots < minLot`, the clamp inflates risk — skip the trade
   instead. Always verify with `OrderCalcProfit` before opening: compute
   actual loss for `minLot` and confirm it doesn't exceed risk budget × 1.5.
   If it does, skip the trade
7. When profit_currency ≠ account_currency, convert risk amount via FX rate

## 6. Backtesting and Optimization

### Strategy Tester

The Strategy Tester is built into MT5. Key concepts:

1. **Single Test**: run EA once with fixed parameters
2. **Optimization**: genetic algorithm searches parameter space
3. **Custom Criterion**: `OnTester()` returns optimization value

**Important**: The Strategy Tester is GUI-only. `metatester64.exe` only manages
remote testing agents (install/start/stop), not test execution itself.
`terminal64.exe` has no command-line parameters. Backtesting and optimization
must be performed through the MT5 Strategy Tester GUI.

### CLI Automation — What Can and Cannot Be Automated

| Task | CLI Possible? | How |
|------|:---:|-----|
| Syntax check | ✅ | `wine MetaEditor64.exe /compile:"path" /log /s` |
| Compile .mq5 → .ex5 | ✅ | `wine MetaEditor64.exe /compile:"path" /log` |
| Run backtest | ❌ | GUI only: Strategy Tester |
| Run optimization | ❌ | GUI only: Strategy Tester |
| Parse test report | ✅ | `scripts/parse_tester_report.py` |
| Parse optimization report | ✅ | `scripts/parse_optimizer_report.py` |

MetaEditor CLI syntax (Linux/Wine, from MT5 base directory):
```
wine MetaEditor64.exe /compile:"MQL5/Experts/MyEA.mq5" /log       # compile
wine MetaEditor64.exe /compile:"MQL5/Experts/MyEA.mq5" /log /s    # syntax check only
```
Log file: same directory as source, same name with `.log` extension.

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

### Parameter Optimization

When running optimization in the GUI, define parameter ranges as
`[start, stop, step]` (stop inclusive). For example:

| Parameter | Start | Stop | Step |
|-----------|-------|------|------|
| RiskPercent | 0.5 | 3.0 | 0.5 |
| Slippage | 5 | 20 | 5 |
| MagicNumber | 10000 | 10010 | 1 |

In MT5 Strategy Tester: set each `input` parameter to "Enable optimization",
then configure range/step in the optimization tab.

### Backtesting Workflow

1. Code the EA with `OnTick()`, `OnInit()`, `OnDeinit()`
2. Add `OnTester()` for custom optimization criterion
3. **Compile and check syntax** via CLI (see CLI Automation above)
4. In MT5: Strategy Tester → select EA → set symbol/timeframe/period
5. Choose "Open prices only" for speed, "Every tick" for accuracy
6. Run single test → check results
7. Run optimization → find best parameters
8. Validate with out-of-sample data

### EA Development Cycle

```
Code → Syntax Check (CLI) → Compile (CLI)
  ↓
GUI: Single Test → Check Results
  ↓
If promising → GUI: Optimize → Analyze Report
  ↓
If validated → GUI: Forward Test → Deploy
  ↓
Monitor → Collect Data → Refine → Repeat
```

Note: steps marked (CLI) can be automated via `mql5_helper.py` or direct
Wine commands. GUI steps require human interaction.

### Report Analysis — Interpreting Tester Results

After each backtest, MT5 exports an HTML report. Use
`scripts/parse_tester_report.py` to extract structured data, or read the
HTML directly. Key areas to evaluate:

#### 1. Data Quality Gate

**Always check first.** If history quality is poor, all metrics are suspect.

| Metric | Acceptable | Action if Failed |
|--------|-----------|-----------------|
| History Quality | ≥ 95% real ticks | Re-download tick data or use different broker |
| Bars | Enough for strategy (e.g. 1000+ for H4) | Extend test period |
| Modelling quality | Every tick or Every tick based on real ticks | Never trust "Open prices only" for final eval |

#### 2. Profitability Metrics

| Metric | Good | Warning | Bad |
|--------|------|---------|-----|
| Net Profit | > 0 | ≈ 0 | < 0 |
| Profit Factor | > 1.5 | 1.0–1.5 | < 1.0 |
| Expected Payoff | > 0 | ≈ 0 | < 0 |
| Recovery Factor | > 2.0 | 1.0–2.0 | < 1.0 |

**Profit Factor < 1.0** = guaranteed loss. The EA loses more than it wins.
No amount of parameter tuning will fix a fundamentally negative PF — the
strategy logic itself needs rethinking.

#### 3. Drawdown Analysis

Drawdown is the real killer. A 100% drawdown means account wiped.

| Metric | Safe | Risky | Dangerous |
|--------|------|-------|-----------|
| Max DD% | < 20% | 20–50% | > 50% |
| DD Absolute / Deposit | < 0.5x | 0.5–1x | > 1x (blown) |

**Check both Balance DD and Equity DD.** Equity DD captures floating
losses that haven't realized yet — often much worse than balance DD.

If `Balance DD Max% ≈ 100%`, the account was wiped. Look at the balance
curve: did it recover or flatline at zero?

#### 4. Trade Distribution

| Metric | Healthy | Concerning |
|--------|---------|------------|
| Win Rate | 40–60% | < 30% or > 70% |
| Avg Win / Avg Loss | > 1.5 | < 1.0 |
| Profit Trades % | > 40% | < 30% |
| Largest Loss / Avg Loss | < 3x | > 5x (outlier risk) |

Low win rate is fine if avg win >> avg loss (trend following).
High win rate is fine if avg loss << avg win (mean reversion).
**Red flag**: low win rate AND small avg win = guaranteed bleed.

#### 5. Consecutive Losses

| Metric | Tolerable | Stressed |
|--------|-----------|----------|
| Max Consecutive Losses | < 5 | > 8 |
| Max Consecutive Loss $ | < 2x deposit | > deposit |

More than 8 consecutive losses suggests the strategy has long anti-trend
periods. With martingale or grid sizing, consecutive losses compound
catastrophically.

#### 6. Holding Time

| Pattern | Meaning | Risk |
|---------|---------|------|
| Very short avg (< 1 min) | Scalping / arbitrage | Spread/slippage sensitive |
| Very long avg (> 100 hrs) | Swing / position trading | Gap/overnight risk |
| Huge variance (min vs max) | Mixed strategy | Hard to predict behavior |

#### 7. MFE/MAE Analysis

- **MFE (Most Favorable Excursion)**: how far price went in your favor
  before exit. High MFE + low profit = premature exit (tight TP).
- **MAE (Most Adverse Excursion)**: how far price went against you.
  High MAE + small loss = lucky exit (SL barely held).
- **Correlation (Profits, MAE)**: high positive = losses come from
  large adverse moves (SL too loose or absent).
- **Correlation (MFE, MAE)**: negative = when price moves far in one
  direction, it doesn't retrace (good for trend following).

#### 8. Stop-Out Detection

Stop-outs (comment contains `so`) mean margin was insufficient — the
broker force-closed before SL was reached. This is always a critical bug:

```
Root causes:
1. SL too far from entry → floating loss exceeds available margin
2. Lot size too large for account balance
3. Risk per trade exceeds account capacity
4. Multiple concurrent positions drain margin
```

Fix: reduce lot size, tighten SL, or reduce concurrent positions.

#### 9. Short vs Long Bias

Compare `Short Trades (won%)` vs `Long Trades (won%)`:

- Heavily skewed (e.g. 91 long / 5 short) → EA only trades one direction
- Check if this is intentional (bullish filter) or a bug
- In trending markets, one-direction bias can mask poor signal quality

#### 10. Commission & Swap Impact

In the Deals table, check `Commission` and `Swap` columns:

- Commission should be consistent per deal (proportional to volume)
- Swap accumulates on overnight positions — can turn winners into losers
- `Profit = Price P&L + Commission + Swap` — verify this sums correctly

#### 11. Market Regime Filtering

Trend-following strategies (including order-block / price-structure)
degrade in choppy or sideways markets — order blocks get repeatedly
broken, producing false signals and consecutive losses. Two simple
filters can help:

**ADX Trend Strength Filter**: Only trade when ADX(14) on a higher
timeframe (e.g. H4) exceeds a threshold (commonly 25). ADX below the
threshold means no clear trend — the strategy's edge weakens.

```mql5
// In entry logic, before trend check:
double adx[];
ArraySetAsSeries(adx, true);
if (CopyBuffer(g_h4adx, 0, 0, 1, adx) == 1) {
    if (adx[0] < InpADX_Threshold) {  // e.g. 25.0
        Print("ADX ", adx[0], " < threshold, skipping");
        return;
    }
}
```

**Time-Based Filter**: Certain hours produce noise signals (session
transitions, low liquidity). Identify the worst-performing hours from
monthly breakdowns and skip them:

```mql5
MqlDateTime dt;
TimeCurrent(dt);
// Parse InpBadHours = "4,16,18" and skip if match
```

#### 12. Deal-Level Debugging Methodology

When summary metrics reveal problems, drill into individual trades.
Use `scripts/parse_tester_report.py --analyze` for automated analysis
(pairs deals, computes risk per trade, monthly breakdown, re-entry
detection, streak analysis). For raw data, use `--json` instead.

1. **Pair deals**: Iterate deals, pair each `direction=in` with the next
   `direction=out` to form a complete trade (entry price, exit price, P&L,
   close reason from comment).
2. **Risk check**: For each trade, compute `|net_loss| / deposit × 100` to
   verify risk % is within budget. Flag any trade exceeding 2× target risk.
3. **SL distance analysis**: For SL hits, compute `|entry - exit| / point`
   to get SL distance in points. Check if the EA is entering with SL too
   close (oversized lots) or too far (oversized risk).
4. **Re-entry detection**: Sort trades by entry time. If an SL hit is
   immediately followed by a trade at similar entry price with larger lot,
   the EA is doing implicit martingale on the same setup.
5. **Volume pattern**: Plot lot sizes across trades. Consistent 0.01 lots
   regardless of SL distance = minLot clamp bug.
6. **Monthly breakdown**: Group trades by month, compute win rate and net P&L
   per month. Identify worst months and correlate with market conditions.

#### 13. Time-Window Stability (Over-Fitting Detection)

Aggregate metrics over the full backtest period can hide **regime
change** — the strategy might be profitable in H2 2025 and
catastrophic in H1 2025, with the two cancelling out to a "good"
net profit. To detect this, use the `windows` subcommand to slice
the backtest into N equal time windows and recompute the same 7
metrics per window:

```bash
python skills/mql5/scripts/parse_tester_report.py <report.html> windows --count 4
python skills/mql5/scripts/parse_tester_report.py <report.html> windows --count 6 --json
```

Each window is flagged `▲2σ`, `■EXT`, or `-` based on the per-metric
z-score (this window's value − mean across all windows) / std:

- `▲2σ` — at least one metric has |z| ≥ 2 (notable — this window's
  value is far from the rest of the windows). The marker is followed
  by `k=N` (count of outlier metrics) and the metric abbreviations
  with their signed z (e.g. `prof(+2.3σ),reco(+2.3σ)`).
- `■EXT` — at least one metric has |z| ≥ 5 (extreme — extreme outlier).
  Same `k=N` breakdown.
- `-` — no metric crosses the thresholds.

z is sign-bearing (+/-); the threshold is on |z|. Lower-is-better
metrics (bal_dd_rel_pct) are NOT inverted — a negative z means
"unusually low DD" (good for safety, neutral for consistency), a
positive z means "unusually high DD" (a red flag). For all other
metrics, the natural sign applies (high profit, high PF, etc. = good).

**Red flags (over-fitting / regime change):**

- A single window with a `■EXT` (|z|≥5) outlier on any metric — a
  window whose value is 5 standard deviations from the rest is
  almost certainly a different regime (or a metric that is
  unstable across the backtest).
- Several windows each with their own `▲2σ` outliers on different
  metrics — high cross-metric variance.
- A monotonic gradient in the raw values (e.g. profit rising from
  win 0 to win N-1) — the strategy performs better late in the
  backtest; could be a regime change or could be selection bias.
|- Adjacent windows have very different `bal_dd_rel_pct` (e.g. 5% vs
  35%) — the strategy behaves inconsistently across sub-regimes.

**Use `--count 1` first** to verify the calculation matches the full
report within tolerance. Of 7 metrics, 4 are exact (Profit, EP, PF,
Trades); 3 are documented approximations: Recovery Factor (downstream
of bal_dd_rel_abs), Balance DD Rel% (maximum relative drawdown from
the balance curve — matches HTML's Balance Drawdown Relative within
0.03% on 246753), and Sharpe Ratio (MT5's reported value is
inconsistent with the textbook formula the MQL5 community
reverse-engineers derive — see the cross-check table printed at the
end of the N=1 output).

### Optimization Report Analysis

Optimization exports a different artifact: a single-worksheet XML-tagged
Excel workbook (`ReportOptimizer-*.xml`, also openable in LibreOffice Calc).
Each row is one parameter pass; the first worksheet name is
`Tester Optimizator Results`. Use `scripts/parse_optimizer_report.py` to
extract and analyze it. Top-level modes:

```bash
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml --json
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml --analyze
```

Plus a subcommand:

```bash
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml outliers [--sigma 2] [--top-outliers 10] [--top-normal 5] [--sort ABBR_LIST] [--json]
```

The `outliers` subcommand does a per-pass z-score scan on the 8
performance metrics and splits passes into "strongly-strong" (Set A,
at least one metric `|z| >= σ` in the favourable direction) vs
"no-outlier" (Set B), sorted by a configurable priority chain.
Default: `R↓, EP↓, PF↓, RF↓, SR↓, P↓, DD↑, C↓, T↓` (≈ by `Result`,
then `Expected Payoff`, … `Trades`; `↓` = descending, `↑` = ascending).
See §10 below.

The `Title` field in `<DocumentProperties>` encodes the strategy
environment on one line: `<EA> <SYMBOL>,<PERIOD> <YYYY.MM.DD>-<YYYY.MM.DD>`.
`<DocumentProperties>` also carries `Deposit`, `Leverage`, `Server`,
MT5 `Version`/`Build`, and the run timestamp — use these to verify the
backtest ran on the intended setup (wrong demo server, wrong leverage,
or stale build all invalidate the run).

#### 1. Strategy Environment Card

Read the parsed `env_card` first. Confirm before evaluating any pass:

- **EA / Symbol / Period / Date range** match the spec
- **Deposit × Leverage** match the broker account class
- **Server** is the intended broker (demo vs live, broker name)
- **MT5 build** is current (5.00 / build 5000+ as of 2025)
- **Date range** covers the regime you want to test (≥ 1 year for swing,
  ≥ 3 years for trend)

If the date range is shorter than the strategy's intended holding period,
the optimization is structurally biased.

#### 2. Orthogonality Check

Compare `orthogonality.actual` vs `orthogonality.expected_cartesian` (product
of parameter cardinalities). Mismatch means the Strategy Tester skipped
passes (e.g. due to errors) — the table is incomplete and per-parameter
means will be biased. Re-run with longer timeout or fix the EA so every
pass completes.

#### 3. Dead Parameter Detection

The single highest-value analysis step. A "dead" parameter is one whose
value has no measurable effect on any output metric. The script flags two
patterns:

- **`parameter_effect[X].dead_param == true`**: the per-group mean
  Profit range is < 1% of the maximum group mean. This parameter is not
  doing anything; remove it from optimization to halve the search space.
- **`dead_boolean_params[X]`**: for a boolean Inp* (e.g. NewsFilter), all
  metrics (Profit, PF, RF, Trades) are bit-for-bit identical between
  `true` and `false` groups. This is the cleanest dead-parameter signal:
  the parameter is either never read in the EA, or it toggles a code path
  that never triggers on this backtest.

When you see dead boolean parameters, check the EA's logic for that input:
is the toggle actually wired? `if(InpUseNewsFilter) { ... }` requires
genuine news data to take effect — if the EA cannot load news (wrong
calendar URL, demo server, off-hours), the filter silently no-ops.

#### 4. Duplicate Metric Vectors

`duplicates.groups_with_dupes` counts rows with identical metric vectors
(Profit, PF, RF, Trades, ...). A high count (>30% of total) almost always
points to a dead parameter — the duplicated rows differ only in the dead
parameter's value. Example: 432 passes with a binary dead parameter will
collapse to 216 unique metric vectors, producing 216 duplicate pairs.

#### 5. Best Pass Selection — Use Multiple Criteria

The script reports top-5 by four criteria. They usually agree on the top
few but diverge on the tail. Read them together:

| Criterion | Favors | Watch out |
|-----------|--------|-----------|
| **Profit** | Total return | Can hide low win rate with lucky runs |
| **Profit Factor** | Edge per unit of risk | Trade-count blind (low n) |
| **Recovery Factor** | Return per unit of max DD | Inflated by small DD, not big wins |
| **Custom (OnTester)** | Whatever your `OnTester()` returns | If OnTester only counts profit, equivalent to Profit |

For a robust pick, find the pass that appears in multiple top-5 lists AND
has a `Trades` count near the median (statistical significance). A
pass with 161 trades near the min is barely significant; a pass with 175
trades is the most reliable signal.

#### 6. Parameter Effect Ranking

`parameter_effect` orders parameters by `effect_ratio_spread_over_std`
(= spread between best and worst group means, divided by the global
Profit std). This is a quick "how much does each parameter matter" view:

- `effect_ratio > 1.0` — dominant driver, focus tuning here
- `0.3 < ratio < 1.0` — meaningful but secondary
- `ratio < 0.3` — weak; many values perform similarly

Combined with the per-group means, this tells you the gradient direction:
if `InpSLPips=30` mean is 269 and `InpSLPips=50` mean is 108, SL=30 wins
by 161. But beware counterintuitive results (e.g. tighter SL winning on
mean Profit) — they often mean SL is rarely hit and the "edge" is just
trade-count noise.

#### 7. Trade Count Distribution

`trades.deciles` and `trades.corr_trades_vs_*` expose overtrading and
under-trading patterns. Watch for:

- **`corr_trades_vs_profit < -0.3`**: more trades → less profit.
  Strategy degrades as it scales; common with mean-reversion or
  re-entry on loss.
- **`corr_trades_vs_equity_dd > 0.3`**: more trades → more drawdown.
  Overtuning costs both ways.
- **`trades_per_day_median`**: convert the trade count to a rate against
  the backtest days. < 0.1/day for H4 = fine, > 1/day on H4 = scalper
  regime (spread-sensitive).

The trade-count RANGE itself is diagnostic. Range of 14 (161-175) on 432
passes means parameters only changed entry/exit timing slightly, not the
core signal. Range of 50+ means a parameter is blocking trades entirely.

#### 8. Cross-Analysis: `param_cross`

`param_cross[X]` is the per-X mean Profit/PF/Trades table — the most
direct view of each parameter's gradient. To decide whether to widen
or narrow the optimization range, check the edges: are the best and
worst values at the boundaries of your range? If yes, the optimum may lie
outside — re-run with a wider range.

#### 9. Optimization Reporting Template

When reporting optimization results, include:

1. **Environment card** (EA, symbol, period, date range, deposit, server)
2. **Pass count** vs expected cartesian (orthogonality status)
3. **Dead parameters** (if any) — these are bugs to fix, not "remove from
   optimization" wins
4. **Top-3 passes by Profit**, with their parameter vector
5. **Top-3 by Recovery Factor** (more important than raw profit for live
   trading)
6. **Trade count distribution** (median, range, correlation with profit)
7. **Per-parameter gradient** (which direction to push next iteration)
8. **Recommended next pass** (extend ranges if any edge is the optimum)

Skip the "best PF" and "best recovery factor" sections only when they
identify the same pass as "best profit" — otherwise the disagreement is
the most interesting finding (it means there's a regime-specific trade-off
you should investigate, not average away).

#### 10. Per-Pass Outlier Scan

`--analyze` tells you which **parameter ranges** win and which are dead,
but it doesn't tell you which **individual passes** are statistical
outliers — passes so far above (or, for DD, so far below) the run's
own mean that they deserve separate scrutiny. The `outliers`
subcommand does this with a per-metric z-score scan over the 8
performance metrics.

```
# Default: σ=2.0, top 10 outlier passes, top 5 normal passes
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml outliers

# Custom sort: priority by ExpectedPayoff, RecoveryFactor, Result, Profit
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml outliers --sort EP,RF,R,P

# Single priority metric; rest in default order
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml outliers --sort DD

# Tighter threshold + custom top-N
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml outliers --sigma 2.5 --top-outliers 5

# JSON for further processing
python skills/mql5/scripts/parse_optimizer_report.py ReportOptimizer-*.xml outliers --json
```

**The 8 performance metrics scanned** are everything in `METRIC_COLS`
except `Trades`: `Result`, `Profit`, `Expected Payoff`, `Profit Factor`,
`Recovery Factor`, `Sharpe Ratio`, `Custom`, `Equity DD %`. `Trades` is
explicitly excluded from the metric scan and used only as an exclusion
filter (see below).

**Direction conventions** — per-metric outlier criterion:
- **Higher-is-better** (`Result`, `Profit`, `Expected Payoff`,
  `Profit Factor`, `Recovery Factor`, `Sharpe Ratio`, `Custom`):
  outlier = `z >= +σ`
- **Lower-is-better** (`Equity DD %`): outlier = `z <= -σ` (low DD is
  good; high DD is bad but is not a "strong" outlier — those passes
  are simply average)

**Sort priority (`--sort`)** — control the ranking of passes within
Set A and Set B. Default priority (in abbreviation form):

```
R↓, EP↓, PF↓, RF↓, SR↓, P↓, DD↑, C↓, T↓
```

Abbreviations:
| Code | Full metric        | Direction |
|------|--------------------|-----------|
| R    | Result             | ↓ (desc)  |
| P    | Profit             | ↓ (desc)  |
| EP   | Expected Payoff    | ↓ (desc)  |
| PF   | Profit Factor      | ↓ (desc)  |
| RF   | Recovery Factor    | ↓ (desc)  |
| SR   | Sharpe Ratio       | ↓ (desc)  |
| C    | Custom             | ↓ (desc)  |
| DD   | Equity DD %        | ↑ (asc)   |
| T    | Trades             | ↓ (desc)  |

`DD↑` sorts ascending (lower drawdown first, because lower-is-better).
All other metrics sort descending (higher values first). Supply a
comma-separated list of abbreviations to reorder — e.g.
`--sort EP,RF,R,P` puts Expected Payoff first, then Recovery Factor,
then Result, then Profit, with the remaining metrics (`PF, SR, DD, C, T`)
appended in their default order at the end. Unmentioned abbreviations
are automatically appended in their default positional order.

**Two disjoint sets** (both sorted by the configured priority, both
excluding low-Trades passes):

- **Set A — passes with at least one perf-metric outlier.** These are
  candidates for closer inspection: a pass posting `z > +2` on Profit
  *and* `z > +2` on Sharpe together is genuinely exceptional; a pass
  posting `z > +2` on Profit alone with everything else flat is more
  likely a fluke of small-sample variance.
- **Set B — passes with no perf-metric outlier** (top M by Result).
  The "next-tier" passes — strong but unremarkable relative to the
  rest of the run. Use these when Set A is too small to draw
  conclusions.

**Low-Trades exclusion** — passes with `Trades z <= -σ` (too few
trades to trust) are dropped before either set is built. They are
listed separately in the output so you can see what was filtered.

**Reference table** — the output header prints `mean`, `std`, and
`±σ threshold` for every metric so you can judge whether the outlier
count is meaningful. A run with `Profit std` tiny relative to `mean`
will have many `z > +2` candidates because the threshold is near the
mean; a run with `Profit std` large (high EA variance) will have few.
Always read the std row before trusting the count.

**Sigma choice** — `σ=2.0` is the default. For runs with hundreds of
passes that's strict enough to be useful (~5% of values expected to
clear it under a normal distribution, concentrated at the extremes).
For runs with <100 passes, drop to `σ=1.5` if Set A is empty;
`σ=3.0` is appropriate only for runs with >1000 passes (then
`z > 3` outliers are real signal, not tails).

**Generic column typing** — `parse_optimizer_report.py` does not
hardcode input-parameter names. Two techniques that make the script
EA-agnostic:
- **Type inference** comes from the SpreadsheetML header: a body cell
  with `<Data ss:Type="String">` stays as a string column (e.g.
  boolean Inp* rendered as `"true"`/`"false"`); numeric cells become
  `float64` (or `Int64` when every value is whole). No `Inp*` name
  is ever referenced.
- **Input-parameter detection** uses column position, not name
  prefix: `Trades` is the last fixed column; every column after it is
  an optimization input parameter regardless of whether its name
  starts with `Inp`. So an EA that names parameters `StopLoss`,
  `TakeProfit`, `UseNewsFilter` is parsed correctly without any
  script changes.

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

### General

1. **Always check `ResultRetcode()`** after `PositionOpen()` — success != execution
2. **Use `SetExpertMagicNumber()`** to distinguish your EA's trades
3. **Normalize prices** with `NormalizeDouble(price, SYMBOL_DIGITS)`
4. **Check `Bars() > N`** before trading to ensure enough history
5. **Use `ArraySetAsSeries(true)`** for timeseries arrays (index 0 = latest)
6. **Release indicator handles** in `OnDeinit()` with `IndicatorRelease()`
7. **Don't trade on `OnInit()`** — wait for first `OnTick()`
8. **Account type matters**: Hedging requires iterating positions, Netting uses select
9. **Spread varies**: use `SymbolInfoInteger(_Symbol, SYMBOL_SPREAD)` for live spread
10. **Timer in tester**: use `EventSetTimer()` in `OnInit()`, not hardcoded delays

### SL/TP and Risk Calculation

11. **PointValue ≠ TICK_VALUE**: `SYMBOL_TRADE_TICK_VALUE` is per tick (broker-defined step), `PointValue = point × ContractSize` is per point (smallest price unit). For most Forex: TickSize = Point, so they coincide; for futures/metals they may differ.
12. **TickSize ≠ Point**: Always use the correct formula for the symbol's `SYMBOL_TRADE_CALC_MODE`. Forex/CFD: `loss = delta_price × ContractSize × Lots`. Futures: `loss = delta_price × TickValue / TickSize × Lots`.
13. **Profit currency ≠ Account currency**: USDJPY profit is JPY, not USD. Risk amount must be converted: `risk_JPY = risk_USD × USDJPY_bid`. Failing this makes risk 100×+ too small.
14. **NormalizeDouble introduces rounding**: SL price rounded to `SYMBOL_DIGITS` causes ~0.01-0.02% deviation from target loss. Acceptable; verify with `OrderCalcProfit`.
15. **Lot step quantization**: `MathFloor(rawLots / lotStep) * lotStep` can leave residual risk unmet. For large lot_step or small risk budgets, actual loss may differ from target by up to one lot_step worth of loss.
16. **STOPS_LEVEL check**: SL must be ≥ `SYMBOL_TRADE_STOPS_LEVEL × Point` from current price. If stops_level ≤ 0, use a safety margin (e.g. 150 points).

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
//| PointValue: profit-currency per 1-point move for 1 lot            |
//+------------------------------------------------------------------+
double PointValue(string symbol) {
    double point    = SymbolInfoDouble(symbol, SYMBOL_POINT);
    double contract = SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE);
    ENUM_SYMBOL_CALC_MODE mode =
        (ENUM_SYMBOL_CALC_MODE)SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE);
    if (mode == SYMBOL_CALC_MODE_FUTURES ||
        mode == SYMBOL_CALC_MODE_EXCH_FUTURES ||
        mode == SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS)
        return point * SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
                            / SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
    return point * contract;  // Forex, CFD, Stocks
}

//+------------------------------------------------------------------+
//| FindFXRate: locate a Forex pair for currency conversion            |
//+------------------------------------------------------------------+
int FindFXRate(string from, string to, string &result) {
    for (int i = 0; i < SymbolsTotal(true); i++) {
        string sym = SymbolName(i, true);
        ENUM_SYMBOL_CALC_MODE m =
            (ENUM_SYMBOL_CALC_MODE)SymbolInfoInteger(sym, SYMBOL_TRADE_CALC_MODE);
        if (m != SYMBOL_CALC_MODE_FOREX &&
            m != SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE) continue;
        string base   = SymbolInfoString(sym, SYMBOL_CURRENCY_BASE);
        string profit = SymbolInfoString(sym, SYMBOL_CURRENCY_PROFIT);
        if (base == from && profit == to) { result = sym; return +1; }
        if (base == to   && profit == from) { result = sym; return -1; }
    }
    return 0;
}

//+------------------------------------------------------------------+
//| CalcSLFromRisk: risk% + lots → SL price                           |
//+------------------------------------------------------------------+
double CalcSLFromRisk(string symbol, double balance, double riskPct,
                      double lots, double openPrice, bool isBuy) {
    double pv = PointValue(symbol);
    if (pv == 0 || lots == 0) return 0;
    double riskAmount = balance * riskPct / 100.0;

    // Currency conversion if needed
    string profCy = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
    string accCy  = AccountInfoString(ACCOUNT_CURRENCY);
    if (profCy != accCy) {
        string rateSym = "";
        int dir = FindFXRate(accCy, profCy, rateSym);
        if (dir == 0) return 0;
        MqlTick tick; SymbolInfoTick(rateSym, tick);
        riskAmount *= (dir > 0) ? tick.bid : 1.0 / tick.ask;
    }

    double points  = riskAmount / (pv * lots);
    double slPrice = points * SymbolInfoDouble(symbol, SYMBOL_POINT);
    int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
    return isBuy ? NormalizeDouble(openPrice - slPrice, digits)
                 : NormalizeDouble(openPrice + slPrice, digits);
}

//+------------------------------------------------------------------+
//| CalcLotsFromSL: SL price + risk% → lot size                       |
//+------------------------------------------------------------------+
double CalcLotsFromSL(string symbol, double balance, double riskPct,
                      double openPrice, double slPrice) {
    double pv = PointValue(symbol);
    if (pv == 0) return 0;
    double riskAmount = balance * riskPct / 100.0;

    string profCy = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
    string accCy  = AccountInfoString(ACCOUNT_CURRENCY);
    if (profCy != accCy) {
        string rateSym = "";
        int dir = FindFXRate(accCy, profCy, rateSym);
        if (dir == 0) return 0;
        MqlTick tick; SymbolInfoTick(rateSym, tick);
        riskAmount *= (dir > 0) ? tick.bid : 1.0 / tick.ask;
    }

    double slDist = MathAbs(openPrice - slPrice);
    if (slDist == 0) return 0;
    double points = slDist / SymbolInfoDouble(symbol, SYMBOL_POINT);
    double rawLots = riskAmount / (pv * points);

    double minLot  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
    double maxLot  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
    double lotStep = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);
    double lot = MathFloor(rawLots / lotStep) * lotStep;
    lot = MathMax(lot, minLot);
    lot = MathMin(lot, maxLot);
    return NormalizeDouble(lot, 2);
}

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

    // Example: buy with 1% risk, SL at 500 points
    double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    int slPts = 500;
    double sl = CalcSLFromPoints(_Symbol, bid, slPts, true);
    // Or: double sl = CalcSLFromRisk(_Symbol,
    //         AccountInfoDouble(ACCOUNT_BALANCE), RiskPercent,
    //         0.10, bid, true);

    double lots = CalcLotsFromSL(_Symbol,
        AccountInfoDouble(ACCOUNT_BALANCE), RiskPercent, bid, sl);

    // Verify loss matches risk budget
    double profit;
    OrderCalcProfit(ORDER_TYPE_BUY, _Symbol, lots, bid, sl, profit);
    PrintFormat("SL=%.5f lots=%.2f expected_loss=%.2f",
                sl, lots, profit);

    // trade.Buy(lots, _Symbol, 0, sl, 0, "EA Signal");
}

double OnTester() {
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
  - `01-constants/` — Enums and structures (MqlTradeRequest, ENUM_SYMBOL_CALC_MODE)
- `references/symbol-spec/` — Symbol specification CSVs (broker-specific)
  - `specs-XAUUSD.csv` — XAUUSD: CFD Leverage, ContractSize=100, Digits=2
  - `specs-USDJPY.csv` — USDJPY: Forex, ContractSize=100000, Digits=3
- `scripts/verify_sl_tp_formulas.py` — Python verification of SL/TP risk formulas

### External

- [MQL5 Reference](https://www.mql5.com/en/docs)
- [MQL5 Book](https://www.mql5.com/en/book)
- [Strategy Tester Guide](https://www.mql5.com/en/terminal/strategytester)
