# Pine Script → MQL5 construct mapping

Companion to `../SKILL.md` §Step 3. Everything here is derived from the
local MQL5 docs (`skills/mql5/references/docs/24-customind/`,
`docs/01-constants/`) and from the first full port
(`references/ports/0001-modern-ichimoku-cloud.md`).

Series convention: all mappings assume **as-series arrays**
(`ArraySetAsSeries(..., true)`), index 0 = newest bar, `i + k` = k bars
ago — the same direction as Pine's `x[k]`.

## 1. Shell

| Pine | MQL5 |
|------|------|
| `indicator(..., overlay=true)` | `#property indicator_chart_window` |
| `indicator(..., overlay=false)` | `#property indicator_separate_window` |
| `input.bool/int/float/string` | `input bool/int/double/string` (group with `input group "..."`, fall back to `// [Group]` comments on old builds) |
| `input.timeframe` | `input ENUM_TIMEFRAMES` — `PERIOD_CURRENT` = Pine's `""` (auto); never parse free-text TF strings |
| `input.options=[a,b,c]` | `enum` type input (ALL_CAPS members) |
| `var` globals / `var array<…>` | class members of one state class, reset in `OnInit()` |
| `barstate.islast` | index `0` in `OnCalculate` |
| `barstate.isconfirmed` | closed-bar state machine (§4) |
| `bar_index` | a monotonic counter incremented by the state machine, or `rates_total - 1 - i` |
| `na` | `EMPTY_VALUE` sentinel + `IsNa(v)` helper (`v == EMPTY_VALUE`) |
| `max_lines_count / max_labels_count` | bounded member arrays; delete all with `ObjectsDeleteAll(chart, prefix)` in `OnDeinit()` |

## 2. Plots

| Pine | MQL5 |
|------|------|
| `plot(src)` | `DRAW_LINE` plot + buffer |
| `plot(src, offset=+k)` (Senkou forward) | store `src` **raw** in the buffer + `PlotIndexSetInteger(plot, PLOT_SHIFT, k)`. Positive shift = right / "future direction" (MQL5 Book: *positive shifts to the right*; points are *displayed to the right of the bar with index 0*). This is the only way to extend the plot k bars **beyond the last bar** — the pattern of `MQL5/Indicators/Examples/Ichimoku.mq5` (`PlotIndexSetInteger(2,PLOT_SHIFT,InpKijun)`). A value-remap (`buf[i]=raw[i+k]`) reproduces only the in-chart alignment and silently loses the future tail. |
| `plot(src, offset=-k)` (Chikou back) | store `src` **raw** + `PLOT_SHIFT = -k` (negative shifts are supported — the official Ichimoku example uses `PLOT_SHIFT, -InpKijun` for Chikou), so the buffer equals Pine's data-window value at the bar. Logic that needs the *displayed* value of a raw+shifted series reads it through a helper (`DispAt(arr,i,sz)` = Pine `series[k]`). A value-remap variant (`buf[i]=src[i-k]`, slots `0..k-1` EMPTY, slot `k` fed each tick with `src[0]`) draws the same line but puts *displayed* values into the data window — a fidelity loss; use only when a remap is unavoidable. |
| `fill(pA, pB, color=cond ? cUp : cDn)` | `DRAW_FILLING` plot (2 buffers): color0 where buf0>buf1, color1 where buf1>buf0, switched via `PlotIndexSetInteger(plot, PLOT_LINE_COLOR, idx, color)` each tick. **No per-bar alpha/grade** — only 2 dynamic colors (docs: DRAW_FILLING has no color-index version) |
| `color.new(c, t)` transparency on plots | plots have **no alpha**: `BlendWithBg(c, t)` = per-channel lerp toward `CHART_COLOR_BACKGROUND` (read via `ChartGetInteger`, type `color`) |
| `plot(..., display=display.data_window)` | `DRAW_NONE` plot + buffer (visible in Data Window, drawn nowhere) |
| `plotshape` (below/above bar) | `DRAW_ARROW` plot; anchor = `low[i]`/`high[i]`; glyph via `PLOT_ARROW` (Wingdings); pixel nudge via `PLOT_ARROW_SHIFT` (neg = up) |
| `shape.triangleup` big/small | verified codes: `241`/`242` (bold arrow), `217`/`218` (thin arrow, iFractals' own), `159` (circle, default). Use color/width for size differences; glyph tables beyond these are unverified |
| `shape.diamond` at `location.top/bottom` | anchor at `high`/`low`, push to the window edge with `PLOT_ARROW_SHIFT` (±N px). Deviation: pixel shift ≠ true window-edge anchoring (MQL5 buffers are price-anchored) |
| `bgcolor(c)` | no equivalent — indicator cannot tint the chart bg. Use a corner `OBJ_LABEL` state readout; document as deviation |
| `label.new` (price-anchored) | `OBJ_TEXT` (time/price anchored, no background box) |
| `table` / corner `label` | grid of `OBJ_LABEL` at `CORNER_RIGHT_UPPER` + `ANCHOR_RIGHT_UPPER`; no background, no tooltip — document |

## 3. Calculations

| Pine | MQL5 |
|------|------|
| `ta.highest(high, n)` / `ta.lowest` | bounded max/min loop; return `EMPTY_VALUE` when `i + n - 1` exceeds history (Pine `na`) |
| `ta.atr(n)` | **Wilder RMA computed inline**: `atr[i] = (atr[i+1]*(n-1) + tr[i]) / n`, seeded with the SMA of the first n TRs. Do **not** use `iATR` — MQL5's built-in is SMA of TR (parity finding in `skills/mql5-ta`), TV Pine is Wilder |
| `ta.crossover(a, b)` | `a[i] > b[i] && a[i+1] <= b[i+1]` (guard both `!IsNa`) |
| `ta.crossunder(a, b)` | `a[i] < b[i] && a[i+1] >= b[i+1]` |
| `ta.percentile_nearest_rank(s, len, p)` | copy window `s[i .. i+len-1]` (skip `na`), sort, take `ceil(p/100 * n)`-th (1-based). Require `len` valid samples + `bar_index >= len`; else `EMPTY_VALUE` (stricter than Pine during warm-up — document if it changes early grades) |
| `math.sign / math.max / …` | `Sign() / MathMax() / …` — note `MathSign` does not exist; write a helper |
| `request.security(tf, expr, lookahead_off)` | hand-built HTF series: `CopyTime/High/Low/Close(_Symbol, tf, ...)` → as-series arrays → precompute `expr` over HTF bars → map each chart bar to the **latest HTF bar whose time ≤ chart bar time**; Pine's extra `[1]` inside the expression becomes index `hIdx + 1 + shifts` (always uses fully closed data). Rebuild when history grows; amortize with over-allocation |
| `timeframe.from_seconds(4 * in_seconds())` | enum lookup: smallest `ENUM_TIMEFRAMES` with `PeriodSeconds(x) >= 4 * PeriodSeconds(chart)` (MT5 has M2/M3/M4/M6/M10/M12/M20/H2/H3/H6/H8/H12) |

## 4. Stateful semantics (the part that breaks naive ports)

1. **Shift-invariance rule.** A value displayed at bar B that depends only
   on bars at fixed offsets from B (spans, chikou, percentile grades,
   cross events) is *intrinsic to B*: compute once, let MT5's automatic
   buffer shifting carry it with the bar. Only refresh index 0 per tick
   and — only if you chose the value-remap variant — the one slot whose
   supplier bar was born (or died) at the bar boundary. Never recompute
   the whole array per tick. Offset plots should prefer `PLOT_SHIFT`
   (§2 rows), which removes that slot bookkeeping entirely.
2. **Closed-bar state machine.** Pine code under `barstate.isconfirmed`
   (level objects, running counters, alerts) must run **exactly once per
   closed bar, in chronological order**. Drive it from `rates_total` /
   `prev_calculated`, guard with a `m_lastProcessedTime`, and
   bulk-process the whole history on the first call (backfill).
3. **Realtime vs backfill.** Fire `Alert()` only for bars closed *after*
   init; during backfill only accumulate. Mirrors Pine, where
   `alertcondition` never replays history.
4. **Objects from state.** Pine `line`/`label` objects created during a
   series walk become chart `OBJ_*` objects created inside the state
   machine; cap the count (Pine's `max_lines_count`) with a FIFO that
   deletes the oldest object; prefix every name for `OnDeinit` cleanup.
5. **Idempotence check.** Two consecutive `OnCalculate` calls with no new
   bar must produce byte-identical buffers/objects (Pine re-runs, MQL5
   must not double-count).

## 5. Verification checklist (per port)

- `mql5_helper.py check FILE.mq5` clean (Wine exit 0 **and** fresh `.ex5`).
- Attach to chart: backfill completes with no `OnInit` errors; no object
  count growth on repeated ticks (check idempotence).
- Closed bars: values/objects never change after their bar closes
  (no-repaint spot check: screenshot twice, 1 minute apart).
- **Forward tails**: any Pine `offset > 0` plot must visibly extend that
  many bars **beyond the last bar** (needs right-side chart space; same
  constraint as MT5's built-in Ichimoku).
- **Numeric parity (when same-data proof is needed)**: headless-tester
  export + independent Python re-transcription — precedent:
  `assets/mql5-side/BufferDump-EA.mq5` + `parity_*.ini` +
  `scripts/check_0002_parity.py`. The port-0002 record shows the report
  format and the indicator-lifecycle caveat at the test-range start
  (attach-time bar freezes at a mid-tick snapshot in the tester).
- Compare against the Pine original on the same symbol/timeframe: five
  lines overlay-identical, cloud position identical, event markers within
  ±1 bar only where documented (HTF mapping / warm-up guard).
- Alerts: fire once per realtime bar, never on attach/history load.
