# TimeDone

Gets the time of order execution or cancellation.

```
datetime  TimeDone() const

```

Return Value

Time of order execution or cancellation.

Note

The historical order should be selected using the [Ticket](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoticket) (by ticket) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoselectbyindex) (by index) methods.
