# IndicatorsTotal

Returns the number of all indicators applied to the specified chart window.

```
int  IndicatorsTotal(
   long   chart_id,  // chart identifier
   int    sub_win    // number of the subwindow
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 denotes the main chart.

sub_win

[in]  Number of the chart subwindow. 0 denotes the main chart window.

Return Value

The number of indicators in the specified chart window. To get [error](/en/docs/constants/errorswarnings/errorcodes) details, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The function allows going searching through all the indicators attached to the chart. The number of all the windows of the chart can be obtained from the [CHART_WINDOWS_TOTAL](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer) property using the [GetInteger()](/en/docs/standardlibrary/cchart/cchartgetinteger) function.

See also

[IndicatorAdd()](/en/docs/standardlibrary/cchart/cchartindicatoradd), [IndicatorDelete()](/en/docs/standardlibrary/cchart/cchartindicatordelete), [IndicatorsTotal()](/en/docs/standardlibrary/cchart/cchartindicatorstotal), [iCustom()](/en/docs/indicators/icustom), [IndicatorCreate()](/en/docs/series/indicatorcreate), [IndicatorSetString()](/en/docs/customind/indicatorsetstring).
