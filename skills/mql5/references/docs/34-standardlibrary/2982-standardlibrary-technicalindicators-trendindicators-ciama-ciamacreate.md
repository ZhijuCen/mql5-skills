# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           string,              // symbol
   ENUM_TIMEFRAMES  period,              // period
   int              ma_period,           // averaging period
   int              fast_ema_period,     // fast EMA period
   int              slow_ema_period,     // slow EMA period
   int              ind_shift,           // shift
   int              applied              // price type, handle
   )

```

Parameters

string

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

ma_period

[in]  Averaging period.

fast_ema_period

[in]  Fast EMA averaging period.

slow_ema_period

[in]  Slow EMA averaging period.

ind_shift

[in]  Horizontal shift.

applied

[in]  Price type or handle to apply.

Return Value

true - successful, false - cannot create the indicator.
