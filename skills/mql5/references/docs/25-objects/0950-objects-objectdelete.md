# ObjectDelete

The function removes the object with the specified name from the specified chart.

```
bool  ObjectDelete(
   long    chart_id,     // chart identifier
   string  name          // object name
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

name

[in]  Name of object to be deleted.

Return Value

The function returns true if the command has been successfully added to the queue of the specified chart, or false otherwise.

Note

An asynchronous call is always used for ObjectDelete(), that is why the function only returns the results of adding the command to a chart queue. In this case, true only means that the command has been successfully enqueued, but the result of its execution is unknown.

To check the command execution result, you can use the [ObjectFind()](/en/docs/objects/objectfind) function or any other function that requests object properties, such as ObjectGetXXX. However, you should keep in mind that such functions are added to the end of the queue of that chart, and they wait for the execution result (due to the synchronous call), and can therefore be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

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
 
//--- in a loop through all chart graphical objects
   int obj_total=ObjectsTotal(chart_id);
   for(int i=obj_total-1; i>=0; i--)
     {
      //--- skip every second object 
      if(i%2==0)
         continue;
      
      //--- get the name of the graphical object
      //--- if this is an auto-trade deal label, skip this object
      string obj_name=ObjectName(chart_id, i);
      if(StringFind(obj_name, "autotrade")==0)
         continue;
      
      //--- delete the graphical object from the chart with chart_id
      ResetLastError();
      if(ObjectDelete(chart_id, obj_name))
        {
         PrintFormat("[%d] Graphic object named \"%s\" removed from the chart with ID #%I64d", i, obj_name, chart_id);
        }
      else
        {
         Print("ObjectDelete() failed. Error ", GetLastError());
        }
     }
   /*
   result for the chart where 6 graphical objects and auto trading labels (skipped) are placed:
   [659] Graphic object named "M30 Rectangle 5636" removed from the chart with ID #128968168951083984
   [657] Graphic object named "M30 Trendline 40731" removed from the chart with ID #128968168951083984
   [1] Graphic object named "M30 Vertical Line 13600" removed from the chart with ID #128968168951083984
   */
  }

```
