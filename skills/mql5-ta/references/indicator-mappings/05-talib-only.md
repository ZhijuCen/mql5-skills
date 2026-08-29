# TA-Lib-only Functions — no MQL5 native counterpart

These TA-Lib families have no MQL5 built-in indicator handle. Use TA-Lib
directly on the aligned quotes; there is no mapping to document, only the
pointer here. Full per-function docs: `references/docs-talib/func_groups/`.

| Group | Count | Examples |
|---|---|---|
| Pattern Recognition (`CDL*`) | 61 | `CDLENGULFING`, `CDLDOJI`, `CDLHAMMER`, `CDLHARAMI`, `CDL3BLACKCROWS` |
| Cycle Indicators | 5 | `HT_DCPERIOD`, `HT_DCPHASE`, `HT_PHASOR`, `HT_SINE`, `HT_TRENDMODE` |
| Statistic Functions | 9 | `BETA`, `CORREL`, `LINEARREG`, `STDDEV`* , `VAR` |
| Math Transform | 15 | `ACOS`, `ASIN`, `ATAN`, `CEIL`, `COS`, `EXP`, `FLOOR`, `LN`, `SIN`, `SQRT`, `TAN` |
| Math Operators | 11 | `ADD`, `DIV`, `MAX`, `MIN`, `MULT`, `SUB`, `SUM` |
| Price Transform | 5 | `AVGPRICE`, `MEDPRICE`, `TYPPRICE`, `WCLPRICE` |

\* `STDDEV` also serves as the MQL5 `iStdDev` counterpart (01-trend.md);
`HT_*` require ≥ ~63 bars of warm-up.

Also note: TA-Lib's Overlap Studies include `T3`, `TRIMA`, `MAVP`, `MAMA`,
`HT_TRENDLINE`, `SAREXT`, `MIDPOINT`, `MIDPRICE` — available in Python
even though MQL5 has no handle for them (`SAREXT` extends `iSAR`).

If an MQL5 custom indicator (via `iCustom` + `CopyBuffer`) must be
reproduced in Python, none of the above applies: read the custom
indicator's source, find its buffers, and port the formula — the
conventions in [0000-index.md](0000-index.md) (series direction, lookback,
applied price) still govern the comparison.
