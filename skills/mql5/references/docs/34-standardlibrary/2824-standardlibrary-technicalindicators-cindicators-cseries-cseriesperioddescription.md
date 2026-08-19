# PeriodDescription

Gets the string representation of the specified [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration.

```
string  PeriodDescription(
   const int  val=0      // value
   )

```

Parameters

val=0

[in]  Value to convert.

Return Value

The string representation of the specified [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration.

Note

If the value is not specified or equal to zero,the timeframe of timeseries or indicator is transformed into a string.
