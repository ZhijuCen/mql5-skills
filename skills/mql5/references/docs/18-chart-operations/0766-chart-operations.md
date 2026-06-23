# Chart Operations

Functions for setting chart properties ([ChartSetInteger](/en/docs/chart_operations/chartsetinteger), [ChartSetDouble](/en/docs/chart_operations/chartsetdouble), [ChartSetString](/en/docs/chart_operations/chartsetstring)) are asynchronous and are used for sending update commands to a chart. If these functions are executed successfully, the command is included in the common queue of the chart events. Chart property changes are implemented along with handling of the events queue of this chart.

Thus, do not expect an immediate update of the chart after calling asynchronous functions. Use the [ChartRedraw()](/en/docs/chart_operations/chartredraw) function to forcedly update the chart appearance and properties.

| Function | Action |
| --- | --- |
| ChartApplyTemplate | Applies a specific template from a specified file to the chart |
| ChartSaveTemplate | Saves current chart settings in a template with a specified name |
| ChartWindowFind | Returns the number of a subwindow where an indicator is drawn |
| ChartTimePriceToXY | Converts the coordinates of a chart from the time/price representation to the X and Y coordinates |
| ChartXYToTimePrice | Converts the X and Y coordinates on a chart to the time and price values |
| ChartOpen | Opens a new chart with the specified symbol and period |
| ChartClose | Closes the specified chart |
| ChartFirst | Returns the ID of the first chart of the client terminal |
| ChartNext | Returns the chart ID of the chart next to the specified one |
| ChartSymbol | Returns the symbol name of the specified chart |
| ChartPeriod | Returns the period value of the specified chart |
| ChartRedraw | Calls a forced redrawing of a specified chart |
| ChartSetDouble | Sets the double value for a corresponding property of the specified chart |
| ChartSetInteger | Sets the integer value ( datetime, int, color, bool or char ) for a corresponding property of the specified chart |
| ChartSetString | Sets the string value for a corresponding property of the specified chart |
| ChartGetDouble | Returns the double value property of the specified chart |
| ChartGetInteger | Returns the integer value property of the specified chart |
| ChartGetString | Returns the string value property of the specified chart |
| ChartNavigate | Performs shift of the specified chart by the specified number of bars relative to the specified position in the chart |
| ChartID | Returns the ID of the current chart |
| ChartIndicatorAdd | Adds an indicator with the specified handle into a specified chart window |
| ChartIndicatorDelete | Removes an indicator with a specified name from the specified chart window |
| ChartIndicatorGet | Returns the handle of the indicator with the specified short name in the specified chart window |
| ChartIndicatorName | Returns the short name of the indicator by the number in the indicators list on the specified chart window |
| ChartIndicatorsTotal | Returns the number of all indicators applied to the specified chart window. |
| ChartWindowOnDropped | Returns the number (index) of the chart subwindow the Expert Advisor or script has been dropped to |
| ChartPriceOnDropped | Returns the price coordinate of the chart point the Expert Advisor or script has been dropped to |
| ChartTimeOnDropped | Returns the time coordinate of the chart point the Expert Advisor or script has been dropped to |
| ChartXOnDropped | Returns the X coordinate of the chart point the Expert Advisor or script has been dropped to |
| ChartYOnDropped | Returns the Y coordinate of the chart point the Expert Advisor or script has been dropped to |
| ChartSetSymbolPeriod | Changes the symbol value and a period of the specified chart |
| ChartScreenShot | Provides a screenshot of the chart of its current state in a GIF, PNG or BMP format depending on specified extension |
