# ObjectName

The function returns the name of the corresponding object in the specified chart, in the specified subwindow, of the specified type.

```
string  ObjectName(
   long  chart_id,           // chart identifier
   int   pos,                // number in the list of objects
   int   sub_window=-1,      // window index
   int   type=-1             // object type
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

pos

[in]  Ordinal number of the object according to the specified filter by the number and type of the subwindow.

sub_window=-1

[in]  Number of the chart subwindow. 0 means the main chart window, -1 means all the subwindows of the chart, including the main window.

type=-1

[in]  Type of the object. The value can be one of the values of the [ENUM_OBJECT](/en/docs/constants/objectconstants/enum_object) enumeration. -1 means all types.

Return Value

Name of the object is returned in case of success.

Note

The function uses a synchronous call, which means that the function waits for the execution of all commands that have been enqueued for this chart prior to its call, that is why this function can be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

When an object is renamed, two events are formed simultaneously. These events can be handled in an Expert Advisor or indicator by the [OnChartEvent()](/en/docs/event_handlers/onchartevent) function:

- an event of deletion of an object with the old name;
- an event of creation of an object with a new name.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- chart ID
   long chart_id=ChartID();
   
//--- get the number of chart subwindows together with the main window
   long wnd=0;
   ResetLastError();
   if(!ChartGetInteger(chart_id, CHART_WINDOWS_TOTAL, 0, wnd))
     {
      Print("ChartGetInteger() failed. Error ", GetLastError());
      return;
     }
   
//--- in a loop by the number of chart subwindows, including the main window
   for(int sub_wnd=0; sub_wnd<(int)wnd; sub_wnd++)
     {
      //--- display the chart header in the journal
      string wnd_name=(sub_wnd==0 ? "Main window:" : StringFormat("Subwindow %d:", sub_wnd));
      Print(wnd_name);
      
      //--- get the number of graphical objects in the current subwindow
      //--- and output the name of each of them in a loop through all the subwindow objects
      int objects=ObjectsTotal(chart_id, sub_wnd);
      for(int obj_index=0; obj_index<objects; obj_index++)
        {
         //--- current object name in a loop
         string obj_name=ObjectName(chart_id, obj_index, sub_wnd);
         
         //--- if this is a deal label (auto trading), the name of this object is not displayed in the journal
         if(sub_wnd==0 && StringFind(obj_name, "autotrade")==0)
            continue;
         
         PrintFormat("  [%d] Graphic object name: \"%s\"", obj_index, obj_name);
        }
     }
   /*
   result for the main window with two subwindows,
   where the main window contains two graphical objects and deal labels (skipped),
   and two graphical objects are constructed in each chart subwindow:
   Main window:
     [0] Graphic object name: "M30 Fibo 29182"
     [1] Graphic object name: "M30 Vertical Line 13600"
   Subwindow 1:
     [0] Graphic object name: "M30 Cycle Lines 63004"
     [1] Graphic object name: "M30 Trendline 40731"
   Subwindow 2:
     [0] Graphic object name: "M30 Equidistant Channel 58930"
     [1] Graphic object name: "M30 Rectangle 5636"
   */
  }

```
