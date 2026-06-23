# TimeMsc

Receives position opening time in milliseconds since 01.01.1970.

```
ulong  TimeMsc() const

```

Return Value

Position opening time in milliseconds since 01.01.1970.

Note

Position should be preliminarily selected for access using [Select](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselect) (by symbol) or [SelectByIndex](/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfoselectbyindex) (by index) method.
