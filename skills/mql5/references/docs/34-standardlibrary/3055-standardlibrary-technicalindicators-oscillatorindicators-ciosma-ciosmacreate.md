# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           symbol,              // symbol
   ENUM_TIMEFRAMES  period,              // period
   int              fast_ema_period,     // fast EMA period
   int              slow_ema_period,     // slow EMA period
   int              signal_period,       // signal line period
   int              applied              // price type, handle
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

fast_ema_period

[in]  Fast EMA averaging period.

slow_ema_period

[in]  Slow EMA averaging period.

signal_period

[in]  Signal line averaging period.

applied

[in]  Price type or handle to apply.

Return Value

true - successful, false - cannot create the indicator.
