# ChartGetInteger

Returns the value of a corresponding property of the specified chart. Chart property must be of [datetime, int or bool](/en/docs/basis/types/integer) type. There are 2 variants of the function calls.

1. Returns the property value directly.

```
long  ChartGetInteger(
   long                          chart_id,          // Chart ID
   ENUM_CHART_PROPERTY_INTEGER   prop_id,           // Property ID
   int                           sub_window=0       // subwindow number, if necessary
   );

```

2. Returns true or false, depending on the success of a function. If successful, the value of the property is placed in a target variable long_var passed by reference.

```
bool  ChartGetInteger(
   long                          chart_id,          // Chart ID
   ENUM_CHART_PROPERTY_INTEGER   prop_id,           // Property ID
   int                           sub_window=0       // subwindow number
   long&                         long_var           // Target variable for the property
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

prop_id

[in]  Chart property ID. This value can be one of the  [ENUM_CHART_PROPERTY_INTEGER](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer) values.

sub_window

[in]  Number of the chart subwindow. For the first case, the default value is 0 (main chart window). The most of the properties do not require a subwindow number.

long_var

[out]  Target variable of long type for the requested property.

Return Value

The value of long type.

For the second call case it returns true if specified property is available and its value has been stored into long_var variable, otherwise returns false. To get additional information about the [error](/en/docs/constants/errorswarnings/errorcodes), it is necessary to call the function [GetLastError()](/en/docs/check/getlasterror).

Note

The function is synchronous, which means that it waits for the execution of all the commands that have been added to the chart queue prior to its call.

Example:

```
void OnStart()
  {
   int height=ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0);
   int width=ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0);
   Print("CHART_HEIGHT_IN_PIXELS =",height,"pixels");
   Print("CHART_WIDTH_IN_PIXELS =",width,"pixels");
  }

```
