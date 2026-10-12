# Indicator and Multi-Timeframe Review Guide

Static review of indicator handles, buffers, and multi-timeframe (MTF)
semantics in MQL5 EA/indicator source. Severity: 🔴 silent wrong
signals / execution, 🟡 degraded behaviour, 🟢 readability.

## Table of Contents

- [Handle Lifecycle](#handle-lifecycle)
- [CopyBuffer Discipline](#copybuffer-discipline)
- [Series Order and Indexing](#series-order-and-indexing)
- [New-Bar and Unfinished-Bar Semantics](#new-bar-and-unfinished-bar-semantics)
- [Multi-Timeframe Alignment](#multi-timeframe-alignment)
- [Repaint and Look-Ahead](#repaint-and-look-ahead)
- [Custom Indicator (iCustom) Contracts](#custom-indicator-icustom-contracts)
- [OnCalculate for Indicator Authors](#oncalculate-for-indicator-authors)
- [Review Checklist](#review-checklist)

---

## Handle Lifecycle

```mql5
// ❌ Blocking: handle never checked — all CopyBuffer calls fail,
// EA trades on an all-zero "RSI"
int rsi = iRSI(_Symbol, PERIOD_CURRENT, 14, PRICE_CLOSE);

// ✅ Validate at creation AND at use
int rsi = iRSI(_Symbol, PERIOD_CURRENT, 14, PRICE_CLOSE);
if(rsi == INVALID_HANDLE) {
    Print("iRSI failed — ", GetLastError());
    return INIT_FAILED;      // fail fast in OnInit
}
```

Reviewer checklist:
- [ ] 🔴 Every `iMA/iRSI/iMACD/iADX/iATR/iBands/iCustom/...` handle
  checked against `INVALID_HANDLE`; failure path returns
  `INIT_FAILED` (EA) — not "log and continue".
- [ ] 🟡 Handles created in `OnInit`, **not** in OnTick/on-demand
  (re-creating a handle per tick allocates internal series and
  defeats the terminal's cache).
- [ ] 🟡 `IndicatorRelease(handle)` in `OnDeinit` for every created
  handle. Missing release is a per-chart-cycle leak — invisible in a
  2-day backtest, painful on a VPS running for months.
- [ ] 🟡 Handle array for N symbols/TFs: released in a loop in
  OnDeinit; index bookkeeping consistent (off-by-one leaves one
  handle dangling).
- [ ] 🟢 Handle array declared with the right size via `ArrayResize`
  once — not grown per tick.

## CopyBuffer Discipline

```mql5
// ❌ Blocking: return ignored — on failure buffer keeps PREVIOUS
// values, signal computed on stale data with no error anywhere
CopyBuffer(handle, 0, start, count, buf);

// ❌ Blocking: `> 0` is not enough — may be 1 of 3 requested
if(CopyBuffer(handle, 0, 0, 3, buf) > 0) { /* use buf[2] */ }

// ✅ Exact count, explicit failure path
if(CopyBuffer(handle, 0, 0, 3, buf) != 3) {
    PrintFormat("CopyBuffer failed: %d, err=%d",
                CopyBuffer(handle, 0, 0, 3, buf), GetLastError());
    return;   // skip this bar — never trade on partial data
}
```

Reviewer checklist:
- [ ] 🔴 Return compared to the **exact** requested count, not `> 0`
  or `!= -1`.
- [ ] 🔴 Failure path actually skips the trade/calculation — a
  `Print` followed by continued use of the buffer is a silent bug.
- [ ] 🟡 `GetLastError()` captured **immediately** after the failing
  call (later calls overwrite it).
- [ ] 🟡 Array sized for the request (`ArrayResize(buf, count)` or
  passed with exact size) — under-sized destination = truncated copy.
- [ ] 🟡 Buffer direction set once, globally:
  `ArraySetAsSeries(buf, true)` before first use, not toggled
  intermittently between reads.
- [ ] 🟢 Repeated `CopyBuffer(handle,0,0,N,buf)` inside a loop over
  the same bars — hoist out; copy once.

## Series Order and Indexing

The single most common silent inversion:

```mql5
double buf[];
CopyBuffer(handle, 0, 0, 3, buf);
// Without ArraySetAsSeries(buf, true):
//   buf[0] = OLDEST of the 3, buf[2] = current bar

// ❌ Blocking: comparing "previous" vs "current" backwards
if(buf[0] > buf[1]) signal();    // actually oldest > middle

// ✅ Explicit direction, stated once at declaration site
ArraySetAsSeries(buf, true);
if(CopyBuffer(handle, 0, 0, 3, buf) != 3) return;
if(buf[1] > buf[0]) signal();    // prev > current, as intended
```

Reviewer checklist:
- [ ] 🔴 Every timeseries-like array (`MqlRates`, `CopyBuffer`,
  `CopyClose`, `MqlTick` arrays) has an explicit, visible
  `ArraySetAsSeries` decision. Mixed directions within one file is a
  🟡 at minimum — document each.
- [ ] 🔴 `MqlRates rates[]` + `ArraySetAsSeries(rates, true)` +
  `rates[0]` described as "current bar" in comments — verify comment
  matches reality (comments lie most often here).
- [ ] 🟡 `ArraySetAsSeries` on a **static** array is a no-op — grep
  for static arrays passed through the same helper.
- [ ] 🟢 Index constants (`#define CUR 0`, `#define PREV 1`) instead
  of raw numbers when the file mixes both orders.

## New-Bar and Unfinished-Bar Semantics

```mql5
// ❌ Blocking: decides on every tick of the forming bar —
// "signal" flickers with each tick; tester fills at intra-bar
// prices the author never saw on the chart
void OnTick() { CheckSignal(); }

// ✅ Gate on new bar when decisions are bar-close based
void OnTick() {
    if(iTime(_Symbol, _Period, 0) == m_lastBar) return;
    m_lastBar = iTime(_Symbol, _Period, 0);
    CheckSignal();
}
```

Reviewer checklist:
- [ ] 🔴 Explicit decision: is the EA tick-driven or bar-close
  driven? Bar-close logic **must** have a new-bar gate; tick logic
  must tolerate re-entry safely.
- [ ] 🔴 New-bar detection compares `iTime()` values — **not**
  elapsed-seconds arithmetic (`TimeCurrent()-last >= 60*period`),
  which misfires around DST changes and tick gaps
  → [failure-modes.md](failure-modes.md) §B.
- [ ] 🟡 Signals computed from `close[0]`/`buf[0]` of the *forming*
  bar are provisional; is that the documented intent? A backtest full
  of intra-bar flips vs a chart reviewed at bar close = strategy
  identity mismatch
  → [tester-live-parity.md](tester-live-parity.md).
- [ ] 🟢 `lastBarTime` state variable named and commented (e.g.
  `m_lastBarTime` — member, per code style).

## Multi-Timeframe Alignment

The classic MTF bug: reading a higher-TF buffer index that corresponds
to its **still-forming** bar.

```mql5
// ❌ Blocking: h4[1] is the forming H4 bar for most of the H1 bar —
// the "closed H4 trend" repaints continuously; backtest sees data
// the live chart never showed at decision time
double trend[];
ArraySetAsSeries(trend, true);
CopyBuffer(h4Handle, 0, 0, 2, trend);
if(trend[1] > 0) Buy();    // trend[1] is NOT closed yet

// ✅ Closed higher-TF bar only: index 1 (index 0 = forming)
if(CopyBuffer(h4Handle, 0, 1, 1, trend) != 1) return;
if(trend[0] > 0) Buy();

// ✅ Even stricter: verify the H4 bar time precedes the current H4
// bar start
datetime h4BarTime = iTime(_Symbol, PERIOD_H4, 1);
datetime h4Now     = iTime(_Symbol, PERIOD_H4, 0);
if(h4BarTime >= h4Now) return;   // paranoia against build quirks
```

Reviewer checklist:
- [ ] 🔴 For each higher-TF read: index = 1 (closed bar), or index 0
  explicitly justified (rare — only for "current forming value is
  the intended signal").
- [ ] 🔴 Entry evaluated at an H1 boundary vs H4 boundary: when the
  H4 bar rolls over, does the EA re-evaluate within the same tick,
  or does it wait for the next H1 bar (one-bar-late entries)?
- [ ] 🟡 One handle per (symbol, TF, params) — not one per signal
  check. Handle explosion per tick →
  [performance-review.md](performance-review.md).
- [ ] 🟡 Higher-TF history availability: `iBars(_Symbol, PERIOD_H4)`
  guard before the first H4 read (warm-up period), otherwise
  `CopyBuffer` fails for the first N bars and the EA trades the
  warm-up anyway.
- [ ] 🟢 TF constants as inputs (`input ENUM_TIMEFRAMES InpTrendTF`)
  instead of hardcoded `PERIOD_H4`.

## Repaint and Look-Ahead

- [ ] 🔴 Indicator buffers with `INDICATOR_CALCULATIONS` +
  `PlotIndexSetInteger(..., PLOT_DRAW_BEGIN, ...)` — does the EA read
  indices before the draw-begin offset? Those values are shifting
  initialization garbage.
- [ ] 🔴 Zigzag/Envelopes-style repainters used as entry filters —
  their history *will* change; a backtest on them is unknowingly a
  look-ahead test. If present, the report must say so loudly.
- [ ] 🟡 `iBarShift(sym, tf, time)` returning `-1` (time not found)
  used directly as an index — check the sentinel.
- [ ] 🟡 `CopyRates` of a symbol at a *lower* TF used to reconstruct
  higher-TF bars manually — one-bar alignment errors are near
  guaranteed; prefer `iHigh/iLow` on the target TF.

## Custom Indicator (iCustom) Contracts

- [ ] 🔴 Buffer indices are positional — `iCustom(_Symbol,tf,"MyInd")`
  then `CopyBuffer(h, 3, ...)` with a bare `3`. Is 3 documented in a
  comment or enum? Without it the contract breaks silently when the
  indicator is edited.
- [ ] 🔴 Indicator inputs by **position** vs **name** — verify the
  parameter list order matches the .mq5 source being shipped.
- [ ] 🟡 `#resource`-embedded custom indicator: name starts with `\\`:
  `iCustom(_Symbol, tf, "\\Scripts::MyInd")` — verify the resource
  pragma exists; a missing resource fails at runtime only.
- [ ] 🟡 Hidden dependency: custom indicator reads global variables or
  files in its `OnCalculate` — in the tester these may behave
  differently than live
  → [tester-live-parity.md](tester-live-parity.md).

## OnCalculate for Indicator Authors

- [ ] 🔴 `prev_calculated` used as an absolute count vs a *cached*
  count — the two conventions both exist in the wild; mixing them
  produces an off-by-one that shifts all buffers by one bar
  (indicators look right, values are one bar late).
- [ ] 🔴 `rates_total`-driven loops with no `min_calculated`/warm-up
  handling — first invocation reads uninitialized history.
- [ ] 🟡 `#property indicator_buffers` / `indicator_plots` counts
  match the buffer declarations — mismatch is a compile warning at
  best, silent wrong plot at worst on old builds.
- [ ] 🟡 `PlotIndexSetInteger(plot, PLOT_EMPTY_VALUE, ...)` set —
  otherwise zeros are drawn as values and downstream readers
  (`CopyBuffer` in an EA) see 0 as a real reading.
- [ ] 🟢 Buffer colors/types set via
  `PlotIndexSetInteger(plot, PLOT_LINE_COLOR, ...)` in `OnInit`, not
  hardcoded `#property` only (allows theme handling).

## Review Checklist

1. All handles: `INVALID_HANDLE` checked, created in OnInit, released
   in OnDeinit
2. All `Copy*`: exact-count check, failure path skips trading
3. All series arrays: explicit `ArraySetAsSeries` decision, comments
   match reality
4. New-bar gate present for bar-close logic; `iTime` comparison only
5. Higher-TF reads use closed bars (index 1); overlap re-evaluation
   understood
6. Repainting indicators flagged; no manual HTF reconstruction from LTF
7. iCustom buffer indices/params documented
8. OnCalculate authors: prev_calculated convention consistent,
   empty-value set
