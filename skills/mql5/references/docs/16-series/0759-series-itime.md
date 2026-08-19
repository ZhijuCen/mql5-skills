# iTime

Returns the opening time of the bar (indicated by the 'shift' parameter) on the corresponding chart.

```
datetime  iTime(
   const string        symbol,          // Symbol
   ENUM_TIMEFRAMES     timeframe,       // Period
   int                 shift            // Shift
   );

```

Parameters

symbol

[in]  The symbol name of the financial instrument. [NULL](/en/docs/constants/namedconstants/otherconstants) means the current symbol.

timeframe

[in]  Period. It can be one of the values of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) enumeration. 0 means the current chart period.

shift

[in]  The index of the received value from the timeseries (backward shift by specified number of bars relative to the current bar).

Return Value

The opening time of the bar (indicated by the 'shift' parameter) on the corresponding chart or 0 in case of an error. For [error](/en/docs/constants/errorswarnings/errorcodes) details, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

The function always returns actual data. For this purpose it performs a request to the timeseries for the specified symbol/period during each call. This means that if there is no ready data during the first function call, some time may be taken to prepare the result.

The function does not store previous calls results, and there is no local cache for quick value return.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- The date is on Sunday
   datetime time=D'2018.06.10 12:00';
   string symbol="GBPUSD";
   ENUM_TIMEFRAMES tf=PERIOD_H1;
   bool exact=false;
//--- there is no bar at the specified time, iBarShift will return the index of the nearest bar
   int bar_index=iBarShift(symbol,tf,time,exact);
   PrintFormat("1. %s %s %s(%s): bar index is %d (exact=%s)",
               symbol,EnumToString(tf),TimeToString(time),DayOfWeek(time),bar_index,string(exact));
   datetime bar_time=iTime(symbol,tf,bar_index);
   PrintFormat("Time of bar #%d is %s (%s)",
               bar_index,TimeToString(bar_time),DayOfWeek(bar_time));
//PrintFormat(iTime(symbol,tf,bar_index));
//--- Request the index of the bar with the specified time; but there is no bar, return -1
   exact=true;
   bar_index=iBarShift(symbol,tf,time,exact);
   PrintFormat("2. %s %s %s (%s):bar index is %d (exact=%s)",
               symbol,EnumToString(tf),TimeToString(time),DayOfWeek(time),bar_index,string(exact));
  }
//+------------------------------------------------------------------+
//| Returns the name of the day of the week                          |
//+------------------------------------------------------------------+
string DayOfWeek(const datetime time)
  {
   MqlDateTime dt;
   string day="";
   TimeToStruct(time,dt);
   switch(dt.day_of_week)
     {
      case 0: day=EnumToString(SUNDAY);
      break;
      case 1: day=EnumToString(MONDAY);
      break;
      case 2: day=EnumToString(TUESDAY);
      break;
      case 3: day=EnumToString(WEDNESDAY);
      break;
      case 4: day=EnumToString(THURSDAY);
      break;
      case 5: day=EnumToString(FRIDAY);
      break;   
      default:day=EnumToString(SATURDAY);
      break;
     }
//---
   return day;
  }
/* The result:
   1. GBPUSD PERIOD_H1 2018.06.10 12:00(SUNDAY): bar index is 64 (exact=false)
   Time of bar #64 is 2018.06.08 23:00 (FRIDAY)
   2. GBPUSD PERIOD_H1 2018.06.10 12:00 (SUNDAY):bar index is -1 (exact=true)
*/  

```

See also

[CopyTime](/en/docs/series/copytime), [CopyRates](/en/docs/series/copyrates)
