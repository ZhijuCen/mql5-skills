# ChartWindowOnDropped

Returns the number (index) of the chart subwindow the Expert Advisor or script has been dropped to. 0 means the main chart window.

```
int  ChartWindowOnDropped();

```

Return Value

Value of [int](/en/docs/basis/types/integer/integertypes) type.

Example:

```
   int myWindow=ChartWindowOnDropped();
   int windowsTotal=ChartGetInteger(0,CHART_WINDOWS_TOTAL);
   Print("Script is running on the window #"+myWindow+
         ". Total windows on the chart "+ChartSymbol()+":",windowsTotal);

```

See also

[ChartPriceOnDropped](/en/docs/chart_operations/chartpriceondropped), [ChartTimeOnDropped](/en/docs/chart_operations/charttimeondropped), [ChartXOnDropped](/en/docs/chart_operations/chartxondropped), [ChartYOnDropped](/en/docs/chart_operations/chartyondropped)
