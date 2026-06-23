# CChart

CChart is a class for simplified access to "Chart" graphic object properties.

### Description

CChart class provides access to "Chart" object properties.

### Declaration

```
   class CChart : public CObject

```

### Title

```
   #include <Charts\Chart.mqh>

```

```
Inheritance hierarchy
   CObject
       CChart

```

### Class Methods by Groups

| Access to protected data |  |
| --- | --- |
| ChartID | Gets identifier of the chart |
| General properties |  |
| Mode | Gets/sets the value of "Mode" property (bars, candles, or line) |
| Foreground | Gets/sets the value of "Foreground" property |
| Shift | Gets/sets the value of "Shift" property |
| ShiftSize | Gets/sets the value of "ShiftSize" property (in percents) |
| AutoScroll | Gets/sets the value of "AutoScroll" property |
| Scale | Gets/sets the value of "Scale" property |
| ScaleFix | Gets/sets the value of "ScaleFix" property (fixed chart scale or not) |
| ScaleFix_11 | Gets/sets the value of "ScaleFix_11" property (chart scale is 1:1, or not) |
| FixedMax | Gets/sets the value of "FixedMax" property (fixed maximal price) |
| FixedMin | Gets/sets the value of "FixedMin" property (fixed minimal price) |
| ScalePPB | Gets/sets the value of "ScalePPB" property (scale is "point per bar" or not) |
| PointsPerBar | Gets/sets the value of "PointsPerBar" property (in points per bar) |
| Show properties |  |
| ShowOHLC | Gets/sets the value of "ShowOHLC" property |
| ShowLineBid | Gets/sets the value of "ShowLineBid" property |
| ShowLineAsk | Gets/sets the value of "ShowLineAsk" property |
| ShowLastLine | Gets/sets the value of "ShowLastLine" property |
| ShowPeriodSep | Gets/sets the value of "ShowPeriodSep" property (show period separators) |
| ShowGrid | Gets/sets the value of "ShowGrid" property |
| ShowVolumes | Gets/sets the value of "ShowVolumes" property (color for volumes and levels of opened positions) |
| ShowObjectDescr | Gets/sets the value of "ShowObjectDescr" property (show description for graphic objects) |
| ShowDateScale | Sets the value of "ShowDateScale" property (date scale of the chart) |
| ShowPriceScale | Sets the value of "ShowPriceScale" property (price scale of the chart) |
| Color properties |  |
| ColorBackground | Gets/sets the value of "ColorBackground" property (background color of the chart) |
| ColorForeground | Gets/sets the value of "ColorForeground" property (color of axes, scale and OHLC strings of the chart) |
| ColorGrid | Gets/sets the value of "ColorGrid" property (color of the grid) |
| ColorBarUp | Gets/sets the value of "ColorBarUp" property (color for bull bars, their shadow and candle body outlines) |
| ColorBarDown | Gets/sets the value of "ColorBarDown" property (color for bear bars, their shadow and candle body outlines) |
| ColorCandleBull | Gets/sets the value of "ColorCandleBull" property (body color of the bull candle) |
| ColorCandleBear | Gets/sets the value of "ColorCandleBear" property (body color of the bear candle) |
| ColorChartLine | Gets/sets the value of "ColorChartLine" property (color for line chart and Doji candles) |
| ColorVolumes | Gets/sets the value of "ColorVolumes" property (color for volumes and levels of opened positions) |
| ColorLineBid | Gets/sets the value of "ColorLineBid" property (color of Bid line) |
| ColorLineAsk | Gets/sets the value of "ColorLineAsk" property (color of Ask line) |
| ColorLineLast | Gets/sets the value of "ColorLineLast" property (color of the last deal price line) |
| ColorStopLevels | Gets/sets the value of "ColorStopLevels" property (color of the SL and TP levels) |
| Read only properties |  |
| VisibleBars | Gets total number of visible chart bars |
| WindowsTotal | Gets total number of chart windows, including the chart indicator subwindows |
| WindowIsVisible | Gets visibility flag of the specified chart subwindow |
| WindowHandle | Gets window handle of the chart (HWND) |
| FirstVisibleBar | Gets the number of the first visible bar of the chart |
| WidthInBars | Gets window width in bars. |
| WidthInPixels | Gets subwindow width in pixels. |
| HeightInPixels | Gets subwindow height in pixels. |
| PriceMin | Gets minimal price of the specified subwindow |
| PriceMax | Gets maximal price of the specified subwindow |
| Properties |  |
| Attach | Assigns the current chart to the class instance |
| FirstChart | Assigns the first chart of the client terminal to the class instance |
| NextChart | Assigns the next chart of the client terminal to the class instance |
| Open | Opens chart with specified parameters and assign it to the class instance |
| Detach | Detaches chart from the class instance |
| Close | Closes chart assigned to the class instance |
| BringToTop | Show chart on top of other charts |
| EventObjectCreate | Sets a flag to send notifications of an event of new object creation on a chart |
| EventObjectDelete | Sets a flag to send notifications of an event of object deletion on a chart |
| Indicators |  |
| IndicatorAdd | Adds an indicator with the specified handle into a specified chart subwindow |
| IndicatorDelete | Removes an indicator with a specified name from the specified chart subwindow |
| IndicatorsTotal | Returns the number of all indicators applied to the specified chart subwindow |
| IndicatorName | Returns the short name of the indicator on the specified chart subwindow |
| Navigation |  |
| Navigate | Navigates the chart |
| Access to MQL5 API |  |
| Symbol | Gets symbol of the chart |
| Period | Gets period of the chart |
| Redraw | Redraws chart, assigned to the class instance |
| GetInteger | The function returns the value of the corresponding object property |
| SetInteger | Sets new value for the property of the integer type |
| GetDouble | The function returns the value of the corresponding object property |
| SetDouble | Sets new value for the property of the double type |
| GetString | The function returns the value of the corresponding object property |
| SetString | Sets new value for the property of the string type |
| SetSymbolPeriod | Changes symbol and period of the chart assigned to the class instance |
| ApplyTemplate | Applies specified template to the chart |
| ScreenShot | Creates screenshot of the specified chart and saves it to .gif file |
| WindowOnDropped | Gets chart subwindow number corresponding to the object (expert or script) drop point |
| PriceOnDropped | Gets price coordinate corresponding to the object (expert or script) drop point |
| TimeOnDropped | Gets time coordinate corresponding to the object (expert or script) drop point |
| XOnDropped | Gets X coordinate corresponding to the object (expert or script) drop point |
| YOnDropped | Gets Y coordinate corresponding to the object (expert or script) drop point |
| Input/Output |  |
| virtual  Save | Saves object parameters to file |
| virtual  Load | Loads object parameters from file |
| virtual  Type | Gets graphic object type identifier |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Compare

```
