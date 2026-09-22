# Pine Script docs — curated excerpts (porting-needed only)

Deliberately **not a full mirror** of https://www.tradingview.com/pine-script-docs/ —
only the pages and API entries that ports 0001–0006 actually consulted.
API entries keep Syntax / Arguments / Returns /Remarks / See-also but
**omit the Example code blocks** (available online via each anchor).

TradingView documents Pine in **two separate trees**:

| Tree | URL pattern | Delivery |
|------|-------------|----------|
| User manual (concepts / language / faq) | `/pine-script-docs/<section>/<page>/` | server-rendered HTML → curl+bs4 |
| API reference v6 (`fun_*`, `var_*`, `const_*` anchors) | `/pine-script-reference/v6/#fun_ta.atr` | **JS-only shell** — content is hydrated client-side into `div.tv-pine-reference-item`; not in the HTML or any fetchable API |

## User manual (14 pages, fetched by `scripts/fetch_pine_docs.py`)

| File | Why it is here (ports) |
|------|------------------------|
| `concepts-bar-states.md` | `barstate.isconfirmed/islast` → closed-bar state machine (0001–0006) |
| `concepts-inputs.md` | `input.*` title/tooltip/inline/group/display → MQL5 inputs (all) |
| `concepts-strategies.md` | `strategy()` properties: pyramiding, fills, commission, slippage (0004–0006) |
| `concepts-alerts.md` | `alertcondition` semantics → realtime-closed-bar `Alert()` gate (0001–0003) |
| `concepts-repainting.md` | repainting rules behind HTF / `isconfirmed` decisions (0001, 0006) |
| `concepts-other-timeframes-and-data.md` | `request.security` + `lookahead` → HTF wash mapping (0001) |
| `concepts-timeframes.md` | `timeframe.from_seconds/in_seconds` → auto-HTF input (0001) |
| `concepts-chart-information.md` | `syminfo.*` / `chart.*` reads (mintick, mincontract, bg/fg) (0002, 0005) |
| `language-execution-model.md` | per-bar evaluation order = chronological state machines (all) |
| `language-variable-declarations.md` | `var` / `varip` = persistent state we port to members (all) |
| `language-type-system.md` | series vs simple typing behind `x[k]` lookbacks (all) |
| `language-built-ins.md` | namespace map: which function lives where |
| `faq-strategies.md` | broker emulator & next-bar-open fill model (0004–0006) |
| `faq-variables-and-operators.md` | `na` propagation in ternaries/comparisons (all) |

## API reference excerpts (6 files, one-time browser DOM extraction)

Extracted 2026-09-23 from the hydrated DOM of
`https://www.tradingview.com/pine-script-reference/v6/` (each entry is a
self-contained `div#<anchor>`; serializer = browser-side `__grab`, results
assembled from the harness output artifacts).

| File | Anchors | Why it is here (ports) |
|------|--------:|------------------------|
| `reference-ta.md` | 12 | `atr/rma` (Wilder parity!), `ema/sma` seeding, `crossover/crossunder`, `dmi` (0004/0005), `percentile_nearest_rank` (0001), `rising/falling` (0006), `highest/lowest` (0001) |
| `reference-strategy.md` | 8 | `strategy()` full property text + `entry/exit/close` + `position_size/avg_price/equity/opentrades` (0004–0006). `default_qty_*` have no own anchors — documented inside `fun_strategy`. |
| `reference-input.md` | 7 | `input()` + `int/bool/float/string/source/time` — parameter typing, `confirm`, `display` (all) |
| `reference-plotting.md` | 7 | `plot` (offset/force_overlay/display), `plotshape` (location/size/style), `fill`, `hline`, `barcolor` (0002 D2), `bgcolor` (0001 D2), `plotcandle` (0003 D2) |
| `reference-drawing.md` | 11 | `label.*`, `table.*`, `line.*` object lifecycle for the 0001 dashboard/geometry |
| `reference-misc.md` | 18 | `color.new` (no-alpha emu), `nz`/`na`, `alertcondition`, `math.abs/max/min/pow/round/sqrt/sum` + `const_math.pi` (0002 α), `request.security` (0001), `chart.bg/fg_color`, `syminfo.mintick/mincontract`, `timeframe.from_seconds/in_seconds` |

## Regeneration

```bash
# manual pages (rerunnable; skips nothing, fails only on HTTP/content errors)
uv run python skills/mql5-from-pinescript/scripts/fetch_pine_docs.py
```

Reference files are **not** curl-able (JS shell) — if they must be rebuilt,
re-run the browser extraction: load `/pine-script-reference/v6/`, install
the `__grab(ids, file)` serializer on the page, call it per group with the
anchor lists above, and write `result.text` per file (large results land in
the harness `browser-output-*.json` artifacts as
`{result:{file,missing,text}}`). Keep the provenance header comment each
file starts with.

Provenance: fetched 2026-09-23 from tradingview.com; text © TradingView,
kept as internal porting reference for this skill.
