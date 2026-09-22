# Pine Script assets — provenance

Fixed-source assets for MQL5 ports. One `.pine` file per port, kept
byte-faithful to the publisher's source (except line endings, see below).

## modern-ichimoku-cloud.pine

| Field  | Value |
|--------|-------|
| Script | Modern Ichimoku Cloud [GBB] v0.5 (2026-09-19) |
| Author | GoodBadBitcoin (TradingView) |
| Page   | https://www.tradingview.com/script/jJAqvJP5-Modern-Ichimoku-Cloud-GBB/ |
| Pine   | `//@version=6`, open-source (`script_access=all`) |
| Script id | `PUB;5b2db444633445b6b274ac42aba19621` |
| Source endpoint | `https://pine-facade.tradingview.com/pine-facade/get/PUB%3B5b2db444633445b6b274ac42aba19621/1?no_4xx=true` (JSON key `source`) |
| Fetched | 2026-09-22 via `scripts/extract_pine.py fetch` |
| Size    | 410 lines |
| Normalization | CRLF → LF only (API returns `\r\n`); content otherwise untouched |

Do NOT re-extract by copy/paste from the rendered code viewer: the viewer
renders spaces as U+00A0 (non-breaking space), which silently corrupts the
source. The `pine-facade` endpoint returns real ASCII spaces.

The corresponding MQL5 port: `../mql5/ModernIchimokuCloud.mq5`.
Port notes and documented deviations: `../../references/ports/0001-modern-ichimoku-cloud.md`.

---

## adaptive-decycler-supertrend.pine

| Field  | Value |
|--------|-------|
| Script | Adaptive Decycler Supertrend |
| Author | SchizoQuant (TradingView) |
| Page   | https://www.tradingview.com/script/vEWWRSv8-Adaptive-Decycler-Supertrend-SchizoQuant/ |
| License | **MPL-2.0** (header inside the Pine file — the MQL5 port inherits it) |
| Pine   | `//@version=6`, open-source (`scriptAccess=open_no_auth`) |
| Script id | `PUB;2b4504b1f2c844f8a342028195715570` |
| Source endpoint | `https://pine-facade.tradingview.com/pine-facade/get/PUB%3B2b4504b1f2c844f8a342028195715570/1?no_4xx=true` (JSON key `source`) |
| Fetched | 2026-09-23 via `scripts/extract_pine.py fetch` |
| Size    | 105 lines |
| Normalization | CRLF → LF only; content otherwise untouched |

MQL5 port: `../mql5/AdaptiveDecyclerSupertrend.mq5` ·
Port record: `../../references/ports/0002-adaptive-decycler-supertrend.md`.

---

## directional-kernel-filter.pine

| Field  | Value |
|--------|-------|
| Script | Directional Kernel Filter [BackQuant] |
| Author | BackQuant (TradingView) |
| Page   | https://www.tradingview.com/script/5AnxLyjj-Directional-Kernel-Filter-BackQuant/ |
| License | **MPL-2.0** (header inside the Pine file — the MQL5 port inherits it) |
| Pine   | `//@version=6`, open-source (`scriptAccess=open_no_auth`) |
| Script id | `PUB;1c48d645e9974f42a85e2b169bd3b7e9` |
| Source endpoint | `https://pine-facade.tradingview.com/pine-facade/get/PUB%3B1c48d645e9974f42a85e2b169bd3b7e9/1?no_4xx=true` (JSON key `source`) |
| Fetched | 2026-09-23 via `scripts/extract_pine.py fetch` |
| Size    | 124 lines |
| Normalization | CRLF → LF only; content otherwise untouched |

MQL5 port: `../mql5/DirectionalKernelFilter.mq5` ·
Port record: `../../references/ports/0003-directional-kernel-filter.md`.

---

## supertrend-regime-confluence.pine

| Field  | Value |
|--------|-------|
| Script | SuperTrend Regime Confluence |
| Author | DefinedEdge (TradingView) |
| Page   | https://www.tradingview.com/script/mpjNqADq-SuperTrend-Regime-Confluence/ |
| License | **MPL-2.0** (header inside the Pine file - the MQL5 EA inherits it) |
| Pine   | `//@version=6`, open-source (`scriptAccess=open_no_auth`) |
| Script id | `PUB;523784a4809e405eb1dd09d9eef7a3d3` |
| Source endpoint | `https://pine-facade.tradingview.com/pine-facade/get/PUB%3B523784a4809e405eb1dd09d9eef7a3d3/1?no_4xx=true` |
| Fetched | 2026-09-23 via `scripts/extract_pine.py fetch` |
| Size    | 372 lines |
| Normalization | CRLF → LF only; content otherwise untouched |
| Recommended asset | **BTCUSDT, 4H** (author's default-settings/backtest block) |

MQL5 EA: `../mql5/SuperTrendRegimeConfluence-EA.mq5` ·
Tester INI: `../mql5-side/0004-supertrend-regime-confluence.ini` ·
Port record: `../../references/ports/0004-supertrend-regime-confluence.md`.

---

## macd-pullback-sniper.pine

| Field  | Value |
|--------|-------|
| Script | MACD Pullback Sniper \| Trend + ADX Filtered Strategy |
| Author | blitz_locked (TradingView) |
| Page   | https://www.tradingview.com/script/V87nRt9v-MACD-Pullback-Sniper-Trend-ADX-Filtered-Strategy/ |
| License | **MPL-2.0** (header inside the Pine file - the MQL5 EA inherits it) |
| Pine   | `//@version=6`, open-source (`scriptAccess=open_no_auth`) |
| Script id | `PUB;aeae32205bbc4e4eb1e472b3bbe4e57d` |
| Source endpoint | `https://pine-facade.tradingview.com/pine-facade/get/PUB%3Baeae32205bbc4e4eb1e472b3bbe4e57d/1?no_4xx=true` |
| Fetched | 2026-09-23 via `scripts/extract_pine.py fetch` |
| Size    | 119 lines |
| Normalization | CRLF → LF only; content otherwise untouched |
| Recommended asset | trending markets, **1H/4H/Daily**; sizing note fits **crypto & stocks** (INI: BTCUSD H4) |

MQL5 EA: `../mql5/MACDPullbackSniper-EA.mq5` ·
Tester INI: `../mql5-side/0005-macd-pullback-sniper.ini` ·
Port record: `../../references/ports/0005-macd-pullback-sniper.md`.

---

## aurora-kama.pine

| Field  | Value |
|--------|-------|
| Script | Aurora KAMA Trend (page: "Aurora KAMA \| KAMA Adaptive Trend Strategy") |
| Author | blitz_locked (TradingView) |
| Page   | https://www.tradingview.com/script/kbYTJ8V2-Aurora-KAMA-KAMA-Adaptive-Trend-Strategy/ |
| License | **none declared in the source** (TV open-source access only) — the port credits the author and claims no license; personal-research use |
| Pine   | `//@version=6`, open-source (`scriptAccess=open_no_auth`) |
| Script id | `PUB;426d44d5850b4168b7bfb48e03e8e0d6` |
| Source endpoint | `https://pine-facade.tradingview.com/pine-facade/get/PUB%3B426d44d5850b4168b7bfb48e03e8e0d6/1?no_4xx=true` |
| Fetched | 2026-09-23 via `scripts/extract_pine.py fetch` |
| Size    | 179 lines |
| Normalization | CRLF → LF only; content otherwise untouched |
| Recommended asset | **DAILY bars: BTCUSD, ES1!, SPY, QQQ** (INI: BTCUSD D1) |

MQL5 EA: `../mql5/AuroraKamaTrend-EA.mq5` ·
Tester INI: `../mql5-side/0006-aurora-kama.ini` ·
Port record: `../../references/ports/0006-aurora-kama.md`.
