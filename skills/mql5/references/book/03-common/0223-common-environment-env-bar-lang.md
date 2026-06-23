# Custom properties: Bar limit and interface language

Among the properties of the terminal, there are two special properties which the user can change interactively. These include the default maximum number of bars displayed on each chart (it corresponds to the value of the Max. bars in the window field in the Options dialog, as well as the interface language (selected using the View -> Languages command).

| Identifier | Description |
| --- | --- |
| TERMINAL_MAXBARS | Maximum number of bars on the chart |
| TERMINAL_CODEPAGE | Code page number of the language selected in the client terminal |

Please note that the TERMINAL_MAXBARS value sets the upper limit for displaying bars, but in fact, their number may be less if the depth of the available quotes history is not sufficient on any timeframe. On the other hand, the length of the history may also exceed the specified limit TERMINAL_MAXBARS. Then you can find the number of potentially available bars using the function from the [timeseries](/en/book/applications/timeseries) property group: SeriesInfoInteger with the SERIES_BARS_COUNT property. Please note that the TERMINAL_MAXBARS value directly affects the consumption of RAM.
