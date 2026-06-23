# Chart redraw request

In most cases, charts automatically respond to changes in data and terminal settings, refreshing the window image accordingly (price charts, indicator charts, etc.). However, MQL programs are too versatile and can perform arbitrary actions, for which it is not so easy to determine whether redrawing is required or not. In addition, analyzing any action of each MQL program on this account can be resource-intensive and cause a drop in the overall performance of the terminal. Therefore, the MQL5 API provides the ChartRedraw function, with the help of which the MQL program itself can, if necessary, request a redrawing of the chart.

void ChartRedraw(long chartId = 0)

The function causes a forced redrawing of the chart with the specified identifier (default value 0 means the current chart). Usually, it is applied after the program changes the properties of the chart or [objects](/en/book/applications/objects) placed on it.

We have seen an example of using ChartRedraw in the indicator IndSubChart.mq5 in the section [Chart display modes](/en/book/applications/charts/charts_mode). Another example will be given in the section [Opening and closing charts](/en/book/applications/charts/charts_open_close).

This function affects exactly the redrawing of the chart, without causing the recalculation of timeseries with quotes and indicators. The last option for updating (in fact, rebuilding) the chart is more "hard" and is performed by the ChartSetSymbolPeriod function (see the next section).
