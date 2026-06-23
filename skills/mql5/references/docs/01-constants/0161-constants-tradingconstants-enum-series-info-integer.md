# History Database Properties

When accessing [timeseries](/en/docs/series) the [SeriesInfoInteger()](/en/docs/series/seriesinfointeger) function is used for obtaining additional [symbol information](/en/docs/constants/environment_state/marketinfoconstants). Identifier of a required property is passed as the function parameter. The identifier can be one of values of ENUM_SERIES_INFO_INTEGER.

ENUM_SERIES_INFO_INTEGER

| Identifier | Description | Type |
| --- | --- | --- |
| SERIES_BARS_COUNT | Bars count for the symbol-period for the current moment | long |
| SERIES_FIRSTDATE | The very first date for the symbol-period for the current moment | datetime |
| SERIES_LASTBAR_DATE | Open time of the last bar of the symbol-period | datetime |
| SERIES_SERVER_FIRSTDATE | The very first date in the history of the symbol on the server regardless of the timeframe | datetime |
| SERIES_TERMINAL_FIRSTDATE | The very first date in the history of the symbol in the client terminal, regardless of the timeframe | datetime |
| SERIES_SYNCHRONIZED | Symbol/period data synchronization flag  for the current moment | bool |
