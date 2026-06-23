# TimeMsc

Receives the time of a deal execution in milliseconds since 01.01.1970.

```
ulong  TimeMsc() const

```

Return Value

The time of a deal execution in milliseconds since 01.01.1970.

Note

Deal should be preliminarily selected for access using [Ticket](/en/docs/standardlibrary/tradeclasses/cdealinfo/cdealinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/cdealinfo/cdealinfoselectbyindex) (by index) method.
