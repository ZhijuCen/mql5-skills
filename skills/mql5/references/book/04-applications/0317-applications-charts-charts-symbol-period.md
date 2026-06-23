# Getting the symbol and timeframe of an arbitrary chart

Two fundamental properties of any chart are its working symbol and timeframe. As we saw earlier, these properties for the current chart are available as built-in variables _Symbol and _Period, as well as through the relevant functions [Symbol](/en/book/applications/charts/charts_main_properties)[ and ](/en/book/applications/charts/charts_main_properties)[Period](/en/book/applications/charts/charts_main_properties). The following functions can be used to determine the same properties for other charts: ChartSymbol and ChartPeriod.

string ChartSymbol(long chartId = 0)

The function returns the name of the symbol of the chart with the specified identifier. If the parameter is 0, the current chart is assumed.

If the chart does not exist, an empty string ("") is returned and _LastError sets error code ERR_CHART_WRONG_ID (4101).

ENUM_TIMEFRAMES ChartPeriod(long chartId = 0)

The function returns the period value for the chart with the specified identifier.

If the chart does not exist, 0 is returned.

The script ChartList2.mq5, similar to ChartList1.mq5, generates a list of charts indicating the symbol and timeframe.

```
#include <MQL5Book/Periods.mqh>
   
void OnStart()
{
   ChartList();
}
   
void ChartList()
{
   const long me = ChartID();
   long id = ChartFirst();
   int count = 0;
   
   Print("Chart List\nN, ID, Symbol, TF, *active");
   // keep iterating over charts until there are none left
   while(id != -1)
   {
      const string header = StringFormat("%d %lld %s %s %s",
         count, id, ChartSymbol(id), PeriodToString(ChartPeriod(id)),
         (id == me ? " *" : ""));
    
      // fields: N, id, symbol, timeframe, label of the current chart
      Print(header);
      count++;
      id = ChartNext(id);
   }
   Print("Total chart number: ", count);
}

```

Here is an example of the log content after running the script on the EURUSD, H1 chart (on the second line).

```
Chart List
N, ID, Symbol, TF, *active
0 132358585987782873 EURUSD M15 
1 132360375330772909 EURUSD H1  *
2 132544239145024745 XAUUSD H1 
3 132544239145024732 USDRUB D1 
4 132544239145024744 EURUSD H1 
Total chart number: 5

```

MQL5 allows not only to identify but also to [switch the symbol and timeframe](/en/book/applications/charts/charts_set_symbol_period) of any chart.
