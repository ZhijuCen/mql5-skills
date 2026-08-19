# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           symbol,      // symbol
   ENUM_TIMEFRAMES  period,      // period
   double           step,        // step
   double           maximum      // coefficient
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

step

[in]  Step for the velocity increasing.

maximum

[in]  Price following coefficient.

Return Value

true - successful, false - cannot change the indicator.
