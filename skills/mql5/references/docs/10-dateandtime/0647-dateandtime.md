# Date and Time

This is the group of functions for working with data of [datetime](/en/docs/basis/types/integer/datetime) type (an integer that represents the number of seconds elapsed from 0 hours of January 1, 1970).

To arrange high-resolution counters and timers, use the [GetTickCount()](/en/docs/common/gettickcount) function, which produces values in milliseconds.

| Function | Action |
| --- | --- |
| TimeCurrent | Returns the last known server time (time of the last quote receipt) in the datetime format |
| TimeTradeServer | Returns the current calculation time of the trade server |
| TimeLocal | Returns the local computer time in datetime format |
| TimeGMT | Returns GMT in datetime format with the Daylight Saving Time by local time of the computer, where the client terminal is running |
| TimeDaylightSavings | Returns the sign of Daylight Saving Time switch |
| TimeGMTOffset | Returns the current difference between GMT time and the local computer time in seconds, taking into account DST switch |
| TimeToStruct | Converts a datetime value into a variable of MqlDateTime structure type |
| StructToTime | Converts a variable of MqlDateTime structure type into a datetime value |
