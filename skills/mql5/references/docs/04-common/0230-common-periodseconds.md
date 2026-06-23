# PeriodSeconds

This function returns number of seconds in a period.

```
int  PeriodSeconds(
   ENUM_TIMEFRAMES  period=PERIOD_CURRENT      // chart period
   );

```

Parameters

period=PERIOD_CURRENT

[in]  Value of a chart period from the enumeration [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes). If the parameter isn't specified, it returns the number of seconds of the current chart period, at which the program runs.

Return Value

Number of seconds in a selected period.

Example:

```
//--- input parameters
input ENUM_TIMEFRAMES InpPeriod1 = PERIOD_CURRENT;   // First Period
input ENUM_TIMEFRAMES InpPeriod2 = PERIOD_M1;        // Second Period
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the number of seconds in the InpPeriod1 and InpPeriod2 chart periods
   int sec1=PeriodSeconds(InpPeriod1);
   int sec2=PeriodSeconds(InpPeriod2);
//--- display the received values in the log
   PrintFormat("Seconds in period %s: %lu, in period %s: %lu",TimeframeDescription(InpPeriod1),sec1,TimeframeDescription(InpPeriod2),sec2);
//--- calculate how many bars of the InpPeriod2 chart period are contained in a bar with the chart period of InpPeriod1
   int res=sec1/sec2;
   if(res==0)
      res=1;
//--- display the obtained value in the log
   PrintFormat("One bar %s contains %d bars %s",TimeframeDescription(InpPeriod1),res,TimeframeDescription(InpPeriod2));
   /*
   Result:
   Seconds in period M5: 300, in period M1: 60
   One bar M5 contains 5 bars M1
   */
  }
//+------------------------------------------------------------------+
//| Return the timeframe name                                        |
//+------------------------------------------------------------------+
string TimeframeDescription(const ENUM_TIMEFRAMES period)
  {
   return(StringSubstr(EnumToString(period==PERIOD_CURRENT ? Period() : period), 7));
  }

```

See also

[_Period](/en/docs/predefined/_period), [Chart timeframes](/en/docs/constants/chartconstants/enum_timeframes), [Date and Time](/en/docs/dateandtime), [Visibility of objects](/en/docs/constants/objectconstants/visible)
