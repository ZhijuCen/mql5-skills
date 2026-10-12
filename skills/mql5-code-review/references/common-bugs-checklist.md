# MQL5 Common Bugs Checklist

Quick-reference bug catalog for static EA review. Each entry names the
bug, the failure scenario, and the fix. For full ❌/✅ code walkthroughs
see the dedicated guides linked per section.

Severity used in this file: 🔴 = money/execution failure, 🟡 =
degraded behaviour or diagnosability gap, 🟢 = readability.

## Trade Execution

- [ ] 🔴 `CTrade` order call without `ResultRetcode()` check — success
  ≠ execution; `false` return or retcode ≠ `TRADE_RETCODE_DONE` means
  the position does not exist while the EA believes it does
  → `references/trading-logic-review.md`
- [ ] 🔴 No magic number, or magic not set before first order
  (`SetExpertMagicNumber` after `PositionOpen`) — EA adopts/manages
  foreign positions, double-manages on restart
- [ ] 🔴 Hedging account iterated with netting logic (`PositionSelect`
  without magic scan) or vice versa — wrong position targeted
- [ ] 🔴 Filling mode hardcoded (`ORDER_FILLING_FOK`) instead of
  `SetTypeFillingBySymbol` — broker rejects order, retcode
  `TRADE_RETCODE_INVALID_FILL`
- [ ] 🟡 SL/TP price not `NormalizeDouble`d to `SYMBOL_DIGITS` —
  broker rejects or silently rounds
- [ ] 🟡 SL distance < `SYMBOL_TRADE_STOPS_LEVEL × Point` — retcode
  `TRADE_RETCODE_INVALID_STOPS`, intermittent by broker
- [ ] 🟡 Trade opened in `OnInit()` — no valid tick yet, price is 0
  or stale; tester statistics distorted
- [ ] 🟡 `PositionClose` by ticket without re-selecting — stale ticket
  after a partial close elsewhere

## Risk and Money Math

- [ ] 🔴 `PointValue` conflated with `SYMBOL_TRADE_TICK_VALUE` — lot
  sizing off by `TickSize/Point` on 3/5-digit symbols
- [ ] 🔴 Profit currency ≠ account currency and no FX conversion —
  USDJPY account in USD: risk 100×+ off
- [ ] 🔴 Lot not clamped to `[SYMBOL_VOLUME_MIN, VOLUME_MAX]` and
  quantized to `SYMBOL_VOLUME_STEP` — retcode
  `TRADE_RETCODE_INVALID_VOLUME`, or silent clamp by broker inflates
  actual risk
- [ ] 🟡 `MathFloor(lots/step)*step` residual risk never verified with
  `OrderCalcProfit` — actual loss ≠ planned loss
- [ ] 🟡 Division by `SYMBOL_TRADE_TICK_SIZE`/`CONTRACT_SIZE` without
  zero check — NaN lots on a newly added symbol
  → `references/diagnostics-and-numeric.md` §G

## Time-Series Semantics

- [ ] 🔴 MTF: higher-TF buffer read before that bar closed — signal
  repaints on every tick of the forming bar
  → `references/indicator-review.md`
- [ ] 🔴 New-bar detection via `TimeCurrent()-lastTime >= period`
  instead of `iTime()` compare — DST shift or tick gap misfires
  → `references/failure-modes.md` §B
- [ ] 🟡 `ArraySetAsSeries` missing/wrong direction — index 0 is
  oldest, every comparison silently inverted
- [ ] 🟡 `CopyBuffer`/`CopyRates` return count not checked (`!= expected`)
  — array holds stale data from previous call, logic runs on garbage
- [ ] 🟡 `Bars() > N` guard missing before first history-dependent
  calculation — first ticks compute on 10 bars
- [ ] 🟢 `iBarShift` on every loop iteration (O(n) each) — cache the
  shift → `references/performance-review.md`

## Indicator Handles

- [ ] 🔴 `INVALID_HANDLE` from `iMA()`/`iCustom()` not checked — every
  later `CopyBuffer` fails silently, indicator prints zeros
- [ ] 🟡 `IndicatorRelease()` missing in `OnDeinit` — handle leak per
  chart-cycle; terminal long-run degradation
- [ ] 🟡 Handle re-created inside OnTick ("just to be safe") — heavy
  internal allocation per tick

## State and Lifecycle

- [ ] 🔴 State machine lives only in global variables — terminal
  restart zeroes it; EA opens duplicate positions on first tick
  → `references/failure-modes.md` §A
- [ ] 🔴 GUI objects created but `OnDeinit` has no cleanup — objects
  survive EA removal; name collision on re-attach
  → `references/gui-ux-review.md` §4
- [ ] 🟡 `EventSetTimer` never paired with `EventKillTimer` — duplicate
  timers on re-init (parameter change re-runs OnInit)
- [ ] 🟡 Comment "handled" branches: `if(failed) { /* retry later */ }`
  — retry path never implemented, state desyncs

## Notifications and Logging

- [ ] 🔴 `Alert()`/`SendNotification()`/`SendMail()` in the OnTick path
  without a once-per-signal guard — hundreds of pushes per hour,
  terminal/broker throttles the account
  → `references/gui-ux-review.md` §5
- [ ] 🟡 `Print` in per-tick path — journal grows unbounded, real
  incidents drown; add log-level or once-per-bar gating
- [ ] 🟡 Log lines without context (symbol/magic/ticket/price) — live
  incident cannot be reconstructed
  → `references/diagnostics-and-numeric.md` §F

## Numeric

- [ ] 🔴 Double equality `price == entry` — almost never true on
  3/5-digit symbols; comparison branch dead
- [ ] 🔴 NaN propagation: `MathSqrt(negative)`, `0/0` in sizing —
  NaN passes all `<`/`>` checks, reaches `PositionOpen` as invalid
  volume
- [ ] 🟡 `NormalizeDouble` applied mid-cascade (risk chain) instead of
  only at the final price — rounding error accumulates
- [ ] 🟡 First-tick price = 0 used before `SymbolInfoTick` success —
  SL computed at 0, order rejected or accepted at nonsense level

## Readability and Structure

- [ ] 🟢 Members without `m_` prefix, classes without `C` prefix —
  violates `../mql5/references/quick-ref-code-style.md`; locals and
  fields indistinguishable
- [ ] 🟢 Magic numbers: `500` (points?), `0.02` (lots? risk?) inline —
  name them (`input int InpSLPoints`)
- [ ] 🟢 Commented-out code ≥3 lines, TODO/FIXME left in source
- [ ] 🟢 OnTick > ~100 lines — extract signal/risk/execute functions
- [ ] 🟢 Copy-pasted block with 2 differing tokens — extract parameterized
  function

## Full Guides

- Order flow & risk: [trading-logic-review.md](trading-logic-review.md)
- Buffers & MTF: [indicator-review.md](indicator-review.md)
- Runtime failure scenarios: [failure-modes.md](failure-modes.md)
- Silent numeric errors: [diagnostics-and-numeric.md](diagnostics-and-numeric.md)
- Hot path: [performance-review.md](performance-review.md)
- Backtest lies: [tester-live-parity.md](tester-live-parity.md)
- Panels & notifications: [gui-ux-review.md](gui-ux-review.md)
