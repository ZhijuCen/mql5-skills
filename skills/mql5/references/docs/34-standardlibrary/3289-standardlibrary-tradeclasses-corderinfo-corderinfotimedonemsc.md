# TimeDoneMsc

Receives order execution or cancellation time in milliseconds since 01.01.1970.

```
ulong  TimeDoneMsc() const

```

Return Value

Order execution or cancellation time in milliseconds since 01.01.1970.

Note

Order should be preliminarily selected for access using [Select](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselectbyindex) (by index) method.
