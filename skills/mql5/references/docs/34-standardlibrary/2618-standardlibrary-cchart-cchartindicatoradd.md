# IndicatorAdd

Adds an indicator with the specified handle into a specified chart window.

```
bool  IndicatorAdd(
   int   sub_win         // number of the subwindow
   int   handle          // handle of the indicator
   );

```

Parameters

sub_win

[in]  The number of the chart subwindow. 0 means the main chart window. if the number of a non-existing window is specified, a new window will be created.

handle

[in]  The handle of the indicator.

Return Value

The function returns true in case of success, otherwise it returns false. In order to obtain information about the [error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

See also

[IndicatorDelete()](/en/docs/standardlibrary/cchart/cchartindicatordelete), [IndicatorsTotal()](/en/docs/standardlibrary/cchart/cchartindicatorstotal), [IndicatorName()](/en/docs/standardlibrary/cchart/cchartindicatorname).
