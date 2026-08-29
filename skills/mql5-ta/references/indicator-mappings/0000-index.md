# Indicator Mappings — MQL5 ↔ TA-Lib

Conventions used by every mapping file in this directory.

## Coverage classes

| Mark | Meaning |
|------|---------|
| ✅ consistent | Same algorithm; values match (modulo lookback/NaN semantics) |
| ⚠️ adapt | Same family but parameters/formula/outputs differ — see notes |
| ✗ none | No TA-Lib function; hand-code or compose from TA-Lib primitives |

## Global conventions (apply everywhere)

### Buffer count & access
MQL5 indicators are **handles**: create once with `iXXX(...)`, then read
buffers via `CopyBuffer(handle, buffer, start, count, array)`. Buffer
numbering starts at 0 (MAIN_LINE, SIGNAL_LINE, ... per indicator docs).
TA-Lib functions are **stateless**: one call in, N arrays out.

### Index direction
- TA-Lib output: **index 0 = oldest** (aligned with the ascending input).
- MQL5 `CopyBuffer` result: by default **as-series, index 0 = newest**.
- Convert with `series[::-1]` (numpy) or `pd.Series(...).iloc[::-1]`;
  in MQL5 use `ArraySetAsSeries(arr, false)` before comparing.

### Lookback / NaN
- TA-Lib: first `lookback` values are `NaN`; lookback can exceed the
  nominal period (RSI(14) → 15 bars).
- MQL5: no NaN; bars before the lookback carry `EMPTY_VALUE` (or garbage
  values from partial warm-up depending on the vendor's history depth).
  When comparing, **drop TA-Lib NaNs and the same count of leading MQL5
  bars**, then compare from the first valid index onward.

### Burn-in for history-seeded indicators
EMA/SMMA/Wilder-family indicators (RSI, ADXW, MACD, EMA, SMMA) depend on
**all bars before the analysis window**. When MQL5 computes on full chart
history but TA-Lib sees a truncated slice, the seed difference decays
geometrically but must burn in first (measured on XAUUSD M1, 1000-bar
window: RSI14 ~212 bars, ADXW ~191, MACD ~164, EMA10 ~61). `scripts/
parity_check.py` therefore compares only after a `BURN_IN = 250` bars
head. The same rule applies whenever re-basing any history-seeded
indicator on a fresh data window.

### Applied price → column selection
MQL5 `ENUM_APPLIED_PRICE` maps to a column (or derived series) chosen by
the caller in TA-Lib:

| ENUM_APPLIED_PRICE | Series |
|---|---|
| PRICE_CLOSE | `<CLOSE>` |
| PRICE_OPEN | `<OPEN>` |
| PRICE_HIGH | `<HIGH>` |
| PRICE_LOW | `<LOW>` |
| PRICE_MEDIAN | `(<HIGH>+<LOW>)/2` |
| PRICE_TYPICAL | `(<HIGH>+<LOW>+<CLOSE>)/3` |
| PRICE_WEIGHTED | `(<HIGH>+<LOW>+2*<CLOSE>)/4` |

### MA method → TA-Lib function
MQL5's single `ENUM_MA_METHOD` splits into separate TA-Lib functions:

| ENUM_MA_METHOD | TA-Lib | Note |
|---|---|---|
| MODE_SMA | `SMA` | ✅ |
| MODE_EMA | `EMA` | ⚠️ seed differs (MT5: first price; talib: SMA seed) — burn-in per 0000-index |
| MODE_SMMA | ✗ | Wilder smoothing; no direct TA-Lib function. Reproduce with `pandas.Series.ewm(alpha=1/n, adjust=False).mean()` (matches talib's internal Wilder smoothing used by RSI/ATR/ADXWilder) |
| MODE_LWMA | `WMA` | ✅ |
| MODE_AMA | `KAMA` | ✅ Kaufman AMA (default ER n=2..30, fast 2, slow 30) |

### Session gaps & volume
Gaps (maintenance/weekend) are never filled; indicators see contiguous
bars, same as MQL5 on chart data. FX/CFD real volume (`<VOL>`) is 0 —
volume-based indicators must use `<TICKVOL>`, stated in the output.

## Files

- [01-trend.md](01-trend.md) — iADX…iVIDyA (trend/bands/MA family)
- [02-oscillators.md](02-oscillators.md) — iAC…iWPR (oscillators/volatility)
- [03-volumes.md](03-volumes.md) — iAD, iBWMFI, iMFI, iOBV, iVolumes, iChaikin
- [04-bill-williams.md](04-bill-williams.md) — iAC, iAO, iAlligator, iFractals, iGator
- [05-talib-only.md](05-talib-only.md) — TA-Lib functions with no MQL5 native counterpart
