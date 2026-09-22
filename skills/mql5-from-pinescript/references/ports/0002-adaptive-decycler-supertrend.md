# Port 0002 — Adaptive Decycler Supertrend → AdaptiveDecyclerSupertrend.mq5

| Field | Value |
|-------|-------|
| Pine source | `../../assets/pine-scripts/adaptive-decycler-supertrend.pine` (105 lines, v6, **MPL-2.0**, © SchizoQuant, `scriptAccess=open_no_auth`) |
| Script id | `PUB;2b4504b1f2c844f8a342028195715570` (see `PROVENANCE.md`) |
| MQL5 port | `../../assets/mql5/AdaptiveDecyclerSupertrend.mq5` (16 buffers / 14 plots) |
| Status | **numeric parity verified** (see "Numeric parity verification" below): 10176 bars, state/signal columns exact, math ≤1e-6 relative except one documented boundary bar; chart-visual diffs vs Pine are D1–D3 + data feed |

## License

The Pine original is MPL-2.0. The port keeps the attribution/license
header (file-level copyleft — the `.mq5` is distributed under MPL-2.0).

## Faithful (1:1)

- **Efficiency stage** — directional efficiency `direction/noise` over
  `efficiencyLength` with Pine's `nz(x, src)` warm-up fallbacks, clamped
  0..1; adaptive cutoff `slow - eff*(slow-fast)` with
  `fast/slow = min/max(InpMinCutoff, InpMaxCutoff)`.
- **Decycler** — Ehlers-style alpha from `2π/cutoff`
  (`(cos+sin-1)/cos`, clamped, `|cos|>1e-6` guard), IIR recursion seeded
  with `src` at the oldest bar; computed oldest→newest so the recursion
  order matches Pine's `var` state.
- **RMS envelope** — residual = src − decycler, SMA of squares over
  `rmsLength`, sqrt, floored at `syminfo.mintick`
  (`SYMBOL_TRADE_TICK_SIZE`, a *double* property — `SymbolInfoDouble`);
  independent upper/lower multipliers.
- **Persistent trail regime** — `SQ`/`trendTrail` `var` semantics exactly:
  previous-bar finals drive the flip tests, trail moves only in the
  favourable direction; signals gated `(i+1 < sz)` so history bar 0 never
  fires (Pine's `nz(SQ[1], SQ)` hides it there).
- **Plots** — conditional Bullish/Bearish trail lines (`linebr` ≙ EMPTY
  breaks), regime-colored decycler (`DRAW_COLOR_LINE`), envelope lines,
  band fill, LONG/SHORT arrows, 4 data-window diagnostics
  (efficiency/cutoff/residual/RMS) + trail/regime extras.
- **Inputs** — all 14 Pine inputs with identical defaults/groups; visual
  toggles (`showDecycler/showEnvelope/showFill/showSignals`) switch plot
  draw types at `OnInit` while buffers keep computing (logic unchanged).

## Decisions

- No ATR in this script (mintick only) — no iATR parity concern.
- First-bar seeds replicated: `decycler = src`,
  `SQ = src >= decycler ? 1 : -1`, `trendTrail = na → envelope fallback`.

## Deviations

- **D1 — band fill color.** Pine colors the fill per bar from the current
  regime (`color.new(col, 93)`); `DRAW_FILLING` has only 2 colors, set
  per tick from the **latest** regime (same class as 0001 D1).
- **D2 — `barcolor()` dropped.** MQL5 indicators cannot color candles.
  `InpColorBars` is kept as a documented no-op for parameter parity.
- **D3 — plotshape text "LONG"/"SHORT" omitted.** `DRAW_ARROW` has no
  text; markers are arrows 241/242 with ±6 px pixel shift instead.
- **D4 — `input.source` approximated.** `ENUM_PINE_SOURCE`
  (close/open/high/low/hl2/hlc3/hlcc4); Pine's exact `ohlc4`
  is not an MQL5 applied-price — `hlcc4` (weighted) is offered as the
  closest match.
- **D5 — tooltips.** Pine `tooltip=` strings are not representable in
  MQL5 input dialogs.
- **D6 — alert plumbing.** `alertcondition` → `Alert()` on realtime
  closed bars only, gated by `InpEnableAlerts` (same as 0001 D9).

## Numeric parity verification (2026-09-23)

Method — export the port's own buffers on identical input data and
recompute every value from the Pine semantics in Python:

1. `assets/mql5-side/BufferDump-EA.mq5` (headless tester, `Model=0`
   every-tick, XAUUSD H1, config `assets/mql5-side/parity_0002.ini`)
   bulk-dumps `time,OHLC,b0..b15` via `iCustom` + `CopyBuffer` →
   `parity_0002.csv` (10176 bars, 2025.01.02..2026.09.21).
2. `scripts/check_0002_parity.py <csv>` transcribes the Pine source
   independently (efficiency/alpha/decycler IIR/RMS envelopes/
   SQ+trail state machine/signals) and compares bar-by-bar.

Result (tolerance rel 1e-6):

| Columns | Verdict |
|---------|---------|
| `sq`, `decColor`, `longSig`, `shortSig`, `fillU/V` | **PASS — exact on all 10176 bars** (regime flips and signal bars bit-for-bit; signal prices match) |
| `efficiency`, `cutoff`, `decycler`, `residual`, `rms`, `upper/lower`, `trail*` | PASS everywhere **except the boundary bar `2026.06.01 01:00` + its decaying IIR tail** (≤35 bars, max rel diff ≈1e-4; `efficiency` diverges on that single bar only) |

Boundary-bar artifact: the indicator is created mid-bar at the tester
range start; its last write for that bar carries a mid-tick close
(`residual + decycler = 4527.10` vs final close `4535.29` — columns
are internally consistent with each other and with the cutoff/alpha
formula, i.e. the *math* is right, the *input snapshot* was frozen at
creation time). One-bar shock only; the IIR/ratchet tails decay below
tolerance within ~35 bars. Tester indicator-lifecycle artifact at the
attach bar, not a transcription error — on any bar whose final ticks
were processed, the port reproduces the Pine reference to ≤1e-6.

Implication for chart comparison: with identical data the port matches
the Pine reference, so visible Pine-vs-MT5 differences come from the
documented deviations (**D2 candle painting being the loud one** — TV
paints candles by regime, MQL5 indicators cannot color candles at all;
D3 missing LONG/SHORT text; D1 fill hue) plus **different data feeds**
(TV = IC Markets, MT5 = TradeMaxGlobal → some H1 bars and flip bars
differ before any indicator runs).

Harness reuse: same EA+INI for port 0003 (`InpIndicator`,
`InpBuffers=13`) plus a `check_0003_parity.py` reference transcription
(open task below).

## Open verification tasks

1. ~~Attach side by side with Pine: trail/band geometry identical~~ →
   superseded by the numeric parity verification above (stronger: same
   data ⇒ ≤1e-6).
2. LONG/SHORT arrows: verified numerically (signal columns exact);
   visual position check on chart still open.
   backfill; alerts fire once per realtime flip.
3. `showEnvelope=false` (default) still computes envelopes — verify trail
   flips behave identically with the envelope display toggled.
4. D1 fill color: acceptable lag vs Pine's per-bar coloring?
5. Write `check_0003_parity.py` and run the same harness for port 0003.

## Related

- Port 0001 (Modern Ichimoku Cloud) — same closed-bar state machine,
  `BlendToBg` color-transparency emulation, alert gating pattern.
