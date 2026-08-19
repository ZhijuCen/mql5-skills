# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           symbol,         // symbol
   ENUM_TIMEFRAMES  period,         // period
   int              cmo_period,     // momentum period
   int              ema_period,     // averaging period
   int              ind_shift,      // shift
   int              applied         // price type, handle
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

cmo_period

[in]  Momentum period.

ema_period

[in]  Averaging period.

ind_shift

[in]  Horizontal shift.

applied

[in]  Price type or handle to apply.

Return Value

true - successful, false - cannot create the indicator.
