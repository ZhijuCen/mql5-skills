# TimeSetupMsc

Receives the time of placing an order for execution in milliseconds since 01.01.1970.

```
ulong  TimeSetupMsc() const

```

Return Value

The time of placing an order for execution in milliseconds since 01.01.1970.

Note

Order should be preliminarily selected for access using [Select](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselectbyindex) (by index) method.
