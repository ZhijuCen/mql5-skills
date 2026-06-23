# ObjectsTotal

The function returns the number of objects in the specified chart, specified subwindow, of the specified type.

```
int  ObjectsTotal(
   long  chart_id,           // chart identifier
   int   sub_window=-1,      // window index
   int   type=-1             // object type
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

sub_window=-1

[in]  Number of the chart subwindow. 0 means the main chart window, -1 means all the subwindows of the chart, including the main window.

type=-1

[in]  Type of the object. The value can be one of the values of the [ENUM_OBJECT](/en/docs/constants/objectconstants/enum_object) enumeration. -1 means all types.

Return Value

The number of objects.

Note

The function uses a synchronous call, which means that the function waits for the execution of all commands that have been enqueued for this chart prior to its call, that is why this function can be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

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
   
//--- get and display in the journal the number of graphical objects for each chart subwindow
   for(int i=0; i<(int)wnd; i++)
     {
      int objects=ObjectsTotal(chart_id, i);
      string wnd_head=(i==0 ? "The main chart window" : StringFormat("The window with index %d of the chart", i));
      PrintFormat("%s contains %d graphic objects", wnd_head, objects);
     }
   /*
   result for the main window with two subwindows,
   where the main window contains deal labels,
   and in the subwindows there are two graphical objects:
   The main chart window contains 656 graphic objects
   The window with index 1 of the chart contains 2 graphic objects 
   The window with index 2 of the chart contains 2 graphic objects
   */
  }

```
