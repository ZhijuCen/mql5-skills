# TimeDoneMsc

Receives order execution or cancellation time in milliseconds since 01.01.1970.

```
ulong  TimeDoneMsc() const

```

Return Value

Order execution or cancellation time in milliseconds since 01.01.1970.

Note

Historical order should be preliminarily selected for access using [Ticket](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoselectbyindex) (by index) method.
