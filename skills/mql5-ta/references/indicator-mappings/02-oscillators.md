# Oscillators & Volatility — MQL5 ↔ TA-Lib

See [0000-index.md](0000-index.md) for conventions and coverage marks.
MQL5 handle docs: `skills/mql5/references/docs/26-indicators/`.

| MQL5 | Buffers | TA-Lib | Class |
|---|---|---|---|
| iAC | 1 | ✗ | compose |
| iAO | 1 | ✗ | compose |
| iATR | 1 | `ATR` | ⚠️ SMA(TR) vs Wilder |
| iBearsPower | 1 | ✗ | compose |
| iBullsPower | 1 | ✗ | compose |
| iCCI | 1 | `CCI` | ✅ |
| iDeMarker | 1 | ✗ | compose |
| iForce | 1 | ✗ | compose |
| iMomentum | 1 | `ROC` | ⚠️ name trap |
| iMACD | MAIN / SIGNAL (2) | `MACD` | ⚠️ signal smoothing |
| iOsMA | 1 | ✗ | = `MACD` hist |
| iRSI | 1 | `RSI` | ✅ |
| iRVI | 1 | ✗ | compose |
| iStochastic | MAIN / SIGNAL (2) | `STOCH` | ⚠️ smoothing differs |
| iWPR | 1 | `WILLR` | ✅ |

## Notes

### iMomentum ⚠️ — name trap
MQL5 `iMomentum(n)` = `close / close[n] * 100` — a **percentage**.
TA-Lib has two functions:
- `talib.ROC(close, n)` = same percentage → **use this**
- `talib.MOM(close, n)` = plain difference `close - close[n]` → NOT equal

### iMACD ⚠️ — signal smoothing differs
- Main line: `EMA(fast) - EMA(slow)` — identical both sides.
- Signal line: MQL5 smooths the main line with **SMA** (period `signal`),
  TA-Lib uses **EMA**. Values diverge throughout the series, not just at
  the head.
- For parity, compute manually:
  ```python
  macd = talib.EMA(close, fast) - talib.EMA(close, slow)
  signal = talib.SMA(macd, signal_period)  # SMA = MQL5 behaviour
  ```
- MQL5 has **no histogram buffer**. TA-Lib's third output `macd_hist`
  (= macd − signal) is exactly MQL5's separate `iOsMA` indicator.

### iAC / iAO — compose ✗ (Bill Williams; see 04-bill-williams.md)
- AO = SMA(median, 5) − SMA(median, 34)
- AC = AO − SMA(AO, 5)

### iBearsPower / iBullsPower — compose ✗
Both default `ma_period=13`, EMA of close:
- Bears = `<LOW>` − `talib.EMA(close, 13)`
- Bulls = `<HIGH>` − `talib.EMA(close, 13)`

### iDeMarker — compose ✗
```
DeMax = max(high - prev_high, 0); DeMin = max(prev_low - low, 0)
DeMarker = SMA(DeMax, n) / (SMA(DeMax, n) + SMA(DeMin, n))
```
(MQL5 uses SMMA — use the Wilder/`ewm` recipe from 0000-index for parity.)

### iForce — compose ✗
`Force = <TICKVOL> * (close - prev_close)`, smoothed with
`ma_method` (default MODE_SMA, n=13). No TA-Lib equivalent.

### iRVI — compose ✗ (Relative Vigor Index, not RSI!)
```
num = SMA(open - close, n); den = SMA(high - low, n)
RVI = num / den;  signal = SMMA(RVI, 4)
```

### iStochastic ⚠️ — numerator/denominator smoothed separately (verified)
MQL5 `iStochastic(K, D, slowing)` does **not** average the raw %K ratio.
It smooths numerator and denominator independently (classic MT4
implementation), then divides — verified exact against a live export:
```python
num = (c - l.rolling(K).min()).rolling(slowing).mean()
den = (h.rolling(K).max() - l.rolling(K).min()).rolling(slowing).mean()
main   = num / den * 100            # MAIN_LINE (buffer 0)
signal = main.rolling(D).mean()     # SIGNAL_LINE (buffer 1) = SMA of main
```
TA-Lib's `STOCH` averages the raw ratio first (SMA of %K) — small but
systematic differences (max_rel ~0.37 observed). Do not use `STOCH` when
MQL5 parity is required.

### iATR ⚠️ — smoothing differs (verified by parity check)
MQL5 `iATR(n)` smooths True Range with a **simple MA**:
`ATR = SMA(TR, n)`.
TA-Lib's `ATR` uses **Wilder smoothing** — values differ throughout the
series (max_rel ~0.5 observed), not just at the head.
Parity recipe (exact, verified):
```python
tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
atr = tr.rolling(14).mean()   # == MQL5 iATR(14)
```
Use `talib.ATR` only when Wilder-smoothed ATR is explicitly wanted.

### iRSI ✅ (with burn-in)
Both sides use Wilder smoothing; the only difference is the **seed**,
which decays geometrically (observed: below 1e-6 after ~212 bars).
Compare only after a burn-in (see 0000-index.md); parity confirmed exact
after warm-up.
