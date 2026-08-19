# ChartID

Returns the ID of the current chart.

```
long  ChartID();

```

Return Value

Value of [long](/en/docs/basis/types/integer/integertypes) type.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- variables for chart identifiers
   long curr_chart=ChartFirst();
   int i=0;
   //--- print the first chart data in the journal
   PrintFormat("Chart[%d] ID: %I64d,  symbol: %s", i, curr_chart, ChartSymbol(curr_chart));
   
//--- until the open chart limit is reached (CHARTS_MAX)
   while(!IsStopped() && i < CHARTS_MAX)
     {
      //--- increase the chart counter
      i++;
      //--- get the next chart ID based on the previous one
      curr_chart=ChartNext(curr_chart);
      
      //--- terminate the loop if the end of the chart list is reached
      if(curr_chart<0)
         break;
         
      //--- print the next chart data in the journal
      PrintFormat("Chart[%d] ID: %I64d,  symbol: %s", i, curr_chart, ChartSymbol(curr_chart));
     }
   /*
   result:
   Chart[0] ID: 133246248352168440,  symbol: EURUSD
   Chart[1] ID: 133346697706632015,  symbol: USDJPY
   Chart[2] ID: 133246248352168439,  symbol: GBPUSD
   Chart[3] ID: 133346697706632009,  symbol: RU000A103661
   Chart[4] ID: 133346697706632010,  symbol: AEM4
   Chart[5] ID: 133346697706632011,  symbol: AA.SPB
   Chart[6] ID: 133346697706632012,  symbol: ALLFUTMIX
   Chart[7] ID: 133346697706632013,  symbol: EURUSD
   Chart[8] ID: 133346697706632014,  symbol: SBER
   */
  }

```
