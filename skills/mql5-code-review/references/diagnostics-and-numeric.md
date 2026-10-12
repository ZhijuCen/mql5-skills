# Diagnosability, Numeric Precision, and Security Boundaries

Three review lenses that share a theme: **problems that stay invisible
until they are expensive** — silent failure paths (§F), quietly wrong
numbers (§G), and permission/robustness boundaries (§H). Severity: 🔴
silent wrong behaviour, 🟡 diagnosability/degradation, 🟢 cleanup.

## Table of Contents

- [§F Diagnosability](#f-diagnosability)
- [§G Numeric Precision](#g-numeric-precision)
- [§H Security and Robustness Boundaries](#h-security-and-robustness-boundaries)

---

## §F Diagnosability

The live incident review starts with the journal. If the code does not
record what happened, the incident is unresolvable and will recur.

### Swallowed return values

```mql5
// ❌ Blocking: count/-1 ignored — buffer holds previous values,
// trading continues on stale data, no trace
CopyBuffer(handle, 0, 0, 3, buf);
CopyRates(_Symbol, _Period, 0, 100, rates);

// ❌ Blocking: checked once, then the failure path is a comment
if(CopyBuffer(handle, 0, 0, 3, buf) != 3)
    /* skip */;

// ✅ Exact check, logged with context, control actually leaves
if(CopyBuffer(handle, 0, 0, 3, buf) != 3) {
    PrintFormat("CopyBuffer(h=%d) got!=3 err=%d — skip bar",
                handle, GetLastError());
    return;
}
```

Checklist — grep-level patterns:
- [ ] 🔴 `CopyBuffer/CopyRates/CopyTime/CopyOpen/...` called as a bare
  statement (return discarded)
- [ ] 🔴 `FileOpen` result compared to `INVALID_HANDLE` — absent =
  every later read/write fails, possibly silently
- [ ] 🔴 `GlobalVariableSet/Get`, `ChartGetInteger`,
  `TerminalInfoInteger` results ignored where the failure changes the
  control flow
- [ ] 🟡 `ArraySetAsSeries` / `ArrayResize` return ignored (usually
  fine, but `ArrayResize` failure = undersized array = out-of-range
  at runtime)
- [ ] 🟡 `MathIsValidNumber` absent after any `MathSqrt/MathLog/
  division` feeding a price or volume (see §G)

### Silent failure paths

- [ ] 🔴 `if(!ok) return;` with no log — the trade disappears from
  reality and from history. Every `return` inside a *decision* path
  deserves one line of context.
- [ ] 🔴 Retcode failures logged without the retcode
  (`Print("open failed")` instead of retcode + description) —
  diagnosis requires the code.
- [ ] 🟡 Empty catch-equivalents: `if(err) {}` — MQL5 has no
  exceptions, so the empty branch *is* the anti-pattern; grep `{}\s*$`
  near error variables.

### Log context quality

A journal line is only useful with the **five Ws**:

```mql5
// ❌ "where does this come from?"
Print("SL moved");

// ✅ context-complete
PrintFormat("%s magic=%d ticket=%d %.5f->%.5f reason=BE",
            _Symbol, EA_MAGIC, ticket, oldSl, newSl);
```

- [ ] 🟡 Per-action logs carry: symbol, magic, ticket, prices, and a
  reason tag. Reviews: sample 3 log lines — could *you* reconstruct
  the event offline?
- [ ] 🟡 Log volume: per-tick prints drown the signal —
  [performance-review.md](performance-review.md) for the throttle
  patterns; alert-worthy events must also respect once-per-signal
  throttling → [gui-ux-review.md](gui-ux-review.md) §5.
- [ ] 🟢 Consistent prefix (`[EAName]`) so multi-EA accounts can be
  filtered.

### Input validation — fail fast at OnInit

```mql5
// ❌ Error surfaces at the first signal, days later, as
// TRADE_RETCODE_INVALID_STOPS with no hint about the input
int OnInit() { return INIT_SUCCEEDED; }

// ✅ Validate the *contract* of the inputs at startup
int OnInit() {
    if(RiskPercent <= 0 || RiskPercent > 5.0) {
        PrintFormat("RiskPercent=%.2f out of (0, 5] — refuse to run", RiskPercent);
        return INIT_PARAMETERS_INCORRECT;
    }
    if(InpSLPoints < (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL)) {
        PrintFormat("InpSLPoints=%d < stops_level=%d — refuse to run",
                    InpSLPoints,
                    (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL));
        return INIT_PARAMETERS_INCORRECT;
    }
    return INIT_SUCCEEDED;
}
```

- [ ] 🟡 OnInit validates: risk range, SL vs stops level, lot bounds,
  timeframe enum, handle creation success (`INVALID_HANDLE` →
  `INIT_FAILED`), non-empty symbol. Return
  `INIT_PARAMETERS_INCORRECT` — it names the problem class.
- [ ] 🟢 Validation messages quote the offending value — a message
  without the value requires a second run to diagnose.

## §G Numeric Precision

### Double equality and comparison

```mql5
// ❌ Blocking: exact equality on 5-digit prices — branch is dead
if(bid == m_entryPrice) Close();

// ✅ Tolerance-based comparison
if(MathAbs(bid - m_entryPrice) <= _Point) Close();
```

- [ ] 🔴 `==` / `!=` on any price-like quantity (bid/ask/SL/TP/entry/
  indicator values). Tolerance = 1 point or a stated epsilon.
- [ ] 🟡 `==` on computed doubles (ratios, averages) even when inputs
  are integral — division already destroyed integrality.
- [ ] 🟢 `double` used as a *loop counter* or compared to an integer
  loop bound — use `int`/`long`.

### NaN and Infinity propagation

- [ ] 🔴 `MathSqrt(negative)`, `MathLog(<=0)`, `0.0/0.0` (empty bars,
  zero spread, zero volume inputs) → NaN. NaN fails *every* `<`/`>`
  comparison, so all guards pass it through to `PositionOpen`, which
  rejects with a confusing `INVALID_VOLUME`. Guard the *source* and
  verify the result:

```mql5
double atr = iATR(_Symbol, _Period, 14, 0);   // may be 0 pre-data
double riskPerLot = atr * tickValue / point;   // 0 → NaN downstream
if(atr <= 0. || !MathIsValidNumber(riskPerLot) || riskPerLot <= 0.) {
    Print("sizing inputs invalid — skip trade");
    return;
}
```

- [ ] 🔴 Zero-division candidates reviewed: dividing by spread,
  contract size, tick size, bar count, position volume (empty
  position during close-partial races). Integer division where
  fractional was intended (`int lots = risk / value;`).
- [ ] 🟡 Infinity: division by a tiny (not zero) number — result
  overflows to `INF`, same downstream effect as NaN;
  `MathIsValidNumber` covers both.

### First-tick zero prices

- [ ] 🔴 Any computation on `SymbolInfoDouble(SYMBOL_BID/ASK)` before
  `SymbolInfoTick` success — bid=0 before the first server tick;
  SL/TP at 0 or negative passes arithmetic but dies at the broker.
- [ ] 🟡 `iClose/iOpen` of the forming bar used as "current price" —
  it lags the tick by up to a full bar on quiet symbols.

### Rounding discipline

- [ ] 🟡 `NormalizeDouble` at the **final price** only, to
  `SYMBOL_DIGITS` — mid-cascade normalization (risk chain, averaged
  entries) accumulates error and hides the raw value from review.
- [ ] 🟡 Lot quantization: `MathFloor(lots/step)*step` then re-verify
  actual loss with `OrderCalcProfit` on the *final* lots
  → [trading-logic-review.md](trading-logic-review.md).
- [ ] 🟢 `NormalizeDouble` on a *display* string is wrong tool —
  formatting is `DoubleToString(value, digits)`; the two are
  conflated regularly.

## §H Security and Robustness Boundaries

Personal EAs run with the user's terminal permissions — the boundary
review is lightweight but not optional, because a reviewed third-party
EA is code executing with those permissions.

- [ ] 🟡 `#import "something.dll"` — native code in the terminal
  process. What is it, where does the binary come from, is it needed?
  Reviewer: request justification; for third-party code without an
  explainable need, escalate to 🔴 and refuse to deploy.
- [ ] 🟡 `WebRequest` — the URL must be in the terminal's *Tools →
  Options → Expert Advisors* whitelist, and the call blocks the event
  thread while pending (timeout up to seconds). Check:
  - [ ] failure path handles `4014` (URL not allowed) — not silent
  - [ ] called from a timer/slow path, never per tick
  - [ ] response parsing is defensive (size cap, format check — a
        server change must not feed garbage into trading logic)
- [ ] 🟡 File I/O boundaries: `FileOpen` paths — `FILE_COMMON` vs
  per-terminal; path traversal from a config value (an EA reading a
  symbol name into a path is a stretch vector in shared-host setups).
  Writes append-bounded (`FILE_SIZE_LIMIT`-style handling) — an
  unbounded log file on a small VPS disk is a real outage.
- [ ] 🟡 Config/INI parsing robustness: broker renames a symbol or a
  settings file loses a key → does the parser crash (uninitialized
  string), silently use a default, or refuse to start? "Refuse to
  start" is the correct contract for trading parameters; verify the
  parse failures return `INIT_PARAMETERS_INCORRECT`.
- [ ] 🟢 Sensitive data: account password must never appear in source
  (auto-login EAs); API keys in source = rotate and move to a config
  file with restricted permissions.

## Review Checklist (§F–§H compact pass)

1. Every `Copy*`/`FileOpen`/`GlobalVariable*` return consumed
2. Every decision-path `return` logs one context line
3. Retcode/err codes logged with numbers + descriptions
4. OnInit validates all inputs; `INIT_PARAMETERS_INCORRECT` on breach
5. No `==` on doubles; tolerances stated
6. NaN/Inf sources guarded; `MathIsValidNumber` at sizing boundaries
7. No first-tick zero-price use
8. `NormalizeDouble` only at final prices
9. DLL imports and WebRequest justified, whitelisted, off the tick path
10. Config parsing fails closed
