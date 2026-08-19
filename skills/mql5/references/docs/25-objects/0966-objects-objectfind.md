# ObjectFind

The function searches for an object with the specified name in the chart with the specified ID.

```
int  ObjectFind(
   long    chart_id,     // chart identifier
   string  name          // object name
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

name

[in]  The name of the searched object.

Return Value

If successful the function returns the number of the subwindow (0 means the main window of the chart), in which the object is found. If the object is not found, the function returns a negative number. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

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
 
#define   OBJ_NAME   "TestObjectFind"
#define   WND        0
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- chart ID
   long chart_id=ChartID();
 
//--- if the OBJ_NAME graphical object is found on the chart in the WND window,
//--- report this and finish the work
   ResetLastError();
   if(ObjectFind(chart_id, OBJ_NAME)==WND)
     {
      PrintFormat("A graphic object named \"%s\" exists on chart with ID %I64d", OBJ_NAME, chart_id);
      return;
     }
     
//--- if the object is not found
   else
     {
      //--- if the last error code is not 4202 ("Graphical object not found")
      //--- report an error and exit
      if(GetLastError()!=ERR_OBJECT_NOT_FOUND) 
        {
         Print("ObjectFind() failed. Error ", GetLastError());
         return;
        }
      
      //--- report in the journal that the OBJ_NAME object is not on the chart with chart_id
      PrintFormat("There is no graphic object named \"%s\" on the chart with ID #%I64d. Let's create it.", OBJ_NAME, chart_id);
      
      //--- create the "vertical line" graphical object named OBJ_NAME in the WND window
      ResetLastError();
      if(!ObjectCreate(chart_id, OBJ_NAME, OBJ_VLINE, WND, TimeCurrent(), 0))
        {
         Print("ObjectCreate() failed. Error ", GetLastError());
         return;
        }
      
      //--- redraw the chart to immediately reflect the changes
      ChartRedraw(chart_id);
      
      //--- check if the created object is present
      if(ObjectFind(chart_id, OBJ_NAME)!=WND)
        {
         Print("ObjectFind() failed. Error ", GetLastError());
         return;
        }
      
      //--- if the object is created, report this in the journal,
      //--- wait a second and delete the created graphical object
      PrintFormat("Now a graphic object named \"%s\" exists on the chart with ID #%I64d. Let's delete it.", OBJ_NAME, chart_id);
      Sleep(1000);
      ObjectDelete(chart_id, OBJ_NAME);
      
      //--- redraw the chart to immediately reflect the changes
      ChartRedraw(chart_id);
     }
   /*
   result:
   There is no graphic object named "TestObjectFind" on the chart with ID #133246248352168439. Let's create it.
   Now a graphic object named "TestObjectFind" exists on the chart with ID #133246248352168439. Let's delete it. 
   */
  }

```
