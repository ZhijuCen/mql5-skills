# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           string,        // symbol
   ENUM_TIMEFRAMES  period,        // period
   int              ma_period,     // averaging period
   int              ma_shift,      // shift
   ENUM_MA_METHOD   ma_method,     // averaging method
   int              applied        // price type, handle
   )

```

Parameters

string

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

ma_period

[in]  Averaging period.

ma_shift

[in]  Horizontal shift.

ma_method

[in]  Averaging method ([ENUM_MA_METHOD](/en/docs/constants/indicatorconstants/enum_ma_method) enumeration value).

applied

[in]  Price type or handle to apply.

Return Value

true - successful, false - cannot create the indicator.
