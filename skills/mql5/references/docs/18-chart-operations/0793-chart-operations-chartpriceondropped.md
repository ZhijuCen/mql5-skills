# ChartPriceOnDropped

Returns the price coordinate corresponding to the chart point the Expert Advisor or script has been dropped to.

```
double  ChartPriceOnDropped();

```

Return Value

Value of [double](/en/docs/basis/types/double) type.

Example:

```
   double p=ChartPriceOnDropped();
   Print("ChartPriceOnDropped() = ",p);

```

See also

[ChartXOnDropped](/en/docs/chart_operations/chartxondropped), [ChartYOnDropped](/en/docs/chart_operations/chartyondropped)
