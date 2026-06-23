# ObjectSetString

The function sets the value of the corresponding object property. The object property must be of the [string](/en/docs/basis/types/stringconst) type. There are 2 variants of the function.

Setting property value, without modifier

```
bool  ObjectSetString(
   long                            chart_id,          // chart identifier
   string                          name,              // object name
   ENUM_OBJECT_PROPERTY_STRING     prop_id,           // property
   string                          prop_value         // value
   );

```

Setting a property value indicating the modifier

```
bool  ObjectSetString(
   long                            chart_id,          // chart identifier
   string                          name,              // object name
   ENUM_OBJECT_PROPERTY_STRING     prop_id,           // property
   int                             prop_modifier,     // modifier
   string                          prop_value         // value
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

name

[in]  Name of the object.

prop_id

[in]  ID of the object property. The value can be one of the values of the [ENUM_OBJECT_PROPERTY_STRING](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_string) enumeration.

prop_modifier

[in]  Modifier of the specified property.  It denotes the number of the level in [Fibonacci tools](/en/docs/constants/objectconstants/enum_object) and in the graphical object Andrew's pitchfork. The numeration of levels starts from zero.

prop_value

[in]  The value of the property.

Return Value

The function returns true only if the command to change properties of a graphical object has been sent to a chart successfully. Otherwise it returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

Note

The function uses an asynchronous call, which means that the function does not wait for the execution of the command that has been added to the queue of the specified chart. Instead, it immediately returns control.

To check the command execution result, you can use a function that requests the specified object property. However, you should keep in mind that such functions are added to the end of the queue of that chart, and they wait for the execution result, and can therefore be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

When an object is renamed, two events are formed simultaneously. These events can be handled in an Expert Advisor or indicator by the [OnChartEvent()](/en/docs/event_handlers/onchartevent) function:

- an event of deletion of an object with the old name;
- an event of creation of an object with a new name.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   OBJ_NAME   "TestObjectSetString"   // Object name
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- current chart ID and symbol, flag for displaying object descriptions
   long   chart_id= ChartID();
   string symbol  = ChartSymbol(chart_id);
   bool   descript= ChartGetInteger(chart_id, CHART_SHOW_OBJECT_DESCR); 
   
//--- set the display of object descriptions on the chart
   ChartSetInteger(chart_id, CHART_SHOW_OBJECT_DESCR, true);
 
//--- get the current Bid price
   double bid=0;;
   ResetLastError();
   if(!SymbolInfoDouble(symbol, SYMBOL_BID, bid))
     {
      Print("SymbolInfoDouble() failed. Error ", GetLastError());
      return;
     }
     
//--- create the "Horizontal line" graphical object on the current Bid price
   if(!ObjectCreate(chart_id, OBJ_NAME, OBJ_HLINE, 0, 0, bid))
     {
      Print("ObjectCreate() failed. Error ", GetLastError());
      return;
     }
//--- enter the object name+"Description" into the object description
   if(!ObjectSetString(chart_id, OBJ_NAME, OBJPROP_TEXT, "Bid: "+DoubleToString(bid, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS))))
     {
      Print("ObjectSetString() failed. Error ", GetLastError());
      return;
     }
//--- update the chart to immediately reflect the changes
   ChartRedraw(chart_id);
   
//--- get the object description
   string string_var="";
   if(!ObjectGetString(chart_id, OBJ_NAME, OBJPROP_TEXT, 0, string_var))
     {
      Print("ObjectGetInteger() failed. Error ", GetLastError());
      return;
     }
//--- get the object name
   string obj_name=ObjectGetString(chart_id, OBJ_NAME, OBJPROP_NAME);
   
//--- get the object type
   ENUM_OBJECT object_type=(ENUM_OBJECT)ObjectGetInteger(chart_id, OBJ_NAME, OBJPROP_TYPE);
   
//--- display the object type, its name and description in the journal
   PrintFormat("The %s object named \"%s\" has the description \"%s\"",EnumToString(object_type), obj_name, string_var);
   
//--- wait two seconds and delete the created object
   Sleep(2000);
   ObjectDelete(chart_id, OBJ_NAME);
   
//--- return the initial flag for displaying descriptions of objects for the chart
   ChartSetInteger(chart_id, CHART_SHOW_OBJECT_DESCR, descript);
   ChartRedraw(chart_id);
   /*
   result:
   The OBJ_HLINE object named "TestObjectSetString" has the description "Bid: 0.62096"
   */
  }

```
