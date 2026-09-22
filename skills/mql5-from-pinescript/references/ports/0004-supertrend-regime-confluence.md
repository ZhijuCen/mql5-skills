# Port 0004 — SuperTrend Regime Confluence → SuperTrendRegimeConfluence-EA.mq5

| Field | Value |
|-------|-------|
| Pine source | `../../assets/pine-scripts/supertrend-regime-confluence.pine` (372 lines, v6, **MPL-2.0**, © DefinedEdge, `open_no_auth`) |
| Script id | `PUB;523784a4809e405eb1dd09d9eef7a3d3` (see `PROVENANCE.md`) |
| MQL5 port | `../../assets/mql5/SuperTrendRegimeConfluence-EA.mq5` (EA; shares `strategy-common.mqh`) |
| Recommended asset | **BTCUSDT · 4H** (author's default-settings/backtest block, Jan 2020–Sep 2026) → `../../assets/mql5-side/0004-supertrend-regime-confluence.ini` |
| Status | compiles clean (0 errors / 0 warnings, fresh `.ex5`); **not yet backtest-verified vs the Pine report** |

## License

Pine original is MPL-2.0; the EA keeps the attribution/license header
(file-level copyleft).

## Execution model (shared with ports 0005/0006)

Signal evaluated on the **closed bar** → market order sent on the
**next bar's first tick** (= TradingView broker-emulator next-bar-open
fill, `calc_on_every_tick=false`). Bracket attached on the fill tick;
`SYMBOL_TRADE_STOPS_LEVEL` clamped; gap-through the stop at fill →
immediate close (emulator fires the stop at the stop price). Warm-up:
closed-bar history is backfilled once (state only — **no trades before
the tester start**, D7), then one evaluation per newly closed bar.

## Faithful (1:1)

- **All36 Pine inputs** with identical defaults/groups (enums for the
  `input.string` option triples: sizing / SL mode / TP mode).
- **Regime engine**: ATR-ratio window (40) + manual Wilder ADX chain
  (`ta.dmi(14,14)` = RMA TR/+DM/−DM → DX → RMA), stateful regime
  sequence (volatile >1.4 / ranging ADX<20 & ratio<0.9 / trending),
  adaptive multiplier with the ×0.85 / ×(1+Δ·0.4) formulas and the
  [0.5×, 2×] clamp.
- **SuperTrend**: `stBand`/`stDir` var-sequence exactly (band ratchet,
  flip resets to the opposite base, `nz(stBand[1], base)` first-bar
  fallback, **na-band while ATR warms up** so no premature flips).
- **Five-factor score (0–100)**: volume surge ≥2.5/1.5/1.0 (20/14/8/3),
  displacement ATR units ≥1.5/0.8/0.3/>0 (25/18/12/5), EMA alignment
  +0.5 ATR distance (20/14/8/2 with the exact na-propagation fallback
  to 2), regime quality (15/8/3), prior band distance ≥2/1/0.5
  (20/14/8/3), `min(round(score),100)` ≥ MinSignalScore (65).
- **Gates**: skip-ranging, EMA-trend, volume>MA, long/short toggles,
  cooldown `(seq - lastEntryBar) > 5` (strict, like Pine), backtest
  window dates.
- **Sizing**: Risk% (exact money risk via tick value), Equity%
  (notional), Fixed units, `Cap at No Leverage` = 90% equity notional.
- **Risk**: SL modes ATR/6× / Percent 3% / SuperTrend-band (anchored to
  the SIGNAL bar's close — the Pine `strategy.exit` absolute levels),
  TP modes RR 2.5× / Percent / None, optional trailing with
  **parameters frozen at entry** (Pine passes them only inside the
  entry block), SuperTrend-flip exit only in SuperTrend-SL mode and
  evaluated **after** the entry blocks (Pine's source order).
- Score labels (`*72`/`o58`, bright ≥70 colors) as `OBJ_TEXT`.

## Decisions

- Manual state machines (EMA/RMA/ADX/SuperTrend sequences) instead of
  indicator handles: deterministic, order-exact, no handle lifecycle.
- `input source` reduced to a switch (Pine default hl2 kept).

## Deviations

- **D1** commission0.06% + slippage2 ticks not modeled (broker/tester
  dependent; adjust your broker's symbol commissions).
- **D2** TV "contract units = currency per price point" sizing → MQL5
  lots: Risk% exact via `tick_value`; Equity%/Fixed via
  `SYMBOL_TRADE_CONTRACT_SIZE`; the90% no-leverage cap preserved.
- **D3** visuals skipped: band glow, regime background, flip dots, EMA
  line, hidden data-window plots (score labels kept; no tooltips/size
  tiers on them).
- **D4** warm-up seeding: manual ADX seeds from bar0 (Pine's +DM/−DM
  are `na` there) — first ~`adxLen` bars of a backfill differ, effect
  decays geometrically; EMA/RMA are SMA-seeded like Pine.
- **D5** `input.source` limited to hl2/close.
- **D6** `Band Glow Effect` / `Regime Background` inputs kept as
  documented no-ops (parameter parity with the Pine dialog).
- **D7** cooldown/`lastEntryBar` state starts at the tester start
  (Pine would carry it from its series start); affects at most the
  first cooldown window.
- **D8** gap-through SL closes at market on the fill tick (emulator
  fills at the stop price); SL widened to `STOPS_LEVEL` when the
  distance is below the broker minimum (skill rule 16).

## Comparison — last ~90 trading days (run 2026-09-23)

Method: both sides restricted to the recent window
(**2026-06-16 → 2026-09-13**) per the reviewer's instruction — quote
quality is clean there. TV side = the Trades tab rows with entry ≥
cut (Net PnL column); MT5 side = headless tester on the same window
(**both sides History Quality 100%**).

| Metric | TV (BINANCE:BTCUSDT H4, trades #210-217) | MT5 (BTCUSD H4, same window, risk 6) |
|---|---|---|
| Trades (entries in window) | **8** (#210-217; #217 still open, floating counted) | **9** |
| Net profit | −17,566.65 USDT *(carried ~150k equity from prior years)* | −8.42 USD *(fresh 10k deposit)* |
| Profit factor | 0.40 | 0.99 |
| Win rate | 12.5% (1/8) | 33.3% (3/9) |
| Max DD (subset walk) | 17,566.65 USDT abs | 7.35% rel (735 USD) |
| History quality | (TV spot feed) | **100%** (534 H4 bars, no gaps) |

**Read:** trade COUNT matches within ±1 — the signal engine fires on
essentially the same bars once the feed is clean (this was the whole
point of the short window: the full-range run suffered from a 35%
quality / truncated-2021 history and produced garbage). PF/win-rate
diverge because n≈8 (one exit flips PF) and BTCUSDT spot vs BTCUSD
CFD bars differ at the margin; absolute PnL is not comparable at all
(TV starts the window with ~15× the equity, sizes compound accordingly).

Session queue: no un-retried `MARKET_CLOSED` shortfall visible in this
window (fills landed ≈ signals); the earlier full-window shortfall was
history-fragmentation dominated. Still worth a soak test (task9).

## Open verification tasks

1. Run `assets/mql5-side/0004-supertrend-regime-confluence.ini`
   (adjust `Symbol=` to the broker's crypto symbol) and compare the
   trade list against the TradingView strategy report over the same
   window — expect fill-engine divergence at gaps (D8) and the D1 costs.
2. Verify the score label values against Pine's `Signal Score` hidden
   plot on a few entries.
3. Exercise each sizing/SL/TP mode once (Risk%/Equity%/Fixed ×
   ATR/Percent/SuperTrend × RR/Percent/None).

## Related

- Uses `assets/mql5/strategy-common.mqh` (series backfill, smoothing
  states, bracket entry, risk lots) shared with ports 0005/0006.
- Indicator ports0001–0003 for the Pine→MQL5 mapping baseline.
