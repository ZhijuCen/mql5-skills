# ChartGetDouble

Returns the value of a corresponding property of the specified chart. Chart property must be of double type. There are 2 variants of the function calls.

1. Returns the property value directly.

```
double  ChartGetDouble(
   long                         chart_id,          // Chart ID
   ENUM_CHART_PROPERTY_DOUBLE   prop_id,           // Property ID
   int                          sub_window=0       // subwindow number, if necessary
   );

```

2. Returns true or false, depending on the success of a function. If successful, the value of the property is placed in a target variable double_var passed by reference.

```
bool  ChartGetDouble(
   long                         chart_id,          // Chart ID
   ENUM_CHART_PROPERTY_DOUBLE   prop_id,           // Property ID
   int                          sub_window,      // Subwindow number
   double&                      double_var       // Target variable for the chart property
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

prop_id

[in]  Chart property ID. This value can be one of the [ENUM_CHART_PROPERTY_DOUBLE](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_double) values.

sub_window

[in]  Number of the chart subwindow. For the first case, the default value is 0 (main chart window). The most of the properties do not require a subwindow number.

double_var

[out]  Target variable of double type for the requested property.

Return Value

The value of double type.

For the second call case it returns true if the specified property is available and its value has been placed into double_var variable, otherwise returns false. To get an additional information about the [error](/en/docs/constants/errorswarnings/errorcodes), it is necessary to call the function [GetLastError()](/en/docs/check/getlasterror).

Note

The function is synchronous, which means that it waits for the execution of all the commands that have been added to the chart queue prior to its call.

Example:

```
void OnStart()
  {
   double priceMin=ChartGetDouble(0,CHART_PRICE_MIN,0);
   double priceMax=ChartGetDouble(0,CHART_PRICE_MAX,0);
   Print("CHART_PRICE_MIN =",priceMin);
   Print("CHART_PRICE_MAX =",priceMax);
  }

```
