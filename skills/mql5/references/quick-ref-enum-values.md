# Quick Ref — Enum Values for `*.ini` / `*.set`

Companion to `quick-ref-tester-automation.md` §2. MQL5 `enum` inputs are
serialized as **integers** in `[TesterInputs]` and in `.set` files. The
MQL5 identifier (`PERIOD_H1`) and the short name (`H1`) are **not**
interchangeable with that integer.

## 1. The timeframe trap — read this first

`ENUM_TIMEFRAMES` is the highest-risk enum to hand-fill. An invalid
value is not necessarily rejected when the config is loaded. The tester
may instead keep trying to synchronize market data for a timeframe that
does not exist; the run never reaches the test and looks like a hang,
not an error. `mql5_helper.py tester` then exits **2** (timeout, default
`--timeout 3600` s) with no report. If a run stalls before `automatic
testing started`, check every timeframe value before doing anything
else.

The four common wrong forms:

| Written value | Why it is wrong | Correct value for H1 |
|---------------|-----------------|----------------------|
| `PERIOD_H1` | MQL5 source identifier, not an INI/SET token | `16385` |
| `H1` | short name; valid only in `[Tester] Period=`, not in `[TesterInputs]`/`.set` | `16385` |
| `60` | MQL4 minutes convention | `16385` |
| `240` / `1440` / `10080` / `43200` | MQL4 H4/D1/W1/MN1 minutes | `16388` / `16408` / `32769` / `49153` |

MQL5 timeframes are **not minutes** above M30:

- minute timeframes: the value is the minute count (`M15` = 15);
- hourly timeframes: `0x4000 | hours` (`H1` = 16385, `H4` = 16388);
- `D1` = `0x4000 | 24` = 16408;
- `W1` = `0x8000 | 1` = 32769;
- `MN1` = `0xC000 | 1` = 49153.

`PERIOD_CURRENT` = **0**. It is valid in MQL5 source and means "the
chart's current period". In a tester input it therefore means "use the
`[Tester] Period=` timeframe", not a concrete timeframe. Use 0 only
deliberately.

### ENUM_TIMEFRAMES — complete table

| Identifier | Value | Hex | Meaning | `[Tester] Period=` |
|------------|------:|-----|---------|--------------------|
| `PERIOD_CURRENT` | 0 | 0x0 | current chart period | — |
| `PERIOD_M1` | 1 | 0x1 | 1 minute | `M1` |
| `PERIOD_M2` | 2 | 0x2 | 2 minutes | `M2` |
| `PERIOD_M3` | 3 | 0x3 | 3 minutes | `M3` |
| `PERIOD_M4` | 4 | 0x4 | 4 minutes | `M4` |
| `PERIOD_M5` | 5 | 0x5 | 5 minutes | `M5` |
| `PERIOD_M6` | 6 | 0x6 | 6 minutes | `M6` |
| `PERIOD_M10` | 10 | 0xA | 10 minutes | `M10` |
| `PERIOD_M12` | 12 | 0xC | 12 minutes | `M12` |
| `PERIOD_M15` | 15 | 0xF | 15 minutes | `M15` |
| `PERIOD_M20` | 20 | 0x14 | 20 minutes | `M20` |
| `PERIOD_M30` | 30 | 0x1E | 30 minutes | `M30` |
| `PERIOD_H1` | 16385 | 0x4001 | 1 hour | `H1` |
| `PERIOD_H2` | 16386 | 0x4002 | 2 hours | `H2` |
| `PERIOD_H3` | 16387 | 0x4003 | 3 hours | `H3` |
| `PERIOD_H4` | 16388 | 0x4004 | 4 hours | `H4` |
| `PERIOD_H6` | 16390 | 0x4006 | 6 hours | `H6` |
| `PERIOD_H8` | 16392 | 0x4008 | 8 hours | `H8` |
| `PERIOD_H12` | 16396 | 0x400C | 12 hours | `H12` |
| `PERIOD_D1` | 16408 | 0x4018 | 1 day | `D1` |
| `PERIOD_W1` | 32769 | 0x8001 | 1 week | `W1` |
| `PERIOD_MN1` | 49153 | 0xC001 | 1 month | `MN1` |

**Valid integer set** (excluding 0 = current):

```text
1 2 3 4 5 6 10 12 15 20 30
16385 16386 16387 16388 16390 16392 16396 16408 32769 49153
```

Any other integer — `7`, `8`, `9`, `11`, `13`, `14`, `60`, `240`,
`1440`, `16389`, `16400`, … — is not a timeframe. There is no `H5`,
`H24`, `M7`, or `M60`.

## 2. Where each form goes

| File / section | Field | Accepted form | Example |
|----------------|-------|---------------|---------|
| `.ini` `[Tester]` | `Period=` | short name | `Period=M15` |
| `.ini` `[TesterInputs]` | enum input | integer, 5-field line | `InpTF=16385\|\|16385\|\|0\|\|16385\|\|N` |
| `.set` | enum input | integer, 5-field line | `InpTF=16385\|\|16385\|\|0\|\|16385\|\|N` |
| `.ini` / `.set` | string input, `sinput` | bare `name=value` | `InpName=MyEA` |
| `.ini` / `.set` | bool input | `true`/`false`, step 0 | `InpUse=true\|\|true\|\|0\|\|true\|\|N` |

`.set` / `[TesterInputs]` line shape:

```text
name=value||start||step||stop||Y|N
```

- `value` is the number used when the flag is `N` (single test). The
  other three fields are the optimization range and are ignored for `N`.
- Enums and bools use **step 0**. Do not invent a numeric step for an
  enum; the tester enumerates the enum's declared members between
  `start` and `stop`.
- `Y` switches that input into optimization. For `ENUM_TIMEFRAMES`,
  `start`/`stop` must be valid members, and the pass count should be
  checked. For a one-off backtest, keep `N`.
- MT5's own export may write `value||0||0||last_member||N`; the first
  field is what matters for a single test.

`init-ini` writes enum identifiers verbatim and adds a
`; TODO: ... replace with the numeric enum/datetime value` comment.
Those lines are **not ready to run** until the identifier is replaced.

### Before / after

```ini
; WRONG — none of these is the numeric form the field expects
; [Tester] Period wants the short name, not the enum integer:
Period=16385
; [TesterInputs]/SET want the integer, not the MQL5 identifier:
InpTF=PERIOD_H1
; ... nor the short name:
InpTF=H1
; ... nor MQL4 minutes; an enum step is 0, not 1:
InpTF=60||60||1||60||N

; RIGHT
[Tester]
Period=H1

[TesterInputs]
; InpTF = PERIOD_H1, InpMethod = MODE_EMA, InpPrice = PRICE_CLOSE
InpTF=16385||16385||0||16385||N
InpMethod=1||1||0||1||N
InpPrice=1||1||0||1||N
```

Comments must be on their own lines: an inline `; ...` after a value
becomes part of the value in MT5's INI parser.

## 3. Indicator-input enums

### ENUM_MA_METHOD

| Identifier | Value | Meaning |
|------------|------:|---------|
| `MODE_SMA` | 0 | Simple averaging |
| `MODE_EMA` | 1 | Exponential averaging |
| `MODE_SMMA` | 2 | Smoothed averaging |
| `MODE_LWMA` | 3 | Linear-weighted averaging |

### ENUM_APPLIED_PRICE — 1-based, not 0-based

| Identifier | Value | Meaning |
|------------|------:|---------|
| `PRICE_CLOSE` | **1** | Close price |
| `PRICE_OPEN` | 2 | Open price |
| `PRICE_HIGH` | 3 | High |
| `PRICE_LOW` | 4 | Low |
| `PRICE_MEDIAN` | 5 | (high + low) / 2 |
| `PRICE_TYPICAL` | 6 | (high + low + close) / 3 |
| `PRICE_WEIGHTED` | 7 | (high + low + close + close) / 4 |

This is another common trap. `0` is **not** `PRICE_CLOSE`; it is not a
valid applied price.

### ENUM_APPLIED_VOLUME

| Identifier | Value |
|------------|------:|
| `VOLUME_TICK` | 0 |
| `VOLUME_REAL` | 1 |

### ENUM_STO_PRICE

| Identifier | Value |
|------------|------:|
| `STO_LOWHIGH` | 0 |
| `STO_CLOSECLOSE` | 1 |

## 4. Trading-input enums

### ENUM_POSITION_TYPE

| Identifier | Value |
|------------|------:|
| `POSITION_TYPE_BUY` | 0 |
| `POSITION_TYPE_SELL` | 1 |

### ENUM_ORDER_TYPE

| Identifier | Value |
|------------|------:|
| `ORDER_TYPE_BUY` | 0 |
| `ORDER_TYPE_SELL` | 1 |
| `ORDER_TYPE_BUY_LIMIT` | 2 |
| `ORDER_TYPE_SELL_LIMIT` | 3 |
| `ORDER_TYPE_BUY_STOP` | 4 |
| `ORDER_TYPE_SELL_STOP` | 5 |
| `ORDER_TYPE_BUY_STOP_LIMIT` | 6 |
| `ORDER_TYPE_SELL_STOP_LIMIT` | 7 |
| `ORDER_TYPE_CLOSE_BY` | 8 |

### ENUM_ORDER_TYPE_FILLING

| Identifier | Value | Note |
|------------|------:|------|
| `ORDER_FILLING_FOK` | 0 | Fill or Kill |
| `ORDER_FILLING_IOC` | 1 | Immediate or Cancel |
| `ORDER_FILLING_RETURN` | 2 | Return remaining volume |
| `ORDER_FILLING_BOC` | 3 | Book or Cancel; not available on all symbols |

### ENUM_ORDER_TYPE_TIME

| Identifier | Value |
|------------|------:|
| `ORDER_TIME_GTC` | 0 |
| `ORDER_TIME_DAY` | 1 |
| `ORDER_TIME_SPECIFIED` | 2 |
| `ORDER_TIME_SPECIFIED_DAY` | 3 |

### ENUM_TRADE_REQUEST_ACTIONS — gaps, and CLOSE_BY is 10

| Identifier | Value |
|------------|------:|
| `TRADE_ACTION_DEAL` | 1 |
| `TRADE_ACTION_PENDING` | 5 |
| `TRADE_ACTION_SLTP` | 6 |
| `TRADE_ACTION_MODIFY` | 7 |
| `TRADE_ACTION_REMOVE` | 8 |
| `TRADE_ACTION_CLOSE_BY` | **10** |

`0`, `2`, `3`, `4`, and `9` do not correspond to any action. In
particular, `TRADE_ACTION_CLOSE_BY` is **10**, not 9.

### ENUM_DEAL_TYPE

| Identifier | Value | Identifier | Value |
|------------|------:|------------|------:|
| `DEAL_TYPE_BUY` | 0 | `DEAL_TYPE_COMMISSION_AGENT_DAILY` | 10 |
| `DEAL_TYPE_SELL` | 1 | `DEAL_TYPE_COMMISSION_AGENT_MONTHLY` | 11 |
| `DEAL_TYPE_BALANCE` | 2 | `DEAL_TYPE_INTEREST` | 12 |
| `DEAL_TYPE_CREDIT` | 3 | `DEAL_TYPE_BUY_CANCELED` | 13 |
| `DEAL_TYPE_CHARGE` | 4 | `DEAL_TYPE_SELL_CANCELED` | 14 |
| `DEAL_TYPE_CORRECTION` | 5 | `DEAL_DIVIDEND` | 15 |
| `DEAL_TYPE_BONUS` | 6 | `DEAL_DIVIDEND_FRANKED` | 16 |
| `DEAL_TYPE_COMMISSION` | 7 | `DEAL_TAX` | 17 |
| `DEAL_TYPE_COMMISSION_DAILY` | 8 | | |
| `DEAL_TYPE_COMMISSION_MONTHLY` | 9 | | |

### ENUM_DEAL_ENTRY

| Identifier | Value |
|------------|------:|
| `DEAL_ENTRY_IN` | 0 |
| `DEAL_ENTRY_OUT` | 1 |
| `DEAL_ENTRY_INOUT` | 2 |
| `DEAL_ENTRY_OUT_BY` | 3 |

`DEAL_ENTRY_OUT_BY` is 3, not 255 or 4.

### ENUM_DEAL_REASON

| Identifier | Value | Identifier | Value |
|------------|------:|------------|------:|
| `DEAL_REASON_CLIENT` | 0 | `DEAL_REASON_SO` | 6 |
| `DEAL_REASON_MOBILE` | 1 | `DEAL_REASON_ROLLOVER` | 7 |
| `DEAL_REASON_WEB` | 2 | `DEAL_REASON_VMARGIN` | 8 |
| `DEAL_REASON_EXPERT` | 3 | `DEAL_REASON_SPLIT` | 9 |
| `DEAL_REASON_SL` | 4 | | |
| `DEAL_REASON_TP` | 5 | | |

Newer builds may add `DEAL_REASON_CORPORATE_ACTION`; dump the value if
you target it.

### ENUM_ORDER_STATE

| Identifier | Value | Identifier | Value |
|------------|------:|------------|------:|
| `ORDER_STATE_STARTED` | 0 | `ORDER_STATE_REJECTED` | 5 |
| `ORDER_STATE_PLACED` | 1 | `ORDER_STATE_EXPIRED` | 6 |
| `ORDER_STATE_CANCELED` | 2 | `ORDER_STATE_REQUEST_ADD` | 7 |
| `ORDER_STATE_PARTIAL` | 3 | `ORDER_STATE_REQUEST_MODIFY` | 8 |
| `ORDER_STATE_FILLED` | 4 | `ORDER_STATE_REQUEST_CANCEL` | 9 |

## 5. Symbol, account, calendar, and GUI enums

### ENUM_SYMBOL_TRADE_MODE

| Identifier | Value |
|------------|------:|
| `SYMBOL_TRADE_MODE_DISABLED` | 0 |
| `SYMBOL_TRADE_MODE_LONGONLY` | 1 |
| `SYMBOL_TRADE_MODE_SHORTONLY` | 2 |
| `SYMBOL_TRADE_MODE_CLOSEONLY` | 3 |
| `SYMBOL_TRADE_MODE_FULL` | 4 |

### ENUM_SYMBOL_TRADE_EXECUTION

| Identifier | Value |
|------------|------:|
| `SYMBOL_TRADE_EXECUTION_REQUEST` | 0 |
| `SYMBOL_TRADE_EXECUTION_INSTANT` | 1 |
| `SYMBOL_TRADE_EXECUTION_MARKET` | 2 |
| `SYMBOL_TRADE_EXECUTION_EXCHANGE` | 3 |

### ENUM_ACCOUNT_TRADE_MODE

| Identifier | Value |
|------------|------:|
| `ACCOUNT_TRADE_MODE_DEMO` | 0 |
| `ACCOUNT_TRADE_MODE_CONTEST` | 1 |
| `ACCOUNT_TRADE_MODE_REAL` | 2 |

### ENUM_DAY_OF_WEEK

| Identifier | Value |
|------------|------:|
| `SUNDAY` | 0 |
| `MONDAY` | 1 |
| `TUESDAY` | 2 |
| `WEDNESDAY` | 3 |
| `THURSDAY` | 4 |
| `FRIDAY` | 5 |
| `SATURDAY` | 6 |

Note that Sunday is 0, not Monday.

### ENUM_CALENDAR_EVENT_IMPORTANCE

| Identifier | Value |
|------------|------:|
| `CALENDAR_IMPORTANCE_NONE` | 0 |
| `CALENDAR_IMPORTANCE_LOW` | 1 |
| `CALENDAR_IMPORTANCE_MODERATE` | 2 |
| `CALENDAR_IMPORTANCE_HIGH` | 3 |

### ENUM_LINE_STYLE

| Identifier | Value |
|------------|------:|
| `STYLE_SOLID` | 0 |
| `STYLE_DASH` | 1 |
| `STYLE_DOT` | 2 |
| `STYLE_DASHDOT` | 3 |
| `STYLE_DASHDOTDOT` | 4 |

## 6. Pre-flight checklist

Before launching a `.ini`/`.set`:

1. **Timeframes.** Find every timeframe input and confirm its first
   field is in the valid set above. Pay special attention to `60`,
   `240`, `1440`, `10080`, `43200`, `PERIOD_*`, and bare `H1`/`D1`.
2. **Applied price.** Confirm `PRICE_CLOSE` is `1`, not `0`.
3. **Action gaps.** Confirm `TRADE_ACTION_CLOSE_BY` is `10` and no
   action uses 0, 2, 3, 4, or 9.
4. **Single test vs optimization.** For a single test every flag is
   `N` and `[Tester] Optimization=0`. `Y` without `Optimization=1/2`
   is a mismatch.
5. **Identifiers.** Search for `PERIOD_`, `MODE_`, `PRICE_`, `ORDER_`,
   `DEAL_`, `TRADE_ACTION_` in the numeric fields. Any remaining
   identifier is a `TODO`, not a value.
6. **Dry run.** `python skills/mql5/scripts/mql5_helper.py tester INI
   --dry-run` validates required keys and the `.ex5`, but it does
   **not** validate enum values — do steps 1–5 manually.

### Verify a candidate value against the installed build

The most reliable check is the terminal itself. Export a `.set` from the
tester Inputs tab for the EA: MT5 writes the numeric value it expects.
Alternatively, compile a tiny script and read the Experts journal:

```mql5
void OnStart()
  {
   Print("H1=", (int)PERIOD_H1);                       // 16385
   Print("60=", EnumToString((ENUM_TIMEFRAMES)60));    // ENUM_TIMEFRAMES::60
  }
```

`EnumToString` returns a `TYPE::value` string for an out-of-range
number. So a timeframe is valid exactly when
`StringFind(EnumToString((ENUM_TIMEFRAMES)v), "::") < 0`. Use the same
round-trip check for any other enum before putting its number into a
config file.

### If a run stalls

- `tester` exit code 2 (timeout) with no report is the signature.
- The journal may show repeated history synchronization and never reach
  `automatic testing started` / `last test passed`.
- Stop the launched process group (the helper does this on timeout),
  fix the timeframe value, and rerun. Do not keep waiting for a report
  that cannot appear.

## Sources

- `docs/01-constants/0087-constants-chartconstants-enum-timeframes.md`
  — `ENUM_TIMEFRAMES` identifiers.
- `book/04-applications/0261-applications-timeseries-timeseries-symbol-period.md`
  — timeframe numeric values and bit encoding.
- `docs/01-constants/0147-constants-indicatorconstants-prices.md`,
  `docs/01-constants/0148-constants-indicatorconstants-enum-ma-method.md`
  — applied price / volume / MA-method identifiers.
- `book/04-applications/0299-applications-indicators-use-indicators-standard.md`
  — applied price / volume / MA-method numeric values.
- `book/05-automation/0421-automation-experts-experts-request-types.md`,
  `book/05-automation/0423-automation-experts-experts-execution-filling.md`,
  `book/05-automation/0424-automation-experts-experts-pending-expiration.md`
  — trade action / filling / order-time identifiers.
- `book/05-automation/0393-automation-symbols-symbols-trade-mode.md`,
  `book/05-automation/0394-automation-symbols-symbols-execution-filling.md`
  — symbol trade mode / execution values.
- `book/01-basis/0024-basis-builtin-types-enums.md`
  — order types and day-of-week values.

Trade enum integers were cross-checked against a live `Print` of the
enum members (`TRADE_ACTION_*`, `DEAL_ENTRY_*`) and the official
MetaTrader5 Python constants. When a build disagrees, the live value
wins; use the `EnumToString` round-trip check above.
