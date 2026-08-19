# Create

# Creates a timeseries with the specified parameters for access to the tick volumes of the bars in the history.

```
bool  Create(
   string           symbol,     // symbol
   ENUM_TIMEFRAMES  period      // period
   )

```

Parameters

symbol

[in]  Timeseires symbol.

period

[in]  Timeseries timeframe ([ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration value).

Return Value

true - successful, false - cannot create a timeseries.
