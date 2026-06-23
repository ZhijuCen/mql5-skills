# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           symbol,          // symbol
   ENUM_TIMEFRAMES  period,          // period
   int              Kperiod,         // %K period
   int              Dperiod,         // %D period
   int              slowing,         // slowing period
   ENUM_MA_METHOD   ma_method,       // averaging method
   ENUM_STO_PRICE   price_field      // application
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

Kperiod

[in]  Averaging period of %K indicator.

Dperiod

[in]  Averaging period of %D indicator.

slowing

[in]  Slowing period.

ma_method

[in]  Averaging method ([ENUM_MA_METHOD](/en/docs/constants/indicatorconstants/enum_ma_method) enumeration value).

price_field

[in]  Object (Low/High or Close/Close) to apply ([ENUM_STO_PRICE](/en/docs/constants/indicatorconstants/prices) enumeration value).

Return Value

true - successful, false - cannot create the indicator.
