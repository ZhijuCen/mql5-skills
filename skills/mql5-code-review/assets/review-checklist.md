# MQL5 Code Review — Quick Checklist

Lightweight pass for small diffs / routine reviews. For comprehensive
reviews use the full 4-phase process in [SKILL.md](../SKILL.md) §4.
Severity: 🔴 must fix, 🟡 should fix, 🟢 optional.

## Pre-Review (2 min)

- [ ] Program type and origin identified (own / third-party / article)
- [ ] Hedging or netting? Single- or multi-symbol?
- [ ] What state must survive a restart?
- [ ] Diff size sane (< 400 lines; slice larger)
- [ ] Scanner run: `mql5_redflags.py scan FILE.mq5`

## Trading Logic (10 min)

- [ ] 🔴 Every `trade.*` order call → `ResultRetcode()` check +
  consistent state on failure
- [ ] 🔴 Magic set in OnInit; all position/order scans filtered by
  magic + symbol
- [ ] 🔴 Hedging/netting branches match the account mode
- [ ] 🟡 SL/TP normalized; distances ≥ stops level; filling mode from
  symbol spec
- [ ] 🟡 Partial close ≥ VOLUME_MIN; breakeven includes commission/swap
- [ ] 🟡 Pending orders: cancel / re-arm / dedup paths exist

## Risk & Sizing (5 min)

- [ ] 🔴 Formula (A/B/C) identified and applied consistently
- [ ] 🔴 Profit currency ≠ account currency → FX conversion + failure
  path fails closed
- [ ] 🔴 Lots clamped to min/max, quantized to step; below-min skips
  the trade (never clamps up)
- [ ] 🟡 Final loss verified with `OrderCalcProfit` before open
- [ ] 🟡 Exposure cap for multi-position systems

## Indicators & Time (5 min)

- [ ] 🔴 Handles checked for `INVALID_HANDLE`; released in OnDeinit
- [ ] 🔴 `Copy*` return compared to exact requested count; failure
  path skips trading
- [ ] 🔴 Series direction (`ArraySetAsSeries`) explicit and correct
- [ ] 🔴 Higher-TF reads use closed bars (index 1); new-bar gate
  present via `iTime()` compare
- [ ] 🟡 Timezone: server vs local not mixed; session filters on
  server time

## Failure Modes (5 min)

- [ ] 🔴 Re-adoption path exists for positions/pending after restart
- [ ] 🔴 Trade functions reentrancy-guarded (OnTick/OnTimer/
  OnTradeTransaction)
- [ ] 🟡 Manual-close / reconnect desync resyncs state
- [ ] 🟡 Weekend gap / rollover spread policy documented or guarded

## Performance (3 min)

- [ ] OnTick statement #1 is a cheap gate
- [ ] No per-tick `CopyRates`/`CopyBuffer`/history scans/prints
- [ ] Object updates change-driven; batched single `ChartRedraw`
- [ ] Arrays/strings bounded; cleanup present (files, timers, handles)

## Diagnosability (3 min)

- [ ] 🟡 No swallowed `Copy*`/`FileOpen`/retcode returns
- [ ] 🟡 Decision-path exits log one context line (symbol, magic,
  ticket, prices, reason)
- [ ] 🟡 OnInit validates inputs → `INIT_PARAMETERS_INCORRECT`
- [ ] 🟡 No `==` on doubles; NaN/Inf sources guarded

## GUI / UX (3 min)

- [ ] Panel width budgeted for worst-case text; truncation present
- [ ] Corner-anchored pixel layout; theme-aware or documented colors
- [ ] OnDeinit prefix-scoped cleanup exists; names instance-unique
- [ ] 🔴 Notifications (Alert/push/e-mail): edge-triggered, cooldown,
  daily budget; capability pre-checked

## Tester↔Live (2 min)

- [ ] 🔴 `MQL_TESTER` branches don't change signal logic
- [ ] 🔴 No live-only data source silently empty in the tester
- [ ] 🟡 Edge > spread + slippage + latency budget; expectation notes
  written

## Readability (2 min)

- [ ] 🟢 Naming per `../mql5/references/quick-ref-code-style.md`
  (`C` classes, `m_` members, PascalCase methods)
- [ ] 🟢 No dead code / TODO blocks / magic numbers
- [ ] 🟢 OnTick decomposed; no copy-paste blocks

---

## Decision Matrix

| Situation | Verdict |
|-----------|---------|
| Any 🔴 | 🔄 Request Changes |
| Only 🟡 + 🟢 | 💬 Comment (merge-able, list 🟡 for next iteration) |
| Only 🟢 / notes | ✅ Approve |
| Third-party code with unexplainable DLL/WebRequest | 🔄 refuse to deploy |
| GUI-only 🟡 | ✅ Approve with note (trading path unaffected) |
