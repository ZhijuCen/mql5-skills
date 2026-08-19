# CGraphic

CGraphic is a base class for creating custom charts.

### Description

The CGraphic class provides numerous aspects of working with custom charts.

The class stores the main chart elements, sets their parameters and performs plotting.

Also, the class stores the curves for the chart and provides various display options.

### Declaration

```
   class CGraphic

```

### Title

```
   #include <Graphics\Graphic.mqh>

```

### Class methods

| Method | Description |
| --- | --- |
| Create | Create a graphical resource bound to a chart object |
| Destroy | Remove a chart and destroy a graphical resource |
| Update | Display implemented changes |
| ChartObjectName | Get the name of an object bound to a chart |
| ResourceName | Get the graphical resource name |
| XAxis | Get the pointer to the X axis |
| YAxis | Get the pointer to the Y axis |
| GapSize | Get/set the size of indents between the chart elements |
| BackgroundColor | Get/set a background color |
| BackgroundMain | Get/set a chart header |
| BackgroundMainSize | Get/set a sub-header font size |
| BackgroundMainColor | Get/set a chart header color |
| BackgroundSub | Get/set a sub-header |
| BackgroundSubSize | Get/set a sub-header font size |
| BackgroundSubColor | Get/set a chart sub-header color |
| GridLineColor | Get/set a grid line color |
| GridBackgroundColor | Get/set a grid background color |
| GridCircleRadius | Get/set the dot radius in the grid nodes |
| GridCircleColor | Get/set the dot color in the grid nodes |
| GridHasCircle | Get/set the dot plotting flag in the grid nodes |
| GridAxisLineColor | Get the value of a real chart axes color. |
| HistoryNameWidth | Get/set the maximum allowed length for displaying a curve name |
| HistoryNameSize | Get/set the font size of a curve name |
| HistorySymbolSize | Get/set a size of notational convention symbols |
| TextAdd | Add a text to the chart |
| LineAdd | Add a line to the chart |
| CurveAdd | Create and add a curve to the chart |
| CurvePlot | Plot a previously created curve by index |
| CurvePlotAll | Plot all previously created curves |
| CurveGetByIndex | Get a curve by a specified index |
| CurveGetByName | Get a curve by a specified name |
| CurveRemoveByIndex | Remove a curve by a specified index. |
| CurveRemoveByName | Remove a curve by a specified name. |
| CurvesTotal | Get the number of curves for the given chart. |
| MarksToAxisAdd | Add a scale mark to the chart axis |
| MajorMarkSize | Get/set the size of the scale's ticks on the chart axis |
| FontSet | Set the current font parameters |
| FontGet | Get the current font parameters |
| Attach | Get/set a graphical resource and bind it to the CGraphic class instance |
| CalculateMaxMinValues | Calculate (re-calculate) minimum and maximum chart values on both axes. |
| Height | Get a chart height in pixels. |
| IndentDown | Get/set a chart indent from the lower border. |
| IndentLeft | Get/set a chart indent from the left border. |
| IndentRight | Get/set a chart indent from the right border. |
| IndentUp | Get/set a chart indent from the upper border. |
| Redraw | Redraw the chart. |
| ResetParameters | Reset the chart redrawing parameters. |
| ScaleX | Scale the value by X axis. |
| ScaleY | Scale the value by Y axis. |
| SetDefaultParameters | Set the chart parameters to default values. |
| Width | Get the chart width in pixels. |
