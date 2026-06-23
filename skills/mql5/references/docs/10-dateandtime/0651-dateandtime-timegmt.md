# TimeGMT

Returns the GMT, which is calculated taking into account the DST switch by the local time on the computer where the client terminal is running. There are 2 variants of the function.

Call without parameters

```
datetime  TimeGMT();

```

Call with MqlDateTime type parameter

```
datetime  TimeGMT(
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

During testing in the strategy tester, TimeGMT() is always equal to [TimeTradeServer()](/en/docs/dateandtime/timetradeserver) simulated server time.

Example:

```
void OnStart()
  {
//--- declare the MqlDateTime variable to be filled with date/time data and get the PC local time and GMT
   MqlDateTime tm={};
   datetime    time1=TimeLocal();            // first form of call: PC local time
   datetime    time2=TimeGMT(tm);            // second form of call: GMT calculated from the PC local time with filling the MqlDateTime structure
   int         shift=int(time1-time2)/3600;  // local time offset relative to GMT
   
//--- display local time and GMT with the data of the filled MqlDateTime structure in the log
   PrintFormat("Time Local: %s\nTime GMT: %s\n- Year: %u\n- Month: %02u\n- Day: %02u\n"+
               "- Hour: %02u\n- Min: %02u\n- Sec: %02u\n- Day of Year: %03u\n- Day of Week: %u (%s)\nLocal time offset relative to GMT: %+d",
               (string)time1, (string)time2, tm.year, tm.mon, tm.day, tm.hour, tm.min, tm.sec, tm.day_of_year, tm.day_of_week,
               EnumToString((ENUM_DAY_OF_WEEK)tm.day_of_week), shift);
   /*
   result:
   Time Local: 2024.04.18 19:37:23
   Time GMT: 2024.04.18 12:37:23
   - Year: 2024
   - Month: 04
   - Day: 18
   - Hour: 12
   - Min: 37
   - Sec: 23
   - Day of Year: 108
   - Day of Week: 4 (THURSDAY)
   Local time offset relative to GMT: +7
   */
  }

```
