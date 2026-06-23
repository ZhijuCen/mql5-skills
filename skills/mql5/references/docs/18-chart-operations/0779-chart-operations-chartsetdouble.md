# ChartSetDouble

Sets a value for a corresponding property of the specified chart. Chart property should be of a [double](/en/docs/basis/types/double) type. The command is added to chart messages queue and will be executed after processing of all previous commands.

```
bool  ChartSetDouble(
   long                           chart_id,     // Chart ID
   ENUM_CHART_PROPERTY_DOUBLE     prop_id,      // Property ID
   double                         value         // Value
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

prop_id

[in]  Chart property ID. Can be one of the [ENUM_CHART_PROPERTY_DOUBLE](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_double) values (except the read-only properties).

value

[in] Property value.

Return Value

Returns true if the command has been added to chart queue, otherwise false. To get an information about the [error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The function is asynchronous, which means that the function does not wait for the execution of the command, which has been successfully added to the queue of specified the chart. Instead, it immediately returns control. The property will only change after the handling of the appropriate command from the chart queue. To immediately execute commands from the chart queue, call the [ChartRedraw](/en/docs/chart_operations/chartredraw) function.

If you want to immediately change several chart properties at once, then the corresponding functions ([ChartSetString](/en/docs/chart_operations/chartsetstring), [ChartSetDouble](/en/docs/chart_operations/chartsetdouble), [ChartSetString](/en/docs/chart_operations/chartsetstring)) should be executed in one code block, after which you should call [ChartRedraw](/en/docs/chart_operations/chartredraw) once.

To check the command execution result, you can use a function, which requests the specified chart property ([ChartGetInteger](/en/docs/chart_operations/chartgetinteger), [ChartGetDouble](/en/docs/chart_operations/chartgetdouble), [ChartSetString](/en/docs/chart_operations/chartsetstring)). However, note that these functions are synchronous and wait for execution results.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the current chart ID
   long chart_id = ChartID();
   
//--- save the initial offset of the zero bar from the right edge in percentage and the auto scroll flag
   double shift = ChartGetDouble(chart_id, CHART_SHIFT_SIZE);
   bool   scroll= ChartGetInteger(chart_id,CHART_AUTOSCROLL);
   
//--- reset the auto scroll chart flag
   ChartSetInteger(chart_id, CHART_AUTOSCROLL, true);
   PrintFormat("Initial chart shift size: %.2f", shift);
 
//--- in the loop from 2.0% to 50.0% with the step of 0.5%
   for(int i=20; i<=500; i+=5)
     {
      //--- set the shift size as i / 10 and print the specified value in the journal
      ChartSetDouble(chart_id, CHART_SHIFT_SIZE, i/10.0);
      PrintFormat("Set chart shift size to %.1f%%", i/10.0);
      
      //--- keep the chart zero bar at the specified shift distance
      ChartNavigate(chart_id, CHART_END, 0);
      
      //--- wait a bit
      Sleep(16);
     }
 
//--- set the initial chart shift and auto scroll
   Print("Set the chart shift size to the initial value of ", shift);
   ChartSetDouble(ChartID(), CHART_SHIFT_SIZE, shift);
   ChartSetInteger(chart_id, CHART_AUTOSCROLL, scroll);
  }

```
