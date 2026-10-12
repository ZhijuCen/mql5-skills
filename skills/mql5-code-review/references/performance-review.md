# Tick-Level Performance Review Guide

Static review of hot-path efficiency in MQL5 EA source. Performance
rules for EAs are *trading* rules too: a frozen event queue means
missed entries and stale trailing stops, i.e. direct money loss.
Severity: 🔴 missed trades / terminal degradation, 🟡 measurable
waste, 🟢 style.

## Table of Contents

- [OnTick Hot-Path Model](#ontick-hot-path-model)
- [Series and Buffer Access](#series-and-buffer-access)
- [Loops and History Scans](#loops-and-history-scans)
- [String and Logging Cost](#string-and-logging-cost)
- [Dynamic Array Discipline](#dynamic-array-discipline)
- [Timer vs Tick Driving](#timer-vs-tick-driving)
- [Object and Redraw Cost](#object-and-redraw-cost)
- [Review Checklist](#review-checklist)

---

## OnTick Hot-Path Model

OnTick on a busy symbol (XAUUSD: 10–100+ ticks/sec during sessions)
is a loop that must exit **cheaply**. Review order:

1. What runs on *every* tick before any gate? (the real hot path)
2. What runs per *new bar*? (should hold the heavy logic)
3. What runs per *signal*? (the trade path — correctness > speed)

```mql5
// ❌ Blocking on busy symbols: full work before any gate
void OnTick() {
    MqlRates rates[];
    ArraySetAsSeries(rates, true);
    int n = CopyRates(_Symbol, _Period, 0, 200, rates);   // every tick
    for(int i = 0; i < 200; i++) { /* heavy loop */ }
    double atr = CalcATR(rates, 14);
    if(IsNewBar()) Decide();                              // gate too late
}

// ✅ Gate first, pay only the gate's cost per tick
void OnTick() {
    if(iTime(_Symbol, _Period, 0) == m_lastBar) return;
    m_lastBar = iTime(_Symbol, _Period, 0);
    MqlRates rates[];
    ArraySetAsSeries(rates, true);
    if(CopyRates(_Symbol, _Period, 0, 200, rates) != 200) return;
    // ... heavy work once per bar
}
```

- [ ] 🔴 Work executed before the new-bar/state gate — this is the
  most common and most expensive EA anti-pattern. The gate (time
  compare or cheap state check) must be statement #1 in OnTick.
- [ ] 🟡 Tick-driven trailing/BE logic: legitimate (needs ticks) but
  must do the *minimum*: one tick read, cheap comparisons, modify
  only when the new SL differs by ≥ stop step — see modify-thrash
  below.

## Series and Buffer Access

- [ ] 🔴 `CopyRates/CopyBuffer` called **more than once per bar** for
  the same window (e.g. inside a helper called per signal check, or
  per position in a loop). Copy once per bar into members, reuse.
- [ ] 🔴 `CopyBuffer(..., 0, N, buf)` copying large N "for safety"
  when the code reads only 3 elements — every element has a cost;
  request what you use.
- [ ] 🟡 Per-element accessors inside loops:
  `iHigh(_Symbol,_Period,i)` in a 500-iteration loop issues 500
  series calls — bulk `CopyRates` into an array once, then index.
- [ ] 🟡 `iBarShift` inside a loop — each call scans history
  (O(bars)); cache the shift for the bar, recompute on new bar only.
- [ ] 🟡 Indicator handle re-created to "refresh params" — handles are
  cheap to *keep*, expensive to create; parameters changing per bar
  is itself a design smell.

## Loops and History Scans

- [ ] 🔴 `HistorySelect(0, now)` + full deal iteration **per tick**
  — grows with account age; after a year this is thousands of deals
  scanned 50×/sec. Cache a cursor (last processed
  `HISTORY_TICKET`/time), scan the delta.
- [ ] 🔴 `PositionsTotal()` full scans repeated 3–4× in one tick for
  the same question (count, sum volume, find max, find oldest) — one
  scan, several accumulators:

```mql5
// ❌ four scans per tick
int    n       = CountMyPositions();
double volTot  = SumMyVolume();
datetime oldest = OldestMyPosition();

// ✅ one scan, three results
int n = 0; double volTot = 0; datetime oldest = 0;
for(int i = PositionsTotal()-1; i >= 0; i--) {
    if(!PositionGetSymbol(i)) continue;
    if(PositionGetInteger(POSITION_MAGIC) != EA_MAGIC) continue;
    if(PositionGetString(POSITION_SYMBOL) != _Symbol) continue;
    n++;
    volTot += PositionGetDouble(POSITION_VOLUME);
    datetime t = (datetime)PositionGetInteger(POSITION_TIME);
    if(oldest == 0 || t < oldest) oldest = t;
}
```

- [ ] 🟡 O(n²) patterns: nested position scans, `ArraySort` per tick,
  string search (`StringFind`) over a growing log.
- [ ] 🟡 Unbounded `for` over `iBars(_Symbol, PERIOD_D1)` with per-
  iteration `CopyBuffer` — cap the warm-up window to what the
  strategy actually needs.
- [ ] 🟢 Magic/symbol filter applied **after** the expensive part of
  the loop body — hoist the cheap filter to the top.

## String and Logging Cost

- [ ] 🔴 `Print/PrintFormat` in the per-tick path — journal I/O is
  synchronous; on a VPS with a slow disk a print storm stalls the
  event thread. Gate logs to new-bar / state-change:

```mql5
// ❌
void OnTick() { PrintFormat("bid=%.5f", SymbolInfoDouble(_Symbol, SYMBOL_BID)); }

// ✅ change-driven, plus an explicit log level input
if(showDebug && isNewBar) PrintFormat(...);
```

- [ ] 🟡 String building in loops (`msg += ...`) — O(n²) on the
  concatenation chain; for reports, pre-size with
  `StringReserve`/build array then join, or stream to file.
- [ ] 🟡 `DoubleToString` with high precision in hot path for values
  only used in comparisons — keep the double, format at the log line.
- [ ] 🟢 `EnumToString`/`IntegerToString` in non-critical paths only —
  fine; in the tick gate, avoid.

## Dynamic Array Discipline

- [ ] 🔴 `ArrayResize` inside a per-tick append without capacity
  doubling — linear resize per append = quadratic total cost AND an
  unbounded memory slope
  → [failure-modes.md](failure-modes.md) §E.
- [ ] 🟡 `ArrayResize(arr, 0)` reset per bar instead of reusing
  capacity — acceptable for small arrays, wasteful for 10k-element
  trackers.
- [ ] 🟡 `ArraySetAsSeries` called repeatedly (per read) — it is a
  flag set; once per array lifetime.
- [ ] 🟢 Arrays declared inside OnTick and filled per tick: members
  reused across ticks avoid repeated allocation (MQL5 allocator is
  not free).

## Timer vs Tick Driving

- [ ] 🟡 Work that only *looks* tick-sensitive (dashboard refresh,
  heartbeat pings, hourly checks) executed per tick —
  `EventSetTimer(1..60)` in OnInit is the correct driver; verify the
  timer is actually set and killed (OnDeinit).
- [ ] 🟡 Timer period < 1s with heavy body — the timer event queues
  behind OnTick on busy symbols anyway; heavy periodic work belongs
  in the bar gate, not the timer, or vice versa by design decision.
- [ ] 🟢 Document the chosen cadence per feature in one table in the
  source header ("feature × cadence") — reviewable in 30 seconds.

## Object and Redraw Cost

Brief here; full treatment in
[gui-ux-review.md](gui-ux-review.md) §3.

- [ ] 🟡 `ObjectSet*/ObjectCreate/ObjectDelete` per tick — each call
  marks the chart dirty; batch updates, single `ChartRedraw()` after.
- [ ] 🟡 `ChartRedraw()` called multiple times per event or per tick —
  it forces a full chart repaint; call once at the end of the update
  batch.
- [ ] 🟢 Tens-to-hundreds of chart objects on one chart slow the whole
  terminal UI, including other charts' responsiveness.

## Review Checklist

1. OnTick statement #1 is a cheap gate (new bar / state change)
2. Bulk copies (`CopyRates/CopyBuffer`) once per bar per window, exact
   counts, results reused
3. No per-element series calls in loops; no `iBarShift` in loops
4. History/position scans: single pass, delta-cached cursor, bounded
   windows
5. Per-tick prints banned; logs change-driven
6. Dynamic arrays bounded, capacity reused
7. Periodic work on timers, heavy work on bar gate
8. Object updates batched; one redraw per batch
