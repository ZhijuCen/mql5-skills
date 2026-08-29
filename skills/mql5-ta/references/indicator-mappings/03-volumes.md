# Volume Indicators — MQL5 ↔ TA-Lib

See [0000-index.md](0000-index.md) for conventions and coverage marks.
MQL5 handle docs: `skills/mql5/references/docs/26-indicators/`.

**Volume source caveat (applies to every row below):** FX/CFD quotes have
real volume `<VOL>` = 0 — always feed `<TICKVOL>` and state the
substitution in the output. TA-Lib's `volume` argument plays the role of
MQL5's `ENUM_APPLIED_VOLUME` choice (`VOLUME_TICK` / `VOLUME_REAL`).

| MQL5 | Buffers | TA-Lib | Class |
|---|---|---|---|
| iAD | 1 | `AD` | ✅ |
| iBWMFI | 1 | ✗ | compose |
| iChaikin | 1 | `ADOSC` | ⚠️ params |
| iMFI | 1 | `MFI` | ✅ |
| iOBV | 1 | `OBV` | ✅ |
| iVolumes | 1 | ✗ | plain column |

## Notes

### iChaikin ⚠️ — identify it correctly
MQL5's `iChaikin` is the **Chaikin A/D Oscillator** (signature
`fast_ma_period, slow_ma_period, ma_method, applied_volume`), i.e.
`(EMA(AD,3) − EMA(AD,10))` — the TA-Lib counterpart is **`ADOSC`**:
`talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)`.
Do NOT confuse it with "Chaikin Volatility" (a H-L range indicator
unrelated to volume) — TA-Lib has no Chaikin Volatility.
Note: MQL5's default smoothing is EMA, matching ADOSC.

### iBWMFI — compose ✗ (Market Facilitation Index)
`BW MFI = (<HIGH> − <LOW>) / <TICKVOL>`, scaled like MT5 (× volume-unit
factor — for cross-platform numeric parity divide tick volume by 1000
only if the MT5 chart does; the shape is identical either way).

### iVolumes — no computation
It is just the volume histogram; TA-Lib has no function — plot
`<TICKVOL>` directly.

### iAD / iMFI / iOBV ✅
- `talib.AD(high, low, close, volume)` ↔ iAD buffers.
- `talib.MFI(high, low, close, volume, timeperiod=14)` ↔ iMFI.
- `talib.OBV(close, volume)` ↔ iOBV.
