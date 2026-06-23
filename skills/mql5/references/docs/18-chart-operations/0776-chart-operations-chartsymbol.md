# ChartSymbol

Returns the symbol name for the specified chart.

```
string  ChartSymbol(
   long  chart_id=0      // Chart ID
   );

```

Parameters

chart_id=0

[in]  Chart ID. 0 means the current chart.

Return Value

If chart does not exist, the result will be an empty string.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the current chart symbol and display the obtained value in the journal
   string chart_symbol = ChartSymbol();
   Print("Current chart symbol: ", chart_symbol);
   
//--- take the existing (in this case, the current) chart ID
   long chart_id=ChartID();
   chart_symbol=ChartSymbol(chart_id);
   PrintFormat("Chart symbol with ID %I64d: %s", chart_id, chart_symbol);
 
//--- set a random chart ID when receiving a symbol
   chart_symbol = ChartSymbol(1234567890);
   if(chart_symbol=="")
      Print("The chart with ID 1234567890 does not exist");
   else
      Print("Chart symbol with ID 1234567890: ", chart_symbol);
   /*
   result:
   Current chart symbol: GBPUSD
   Chart symbol with ID 132966427583395104: GBPUSD
   The chart with ID 1234567890 does not exist
   */
  }

```

See also

[ChartSetSymbolPeriod](/en/docs/chart_operations/chartsetsymbolperiod)
