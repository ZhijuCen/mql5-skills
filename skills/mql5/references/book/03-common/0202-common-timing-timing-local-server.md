# Local and server time

There are always two types of time on the MetaTrader 5 platform: local (client) and server (broker).

Local time corresponds to the time of the computer on which the terminal is running, and increases continuously, at the same rate as in the real world.

Server time flows differently. The basis for it is set by the time on the brokers computer, however, the client receives information about it only together with the next price changes, which are packed into special structures called ticks (see the section about [MqlTick](/en/book/applications/timeseries/timeseries_ticks_mqltick)) and are passed to MQL programs using [events](/en/book/applications/events).

Thus, the updated server time becomes known in the terminal only as a result of a change in the price of at least one financial instrument on the market, that is, from among those selected in the Market Watch window. The last known time of the server is displayed in the title bar of this window. If there are no ticks, the server time in the terminal stands still. This is especially noticeable on weekends and holidays when all exchanges and Forex platforms are closed.

In particular, on a Sunday, the server time will most likely be displayed as Friday evening. The only exceptions are those instances of MetaTrader 5 that offer continuously traded instruments such as cryptocurrencies. However, even in this case, during periods of low volatility, server time can noticeably lag behind local time.

All functions in this section operate on time with an accuracy of up to a second (the accuracy of time representation in the [datetime](/en/book/basis/builtin_types/datetime) type).

To get local and server time, the MQL5 API provides three functions: TimeLocal, TimeCurrent, and TimeTradeServer. All three functions have two versions of the prototype: the first one returns the time as a value of the datetime type, and the second one additionally accepts by reference and fills the MqlDateTime structure with time components.

datetime TimeLocal()

datetime TimeLocal(MqlDateTime &dt)

The function returns the local computer time in the datetime format.

It is important to note that time includes Daylight Savings Time if enabled. I.e., TimeLocal equals the standard time of the computer's time zone, minus the correction [TimeDaylightSavings](/en/book/common/timing/timing_daylight_saving). Conditionally, the formula can be represented as follows:

```
TimeLocal summer() = TimeLocal winter() - TimeDaylightSavings()

```

Here TimeDaylightSavings usually equals -3600, that is, moving the clock forward 1 hour (1 hour is lost). So the summer value of TimeLocal is greater than the winter value (with equal astronomical time of day) relative to UTC. For example, if in winter TimeLocal equals UTC+2, then in summer it is UTC+3. UTC can be obtained using the [TimeGMT](/en/book/common/timing/timing_gmt) function.

datetime TimeCurrent()

datetime TimeCurrent(MqlDateTime &dt)

The function returns the last known server time in the datetime format. This is the time of arrival of the last quote from the list of all financial instruments in the Market Watch. The only exception is the [OnTick](/en/book/automation/experts/experts_ontick) event handler in Expert Advisors, where this function will return the time of the processed tick (even if ticks with a more recent time have already appeared in the Market Watch).

Also, note that the time on the horizontal axis of all charts in MetaTrader 5 corresponds to the server time (in history). The last (current, rightmost) bar contains TimeCurrent. See details in the [Charts](/en/book/applications/charts) section.

datetime TimeTradeServer()

datetime TimeTradeServer(MqlDateTime &dt)

The function returns the estimated current time of the trade server. Unlike TimeCurrent, the results of which may not change if there are no new quotes, TimeTradeServer allows you to get an estimate of continuously increasing server time. The calculation is based on the last known difference between the time zones of the client and the server, which is added to the current local time.

In the tester, the TimeTradeServer value is always equal to TimeCurrent.

An example of how the functions work is given in the script TimeCheck.mq5.

The main function has an infinite loop that logs all types of time every second until the user stops the script.

```
void OnStart()
{
   while(!IsStopped())
   {
      PRTF(TimeLocal());
      PRTF(TimeCurrent());
      PRTF(TimeTradeServer());
      PRTF(TimeTradeServerExact());
      Sleep(1000);
   }
}

```

In addition to the standard functions, a custom function TimeTradeServerExact is applied here.

```
datetime TimeTradeServerExact()
{
   enum LOCATION
   {
      LOCAL, 
      SERVER, 
   };
   static datetime now[2] = {}, then[2] = {};
   static int shiftInHours = 0;
   static long shiftInSeconds = 0;
   
   // constantly detect the last 2 timestamps here and there
   then[LOCAL] = now[LOCAL];
   then[SERVER] = now[SERVER];
   now[LOCAL] = TimeLocal();
   now[SERVER] = TimeCurrent();
   
   // at the first call we don't have 2 labels yet,
   // needed to calculate the stable difference
   if(then[LOCAL] == 0 && then[SERVER] == 0) return 0;
 
   // when the time course is the same on the client and on the server,
   // and the server is not "frozen" due to weekends/holidays,
   // updating difference
   if(now[LOCAL] - now[SERVER] == then[LOCAL] - then[SERVER]
   && now[SERVER] != then[SERVER])
   {
      shiftInSeconds = now[LOCAL] - now[SERVER];
      shiftInHours = (int)MathRound(shiftInSeconds / 3600.0);
      // debug print
      PrintFormat("Shift update: hours: %d; seconds: %lld", shiftInHours, shiftInSeconds);
   }
   
   // NB: The built-in function TimeTradeServer calculates like this:
   //                TimeLocal() - shiftInHours * 3600
   return (datetime)(TimeLocal() - shiftInSeconds);
}

```

It was required because the algorithm of the built-in TimeTradeServer function may not suit everyone. The built-in function finds the difference between local and server time in hours (that is, the time zone difference), and then gets the server time as a local time correction for this difference. As a result, if the minutes and seconds go on the client and server not synchronously (which is very likely), the standard approximation of server time will show the minutes and seconds of the client, not the server.

Ideally, the local clocks of all computers should be synchronized with global time, but in practice, deviations occur. So, if there is even a small shift on one of the sides, TimeTradeServer can no longer repeat the time on the server with the highest precision.

In our implementation of the same function in MQL5, we do not round the difference between the client and server time to hourly timezones. Instead, the exact difference in seconds is used in the calculation. That's why TimeTradeServerExact returns the time at which minutes and seconds go just like on the server.

Here is an example of a log generated by the script.

```
TimeLocal()=2021.09.02 16:03:34 / ok
TimeCurrent()=2021.09.02 15:59:39 / ok
TimeTradeServer()=2021.09.02 16:03:34 / ok
TimeTradeServerExact()=1970.01.01 00:00:00 / ok

```

It can be seen that the time zones of the client and server are the same, but there is a desynchronization of several minutes (for clarity). On the first call, TimeTradeServerExact returned 0. Further, the data for calculating the difference will already arrive, and we will see all four time types, uniformly "walking" with an interval of a few seconds.

```
TimeLocal()=2021.09.02 16:03:35 / ok
TimeCurrent()=2021.09.02 15:59:40 / ok
TimeTradeServer()=2021.09.02 16:03:35 / ok
Shift update: hours: 0; seconds: 235
TimeTradeServerExact()=2021.09.02 15:59:40 / ok
TimeLocal()=2021.09.02 16:03:36 / ok
TimeCurrent()=2021.09.02 15:59:41 / ok
TimeTradeServer()=2021.09.02 16:03:36 / ok
Shift update: hours: 0; seconds: 235
TimeTradeServerExact()=2021.09.02 15:59:41 / ok
TimeLocal()=2021.09.02 16:03:37 / ok
TimeCurrent()=2021.09.02 15:59:41 / ok
TimeTradeServer()=2021.09.02 16:03:37 / ok
TimeTradeServerExact()=2021.09.02 15:59:42 / ok
TimeLocal()=2021.09.02 16:03:38 / ok
TimeCurrent()=2021.09.02 15:59:43 / ok
TimeTradeServer()=2021.09.02 16:03:38 / ok
TimeTradeServerExact()=2021.09.02 15:59:43 / ok

```
