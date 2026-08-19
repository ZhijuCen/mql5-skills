# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string               symbol,             // symbol
   ENUM_TIMEFRAMES      period,             // period
   int                  fast_ma_period,     // fast EMA period
   int                  slow_ma_period,     // slow EMA period
   ENUM_MA_METHOD       ma_method,          // averaging method
   ENUM_APPLIED_VOLUME  applied             // volume type
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

fast_ma_period

[in]  Period for fast EMA.

slow_ma_period

[in]  Period for slow EMA.

ma_method

[in]  Averaging method ([ENUM_MA_METHOD](/en/docs/constants/indicatorconstants/enum_ma_method) enumeration value).

applied

[in]  Object (volume type) to apply ([ENUM_APPLIED_VOLUME](/en/docs/constants/indicatorconstants/prices#enum_applied_volume_enum) enumeration value).

Return Value

true - successful, false - cannot create the indicator.
