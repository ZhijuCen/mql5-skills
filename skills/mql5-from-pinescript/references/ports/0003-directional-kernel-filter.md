# Port 0003 — Directional Kernel Filter → DirectionalKernelFilter.mq5

| Field | Value |
|-------|-------|
| Pine source | `../../assets/pine-scripts/directional-kernel-filter.pine` (124 lines, v6, **MPL-2.0**, © BackQuant, `scriptAccess=open_no_auth`) |
| Script id | `PUB;1c48d645e9974f42a85e2b169bd3b7e9` (see `PROVENANCE.md`) |
| MQL5 port | `../../assets/mql5/DirectionalKernelFilter.mq5` (13 buffers / 10 plots) |
| Status | compiles clean (0 errors / 0 warnings, fresh `.ex5`); chart parity vs Pine **not yet** verified |

## License

The Pine original is MPL-2.0. The port keeps the attribution/license
header (file-level copyleft — the `.mq5` is distributed under MPL-2.0).

## Faithful (1:1)

- **Base Gaussian kernel** — bandwidth `max(1, length × kernelWidth)`,
  weights `exp(-0.5 (k/bw)²)`, window entries with missing source
  skipped (`not na(source[i])` guard), history-boundary behaviour:
  when the last window entry has no older neighbour, Pine's
  `localMove = na` poisons the sums and falls back to `base` — the port
  returns `base_out` in exactly that case.
- **Directional re-weighting** — previous base-kernel direction
  (`nz(base[1]-base[2])`, bases evaluated as window functions at
  `i+1`/`i+2`), ATR-normalised, ±1 clamped; local moves normalised per
  bar (`nz(norm[i], norm)` fallback chain), alignment →
  `exp(clamp(strength × alignment, ±3))` × kernel weight; during ATR
  warm-up (both norm candidates `na`) the filter degrades to `base`,
  matching Pine's na-propagation into `totalWeight > 0`.
- **ATR** — Wilder RMA computed inline (SMA-seeded), **not** `iATR`
  (SMA of TR would change every normalised weight).
- **Fast/slow kernels + trend** — `fastLen=18`, `slowLen=35`,
  `var int trend` state machine (1 / −1 / hold, seed 0) read from the
  previous bar's final value; trend-colored kernel lines
  (`DRAW_COLOR_LINE`), slow line width 2, ribbon `DRAW_FILLING`,
  base-kernel line blended from `chart.fg_color` (Pine `color.new(fg,60)`
  ≙ `BlendToBg(foreground, 60)`).
- **Data-window diagnostics** — Fast/Slow Reference Direction,
  Directional Adjustment (`fast − base`), Kernel Spread (`fast − slow`);
  internal ATR + trend buffers hidden via `PLOT_SHOW_DATA=false` (Pine
  does not expose them).
- **Inputs** — all 13 Pine inputs, identical defaults/groups;
  `showRibbon`/`showBase` switch draw types at `OnInit`.

## Decisions

- Ribbon fill color: both `DRAW_FILLING` colors are re-set each tick to
  the latest-trend blend — visible fill is therefore uniformly
  trend-colored (Pine colors bar-by-bar; see D1).
- Base-kernel line needs a foreground color: read per attach from
  `CHART_COLOR_FOREGROUND`.

## Deviations

- **D1 — ribbon fill color.** Pine `color.new(col, 82)` is a per-bar
  series; MQL5 has 2 static colors → set per tick from the **latest**
  trend (same class as 0001 D1 / 0002 D1; historical fill hue follows
  the current trend instead of each bar's own).
- **D2 — `plotcandle()` candle painting dropped.** Indicators cannot
  color candles; `InpPaintCandles` kept as a documented no-op.
- **D3 — `bgcolor()` background tint dropped.** Same platform limit as
  0001 D2; `InpBgCol` kept as a documented no-op (default off in Pine).
- **D4 — `input.source` approximated** by `ENUM_PINE_SOURCE`
  (close/open/high/low/hl2/hlc3/hlcc4→hlcc4), same mapping as 0002 D4.
- **D5 — tooltips** not representable in MQL5 input dialogs.
- **D6 — alert plumbing.** `alertcondition` (bullish/bearish flips) →
  `Alert()` on realtime closed bars only, gated by `InpEnableAlerts`;
  flip detection reads `trend[i]`/`trend[i+1]` (same as 0001 D9).

## Open verification tasks

1. Attach side by side with Pine: fast/slow kernel lines identical
   (both are window functions + one `var` trend state).
2. `directionStrength = 0` must reproduce the plain base-kernel
   crossover behaviour (directional weight becomes `exp(0) = 1`).
3. Warm-up: first `normLen` bars — trend/fill appear only once ATR
   exists; compare against Pine's na-degraded region.
4. Alerts: one per realtime trend flip, none on history load.

## Related

- Ports 0001/0002 — identical `BlendToBg`, `SymbolInfoDouble` mintick,
  closed-bar alert-gate and OnCalculate skeleton patterns.
