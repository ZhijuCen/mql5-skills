# TimeTradeServer

Returns the calculated current time of the trade server. Unlike [TimeCurrent()](/en/docs/dateandtime/timecurrent), the calculation of the time value is performed in the client terminal and depends on the time settings on your computer. There are 2 variants of the function.

Call without parameters

```
datetime  TimeTradeServer();

```

Call with MqlDateTime type parameter

```
datetime  TimeTradeServer(
   MqlDateTime&  dt_struct      // Variable of structure type
   );

```

Parameters

dt_struct

[out]  Variable of structure type [MqlDateTime](/en/docs/constants/structures/mqldatetime).

Return Value

Value of [datetime](/en/docs/basis/types/integer/datetime) type

Note

If the MqlDateTime structure type variable has been passed as a parameter, it is filled accordingly.

To arrange high-resolution counters and timers, use the [GetTickCount()](/en/docs/common/gettickcount) function, which produces values in milliseconds.

During testing in the strategy tester, TimeTradeServer() is simulated according to historical data and always equal to [TimeCurrent()](/en/docs/dateandtime/timecurrent).

Example:

```
void OnStart()
  {
//--- declare the MqlDateTime variable to be filled with date/time data and get the time of the last quote and the estimated current time of the trade server
   MqlDateTime tm={};
   datetime    time_current=TimeCurrent();                  // first form of call: time of the last quote for one of the symbols in the Market Watch window
   datetime    time_server =TimeTradeServer(tm);            // second form of call: estimated current time of the trade server with filling in the MqlDateTime structure
   int         difference  =int(time_current-time_server);  // difference between Time Current and Time Trade Server
   
//--- display the time of the last quote and the estimated current time of the trade server with the data of the filled MqlDateTime structure in the log
   PrintFormat("Time Current: %s\nTime Trade Server: %s\n- Year: %u\n- Month: %02u\n- Day: %02u\n"+
               "- Hour: %02u\n- Min: %02u\n- Sec: %02u\n- Day of Year: %03u\n- Day of Week: %u (%s)\nDifference between Time Current and Time Trade Server: %+d",
               (string)time_current, (string)time_server, tm.year, tm.mon, tm.day, tm.hour, tm.min, tm.sec, tm.day_of_year, tm.day_of_week,
               EnumToString((ENUM_DAY_OF_WEEK)tm.day_of_week), difference);
   /*
   result:
   Time Current: 2024.04.18 16:10:14
   Time Trade Server: 2024.04.18 16:10:15
   - Year: 2024
   - Month: 04
   - Day: 18
   - Hour: 16
   - Min: 10
   - Sec: 15
   - Day of Year: 108
   - Day of Week: 4 (THURSDAY)
   Difference between Time Current and Time Trade Server: -1
   */
  }

```
