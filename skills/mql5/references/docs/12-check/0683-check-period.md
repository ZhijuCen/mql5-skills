# Period

Returns the current chart timeframe.

```
ENUM_TIMEFRAMES  Period();

```

Return Value

The contents of the [_Period](/en/docs/predefined/_period) variable that contains the value of the current chart timeframe. The value can be one of the values of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration.

Note

Unlike Expert Advisors, indicators and scripts, services are not bound to a specific chart. Therefore, [Period()](/en/docs/check/period) returns 0 for a service.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the timeframe value of the current chart and its description
   ENUM_TIMEFRAMES period    = Period();
   string          timeframe = StringSubstr(EnumToString(period), 7);
   
//--- send the obtained data to the journal
   PrintFormat("Current chart timeframe: %s\nTimeframe value: %s (%d)",
               timeframe, EnumToString(period), period);
   /*
   result:
   Current chart timeframe: H4
   Timeframe value: PERIOD_H4 (16388)
   */
  }

```

See also

[PeriodSeconds](/en/docs/common/periodseconds), [Chart timeframes](/en/docs/constants/chartconstants/enum_timeframes), [Date and Time](/en/docs/dateandtime), [Visibility of objects](/en/docs/constants/objectconstants/visible)
