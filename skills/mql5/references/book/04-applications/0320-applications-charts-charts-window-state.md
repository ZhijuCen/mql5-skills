# Checking the status of the main window

The pair of functions ChartSetInteger/ChartGetInteger allows you to find out some of the chart state characteristics, as well as change some of them.

| Identifier | Description | Value type |
| --- | --- | --- |
| CHART_BRING_TO_TOP | Chart activity (input focus) on top of all others | bool |
| CHART_IS_MAXIMIZED | Chart maximized | bool |
| CHART_IS_MINIMIZED | Chart minimized | bool |
| CHART_WINDOW_HANDLE | Windows-handle of the chart  window (r/o) | int |
| CHART_IS_OBJECT | A flag that a chart is a Chart object ( OBJ_CHART );  true  is for a graphic object and  false  is for a normal chart (r/o) | bool |

As expected, the Window handle and the attribute of the chart object are read-only. Other properties are editable: for example, by calling ChartSetInteger(ID, CHART_BRING_TO_TOP, true), you activate the chart with the specified ID.

An example of applying properties is given in the ChartList4.mq5 script in the next section.
