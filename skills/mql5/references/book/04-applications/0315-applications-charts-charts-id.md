# Chart identification

Each chart in MetaTrader 5 operates in a separate window and has a unique identifier. For programmers familiar with the principles of Windows operation, we would like to clarify that this identifier is not a system window handle (although the MQL5 API allows you to get the latter through the property [CHART_WINDOW_HANDLE](/en/book/applications/charts/charts_window_state)). As we know, in addition to the main working area of the chart with quotes, additional areas (subwindows) with indicators that have the property indicator_separate_window. All subwindows are part of the chart and belong to the same Windows window.

long ChartID()

The function returns a unique identifier for the current chart.

Many of the functions that we'll look at require a chart ID as a parameter, but you can specify 0 for the current chart instead of calling ChartID. It makes sense to use ChartID in cases where the identifier is sent between MQL programs, for example, when exchanging messages ([custom events](/en/book/applications/events/events_custom)) on the same chart, or on different ones. Specifying an invalid ID will result in the ERR_CHART_WRONG_ID (4101) error.

The chart ID generally stays the same from session to session.

We will demonstrate the function ChartID and what the identifiers look like in the example script ChartList1.mq5 after studying the method for obtaining a [chart list](/en/book/applications/charts/charts_list).
