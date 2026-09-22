# Port 0001 — Modern Ichimoku Cloud [GBB] → ModernIchimokuCloud.mq5

| Field | Value |
|-------|-------|
| Pine source | `../../assets/pine-scripts/modern-ichimoku-cloud.pine` (410 lines, v0.5, `//@version=6`, open-source) |
| Provenance | `../../assets/pine-scripts/PROVENANCE.md` |
| MQL5 port | `../../assets/mql5/ModernIchimokuCloud.mq5` |
| Status | compiles clean (0 errors / 0 warnings, fresh `.ex5` via `mql5_helper.py compile`); visual/numeric parity vs Pine **not yet** verified on a live chart (see open tasks) |

## Faithful (1:1)

- **Layer 0** — Tenkan/Kijun/Senkou A/B/Chikou with original 9/26/52/26
  constants; `offset=+26` spans and `-26` Chikou reproduced with **raw
  buffers + `PLOT_SHIFT`** (`+g_off` / `-g_off`), extending the cloud
  `displacement-1` bars beyond the last bar (see Fix log).
- **Layer 1** — ATR-normalised thickness/TK/price-to-cloud/chikou
  momentum; nearest-rank percentile grades (30/70/90 over 150 bars);
  grade drives cloud-fill transparency (see deviation D1) and the
  last-bar grade label text.
- **Layer 2** — raw events (TK cross, Kumo break, twist), qualification
  (bar direction + `pcMin`/`chkMin` ATR distances + optional HTF cloud
  agreement), qualified/unqualified/twist markers, `tkGrade`,
  `qualDir` — all exposed as buffers (Data Window).
- **Layer 3** — flat-run detection (`flatMinK`=6 / `flatMinB`=8), level
  objects (`OBJ_TREND`) with touch (±`touchTol`×ATR) / expiry
  (`maxAgeMul`×Kijun) / width (`seg ≥ 2×flatMin` → 2) / FIFO cap 60 /
  hide-expired, plus created/touched/expired counters.
- **Layer 4** — running hit rates @H1/@H2, range multiple, touch rate,
  HTF cloud position, expanded counts table; 7 alerts gated to
  confirmed/realtime bars; Classic-mode forcing of Layers 1–3 off;
  palette (GBB/Classic/Mono) × theme (Auto/Dark/Light) with Pine's
  background-luminance formula.

## ATR parity decision

Pine `ta.atr` = Wilder RMA. MQL5 `iATR` = SMA of True Range (documented
parity finding in `skills/mql5-ta`). The port computes RMA inline
(SMA-seeded) instead of using `iATR` — using `iATR` would change every
ATR-normalised number (grades, `pc`, `chk`, touch tolerance).

## Deviations (Pine → MQL5 platform limits)

- **D1 — cloud fill transparency.** Pine varies fill alpha per bar from
  `gradeProj` (50/58/68/78/74). `DRAW_FILLING` supports only two static
  colors, re-set per tick from the *current* grade; alpha is emulated by
  blending toward the chart background color. Result: fill density
  follows the latest grade globally, not bar-by-bar.
- **D2 — HTF wash.** `bgcolor()` has no MQL5 equivalent (an indicator
  cannot tint chart background). Replaced by a corner label
  (`MIC_htf`) showing `HTF H4: above/below/inside cloud`, or the
  "wash off" note when the HTF ≤ chart TF — same information, no wash.
- **D3 — twist marker anchoring.** Pine `location.top/bottom` pins
  diamonds to the window edge; MQL5 arrow buffers are price-anchored.
  Twists are anchored at bar high/low plus `PLOT_ARROW_SHIFT` (±60 px).
- **D4 — marker glyphs.** Pine shapes → Wingdings codes
  241/242 (Kumo, bold arrow), 217/218 (TK, thin arrow), 159 (raw,
  circle); size hierarchy via plot width, not glyph. Diamonds reuse
  241/242 shifted (D3).
- **D5 — grade label / stats table.** `OBJ_TEXT` has no background box;
  the stats table is a grid of `OBJ_LABEL`s without bg rectangle or
  cell tooltips (the tooltip disclaimer is documented here instead).
- **D6 — HTF input.** Pine free-text `input.timeframe` →
  `ENUM_TIMEFRAMES InpHtfPeriod` with `PERIOD_CURRENT` = auto 4×,
  snapped up to the nearest MT5 timeframe (MT5 has no arbitrary TFs).
- **D7 — HTF evaluation margin.** Pine's `f_htf()` returns `[1]`-shifted
  values inside `request.security`. Port maps each chart bar to the
  latest HTF bar with `time ≤ chart time` (`hIdx`) and evaluates at
  `hIdx + 1 + displacement` (spans) / `hIdx + 1` (close) — always fully
  closed HTF data; edge placement can differ ±1 HTF bar from Pine's
  internal alignment.
- **D8 — percentile warm-up.** Requires `pctLen` non-`na` samples in the
  window (Pine's `na` handling in `ta.percentile_nearest_rank` is not
  specified); affects grade only during the first ~pctLen bars → grade
  `-1` ("n/a") instead of a possibly-defined value.
- **D9 — alerts.** `alertcondition` → `Alert()` on realtime-closed bars
  only; platform Alert list is the subscription mechanism (no
  `{{ticker}}` templating — text uses `_Symbol`/`_Period`).
- **D10 — data-window extras.** Port adds buffers not plotted by Pine
  (`HTFPos`, `EventsBits`, `FlatRunK/B`) for EA consumption; harmless
  extras in the Data Window.

## Fix log

- **2026-09-22 — cloud must extend beyond the last bar** (found via user
  screenshot `Screenshot_20260922_234104.png`: Pine shows the future cloud
  ~25 bars right of the last candle, the port ended at the last bar).
  *Cause*: spans were drawn by value-remap (`buf[i] = raw[i+off]`), which
  reproduces only the in-chart alignment — an indicator buffer never draws
  past index 0 that way. *Fix*: store spans + Chikou **raw** and apply
  `PLOT_SHIFT` (`+g_off` for spans/fill, `-g_off` for Chikou) — the exact
  pattern of the official `MQL5/Indicators/Examples/Ichimoku.mq5`
  (`PlotIndexSetInteger(2,PLOT_SHIFT,InpKijun)` /
  `(3,...,-InpKijun)`); MQL5 Book: *positive shifts to the right*, points
  *displayed to the right of the bar with index 0*. Logic reads displayed
  values through `DispAt()` (= Pine `senkouA[off]`), so all signal/geometry
  numbers are unchanged. Buffers 30→28, plots 29→27 (two redundant
  `DRAW_NONE` raw slots dropped; data-window `Senkou A/B` + `Chikou` now
  show raw values = Pine-faithful). *Rendering caveat*: points past the
  last bar need right-side chart space (enable chart shift) — the same
  constraint as MT5's built-in Ichimoku.

## Open verification tasks

1. Attach `ModernIchimokuCloud.ex5` and the Pine original to the same
   chart → five-line overlay identity (should be exact; both are
   highest/lowest midpoints).
2. Grade label + cloud position spot check on bars with known Pine
   values (Data Window `Grade` / `PC` / `CHK`).
3. Confirm D1 visual difference is acceptable; if not, the fallback is
   splitting the fill into 5 pairs of `DRAW_FILLING` plots gated by
   grade (5× buffers) — rejected for the initial port.
4. Alert once-per-bar gating under tick flood (new-bar guard).
5. **Future tail visible**: after reload, the cloud extends
   `displacement-1` (25) bars past the last bar; if clipped, enable chart
   shift (right-side margin) — compare side by side with the Pine original.
