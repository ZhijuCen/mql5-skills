# Universal Time

In MQL5, you can find out the global GMT (UTC) based on the computer's local time and its time zone.

datetime TimeGMT()

datetime TimeGMT(MqlDateTime &dt)

The function returns GMT in the datetime format, counting it from the local time of the computer, taking into account the transition to winter or summer time.

Generalized calculation formula:

```
TimeGMT() = TimeLocal() + TimeGMTOffset()

```

Thus, the accuracy of the representation of universal time depends on the correct setting of the clock on the local computer. Ideally, the value retrieved should match the value known to the server.

For trading strategies based on external economic news, it is easiest to use calendars in the GMT time zone: then upcoming events can be tracked by TimeGMT. To bind an event to the server time on the chart, you should correct the event for the difference between the server time zone and GMT (TimeTradeServer() - TimeGMT()). But remember that MQL5 has its own built-in [calendar](/en/book/advanced/calendar).

int TimeGMTOffset()

The function returns the current difference between GMT and the computer's local time in seconds, based on the time zone setting in Windows, taking into account the current daylight savings time. In most cases, the time zone is given as an integer number of hours relative to GMT, so TimeGMTOffset is equal to the time zone multiplied by -3600 (converted to seconds). For example, in winter the time zone can be equal to UTC + 2, which gives an offset of -7200, and in summer it can be UTC + 3, which gives -10800. The minus is needed, because positive time zones when converting their time to GMT require subtraction of the above number of seconds, and negative ones require additions.

A script using TimeGMT and TimeGMTOffset was shown in the [previous section](/en/book/common/timing/timing_daylight_saving).
