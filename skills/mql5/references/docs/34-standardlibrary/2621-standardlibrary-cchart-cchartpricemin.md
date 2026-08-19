# PriceMin

Gets window minimal price.

```
double  PriceMin(
   int  num      // subwindow
   ) const

```

Parameters

num

[in]  Subwindow number (0 means main window).

Return Value

Window minimal price value of the chart assigned to the class instance. If there is not chart assigned, it returns [EMPTY_VALUE](/en/docs/constants/namedconstants/otherconstants).
