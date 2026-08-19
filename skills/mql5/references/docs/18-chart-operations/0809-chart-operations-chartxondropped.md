# ChartXOnDropped

Returns the X coordinate of the chart point the Expert Advisor or script has been dropped to.

```
int  ChartXOnDropped();

```

Return Value

The X coordinate value.

Note

X axis direction from left to right.

Example:

```
   int X=ChartXOnDropped();
   int Y=ChartYOnDropped();
   Print("(X,Y) = ("+X+","+Y+")");

```

See also

[ChartWindowOnDropped](/en/docs/chart_operations/chartwindowondropped), [ChartPriceOnDropped](/en/docs/chart_operations/chartpriceondropped), [ChartTimeOnDropped](/en/docs/chart_operations/charttimeondropped)
