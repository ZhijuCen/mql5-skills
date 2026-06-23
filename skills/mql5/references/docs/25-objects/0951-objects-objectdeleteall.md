# ObjectsDeleteAll

Removes all objects from the specified chart, specified chart subwindow, of the specified type.

```
int  ObjectsDeleteAll(
   long  chart_id,           // chart identifier
   int   sub_window=-1,      // window index
   int   type=-1             // object type
   );

```

Removes all objects of the specified type using prefix in object names.

```
int  ObjectsDeleteAll(
   long           chart_id,   // chart ID
   const string     prefix,   // prefix in object name
   int       sub_window=-1,   // window index
   int      object_type=-1    // object type
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

prefix

[in]  Prefix in object names. All objects whose names start with this set of characters will be removed from chart. You can specify prefix as 'name' or 'name*' – both variants will work the same. If an empty string is specified as the prefix, objects with all possible names will be removed.

sub_window=-1

[in] Number of the chart subwindow. 0 means the main chart window, -1 means all the subwindows of the chart, including the main window.

type=-1

[in]  Type of the object. The value can be one of the values of the [ENUM_OBJECT](/en/docs/constants/objectconstants/enum_object) enumeration. -1 means all types.

Return Value

Returns the number of deleted objects. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

Note

The function uses a synchronous call, which means that the function waits for the execution of all commands that have been enqueued for this chart prior to its call, that is why this function can be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#property script_show_inputs
 
enum ENUM_REMOVE_MODE
  {
   REMOVE_MODE_TRADE_ARROWS,  // Remove all arrows
   REMOVE_MODE_AUTOTRADE      // Remove all autotrade arrows
  };
 
input ENUM_REMOVE_MODE  InpRemoveMethod = REMOVE_MODE_TRADE_ARROWS;  /*Remove Method*/ // Either remove all arrows or only the auto trading ones
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- chart ID and the number of removed objects
   long chart_id=ChartID();
   int  count=0;
   
   ResetLastError();
//--- if deleting all arrow objects is selected
//--- delete all objects of the OBJ_ARROW_BUY and OBJ_ARROW_SELL types, thereby deleting all auto trade deal icons,
//--- also deleting other objects of the same type present on the chart
   if(InpRemoveMethod==REMOVE_MODE_TRADE_ARROWS)
     {
      count+=ObjectsDeleteAll(chart_id, -1, OBJ_ARROW_BUY);
      count+=ObjectsDeleteAll(chart_id, -1, OBJ_ARROW_SELL);
     }
     
//--- if you choose to remove only the auto trade deal icons
//--- delete all objects that have the "autotrade" substring in their name,
//--- removing all auto trade deal icons and leaving other arrow objects
   else
     {
      count=ObjectsDeleteAll(chart_id, "autotrade");
     }
 
//--- If an error occurred while deleting graphical objects, report it and terminate the operation
   if(GetLastError()!=ERR_SUCCESS)
     {
      PrintFormat("ObjectsDeleteAll() failed. Error %d. count=%d", GetLastError(), count);
      return;
     }
     
//--- update the chart to immediately reflect the changes
   ChartRedraw(chart_id);
   
//--- set the number of removed arrow objects in the journal
   string type=(InpRemoveMethod==REMOVE_MODE_TRADE_ARROWS ? "OBJ_ARROW_BUY and OBJ_ARROW_SELL" : "with prefix \"autotrade\"");
   PrintFormat("%d objects %s removed", count, type);
   /*
   result for InpRemoveMethod = REMOVE_MODE_TRADE_ARROWS:
   116 objects OBJ_ARROW_BUY and OBJ_ARROW_SELL removed
   
   result for InpRemoveMethod = REMOVE_MODE_AUTOTRADE:
   131 objects with prefix "autotrade" removed
   */
  }

```
