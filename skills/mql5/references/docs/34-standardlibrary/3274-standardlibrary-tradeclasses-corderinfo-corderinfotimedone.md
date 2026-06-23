# TimeDone

Gets the time of order execution or cancellation.

```
datetime  TimeDone() const

```

Return Value

Time of order execution or cancellation.

Note

The order should be selected using the [Select](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselect) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/corderinfo/corderinfoselectbyindex) (by index) methods.
