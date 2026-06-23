# ChartSetString

Sets a value for a corresponding property of the specified chart. Chart property must be of the string type. The command is added to chart messages queue and will be executed after processing of all previous commands.

```
bool  ChartSetString(
   long                         chart_id,    // Chart ID
   ENUM_CHART_PROPERTY_STRING   prop_id,     // Property ID
   string                       str_value    // Value
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

prop_id

[in]  Chart property ID. Its value can be one of the [ENUM_CHART_PROPERTY_STRING](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_string) values (except the read-only properties).

str_value

[in]  Property value string. String length cannot exceed 2045 characters (extra characters will be truncated).

Return Value

Returns true if the command has been added to chart queue, otherwise false. To get an information about the [error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

ChartSetString can be used for a comment output on the chart instead of the [Comment](/en/docs/common/comment) function.

The function is asynchronous, which means that the function does not wait for the execution of the command, which has been successfully added to the queue of specified the chart. Instead, it immediately returns control. The property will only change after the handling of the appropriate command from the chart queue. To immediately execute commands from the chart queue, call the [ChartRedraw](/en/docs/chart_operations/chartredraw) function.

If you want to immediately change several chart properties at once, then the corresponding functions ([ChartSetString](/en/docs/chart_operations/chartsetstring), [ChartSetDouble](/en/docs/chart_operations/chartsetdouble), [ChartSetString](/en/docs/chart_operations/chartsetstring)) should be executed in one code block, after which you should call [ChartRedraw](/en/docs/chart_operations/chartredraw) once.

To check the command execution result, you can use a function, which requests the specified chart property ([ChartGetInteger](/en/docs/chart_operations/chartgetinteger), [ChartGetDouble](/en/docs/chart_operations/chartgetdouble), [ChartSetString](/en/docs/chart_operations/chartsetstring)). However, note that these functions are synchronous and wait for execution results.

Example:

```
void OnTick()
  {
//---
   double Ask,Bid;
   int Spread;
   Ask=SymbolInfoDouble(Symbol(),SYMBOL_ASK);
   Bid=SymbolInfoDouble(Symbol(),SYMBOL_BID);
   Spread=SymbolInfoInteger(Symbol(),SYMBOL_SPREAD);
   string comment=StringFormat("Display prices:\nAsk = %G\nBid = %G\nSpread = %d",
                               Ask,Bid,Spread);
   ChartSetString(0,CHART_COMMENT,comment);
  }

```

See also

[Comment](/en/docs/common/comment), [ChartGetString](/en/docs/chart_operations/chartgetstring)
