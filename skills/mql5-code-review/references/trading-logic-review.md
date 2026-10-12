# Trading Logic Review Guide

Static review of order/position flow and money management in MQL5 EAs.
Companion to `../mql5/SKILL.md` §2/§5 (the "why"); this file is the
reviewer's checklist with ❌/✅ pairs. Severity: 🔴 money/execution,
🟡 degraded behaviour, 🟢 readability.

## Table of Contents

- [Order Call Discipline](#order-call-discipline)
- [Magic and Ownership](#magic-and-ownership)
- [Hedging vs Netting Branches](#hedging-vs-netting-branches)
- [Pending Order Lifecycle](#pending-order-lifecycle)
- [Position Lifecycle: Partial Close and Modify](#position-lifecycle-partial-close-and-modify)
- [Risk Formulas](#risk-formulas)
- [Money Management Checks](#money-management-checks)
- [Filling, Deviation, Retcode Table](#filling-deviation-retcode-table)
- [Review Checklist](#review-checklist)

---

## Order Call Discipline

### Every order call has an explicit retcode check

`CTrade` returning `true` only means the request was sent. The only
success signal is `ResultRetcode() == TRADE_RETCODE_DONE` (or
`TRADE_RETCODE_PLACED` for pending orders).

```mql5
// ❌ Blocking: believed-open position does not exist after rejection
trade.Buy(lots, _Symbol, ask, sl, tp, "signal");

// ❌ Blocking: `if(!ok)` alone is not enough — ok==true with retcode
// TRADE_RETCODE_REJECT is possible
if(!trade.Buy(lots, _Symbol, ask, sl, tp, "signal"))
    Print("buy failed");

// ✅ Check retcode, log context, and let the caller reconcile state
if(!trade.Buy(lots, _Symbol, ask, sl, tp, "signal") ||
   trade.ResultRetcode() != TRADE_RETCODE_DONE)
{
    PrintFormat("Buy failed: retcode=%u (%s) price=%.5f lots=%.2f",
                trade.ResultRetcode(),
                trade.ResultRetcodeDescription(),
                ask, lots);
    return false;
}
```

Reviewer questions:
- Does the failure path leave internal state consistent (pending flag
  cleared, retry counter incremented), or does it just `return`?
- Is `ResultDeal()`/`ResultOrder()` logged for traceability?

### State reconciliation after a call

```mql5
// ❌ Blocking: EA state updated before broker confirms
m_pending = true;
m_lastTicket = trade.ResultDeal();   // ResultDeal is 0 at rejection
if(trade.ResultRetcode() != TRADE_RETCODE_DONE) return;

// ✅ Update state only from the confirmed result
if(!trade.Buy(...) || trade.ResultRetcode() != TRADE_RETCODE_DONE) {
    m_pending = false;
    return false;
}
m_lastTicket = trade.ResultOrder();
m_pending = true;
```

## Magic and Ownership

```mql5
// ❌ Blocking: magic set in OnTick path, orders before it carry magic=0
void OnTick() {
    trade.SetExpertMagicNumber(EA_MAGIC);   // every tick, redundant
    // ... first-ever tick raced here on some builds
}

// ✅ Set once in OnInit, before any order
int OnInit() {
    trade.SetExpertMagicNumber(EA_MAGIC);
    trade.SetTypeFillingBySymbol(_Symbol);
    return INIT_SUCCEEDED;
}
```

Reviewer questions:
- Does every position/pending scan filter by `POSITION_MAGIC` /
  `ORDER_MAGIC`? An EA without ownership filter will manage — and
  close — positions of another EA or the manual trader
  (🔴 on live accounts shared with other EAs).
- Comment strings used as ownership filter (`"EA Signal"` in comment)?
  Comments are truncated by brokers and forgeable — magic only.

## Hedging vs Netting Branches

```mql5
// ❌ Blocking on netting: two positions assumed, broker has one
int CountPositions() {
    int n = 0;
    for(int i = 0; i < PositionsTotal(); i++) {
        if(PositionGetSymbol(i) == _Symbol &&
           PositionGetInteger(POSITION_MAGIC) == EA_MAGIC)
            n++;
    }
    return n;          // always 1 on netting accounts
}

// ✅ Detect mode once, branch the logic
bool hedging = ((ENUM_ACCOUNT_MARGIN_MODE)
    AccountInfoInteger(ACCOUNT_MARGIN_MODE)
    == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
```

Reviewer checklist per branch:
- **Hedging**: iterate all positions; "close" = loop with
  `PositionCloseTicket`; "reverse" = close all then open.
- **Netting**: `PositionSelect(_Symbol)`; "close" =
  `PositionClose(_Symbol)`; "reverse" = `trade.Buy` flips direction
  automatically — do NOT also call close first (double commission).
- Where is the mode detected — OnInit (static, correct) or per tick
  (wasteful)? Account mode can change only after reconnect with a
  different account: per-tick detection is cargo cult.

## Pending Order Lifecycle

- [ ] 🔴 Stale pending orders: EA places BuyStop, price moves away,
  order stays. Does anything cancel it? A grid of 20 stale stops all
  triggering in a spike = classic blow-up.
- [ ] 🔴 Re-arm logic: after a stop is triggered or cancelled, is it
  re-placed at the new price, or does the EA wait forever?
- [ ] 🟡 `OrdersTotal()` scan filters by `ORDER_MAGIC` and
  `ORDER_SYMBOL` before `OrderModify`/`OrderDelete`?
- [ ] 🟡 Duplicate placement: pending flag set before confirmation
  (see state reconciliation above) → second tick places a second stop.
  Check for `PositionsTotal()`/`OrdersTotal()` dedup guard before
  placing.

```mql5
// ✅ Idempotent placement: at most one of my stops of this type
bool HasMyStop(ENUM_ORDER_TYPE t) {
    for(int i = OrdersTotal()-1; i >= 0; i--) {
        if(!OrderGetSymbol(i) == _Symbol) continue;    // see note
        if(OrderGetInteger(ORDER_MAGIC) != EA_MAGIC)   continue;
        if(OrderGetInteger(ORDER_TYPE)  == t)          return true;
    }
    return false;
}
```

> Note for the reviewer: `OrderGetSymbol(i) == _Symbol` — check the
> comparison is actually written correctly (a `!` applied to the wrong
> operand here inverts the whole filter; the scanner's `double-equality`
> rule does not catch boolean inversions — read these loops carefully).

## Position Lifecycle: Partial Close and Modify

- [ ] 🔴 `PositionModify` SL/TP without re-checking stops level after
  the modify (level can have changed with broker settings intraday).
- [ ] 🔴 Trailing stop logic modifies every tick with no minimum step
  (`SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL)` respected?)
  — server load + retcode spam + log flood
  → [performance-review.md](performance-review.md).
- [ ] 🟡 Partial close: volume clamped to `VOLUME_MIN` —
  `PositionClosePartial(ticket, minVolume)` on a min-lot position is a
  full close. Guard: `currentVolume - step >= VOLUME_MIN`.
- [ ] 🟡 Breakeven move: SL moved to open price **without commission
  and swap** → every BE trade closes at net loss. Add offset:
  `open ± commissionPerLot*lots/tickValue`.
- [ ] 🟡 Modify order after it is already filled: no re-check that the
  order still exists (`OrderGetTicket` failure) → modify hits a reused
  ticket number.

## Risk Formulas

Review which of the three formulas is used and whether it is applied
consistently (mixing B and C in one EA is a red flag).

| Dir | Inputs | Output | Typical use |
|-----|--------|--------|-------------|
| A | SL distance in points | SL price | Fixed-structure strategies |
| B | balance + risk% + fixed lots | SL price | Lot-locked systems |
| C | balance + risk% + SL price | **lot size** | Structure-based entries |

```mql5
// ❌ Blocking: risk amount computed in profit currency, compared to
// account currency — USDJPY account(USD), risk 100x too small
double riskMoney = balance * RiskPercent / 100.0;
double loss = points * SymbolInfoDouble(sym, SYMBOL_TRADE_TICK_VALUE) * lots;
// ❌ Blocking: PointValue conflated with TICK_VALUE
double lossPerPoint = SymbolInfoDouble(sym, SYMBOL_TRADE_TICK_VALUE);
```

```mql5
// ✅ Use the shared helpers; they handle currency conversion and
// calc-mode differences (Forex/CFD/Futures)
#include <risk-helpers.mqh>
double lots = CalcLotsFromSL(_Symbol, balance, riskPct, slPrice, stopPrice);
```

Reviewer questions (all from `../mql5/SKILL.md` §5):
1. Which formula? Is the same formula used for entry, add-on, and
   recovery sizing?
2. Profit currency ≠ account currency → live FX conversion present
   (`FindFXRate`-style)? On which rate source — and what happens when
   the rate fetch fails (fail closed, skip trade — never "assume 1")?
3. `SYMBOL_TRADE_CALC_MODE` handled for Futures
   (`TickValue/TickSize`) vs Forex/CFD (`Δprice × ContractSize`)?
4. Is the **final** loss verified with `OrderCalcProfit` before open,
   within the risk budget? (Formula-then-verify pattern is mandatory.)
5. `NormalizeDouble` only at the final price, not in the middle of the
   cascade?

## Money Management Checks

```mql5
// ❌ Blocking: raw lots reach the broker
double lots = riskMoney / slValuePerLot;

// ✅ Clamp + quantize + reject
double lots = MathFloor(rawLots / step) * step;
if(lots < SymbolInfoDouble(sym, SYMBOL_VOLUME_MIN)) {
    PrintFormat("lots %.2f < min — skip trade", lots);
    return false;    // skipping, never clamping up to min
}
lots = MathMin(lots, SymbolInfoDouble(sym, SYMBOL_VOLUME_MAX));
```

Reviewer checklist:
- [ ] 🔴 Clamping **up** to `VOLUME_MIN` when raw < min → real risk
  exceeds budget; must skip the trade.
- [ ] 🔴 `MathFloor` residual: actual lots below planned → recompute
  expected loss with the final lots, re-verify budget.
- [ ] 🟡 Max concurrent exposure guard (sum of open risk ≤ N%)?
  Grid EAs without an exposure cap fail exactly when correlated
  entries cluster.
- [ ] 🟡 Balance-vs-equity: sizing on `ACCOUNT_BALANCE` during a
  floating-drawdown spiral sizes up a losing account. Intentional?
  Documented?
- [ ] 🟡 Stop-out margin pre-check: `OrderCalcMargin` before the
  order; margin call distance respected?

## Filling, Deviation, Retcode Table

Always present:

| Setting | Review point |
|---------|--------------|
| Filling | `SetTypeFillingBySymbol()` or explicit `SYMBOL_FILLING_MODE` bitmask check — never a hardcoded enum |
| Deviation | `SetDeviationInPoints` value sane for the symbol (points, not pips)? On 5-digit symbols `10` = 1 pip |
| Retcodes | Failure branch handles at least: `INVALID_VOLUME`, `INVALID_STOPS`, `INVALID_FILL`, `NO_MONEY`, `REJECT`, `REQUOTE`, `OFF_QUOTES` |

- [ ] 🔴 `TRADE_RETCODE_NO_MONEY` not distinguished from generic
  failure — margin exhaustion deserves an alert (once per bar), not a
  journal line.
- [ ] 🟡 Requote/off-quotes: retry with refreshed price, bounded
  retries (e.g. 3), then give up with alarm. Infinite retry loops =
  frozen EA.

## Review Checklist

Compact pass for the line-by-line phase:

1. Every `trade.*` order call → retcode check + state reconciliation
2. Magic set in OnInit, all scans filtered by magic + symbol
3. Hedging/netting branch matches the account; reverse logic correct
4. Pending lifecycle: cancel, re-arm, dedup
5. Partial close ≥ VOLUME_MIN; BE includes costs
6. Formula A/B/C identified, consistent, currency-converted
7. Final loss verified with `OrderCalcProfit`
8. Lots clamped (never up), quantized, skipped when below min
9. Exposure cap present for multi-position systems
10. Retcode failure branches distinguish no-money / requote / invalid
