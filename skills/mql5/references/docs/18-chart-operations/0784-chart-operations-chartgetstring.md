# ChartGetString

Returns the value of a corresponding property of the specified chart. Chart property must be of string type. There are 2 variants of the function call.

1. Returns the property value directly.

```
string  ChartGetString(
   long                         chart_id,         // Chart ID
   ENUM_CHART_PROPERTY_STRING   prop_id           // Property ID
   );

```

2. Returns true or false, depending on the success of a function. If successful, the value of the property is placed in a target variable string_var passed by reference.

```
bool  ChartGetString(
   long                          chart_id,        // Chart ID
   ENUM_CHART_PROPERTY_STRING    prop_id,         // Property ID
   string&                       string_var       // Target variable for the property
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

prop_id

[in]  Chart property ID. This value can be one of the  [ENUM_CHART_PROPERTY_STRING](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_string) values.

string_var

[out]  Target variable of string type for the requested property.

Return Value

The value of string type.

For the second call case it returns true if the specified property is available and its value has been stored into string_var variable, otherwise returns false. To get additional information about the [error](/en/docs/constants/errorswarnings/errorcodes), it is necessary to call the function [GetLastError()](/en/docs/check/getlasterror).

Note

ChartGetString can be used for reading comments plotted on the chart using the [Comment](/en/docs/common/comment) or [ChartSetString](/en/docs/chart_operations/chartsetstring) functions.

The function is synchronous, which means that it waits for the execution of all the commands that have been added to the chart queue prior to its call.

Example:

```
void OnStart()
  {
   ChartSetString(0,CHART_COMMENT,"Test comment.\nSecond line.\nThird!");
   ChartRedraw();
   Sleep(1000);
   string comm=ChartGetString(0,CHART_COMMENT);
   Print(comm);
  }

```

See also

[Comment](/en/docs/common/comment), [ChartSetString](/en/docs/chart_operations/chartsetstring)
