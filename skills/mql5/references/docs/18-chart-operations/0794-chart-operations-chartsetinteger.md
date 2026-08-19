# ChartSetInteger

Sets a value for a corresponding property of the specified chart. Chart property must be [datetime, int, color, bool or char](/en/docs/basis/types/integer). The command is added to chart messages queue and will be executed after processing of all previous commands.

```
bool  ChartSetInteger(
   long                           chart_id,     // Chart ID
   ENUM_CHART_PROPERTY_INTEGER    prop_id,      // Property ID
   long                           value         // Value
   );

```

Sets a value for a corresponding property of the specified subwindow.

```
bool  ChartSetInteger(
   long                           chart_id,     // Chart ID
   ENUM_CHART_PROPERTY_INTEGER    prop_id,      // Property ID
   int                            sub_window,   // Subwindow number
   long                           value         // Value
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

prop_id

[in]  Chart property ID. It can be one of the [ENUM_CHART_PROPERTY_INTEGER](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer) value (except the read-only properties).

sub_window

[in]  Number of the chart subwindow. For the first case, the default value is 0 (main chart window). The most of the properties do not require a subwindow number.

value

[in]  Property value.

Return Value

Returns true if the command has been added to chart queue, otherwise false. To get an information about the [error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The function is asynchronous, which means that the function does not wait for the execution of the command, which has been successfully added to the queue of specified the chart. Instead, it immediately returns control. The property will only change after the handling of the appropriate command from the chart queue. To immediately execute commands from the chart queue, call the [ChartRedraw](/en/docs/chart_operations/chartredraw) function.

If you want to immediately change several chart properties at once, then the corresponding functions ([ChartSetString](/en/docs/chart_operations/chartsetstring), [ChartSetDouble](/en/docs/chart_operations/chartsetdouble), [ChartSetString](/en/docs/chart_operations/chartsetstring)) should be executed in one code block, after which you should call [ChartRedraw](/en/docs/chart_operations/chartredraw) once.

To check the command execution result, you can use a function, which requests the specified chart property ([ChartGetInteger](/en/docs/chart_operations/chartgetinteger), [ChartGetDouble](/en/docs/chart_operations/chartgetdouble), [ChartSetString](/en/docs/chart_operations/chartsetstring)). However, note that these functions are synchronous and wait for execution results.

Example:

```
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
void OnInit()
  {
//--- Enabling events of mouse movements on the chart window
   ChartSetInteger(0,CHART_EVENT_MOUSE_MOVE,1);
//--- Forced updating of chart properties ensures readiness for event processing
   ChartRedraw();
  }
//+------------------------------------------------------------------+
//| MouseState                                                       |
//+------------------------------------------------------------------+
string MouseState(uint state)
  {
   string res;
   res+="\nML: "   +(((state& 1)== 1)?"DN":"UP");   // mouse left
   res+="\nMR: "   +(((state& 2)== 2)?"DN":"UP");   // mouse right 
   res+="\nMM: "   +(((state&16)==16)?"DN":"UP");   // mouse middle
   res+="\nMX: "   +(((state&32)==32)?"DN":"UP");   // mouse first X key
   res+="\nMY: "   +(((state&64)==64)?"DN":"UP");   // mouse second X key
   res+="\nSHIFT: "+(((state& 4)== 4)?"DN":"UP");   // shift key
   res+="\nCTRL: " +(((state& 8)== 8)?"DN":"UP");   // control key
   return(res);
  }
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   if(id==CHARTEVENT_MOUSE_MOVE)
      Comment("POINT: ",(int)lparam,",",(int)dparam,"\n",MouseState((uint)sparam));
  }

```
