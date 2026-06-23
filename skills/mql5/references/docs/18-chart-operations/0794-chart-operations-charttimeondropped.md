# ChartTimeOnDropped

Returns the time coordinate corresponding to the chart point the Expert Advisor or script has been dropped to.

```
datetime  ChartTimeOnDropped();

```

Return Value

Value of [datetime](/en/docs/basis/types/integer/datetime) type.

Example:

```
   datetime t=ChartTimeOnDropped();
   Print("Script was dropped on the "+t);

```

See also

[ChartXOnDropped](/en/docs/chart_operations/chartxondropped), [ChartYOnDropped](/en/docs/chart_operations/chartyondropped)
