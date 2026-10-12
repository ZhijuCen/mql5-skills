# Tester vs Live Parity Review Guide

Static review of what an EA's source implies about the gap between its
backtest behaviour and its live behaviour. This skill reviews the
*source* for parity hazards; running the backtest itself belongs to
the `mql5` skill. Severity: 🔴 backtest results invalid as evidence,
🟡 expectation management, 🟢 documented limitation.

## Table of Contents

- [Tester Branching Patterns](#tester-branching-patterns)
- [The No-Internet Tester](#the-no-internet-tester)
- [Execution Realism](#execution-realism)
- [Look-Ahead and Data Leakage](#look-ahead-and-data-leakage)
- [Randomness and Nondeterminism](#randomness-and-nondeterminism)
- [Tester-Only Crutches](#tester-only-crutches)
- [Review Checklist](#review-checklist)

---

## Tester Branching Patterns

`MQLInfoInteger(MQL_TESTER)` / `MQLInfoInteger(MQL_VISUAL_MODE)` /
`MQLInfoInteger(MQL_OPTIMIZATION)` branches are legitimate (the
economic-calendar `#resource` pattern from `../mql5` skill §6 is the
canonical example) — but every branch is a behaviour fork between the
two worlds:

- [ ] 🔴 Trading logic differs between tester and live branches
  (different SL, different sizing, different filters) — then the
  backtest validates *another strategy*. Broker-only logic (filling
  adaptation) is fine; signal logic is not.
- [ ] 🟡 `MQL_TESTER` branch silently degrades (calendar unavailable
  → filter disabled *only in tester*) — the backtest then shows
  filter-free performance presented as filter-protected. Document and
  prefer an explicit "degraded mode" log line.
- [ ] 🟡 Visual-mode-only UI code guarded correctly (objects skipped
  in tester is fine; objects created in *both* but updated only live
  means the visual backtest lies about the dashboard).
- [ ] 🟢 The number of `MQL_TESTER` sites is itself a review metric:
  each one doubles the test surface; many sites = consider redesign.

## The No-Internet Tester

```mql5
// ❌ Blocking: in the tester this call fails (error 4014/65535-era
// behaviour), NewsTime() returns false/0, the news filter silently
// never fires — backtest is "with filter" only on paper
bool NewsTime() {
    MqlCalendarValue v[];
    return CalendarValueHistory(v, t0, t1, currency) > 0;
}
```

Checklist:
- [ ] 🔴 Any `CalendarValueHistory`/`CalendarValueByName`,
  `WebRequest`, DLL-backed lookup — assumed-live-data in a path that
  also runs in the tester. Verify the fallback: the MQL5-article-22196
  pattern (export on live terminal → `#resource` embed → branch in
  OnInit) is the accepted fix; "returns empty → trade anyway" is not.
- [ ] 🟡 Files under `MQL5/Files` written live but not present in the
  tester sandbox — a data file the EA "obviously has" may not exist
  in the tester's file namespace; verify the EA checks `FileOpen`
  failure and degrades explicitly.
- [ ] 🟡 `#resource` data staleness: the embed is frozen at compile
  time. A calendar `.bin` embedded in January is wrong by March —
  review for a rebuild step in the workflow, not just in the README.

## Execution Realism

- [ ] 🔴 Model dependence baked into the strategy: logic that trades
  *inside* a bar (trailing at tick level, scalp TP of 5–10 points,
  martingale add-on per tick) is only meaningful under
  "Every tick based on real ticks". Under "Open prices only" or
  "1-minute OHLC" the tested entity is fiction. Review: identify the
  finest granularity the logic needs; flag any finer assumption.
- [ ] 🔴 Spread assumption: fixed-spread logic (TP of exactly the
  average spread) or code reading `SYMBOL_SPREAD` — in the tester
  spread is modelled (or fixed via `SymbolInfoDouble`), live spread
  floats and spikes at rollover/news. Flag strategies whose edge
  (< ~10 points expectancy) is below plausible spread variation.
- [ ] 🟡 Slippage: `SetDeviationInPoints` is honoured by the tester
  under real-tick modelling only; entries at market open (gap) and
  stop-outs get worse fills live than in most backtests. Review:
  stop-based exits in gap-prone sessions deserve an explicit
  expectation note.
- [ ] 🟡 Latency: the tester executes at the same timestamp the signal
  appeared. Live: VPS latency + server queue. For EAs whose edge
  decays within seconds (breakout bursts), the backtest is an upper
  bound; state it.
- [ ] 🟡 Stop-out/margin semantics: the tester applies the account's
  margin policy precisely; live, dealer intervention (manual
  stop-outs, requotes at stress) exceeds it. Grid/martingale reviews
  must note this.
- [ ] 🟢 Commission: verify the commission in the backtest environment
  matches the live account (raw-spread accounts often do not carry it
  into a mismatched demo environment).

## Look-Ahead and Data Leakage

- [ ] 🔴 Decisions using `iBarShift(sym, tf, someTime)` with a time
  derived from *later* data (e.g. "yesterday's high") without
  verifying the shift resolved to a closed bar.
- [ ] 🔴 `CopyRates` window that includes the current bar used to
  compute "the day's range", then trading a breakout vs that range —
  the forming bar contributes to its own breakout target
  (self-referential look-ahead).
- [ ] 🟡 Indicator warm-up: trades taken during the warm-up window
  where buffers were partially uninitialized (empty-value plots read
  as 0 → phantom signals)
  → [indicator-review.md](indicator-review.md).
- [ ] 🟡 `OnTester`/`OnTesterPass` writing results consumed by a later
  selection step — fine for optimization, but confirm the *final*
  reported numbers come from an untouched validation run (out-of-
  sample discipline lives in the `mql5` skill's workflow; this review
  only checks the code does not leak).
- [ ] 🟢 Strategy parameters that encode known historical regimes
  (e.g. hardcoded 2020-volatility constants) — a data-leak class of
  its own; ask for the justification.

## Randomness and Nondeterminism

- [ ] 🔴 `MathRand`/`srand` seeds: fixed seed = every "robustness"
  run identical; per-tick seed = irreproducible results. Review:
  seed policy stated; better — the strategy has no randomness (most
  shouldn't).
- [ ] 🟡 Nondeterminism via live data in backtests (the no-internet
  case above) — same source code, different results across runs; a
  result that cannot be reproduced is not evidence.
- [ ] 🟡 `GetTickCount()`/`TimeLocal()`-driven decisions — never the
  same in tester and live, and not reproducible between runs.
- [ ] 🟢 Wall-clock in trade comments/logs only (harmless) — flag
  only when it feeds logic.

## Tester-Only Crutches

- [ ] 🟡 `EventSetTimer` used as a tick substitute with the comment
  "works in tester" — timers fire per model tick in the tester;
  verify the intended cadence survives both worlds
  (../mql5 SKILL.md §8 pitfall #10).
- [ ] 🟡 Position sizing computed from `TesterStatistics(...)` inside
  OnTick — returns valid values only in the tester; live path must be
  a separate code path, guarded.
- [ ] 🟡 Hardcoded "if(deposit < X)" style assumptions that only hold
  for the tested environment.
- [ ] 🟢 A single source file with 400+ lines of tester scaffolding —
  recommend extracting to a harness so the strategy core stays
  testable.

## Review Checklist

1. Every `MQL_TESTER` branch: what *changes*? Signal-affecting changes
   invalidate the backtest as evidence
2. No live-only data source (calendar, web, DLL) silently empty in the
   tester — `#resource` pattern or explicit degraded-mode logging
3. Required modelling granularity identified; strategy edge > spread
   + slippage + latency budget
4. No look-ahead: all indices on closed bars; forming bar never feeds
   its own decision
5. Warm-up trades excluded or guarded
6. Randomness: seed policy stated, reproducibility preserved
7. Tester scaffolding (`OnTester*`, `TesterStatistics`) is inert live
8. Report expectation notes written: where live will be worse than the
   backtest and by roughly how much
