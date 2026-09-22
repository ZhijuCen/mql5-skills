# Port 0006 — Aurora KAMA Trend → AuroraKamaTrend-EA.mq5

| Field | Value |
|-------|-------|
| Pine source | `../../assets/pine-scripts/aurora-kama.pine` (179 lines, v6, **no license declared** — TV open-source access only, © blitz_locked as author, `open_no_auth`) |
| Script id | `PUB;426d44d5850b4168b7bfb48e03e8e0d6` (see `PROVENANCE.md`) |
| MQL5 port | `../../assets/mql5/AuroraKamaTrend-EA.mq5` (EA; shares `strategy-common.mqh`) |
| Recommended asset | author: **DAILY bars — BTCUSD, ES1!, SPY, QQQ** → `../../assets/mql5-side/0006-aurora-kama.ini` (BTCUSD D1) |
| Status | compiles clean (0 errors / 0 warnings, fresh `.ex5`); **not yet backtest-verified vs the Pine report** |

## License

The Pine source carries **no license header** (only TV open-source
access). The port credits blitz_locked and claims **no license**; it is
a personal-research reproduction — do not redistribute without the
author's permission (recorded in `PROVENANCE.md`).

## Execution model

Identical to ports0004/0005 (shared `strategy-common.mqh`):
confirmed-bar signal → market order on the next bar's first tick; the
fixed-% stop is then **re-anchored to the real fill price**
(`position_avg_price × stopPct/100` — exactly Pine's usage of
`strategy.position_avg_price`).

## Faithful (1:1)

- **All13 Pine inputs** with identical defaults/groups (plus
  `InpQtyPct = 25` exposing Pine's `default_qty_value`).
- **KAMA recursion verbatim**: ER = change/volatility over the10-bar
  window, `sc = (ER·(fastSC−slowSC)+slowSC)²` with fast=2/slow=30,
  first bar seeds with the source, and — matching Pine's `na`-ternary
  fallback — **before the ER window fills, ER falls back to0** (tiny
  `slowSC²` creep) rather than stalling.
- **Persistence gates**: KAMA strictly rising/falling over
  risingLen/fallingLen bars (see D4 for the length interpretation),
  SMA200 trend filter (na → blocked), direction toggle
  Long/Short/Both, cooldown `seq − lastTradeBar ≥ 5` bars with the
  Pine-`na` first-trade exemption.
- **Entries**: from flat or after closing the opposite side
  (`position_size <= 0 / >= 0` gates → single-position flips).
- **Risk**: fixed % stop (optional), delayed trailing stop — armed
  only after `trailDelay` bars in the position, activates when the
  extreme since entry reaches `trailPct%` from the fill, then trails
  `trailPct%` behind that extreme; evaluated **on each closed bar**
  (Pine `calc_on_order_fills=false` semantics); union with the fixed
  stop = whichever is more favourable (ratchet, never loosened).
- **Sizing**: `percent_of_equity`25% notional (D6).

## Decisions

- Exit markers: position observed flat at a new bar → gray circle at
  that bar's close (see D2/D7).
- Trailing extremes use closed-bar highs/lows since the fill bar —
  matches bar-based evaluation; the broker still enforces the
  intrabar stop itself.

## Deviations

- **D0** no license in the original source (see License above).
- **D1** commission0.05% + slippage1 tick not modeled.
- **D2** visuals skipped: KAMA colored line, KAMA/close glow fills,
  four-layer SMA glow; **entry triangles kept**, exit `X` glyphs →
  gray circles (only verified Wingdings codes are used — see
  pine-to-mql5 §2).
- **D3** Pine `pyramiding=1` is moot: its own `position_size` gates
  make it single-position; the EA enforces one position explicitly.
- **D4** `ta.rising/falling(x, len)` interpreted as **len consecutive
  strict comparisons** (len+1 monotonic values); if Pine's semantics
  differ by one bar, entry timing shifts by ≤1 bar — flagged for the
  parity check below.
- **D5** `input.source` reduced to close/hl2/hlc3 (default close exact).
- **D6** `default_qty_value=25` exposed as `InpQtyPct`; notional
  sizing via `SYMBOL_TRADE_CONTRACT_SIZE` (TV unit assumption →
  broker-true contract math).
- **D7** the exit marker lands on the bar where flat is *observed* (the
  bar after the exit fill) rather than Pine's exact
  `position_size[1] != 0` transition bar — marker placement only,
  no trading impact.

## Comparison — last ~90 trading days (run 2026-09-23) — CURRENT

Method: both sides restricted to **2026-06-15 → 2026-09-12** (reviewer's
instruction: compare the recent ~90 trading days only). TV side =
Trades-tab rows with entry ≥ cut; MT5 = headless tester, same window
(**both sides History Quality 100%**).

| Metric | TV (COINBASE:ETHUSD D1, trades #298-301) | MT5 (BTCUSD D1, same window/defaults) |
|---|---|---|
| Trades (entries in window) | **4** (#298-301; #301 open, floating counted) | **3** |
| Net profit | +127.68 USD | −48.23 USD |
| Profit factor | 1.16 | 0.72 |
| Win rate | 50% (2/4, incl. open) | 33.3% (1/3) |
| Max DD (subset walk) | 801.26 USD abs | 1.73% rel (173 USD) |
| History quality | (TV feed) | **100%** (89 D1 bars) |

**Read:** trade COUNT matches (4 vs3) — with clean data the KAMA
signals align; PnL/PF flips sign on a 3-4 trade sample (ETH vs BTC,
fill timing, commission unmodeled) — statistically meaningless at
this n, but mechanically consistent. The pending-retry queue landed
fills normally in this window.

## (superseded) Full-window comparison — run 2026-09-23

TV page (COINBASE:**ETHUSD** D1, backtest May 23 2016 → Sep 12 2026,
all defaults, commission 0.05%, slippage 1 tick):

| Metric | TV report | MT5 run (TradeMaxGlobal **BTCUSD** D1, same window/defaults) |
|---|---|---|
| Net profit | +29,409.98 USD (**+294.10%**) | **+4,279.27 USD (+42.79%)** |
| Profit factor | 1.428 | 4.27 |
| Max drawdown (rel) | 16.57% | 6.79% |
| Trades | 300 (99 won, 33.00%) | **17** (6 won, 35.29%) |
| History quality | (TV Coinbase feed) | **34%** — 3,400 D1 bars with large gaps; usable D1 data effectively from ~2017/2021 depending on chunk |

**Attribution (ranked):**1) **session-closed queue只兑付了少数信号**
(the pre-fix run rejected169 entries with `TRADE_RETCODE_MARKET_CLOSED`;
the retry fix landed mid-batch and only produced+5 fills → trade count
17 vs300 is dominated by this, **P0 open task**);2) History Quality
34% — gapped D1 corrupts KAMA/SMA200 windows and the
rising/falling-3 persistence (a "3-bar rise" spans far more calendar
time across gaps);3) instrument ETH vs BTC;4) commission/slippage not
modeled (D1).

Verdict: win-rate band is in the same neighbourhood (35% vs 33%) but
everything else is session/gap dominated — **do not read P&L signal
from this run** until the P0 retry issue is fixed and a cleaner-feed
comparison exists.

## Open verification tasks

1. Run `assets/mql5-side/0006-aurora-kama.ini` (adjust `Symbol=`) and
   diff the trade list against the Pine report on **BTCUSD D1**;
   specifically check D4 (`ta.rising` length) — if entries sit1 bar
   early/late, adjust to the other reading and re-run.
2. Trailing: verify activation happens exactly `trailDelay` bars after
   the fill bar and the stop ratchets only in the trade's favour.
3. Re-check the license status with the author before any sharing.
4. **P0 — pending-entry retry只兑付了少数信号** (see port0005 task6:
   queued≈thousands vs fills≈17): fix the retry path on session-bound
   symbols, rerun, then redo this comparison.

## Related

- Shared `assets/mql5/strategy-common.mqh` with ports 0004/0005.
