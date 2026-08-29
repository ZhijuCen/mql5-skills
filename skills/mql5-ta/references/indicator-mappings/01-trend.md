# Trend Indicators — MQL5 ↔ TA-Lib

See [0000-index.md](0000-index.md) for conventions and coverage marks.
MQL5 handle docs: `skills/mql5/references/docs/26-indicators/`.

| MQL5 | Buffers | TA-Lib | Class |
|---|---|---|---|
| iADX | MAIN / +DI / −DI (3) | `ADX` (+`PLUS_DI`, `MINUS_DI`) | ⚠️ |
| iADXWilder | MAIN / +DI / −DI (3) | `ADX` (+`PLUS_DI`, `MINUS_DI`) | ✅ |
| iAMA | 1 | `KAMA` | ✅ |
| iAlligator | 3 (jaws/teeth/lips) | ✗ | compose |
| iBands | BASE / UPPER / LOWER (3) | `BBANDS` | ✅ |
| iDEMA | 1 | `DEMA` | ✅ |
| iEnvelopes | UPPER / LOWER (2) | ✗ | compose |
| iFrAMA | 1 | ✗ | compose |
| iIchimoku | TENKAN/KIJUN/SENKOU_A/SENKOU_B/CHIKOU (5) | ✗ | compose |
| iMA | 1 | `MA` / `SMA`/`EMA`/`WMA`/`KAMA` by method | ✅ |
| iSAR | 1 | `SAR` | ✅ |
| iStdDev | 1 | `STDDEV` | ✅ |
| iTEMA | 1 | `TEMA` | ✅ |
| iTRIX | 1 | `TRIX` | ✅ |
| iVIDyA | 1 | ✗ | compose |

## Notes

### iADX vs iADXWilder ⚠️ / ✅
MQL5's standard `iADX` smooths with exponential-ish averaging, **not**
Wilder smoothing — its values differ from TA-Lib. Use `iADXWilder`
(0984) for parity with `talib.ADX` / `PLUS_DI` / `MINUS_DI`
(Wilder smoothing, `timeperiod=14` default both sides).

### iMA ✅
One handle, `ma_method` selects the family — see the MA-method table in
[0000-index.md](0000-index.md). `MODE_SMMA` has no TA-Lib function
(`ewm(alpha=1/n, adjust=False)`).

### iBands ✅
MQL5 `(ma_period, ma_shift, deviation, applied_price)` ↔
`BBANDS(close, timeperiod, nbdevup, nbdevdn, matype)`.
`deviation=2.0` ↔ `nbdevup=nbdevdn=2`. TA-Lib returns
`(upper, middle, lower)` — buffer order differs from MQL5
(BASE=0, UPPER=1, LOWER=2). `ma_shift` (plot shift) has no TA-Lib
equivalent — shift the resulting series yourself.

### iEnvelopes — compose ✗
No TA-Lib function. `upper = MA(price, n) * (1 + dev/100)`,
`lower = MA(...) * (1 - dev/100)`; MA method per the global table.

### iIchimoku — compose ✗
All from median price `(H+L)/2` with standard periods 9/26/52
(= MQL5 defaults):
- Tenkan-sen = (max(H,9)+min(L,9))/2
- Kijun-sen = (max(H,26)+min(L,26))/2
- Senkou A = (Tenkan+Kijun)/2, **plotted 26 bars ahead**
- Senkou B = (max(H,52)+min(L,52))/2, plotted 26 bars ahead
- Chikou = close, plotted 26 bars **back**
The forward/backward displacement has no TA-Lib counterpart — implement
with `pandas.Series.shift(-26)` / `shift(26)` after computing.

### iAlligator / iFrAMA / iVIDyA — compose ✗
- Alligator: SMMA(median, 13/8/5) shifted forward by 8/5/3 bars
  (jaws/teeth/lips). Use the SMMA recipe from 0000-index.
- FrAMA (Fratcal Adaptive MA) and VIDyA (Variable Index Dynamic Average)
  must be hand-coded; formulas in the MQL5 handle docs.

### Indexing reminder
All compose recipes above assume ascending series (TA-Lib convention);
convert to as-series only at the MQL5 comparison boundary.
