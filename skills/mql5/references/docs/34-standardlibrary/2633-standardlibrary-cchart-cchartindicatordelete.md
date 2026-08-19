# IndicatorDelete

Removes an indicator with a specified name from the specified chart window.

```
bool  IndicatorDelete(
   int            sub_win       // number of the subwindow
   const string   name          // short name of the indicator
   );

```

Parameters

sub_win

[in]  Number of the chart subwindow. 0 denotes the main chart subwindow.

const name

[in]  The short name of the indicator which is set in the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property with the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. To get the short name of an indicator, use the [IndicatorName()](/en/docs/standardlibrary/cchart/cchartindicatorname) function.

Return Value

Returns true in case of successful deletion of the indicator. Otherwise it returns false. To get [error](/en/docs/constants/errorswarnings/errorcodes) details, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

If two indicators with identical short names exist in the chart subwindow, the first one in a row will be deleted.

If other indicators on this chart are based on the values of the indicator that is being deleted, such indicators will also be deleted.

Do not confuse the indicator short name and the file name that is specified when creating an indicator using functions [iCustom()](/en/docs/indicators/icustom) and [IndicatorCreate()](/en/docs/series/indicatorcreate). If the short name of an indicator is not set explicitly, then the name of the file containing the source code of the indicator will be specified during compilation.

Deletion of an indicator from a chart does not mean that its calculation part will be deleted from the terminal memory. To release the indicator handle, use the [IndicatorRelease()](/en/docs/series/indicatorrelease) function.

The indicator's short name should be formed correctly. It will be written to the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property using the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. It is recommended that the short name should contain values of all the input parameters of the indicator, because the indicator to be deleted from the chart by the [IndicatorDelete()](/en/docs/standardlibrary/cchart/cchartindicatordelete) function is identified by the short name.

See also

[IndicatorAdd()](/en/docs/standardlibrary/cchart/cchartindicatoradd), [IndicatorsTotal()](/en/docs/standardlibrary/cchart/cchartindicatorstotal), [IndicatorName()](/en/docs/standardlibrary/cchart/cchartindicatorname), [iCustom()](/en/docs/indicators/icustom), [IndicatorCreate()](/en/docs/series/indicatorcreate),  [IndicatorSetString()](/en/docs/customind/indicatorsetstring).
