# TimeUpdate

Receives the time of position changing in seconds since 01.01.1970.

```
datetime  TimeUpdate() const

```

Return Value

Time of position changing in seconds since 01.01.1970.

Note

Position should be preliminarily selected for access using [Select](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselect) (by symbol) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselectbyindex) (by index) method.
