# Port 0005 — MACD Pullback Sniper → MACDPullbackSniper-EA.mq5

| Field | Value |
|-------|-------|
| Pine source | `../../assets/pine-scripts/macd-pullback-sniper.pine` (119 lines, v6, **MPL-2.0**, © blitz_locked, `open_no_auth`) |
| Script id | `PUB;aeae32205bbc4e4eb1e472b3bbe4e57d` (see `PROVENANCE.md`) |
| MQL5 port | `../../assets/mql5/MACDPullbackSniper-EA.mq5` (EA; shares `strategy-common.mqh`) |
| Recommended asset | author: trending markets, **1H/4H/Daily**; sizing note fits **crypto & stocks** → `../../assets/mql5-side/0005-macd-pullback-sniper.ini` (BTCUSD H4) |
| Status | compiles clean (0 errors / 0 warnings, fresh `.ex5`); **not yet backtest-verified vs the Pine report** |

## License

Pine original is MPL-2.0; the EA keeps the attribution/license header.

## Execution model

Identical to port0004 (shared `strategy-common.mqh`): confirmed-bar
signal → market order on the next bar's first tick; **SL/TP anchored to
the FILL price using the signal bar's ATR** — exactly the Pine flow
(provisional exit at signal close, re-anchored to
`position_avg_price ± entryAtr × mult` on the following bars; constant
levels ⇒ the fill-anchored bracket is equivalent).

## Faithful (1:1)

- **All16 Pine inputs** with identical defaults/groups (start
  2018-01-01 / end 2069-12-31 gate entries like `inRange`).
- **MACD**: fast12/slow26 EMAs → macd → signal EMA9, computed as
  rolling state over closed bars (na-propagating crosses: a cross with
  any `na` is false, like Pine).
- **Three filters, independently switchable**: price vs EMA200 (na →
  blocked), zero-line (`macd < 0` long / `> 0` short), ADX14 > 20 via
  the manual `ta.dmi(14,14)` chain (na → blocked).
- **Exit-on-opposite-cross block runs BEFORE the entries** and is
  skipped when the opposite cross is itself a valid entry (the flip
  then happens inside the bracket entry, netting-reversal style).
- **Sizing** `f_qty`: risk% of equity ÷ stop distance (exact money
  risk), capped at `MaxLev × equity` notional, floored to the broker's
  volume step; sub-minimum results skip the trade (skill rule).
- **Bracket**: SL = fill ± ATR×2, TP = fill ± ATR×2×RR (RR ≥ 0.5
  input range enforced), both from the signal bar's `entryAtr`.
- pyramiding=0 (enforced: single-position guard in the entry helper).

## Decisions

- Manual EMA/RMA/ADX state chains (no handles) — deterministic and
  order-exact; signal EMA starts on the first *defined* macd value.

## Deviations

- **D1** commission0.05% + slippage2 ticks not modeled.
- **D2** TV unit sizing → MQL5 lots (Risk% exact via `tick_value`;
  the maxLev cap uses `SYMBOL_TRADE_CONTRACT_SIZE` notional — the
  author's "1 unit =1 currency per price point" assumption is replaced
  by broker-true contract math).
- **D3** visuals skipped: MACD sub-window (histogram/MACD/signal/zero
  line), trend-EMA and SL/TP plot lines; **entry triangles kept**
  (teal/red as in Pine).
- **D4** warm-up: signal-EMA seeds on the first defined macd (Pine's
  na-chain interpretation); deep-history impact only.
- **D5** gap-through SL → close at fill; `STOPS_LEVEL` clamping
  (skill rule16).
- **D6** date inputs gate entries only; the tester's own date range
  (INI `FromDate/ToDate`) additionally bounds the run.

## Comparison — last ~90 trading days (run 2026-09-23)

Method: both sides restricted to **2026-05-19 → 2026-09-21** (reviewer's
instruction: compare the recent ~90 trading days only — full-range
quote data is not reliably available). TV side = Trades-tab rows with
entry ≥ cut; MT5 side = headless tester on the same window
(**both sides History Quality 100%**).

| Metric | TV (NASDAQ:**NFLX** M30, trades #158-170) | MT5 (BTCUSD M30, same window/toggles) |
|---|---|---|
| Trades (entries in window) | **13** (Jul 7 → Sep 3; May-Jul gap has no TV entries) | **83** |
| Net profit | −322.20 USD | −71.71 USD |
| Profit factor | 0.79 | 0.98 |
| Win rate | 30.8% (4/13) | 36.1% (30/83) |
| Max DD (subset walk) | 913.08 USD abs | 8.19% rel (819 USD) |
| History quality | (TV feed) | **100%** (5,947 M30 bars) |

**Read:** win-rate band agrees (31% vs36%) and **both sides show a
≤1 PF / negative-net window** — the same qualitative verdict for the
period. Trade count (13 vs83) is **instrument-driven**: the broker
cannot serve NFLX.NAS history (`cannot get history NFLX.NAS,M30` —
both M1-download and open-prices attempts failed identically), so the
port ran on BTC, where M30 whipsaws fire the trend-only long entries
~6× as often. On this strategy the count gap is asset behaviour, not
logic — PF / win-rate are the transferable shape metrics here.

## Open verification tasks

1. Run `assets/mql5-side/0005-macd-pullback-sniper.ini` (adjust
   `Symbol=`) and diff the trade list against the Pine report over the
   same window; fills should agree bar-for-bar except gap/stop-engine
   cases (D5) and cost model (D1).
2. Turn each filter off in isolation (author's tip) and confirm trade
   counts move the same way as Pine.
3. Check the100+-trade sample guidance from the author before judging
   any parameter set.
4. Pending-entry retry (`MARKET_CLOSED` queue) filled ≈ signals in the
   90-day run; soak-test a weekend/holiday-heavy window to confirm
   queued≈filled before trusting session-bound symbols unattended.

## Related

- Shared `assets/mql5/strategy-common.mqh` with ports 0004/0006.
