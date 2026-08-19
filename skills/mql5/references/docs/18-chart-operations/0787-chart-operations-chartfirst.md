# ChartFirst

Returns the ID of the first chart of the client terminal.

```
long  ChartFirst();

```

Return Value

Chart ID.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the ID of the very first chart opened in the client terminal
   long            chart_id= ChartFirst();
   
//--- additionally get the chart symbol and period using the obtained ID
   string          symbol  = ChartSymbol(chart_id);
   ENUM_TIMEFRAMES period  = ChartPeriod(chart_id);
   
//--- display the description of the client terminal first chart in the journal
   PrintFormat("ID of the first chart of the client terminal: %I64d, chart symbol: %s, chart period: %s", chart_id, symbol, StringSubstr(EnumToString(period), 7));
   /*
   result:
   ID of the first chart of the client terminal: 133246248352168440, chart symbol: EURUSD, chart period: M1
   */
  }

```
