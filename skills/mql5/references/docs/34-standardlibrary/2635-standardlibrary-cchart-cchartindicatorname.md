# IndicatorName

Returns the short name of the indicator by the index in the indicators list on the specified chart window.

```
string  IndicatorName(
   int   sub_win     // number of the subwindow
   int   index       // index of the indicator in the list of indicators added to the chat subwindow
   );

```

Parameters

sub_win

[in]  Number of the chart subwindow. 0 denotes the main chart window.

index

[in]  Index of the indicator in the list of indicators. The numeration of indicators start with zero, i.e. the first indicator in the list has the 0 index. To obtain the number of indicators in the list, use the [IndicatorsTotal()](/en/docs/standardlibrary/cchart/cchartindicatorstotal) function.

Return Value

The short name of the indicator which is set in the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property with the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. To get [error](/en/docs/constants/errorswarnings/errorcodes) details, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

Do not confuse the indicator short name and the file name that is specified when creating an indicator using functions [iCustom()](/en/docs/indicators/icustom) and [IndicatorCreate()](/en/docs/series/indicatorcreate). If the short name of an indicator is not set explicitly, then the name of the file containing the source code of the indicator will be specified during compilation.

The indicator's short name should be formed correctly. It will be written to the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property using the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. It is recommended that the short name should contain values of all the input parameters of the indicator, because the indicator to be deleted from the chart by the [IndicatorDelete()](/en/docs/standardlibrary/cchart/cchartindicatordelete) function is identified by the short name.

See also

[IndicatorAdd()](/en/docs/standardlibrary/cchart/cchartindicatoradd), [IndicatorDelete](/en/docs/standardlibrary/cchart/cchartindicatordelete), [IndicatorsTotal](/en/docs/standardlibrary/cchart/cchartindicatorstotal), [iCustom()](/en/docs/indicators/icustom), [IndicatorCreate()](/en/docs/series/indicatorcreate), [IndicatorSetString()](/en/docs/customind/indicatorsetstring).
