# Bill Williams — MQL5 ↔ TA-Lib

See [0000-index.md](0000-index.md) for conventions and coverage marks.
MQL5 handle docs: `skills/mql5/references/docs/26-indicators/`.

All Bill Williams indicators use the **median price** `(H+L)/2`.

| MQL5 | Buffers | TA-Lib | Class |
|---|---|---|---|
| iAC | 1 | ✗ | compose |
| iAO | 1 | ✗ | compose |
| iAlligator | GATORJAW/GATORTEETH/GATORLIPS (3) | ✗ | compose |
| iFractals | UPPER/LOWER (2) | ✗ | compose |
| iGator | UPPER/HISTORY/LOWER (3) | ✗ | compose |

None of the Bill Williams family exists in TA-Lib — compose from
primitives on ascending series:

### iAO (Awesome Oscillator)
`SMA(median, 5) − SMA(median, 34)`

### iAC (Accelerator Oscillator)
`AO − SMA(AO, 5)` — compute AO first, then this.

### iAlligator
Three smoothed (SMMA = Wilder) lines of median, shifted **forward**:
- Jaws: SMMA(median, 13), shift +8
- Teeth: SMMA(median, 8), shift +5
- Lips: SMMA(median, 5), shift +3

Use `ewm(alpha=1/n, adjust=False).mean()` for SMMA and
`pandas.Series.shift(-k)` for the forward plot displacement.

### iFractals
Up fractal at bar i: `high[i] > high[i±1..2]` (5-bar pattern);
down fractal: `low[i] < low[i±1..2]`. Buffers: 0 = UPPER, 1 = LOWER;
bars without a fractal carry `EMPTY_VALUE` in MQL5 — represent as `NaN`
in pandas. Pure numpy/pandas, no TA-Lib.

### iGator
The Alligator lines plotted as an oscillator histogram:
`jaws − teeth` (upper), `teeth − lips` (lower); its middle "history"
buffer mirrors the teeth colour phase. Derive from the Alligator recipe.
