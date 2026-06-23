# Overview of functions managing indicators on the chart

As we have already figured out, indicators are the type of MQL programs that combine the calculation part and visualization. The calculations are performed internally, imperceptibly to the user, but the visualization requires linking to the chart. That is why indicators are closely related to charts, and the MQL5 API even contains a group of functions that manage indicators on charts. We will discuss these functions in more detail in the chapter on [charts](/en/book/applications/charts/charts_indicators), and here we just give a list of them.

| Function | Purpose |
| --- | --- |
| ChartWindowFind | Returns the number of the subwindow containing the current indicator or an indicator with the given name |
| ChartIndicatorAdd | Adds an indicator with the specified handle to the specified chart window |
| ChartIndicatorDelete | Removes an indicator with the specified name from the specified chart window |
| ChartIndicatorGet | Returns the indicator handle with the specified short name on the specified chart window |
| ChartIndicatorName | Returns the short name of the indicator by number in the list of indicators on the specified chart window |
| ChartIndicatorsTotal | Returns the number of all indicators attached to the specified chart window |

In the next section about [Combining information output](/en/book/applications/indicators_use/indicators_chart_plus_subwindow) in the main and auxiliary window, we will see an example UseDemoAll.mq5, which uses some of these functions.
