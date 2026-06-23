# Create

Creates the indicator with specified parameters. Use [Refresh()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorrefresh) and [GetData()](/en/docs/standardlibrary/technicalindicators/cindicators/cindicator/cindicatorgetdata) to update and get the indicator values.

```
bool  Create(
   string           symbol,            // symbol
   ENUM_TIMEFRAMES  period,            // period
   int              tenkan_sen,        // period of TenkanSen
   int              kijun_sen,         // period of KijunSen
   int              senkou_span_b      // period of SenkouSpanB
   )

```

Parameters

symbol

[in]  Symbol.

period

[in]  Timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

tenkan_sen

[in]  Period of TenkanSen.

kijun_sen

[in]  Period of KijunSen.

senkou_span_b

[in]  Period of SenkouSpanB.

Return Value

true - successful, false - cannot create the indicator.
