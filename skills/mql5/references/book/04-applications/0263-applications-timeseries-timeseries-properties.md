# Getting characteristics of price arrays

Before reading arrays of timeseries, we should make sure that they are available and that they possess the required characteristics. The SeriesInfoInteger function retrieves the basic properties, such as the depth of available history in the terminal and on the server, the number of constructed bars for a specific symbol/period combination, and the absence of discrepancies in quotes between the terminal and the server.

The function has two forms: the first directly returns the requested value (of type long) and the second uses the fourth parameter result passed by reference. In this case, the second form returns a sign of success (true) or errors (false). In any case, the error code can be found using the [GetLastError](/en/book/common/environment/env_last_error) function.

long SeriesInfoInteger(const string symbol, ENUM_TIMEFRAMES timeframe, ENUM_SERIES_INFO_INTEGER property)

bool SeriesInfoInteger(const string symbol, ENUM_TIMEFRAMES timeframe, ENUM_SERIES_INFO_INTEGER property, long &result)

The function allows you to find out one of the timeseries properties for the specified symbol and timeframe or for the entire symbol history. The requested property is identified by the third argument of type ENUM_SERIES_INFO_INTEGER. This enumeration includes all available properties:

| Identifier | Description | Property type |
| --- | --- | --- |
| SERIES_BARS_COUNT | Number of bars by symbol/period, see  Bars | long |
| SERIES_FIRSTDATE | Very first date by symbol/period | datetime |
| SERIES_LASTBAR_DATE | Opening time of the last bar by symbol/period | datetime |
| SERIES_SYNCHRONIZED | Sign of data synchronization by symbol/period on the terminal and on the server | bool |
| SERIES_SERVER_FIRSTDATE | Very first date in history by symbol on the server regardless of the period | datetime |
| SERIES_TERMINAL_FIRSTDATE | Very first date in the history by symbol in the client terminal regardless of the period | datetime |

Depending on the essence of the property, the resulting value should be converted to a value of a specific type (see column Property type).

All properties are returned as of the current moment.

The script SeriesInfo.mq5 provides an example of querying all properties.

```
void OnStart()
{
   PRTF(SeriesInfoInteger(NULL, 0, SERIES_BARS_COUNT));
   PRTF((datetime)SeriesInfoInteger(NULL, 0, SERIES_FIRSTDATE));
   PRTF((datetime)SeriesInfoInteger(NULL, 0, SERIES_LASTBAR_DATE));
   PRTF((bool)SeriesInfoInteger(NULL, 0, SERIES_SYNCHRONIZED));
   PRTF((datetime)SeriesInfoInteger(NULL, 0, SERIES_SERVER_FIRSTDATE));
   PRTF((datetime)SeriesInfoInteger(NULL, 0, SERIES_TERMINAL_FIRSTDATE));
   PRTF(SeriesInfoInteger("ABRACADABRA", 0, SERIES_BARS_COUNT));
}

```

Here is an example of the result obtained on EURUSD, H1, on the MQ Demo server:

```
SeriesInfoInteger(NULL,0,SERIES_BARS_COUNT)=10001 / ok
(datetime)SeriesInfoInteger(NULL,0,SERIES_FIRSTDATE)=2020.03.02 10:00:00 / ok
(datetime)SeriesInfoInteger(NULL,0,SERIES_LASTBAR_DATE)=2021.10.08 14:00:00 / ok
(bool)SeriesInfoInteger(NULL,0,SERIES_SYNCHRONIZED)=false / ok
(datetime)SeriesInfoInteger(NULL,0,SERIES_SERVER_FIRSTDATE)=1971.01.04 00:00:00 / ok
(datetime)SeriesInfoInteger(NULL,0,SERIES_TERMINAL_FIRSTDATE)=2016.06.01 00:00:00 / ok
SeriesInfoInteger(ABRACADABRA,0,SERIES_BARS_COUNT)=0 / MARKET_UNKNOWN_SYMBOL(4301)

```
