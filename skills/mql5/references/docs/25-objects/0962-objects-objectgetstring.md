# ObjectGetString

The function returns the value of the corresponding object property. The object property must be of the [string](/en/docs/basis/types/stringconst) type. There are 2 variants of the function.

1. Immediately returns the property value.

```
string  ObjectGetString(
   long                            chart_id,          // chart identifier
   string                          name,              // object name
   ENUM_OBJECT_PROPERTY_STRING     prop_id,           // property identifier
   int                             prop_modifier=0    // property modifier, if required
   );

```

2. Returns true or false, depending on the success of the function. If successful, the property value is placed to a receiving variable passed by reference by the last parameter.

```
bool  ObjectGetString(
   long                            chart_id,          // chart identifier
   string                          name,              // object name
   ENUM_OBJECT_PROPERTY_STRING     prop_id,           // property identifier
   int                             prop_modifier,     // property modifier
   string&                         string_var         // here we accept the property value
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

[in]  Modifier of the specified property. For the first variant, the default modifier value is equal to 0. Most properties do not require a modifier.  It denotes the number of the level in [Fibonacci tools](/en/docs/constants/objectconstants/enum_object) and in the graphical object Andrew's pitchfork. The numeration of levels starts from zero.

string_var

[out]  Variable of the string type that receives the value of the requested properties.

Return Value

String value for the first version of the call.

For the second version of the call returns true, if this property is maintained and the value has been placed into the string_var variable, otherwise returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

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
 
#define   OBJ_NAME   "TestObjectGetInteger"  // Object name
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- current chart ID
   long chart_id=ChartID();
 
//--- create a "Vertical Line" graphical object at the current known server time
   if(!ObjectCreate(chart_id, OBJ_NAME, OBJ_VLINE, 0, TimeCurrent(), 0))
     {
      Print("ObjectCreate() failed. Error ", GetLastError());
      return;
     }
//--- update the chart to immediately reflect the changes
   ChartRedraw(chart_id);
   
//--- get the object creation time
   long long_var=0;
   if(!ObjectGetInteger(chart_id, OBJ_NAME, OBJPROP_CREATETIME, 0, long_var))
     {
      Print("ObjectGetInteger() failed. Error ", GetLastError());
      return;
     }
//--- string representation of the object creation time
   string create_time=TimeToString((datetime)long_var, TIME_DATE|TIME_MINUTES|TIME_SECONDS);
   
//--- get the time set in the object
   if(!ObjectGetInteger(chart_id, OBJ_NAME, OBJPROP_TIME, 0, long_var))
     {
      Print("ObjectGetInteger() failed. Error ", GetLastError());
      return;
     }
//--- string representation of the object location time
   string obj_time=TimeToString((datetime)long_var, TIME_DATE|TIME_MINUTES|TIME_SECONDS);
   
//--- get the object type
   ENUM_OBJECT object_type=(ENUM_OBJECT)ObjectGetInteger(chart_id, OBJ_NAME, OBJPROP_TYPE);
   
//--- output to the journal the type of object, the time of its creation and the time on the chart the graphical object is located on
   PrintFormat("%s object created at %s at chart point with time %s",EnumToString(object_type), create_time, obj_time);
   
//--- wait two seconds and delete the created object
   Sleep(2000);
   ObjectDelete(chart_id, OBJ_NAME);
   ChartRedraw(chart_id);
   /*
   result:
   OBJ_VLINE object created at 2025.02.01 12:15:37 at chart point with time 2025.01.31 23:54:59
   */
  }

```
