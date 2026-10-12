# Runtime Failure Modes (Static Analysis)

Failure modes that a healthy backtest systematically fails to reveal:
restarts, session gaps, broker differences, event races, and long-run
resource growth. The review task is to construct the failing scenario
**from the source alone** and mark it with a severity. Severity: 🔴
loses money or stops the EA, 🟡 degraded, 🟢 informational.

## Table of Contents

- [§A State Persistence Across Restarts](#a-state-persistence-across-restarts)
- [§B Time and Session Edges](#b-time-and-session-edges)
- [§C Broker and Symbol Portability](#c-broker-and-symbol-portability)
- [§D Event Reentrancy and Order Races](#d-event-reentrancy-and-order-races)
- [§E Long-Run Resource Growth](#e-long-run-resource-growth)

---

## §A State Persistence Across Restarts

Terminal restart, VPS reboot, connection loss, EA re-attach (parameter
change re-runs OnInit): all zero the global variables. A backtest never
restarts mid-trade.

### Re-adoption path

```mql5
// ❌ Blocking: state machine starts from zero after restart —
// EA "believes" it has no position and opens a second one
int    m_state = FLAT;
datetime m_lastSignal = 0;

void OnTick() {
    if(m_state == FLAT && Signal())
        OpenTrade();    // duplicate on restart while position is open
}

// ✅ On first tick, rebuild state from the broker's reality
bool m_adopted = false;
void OnTick() {
    if(!m_adopted) {
        AdoptExistingState();    // scan PositionsTotal/OrdersTotal
        m_adopted = true;
    }
    ...
}
void AdoptExistingState() {
    for(int i = PositionsTotal()-1; i >= 0; i--) {
        if(!PositionGetSymbol(i)) continue;
        if(PositionGetInteger(POSITION_MAGIC) != EA_MAGIC) continue;
        if(PositionGetString(POSITION_SYMBOL) != _Symbol) continue;
        m_state   = IN_POSITION;
        m_ticket  = PositionGetInteger(POSITION_TICKET);
        return;
    }
    // also re-adopt pending orders here
}
```

Reviewer checklist:
- [ ] 🔴 Which globals encode *broker-side* state (open/pending, entry
  price, SL, ticket, counters tied to open trades)? All of them must
  have a rebuild path from `PositionsTotal()`/`OrdersTotal()`.
- [ ] 🔴 Pure local state (lastBarTime, session counters): is zero on
  restart harmless? Zero `lastBarTime` = first tick counts as new bar
  — usually fine; zero session counter may re-enable a daily limit
  early — often NOT fine. Walk each variable.
- [ ] 🔴 `GlobalVariable*()` used for persistence: names must include
  magic + symbol (multi-instance safety); expiry not set to 0 with
  unbounded growth of the GV table.
- [ ] 🟡 Partial state: position adopted but its companion pending
  order not — the two tables must be scanned together.
- [ ] 🟡 Ticket reuse: code assuming ticket monotonicity or caching
  tickets long-term — a cached ticket can point at a *new, unrelated*
  position after close/reopen.
- [ ] 🟡 Countdown/limit state (max N trades/day) — reconstructable
  from deal history (`HistorySelect` + magic filter)? If yes, verify
  the history window logic; if no, document that restart resets limits
  (🟡 with an explicit note is acceptable, silence is not).

## §B Time and Session Edges

- [ ] 🔴 New-bar logic based on elapsed seconds
  (`TimeCurrent() - m_last >= 60*period`) — DST shift makes the
  "bar" fire an hour early/late; tick gaps (illiquid symbols) fire
  late. Use `iTime()` comparison
  → [indicator-review.md](indicator-review.md).
- [ ] 🔴 `TimeCurrent()` (server) vs `TimeLocal()` (terminal machine)
  mixed in the same decision — on a VPS in another timezone the
  "session filter" opens at the wrong hour. Every time comparison
  must state its clock; session filters use **server** time.
- [ ] 🔴 Weekend-gap logic: EA places a stop Friday 23:59, gap opens
  Sunday/Monday 200 pips through it. Is there a pre-close flatten
  rule or a documented acceptance of gap risk? Silent = 🔴.
- [ ] 🟡 Daylight-saving rollover: server time that shifts by an hour
  — hour-of-day filters keyed to absolute hours (e.g. "trade 8–12")
  drift by one hour twice a year. Acceptable but should be a
  documented decision, not an oversight.
- [ ] 🟡 Rollover spread spike (00:00 server): entry/BE/trailing logic
  that runs "any time" can trigger at the 30-second-wide-spread
  moment. Guard: spread sanity check before action
  (`SYMBOL_SPREAD` vs rolling median, or fixed cap).
- [ ] 🟡 Broker forced closure near market close (some CFDs close
  positions 5 min before rollover): EA state must reconcile — the
  "position closed by broker" path is not the EA's own close path.
- [ ] 🟡 First tick after open: `SymbolInfoTick` succeeds but bid/ask
  may be Friday close + gap; SL computed from stale chart bar values
  (`iClose` of the last bar) is not the tradable price. Entries must
  use live tick prices.
- [ ] 🟢 `TimeDayOfWeek`-based filters documented against the server
  calendar (Middle East servers: Fri/Sat weekend — a "skip Friday"
  rule means something different there).

## §C Broker and Symbol Portability

- [ ] 🔴 Hardcoded symbol name (`"XAUUSD"`) — server variants
  (`GOLD`, `XAUUSD.a`, `XAUUSDm`) silently fail every lookup; prefer
  `_Symbol` or an input.
- [ ] 🔴 Hardcoded digits/point arithmetic (`price*100000`,
  `1.2345` literals) — 4-digit vs 5-digit vs 3-digit JPY symbols
  break the math. Always `SymbolInfoDouble(sym, SYMBOL_POINT)` and
  `SYMBOL_DIGITS`.
- [ ] 🔴 Filling mode: hardcoded `ORDER_FILLING_FOK` rejected by
  IOC-only brokers (and vice versa) —
  [trading-logic-review.md](trading-logic-review.md).
- [ ] 🟡 `SYMBOL_TRADE_CALC_MODE` differences: Forex/CFD formula
  (`Δprice × ContractSize × Lots`) vs Futures (`Δprice × TickValue/
  TickSize × Lots`) — a Futures-spec account silently misprices risk.
- [ ] 🟡 Stops level assumptions: code that treats
  `SYMBOL_TRADE_STOPS_LEVEL == 0` as impossible (hardcoded min
  distance) or that fails to fall back to a safety margin (~150
  points) when the broker reports 0.
- [ ] 🟡 Freeze level: modifying SL near the current price is rejected
  (`TRADE_RETCODE_INVALID_STOPS`) when within `SYMBOL_FREEZE_LEVEL` —
  trailing/BE code must respect it.
- [ ] 🟡 `SYMBOL_VOLUME_STEP` < expected: quantization with a guessed
  step (0.01 vs 0.001) — use the spec value.
- [ ] 🟢 Account currency check in OnInit: warn loudly when
  `ACCOUNT_CURRENCY` is not handled by the risk helper's conversion
  table — fail closed.

## §D Event Reentrancy and Order Races

MQL5 event handlers run sequentially per chart, but multiple events
queue and interleave with broker responses:

- [ ] 🔴 Trade function shared by OnTick and OnTimer (or
  OnTradeTransaction) without a guard: timer fires while OnTick's
  order is in flight (`m_pending` flag exists?) — double orders.
  Review: any `trade.*` call must be gated by an in-flight flag or a
  single-owner design.
- [ ] 🔴 `OnTradeTransaction` assumes ordering: duplicate
  `TRADE_TRANSACTION_DEAL_ADD` notifications for the same deal (both
  DEAL_ADD and POSITION_ADD paths) → counters double-incremented.
  Dedup by deal ticket.
- [ ] 🟡 State desync window: order sent, connection lost before the
  reply — on reconnect the position exists but the EA's `m_pending`
  stayed true forever. Timeout on the in-flight flag.
- [ ] 🟡 Manual intervention: the trader closes the EA's position by
  hand (or from another device). Does OnTick detect the missing
  position (state resync each tick or on OnTradeTransaction), or does
  the state machine wait forever? On live accounts reviewed code
  usually says "wait forever".
- [ ] 🟡 `OnChartEvent` button handler mutating trading state while
  OnTick is mid-decision — single-threaded per chart makes this safe
  only if both paths go through the same state machine; verify no
  second copy of the logic.
- [ ] 🟢 Comment strings noting assumptions ("assumes single-threaded
  per chart — do not add OnTimer trading without a guard") score
  points with the reviewer; absent assumptions are undocumented risk.

## §E Long-Run Resource Growth

Backtests run days; live runs last months. Growth patterns that are
invisible in one and fatal in the other:

- [ ] 🔴 Unbounded arrays/lists appended in OnTick (signal history,
  MFE/MAE trackers, trade logs kept in memory): memory climbs until
  the terminal is killed. Cap with ring-buffer semantics or flush to
  file incrementally.
- [ ] 🔴 GUI objects created per tick / never cleaned —
  [gui-ux-review.md](gui-ux-review.md) §3/§4.
- [ ] 🟡 `HistorySelect(from, to)` with `from = 0` or "last N days"
  recomputed over a growing account history each tick — history
  parsing in OnTick gets slower every month. Cache the scan cursor
  (last processed ticket/time).
- [ ] 🟡 String concatenation in loops (`msg += line + "\n"`) inside
  per-bar/per-tick paths — O(n²) growth; build once, send once.
- [ ] 🟡 File handles: `FileOpen` per write without `FileClose`, or
  handles opened and never checked (`INVALID_HANDLE`) — write fails
  silently for weeks, then the audit trail is gone
  → [diagnostics-and-numeric.md](diagnostics-and-numeric.md).
- [ ] 🟡 `EventSetTimer` re-armed in a path that can re-run (not only
  OnInit) — duplicate timers, multiplied work. Pair with
  `EventKillTimer` in OnDeinit.
- [ ] 🟢 Journal growth: per-tick `Print` — the terminal journal is
  also a performance input on slow VPS disks; treat log volume as a
  budget.

## Review Method

For each handler (OnInit/OnTick/OnTimer/OnTrade/OnTradeTransaction/
OnChartEvent/OnDeinit) ask, in order:

1. What does it *assume* exists (position state, history depth,
   network, clock)? — each assumption needs a failure path.
2. What does it *remember* (globals, statics)? — each memory needs a
   restart story (§A).
3. What does it *accumulate* (arrays, strings, objects, handles,
   files)? — each accumulation needs a bound or a cleanup (§E).
4. When does it *fire more than once* (timers, trade transactions,
   chart events)? — each firing path needs dedup (§D).
