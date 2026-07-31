# Quick Ref — Tester Deal-Level Debugging Methodology

Companion to `SKILL.md` §6 "Report Analysis — Interpreting Tester Results".
When summary metrics reveal problems, drill into individual trades.

## Scripts entry points

- `scripts/parse_tester_report.py analyze REPORT.html` — automated
  analysis: pairs deals, computes risk per trade, monthly breakdown,
  re-entry detection, streak analysis.
- `scripts/parse_tester_report.py report REPORT.html --json` — raw
  parsed `deals[]` and trades JSON for ad-hoc Python queries.

## 6-step methodology

### 1. Pair deals

Iterate deals, pair each `direction=in` with the next `direction=out`
to form a complete trade. For each trade capture:

- `entry_time`, `entry_price`, `entry_deal_id`
- `exit_time`, `exit_price`, `exit_reason` (from `comment`)
- `net_pnl` (price P&L + commission + swap)
- `lot` (entry lot)
- `magic`, `sl_distance_points` (from entry to SL)

### 2. Risk check

For each trade compute `|net_loss| / deposit × 100` and verify it is
within budget. Flag any trade exceeding **2× target risk**. Common
causes:

- `rawLots < minLot` → clamp inflation (see §5 in SKILL.md)
- `sl_distance_points > SYMBOL_TRADE_STOPS_LEVEL * point` ignored
- Position-sizing loop skipped during news volatility spikes

### 3. SL distance analysis

For SL hits, compute `|entry - exit| / point` to get SL distance in
points. Two failure modes:

- SL too close → oversized lots hitting minLot clamp
- SL too far → oversized risk per trade

Plot a histogram of SL distances; a flat distribution = the EA is
random on SL selection.

### 4. Re-entry (implicit martingale) detection

Sort trades by entry time. If an SL hit is immediately followed by a
trade at the same entry price with **larger lot**, the EA is doing
implicit martingale on the same setup. Look for an `InpRecoveryMode`
or grid-state update that you may have missed in the rollback.

### 5. Volume pattern

Plot lot sizes across trades. Consistent `0.01` lots regardless of SL
distance = `minLot` clamp bug. Decay from a larger seed = manual
recovery-mode in effect (verify it should be there).

### 6. Monthly breakdown

Group trades by calendar month, compute win rate and net P&L per
month. Identify the worst months and correlate with:

- Known market regimes (flash crashes, central-bank meetings)
- News blackout windows
- Broker server event log (data quality dips)

A blank month with `Trades=0` is fine if it's adjacent to history
gaps; otherwise check that the EA didn't crash (`Logs/MQL5/...`).
