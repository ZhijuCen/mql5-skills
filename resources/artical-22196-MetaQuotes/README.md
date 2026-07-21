# Article 22196 — MetaTrader 5 and the MQL5 Economic Calendar

Original: <https://www.mql5.com/en/articles/22196>
Author: MetaQuotes Ltd., published 8 May 2026 (4,776 views).

This is the offline copy of the MQL5 article that motivates the
`skills/mql5/references/quick-ref-mql5-economic-calendar.md` format
and the `skills/mql5/scripts/parse_mql_calendar_bin.py` parser. The
article is shipped here in case the original goes behind a login wall
or moves; the directory also contains the six source files referenced
from the article body.

## What the article argues

News trading is a fragmented workflow: open a browser tab for the
calendar, glance at the next release, switch back to MetaTrader 5,
place or close orders. Context loss between the two surfaces leads to
slipped entries and lost opportunities. The article's thesis is that
this is an **engineering problem** — once you treat it as such, the
solution has the same shape as any other MQL5 system: a single data
source, a typed API, deterministic filtering, and reproducible
backtesting.

The MetaTrader 5 economic calendar is unique because it is
**native to the terminal**: access speed under 100 ms after the first
load, no extra integration layer, and historical data is available
for offline testing. No other trading platform has this.

## Architecture proposed in the article

```
  +------------------------+       +-----------------------------+
  | MQL5 Calendar API      |       | MQL5 Calendar API           |
  | (LIVE terminal only)   |       | (data baked into .ex5 as    |
  | CalendarValueHistory() |       |  #resource array of         |
  | CalendarValueLast()    |       |  MqlCalendarValue)          |
  +------------------------+       +-----------------------------+
          |                                      ^
          v                                      |
  +------------------------+       +-----------------------------+
  | Filter sieve           |       | Strategy Tester (no network)|
  |  1. currency           |       | reads #resource from RAM    |
  |  2. importance (HIGH)  |       +-----------------------------+
  |  3. event_code (NONFARM|
  |     / CPI / GDP / ...) |
  |  4. time window        |
  +------------------------+
          |
          v
  +------------------------+
  | Export to binary       |
  |  SaveToBinary uses     |
  |  FileWriteArray on     |
  |  MqlCalendarValue[]    |
  |  → {currency}_cal.bin  |
  +------------------------+
```

The two data-source paths (API in live mode, baked resource in
tester mode) are selected at `OnInit()` by checking
`MQLInfoInteger(MQL_TESTER)`. The rest of the EA does not care which
path served the data.

## Key MQL5 API surface

The article uses these functions (full signatures in the local MQL5
docs mirror `references/docs/15-calendar/`):

| Function | Used for |
|---|---|
| `CalendarValueHistory(values, from, to, country, currency)` | Bulk download a window of values; the workhorse for `OnInit` and for the exporter script. |
| `CalendarValueLast(change_id, updates, ...)` | Incremental fetch of only-new values via `change_id`; the recommended pattern for `OnTimer` to avoid rate-limit errors. |
| `CalendarEventById(id, event)` / `CalendarEventByCountry` / `CalendarEventByCurrency` | Resolve an `event_id` to the `MqlCalendarEvent` descriptor (name, importance, code, sector, source_url). |
| `CalendarCountryById(id, country)` | Resolve a country from the `MqlCalendarEvent.country_id`. |
| `CalendarValueById(id, value)` | Fetch a single value by `value_id`. |

## Three core data structures

Article 22196 gives the full struct definitions; the local mirror is
at `references/docs/01-constants/0186-constants-structures-mqlcalendar.md`.

- `MqlCalendarEvent` — the **family** descriptor (CPI, NFP, FOMC
  statement). Identified by `id`. Carries `importance`, `event_code`,
  `name`, `country_id`, etc.
- `MqlCalendarValue` — one **release** of a family (this month's NFP).
  Identified by `id`; references the family via `event_id`. Carries
  `time`, `period`, `revision`, `actual_value`, `prev_value`,
  `revised_prev_value`, `forecast_value`, `impact_type`. The four
  value fields are `long` × 10⁶ or `LONG_MIN` if unset.
- `MqlCalendarCountry` — the country descriptor. Identified by `id`.
  Carries `code` (ISO 3166-1 alpha-2), `currency` (ISO 4217), `name`.

Relations: `Country 1..* Event 1..* Value`. The first 3 digits of
`event_id` are the ISO 3166-1 **numeric** country code (840 = USA,
978 = EUR, 392 = JPY), the remaining digits are an internal MQL5
counter.

## Time semantics — pay attention here

All calendar function arguments and `MqlCalendarValue::time` /
`MqlCalendarValue::period` are in the **broker-server timezone**
(`TimeTradeServer()`), not local time and not UTC. **There is no need
to convert** when comparing event times against `TimeTradeServer()` or
against other events from the same broker. If the broker's server
follows DST (e.g. EET switching between GMT+2 winter and GMT+3
summer), the calendar automatically tracks the switch — so an event
scheduled at "server 16:30 winter" will show as "server 15:30 summer"
even if the wall-clock moment is unchanged. The article devotes one
of its six anti-patterns to this point.

In the strategy tester, `TimeTradeServer()` returns the model time
identical to the historical data — so the same time-comparison logic
works in both modes.

## Multi-level filter sieve

Calendar publishes 60–90 events daily. Trading on each one is a
sure way to overtrade. The article's filter reduces the stream by
~90% to 3–5 high-signal events:

1. **Currency** — at the API call (`CalendarValueHistory(..., "USD")`).
   `MqlCalendarValue` does NOT carry `currency_id`; the filter is
   applied by the terminal itself.
2. **Importance** — `ENUM_CALENDAR_EVENT_IMPORTANCE::CALENDAR_IMPORTANCE_HIGH`.
   The `LOW` and `MODERATE` events are the noise.
3. **Event code** — even among HIGH events, ECB / IMF speeches are
   algorithmically harder than CPI / NFP / FOMC rate decisions. Use
   a tier-1 list like `NONFARM, CPI, GDP, RATE, FOMC, ECB_RATE,
   RETAIL_SALES, UNEMPLOYMENT, PMI_MANUFACTURING` and substring-match
   against `MqlCalendarEvent.event_code`.
4. **Time window** — typical settings: 15–30 min before release
   (close positions), 60 min after (analyze volatility).

## `LONG_MIN` and unset fields

`MqlCalendarValue.actual_value` / `prev_value` /
`revised_prev_value` / `forecast_value` are all `long` × 10⁶ — and
they can be unset. The MQL5 convention is **`LONG_MIN`
(-9,223,372,036,854,775,808) means "no value published yet"**. The
convenience methods `HasActualValue()` / `GetActualValue()` hide this
on the MQL5 side (the latter returns `NaN`); on the binary-file
side you must mask before dividing by 10⁶ or you will see
`-9_223_372_036.85...` and compare it against real forecasts. Our
`parse_mql_calendar_bin.py` decodes `LONG_MIN → NaN` and divides the
rest by 10⁶ at read time, so the DataFrame matches the MQL5 docs'
description.

## Six anti-patterns (article §"Analysis of typical mistakes")

These are the patterns the article says lose deposits:

1. **"Calendar predicts direction"** — wrong. Calendar tells you
   *when* volatility comes, not which way. Use it as a risk
   filter (`IsHighImpactNewsComingSoon(30) → reduce size or pause`),
   not as an entry signal (`actual > forecast → buy`).
2. **"All HIGH events are equal"** — wrong. `CALENDAR_IMPORTANCE_HIGH`
   is a subjective editor label. NFP moves USD 80–150 pips, EU
   Manufacturing PMI moves EUR 10–30 pips. Always combine the
   importance filter with a tier-1 event-code list.
3. **"`TimeLocal()` instead of `TimeTradeServer()`"** — wrong. The
   calendar is in server time. Mixing with local time gives you a
   1-hour offset on EET-style brokers and the EA will miss the news.
4. **"Assuming value fields are always set"** — wrong. Unset fields
   are `LONG_MIN`. Always check `HasActualValue()` / `MathIsNaN()`
   before using the value.
5. **"Calling calendar API in `OnTick()`"** — wrong. Rate limits
   (5204 `ERR_CALENDAR_TOO_MANY_REQUESTS`) will block you. Load
   once in `OnInit`, incrementally refresh in `OnTimer` (5–10 min
   interval), read the local cache in `OnTick`.
6. **"Forgetting to recompile after updating the `.bin`"** — wrong.
   The `#resource` directive bakes the data into the `.ex5` at
   compile time. Touching the `.bin` afterwards has no effect until
   you press F7.

## Performance numbers from the article's stress test

| Filter set | Fetched | Kept | File size | Time |
|---|---|---|---|---|
| USD, HIGH, all events, all history | 53,346 | 9,009 | 1,153,152 B | 1.80 s |
| USD+EUR+JPY, HIGH, all events, all history | 117,392 | 11,048 | 1,414,144 B | 2.68 s |
| USD, HIGH, NONFARM only | 53,346 | 473 | 60,544 B | 0.09 s |

The local files in `outputs/` differ slightly from these numbers
because the article's stress test used a different `event_code`
filter set; the same `MqlCalendarValue[] → FileWriteArray` mechanism
is in use.

## File inventory

| Path | Purpose | In git? |
|---|---|---|
| `*.html` | The article as downloaded | no (`.gitignore` excludes it) |
| `*_files/` | Browser-cached images referenced by the HTML | no |
| `22196-attaches/CalendarEventMonitor-EA.mq5` | EA demonstrating `OnTimer`-driven `CalendarValueLast` updates | yes |
| `22196-attaches/GetTodayEvents-S.mq5` | Script that fetches today's events for USD | yes |
| `22196-attaches/ExportCalendarForTester-S.mq5` | Script that exports filtered events to a binary file (the one that produces `*.bin` in `outputs/`) | yes |
| `22196-attaches/ImportCalendarValidation-EA.mq5` | EA that consumes the binary via `#resource` and switches between tester / live mode | yes |
| `22196-attaches/ImportTesterLog.txt` | Tester log fragment from the article's validation run | yes |
| `22196-attaches/FullLiveLog.txt` | Full live-mode log (368 KB) | yes |
| `outputs/USD_calendar_test_res*.bin` | Exported binaries (excluded by `.gitignore`) | no |
| `README.md` | This file | yes |
| `.gitignore` | Excludes the article HTML, its browser-cached images, and the `outputs/` directory | yes |

## Where to read the source

The full MQL5 code is in `22196-attaches/`. The article's body is
the saved HTML at the top of this directory (read it with
`lynx -dump file.html | head -200` or in a browser — git ignores it
because it is 250 KB of page chrome plus the body).

The schema reference lives at
`../../skills/mql5/references/quick-ref-mql5-economic-calendar.md`
and the offline reader at
`../../skills/mql5/scripts/parse_mql_calendar_bin.py`.