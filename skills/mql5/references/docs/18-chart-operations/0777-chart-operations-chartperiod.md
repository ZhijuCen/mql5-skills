# ChartPeriod

Returns the timeframe [period](/en/docs/constants/chartconstants/enum_timeframes) of specified chart.

```
ENUM_TIMEFRAMES  ChartPeriod(
   long  chart_id=0      // Chart ID
   );

```

Parameters

chart_id=0

[in]  Chart ID. 0 means the current chart.

Return Value

The function returns one of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) values. If chart does not exist, it returns 0.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the current chart period and display the obtained value in the journal
   ENUM_TIMEFRAMES period=ChartPeriod();
   Print("Current chart period: ", EnumToString(period));
   
//--- take the existing (in this case, the current) chart ID
   long chart_id=ChartID();
   period=ChartPeriod(chart_id);
   PrintFormat("Chart period with ID %I64d: %s", chart_id, EnumToString(period));
   
//--- set a random chart ID
   period=ChartPeriod(1234567890);
   if(period==0)
      Print("The chart with ID 1234567890 does not exist");
   else
      Print("Chart period with ID 1234567890: ", EnumToString(period));
   /*
   result:
   Current chart period: PERIOD_M15
   Chart period with ID 133510090240498505: PERIOD_M15
   The chart with ID 1234567890 does not exist
   */
  }

```
