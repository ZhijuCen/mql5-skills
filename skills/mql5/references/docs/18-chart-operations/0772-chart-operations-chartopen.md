# ChartOpen

Opens a new chart with the specified symbol and period.

```
long  ChartOpen(
   string           symbol,     // Symbol name
   ENUM_TIMEFRAMES  period      // Period
   );

```

Parameters

symbol

[in]  Chart symbol. [NULL](/en/docs/basis/types/void) means the symbol of the  current chart (the Expert Advisor is attached to).

period

[in]  Chart period (timeframe). Can be one of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) values. 0 means the current chart period.

Return Value

If successful, it returns the opened chart ID. Otherwise returns 0.

Note

The maximum possible number of simultaneously open charts in the terminal can't exceed the [CHARTS_MAX](/en/docs/constants/namedconstants/otherconstants) value.

Example:

```
#define CHART_SYMBOL  NULL
#define CHART_PERIOD  PERIOD_CURRENT
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set a new chart symbol and timeframe
   string symbol=CHART_SYMBOL;
   if(symbol==NULL)
      symbol=Symbol();
   ENUM_TIMEFRAMES timeframe = (CHART_PERIOD==PERIOD_CURRENT ? Period() : CHART_PERIOD);
   
//--- open a new chart with the specified symbol and period
   long chart_id=ChartOpen(symbol, timeframe);
   if(chart_id==0)
     {
      Print("ChartOpen() failed. Error ", GetLastError());
      return;
     }
 
//--- print open chart parameters in the journal
   PrintFormat("A new chart of the %s symbol has been opened with a period of %s and ChartID %I64u",
               symbol, StringSubstr(EnumToString(timeframe), 7), chart_id);
   /*
   result:
   A new chart of the GBPUSD symbol has been opened with a period of M1 and ChartID 133346697706632016
   */
  }

```
