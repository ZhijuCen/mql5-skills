# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           symbol,        // symbol
   ENUM_TIMEFRAMES  period,        // period
   int              ma_period,     // averaging period
   int              ma_shift,      // shift
   double           deviation,     // deviation
   int              applied        // applied price, handle
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

ma_period

[in]  Averaging period.

ma_shift

[in]  Horizontal shift of the indicator.

deviation

[in]  Deviation.

applied

[in]  Price type or handle to apply.

Return Value

true - successful, false - cannot create the indicator.
