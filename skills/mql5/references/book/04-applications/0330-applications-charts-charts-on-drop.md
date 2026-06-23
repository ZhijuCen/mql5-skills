# Getting MQL program drop coordinates on a chart

Users often drag MQL programs onto a chart using a mouse. In addition to being convenient, this allows you to set some context for the algorithm. For example, an indicator can be applied in different subwindows, or a script can place a pending order at the price where the user placed it on the chart. The next group of functions is designed to get the coordinates of the point to which the program was dragged and dropped.

int ChartWindowOnDropped()

This function returns the number of the chart subwindow on which the current Expert Advisor, script, or indicator is dropped by the mouse. The main window, as we know, is numbered 0, and the subwindows are numbered starting from 1. The number of a subwindow does not depend on whether there are hidden subwindows above it, as their indices remain assigned to them. In other words, the visible subwindow number may differ from its real index if there are [hidden subwindows](/en/book/applications/charts/charts_count_visibility).

double ChartPriceOnDropped()

datetime ChartTimeOnDropped()

This pair of functions returns the program drop point coordinates in units of price and time. Please note that arbitrary data can be displayed in subwindows, and not just prices, although the function name ChartPriceOnDropped includes 'Price'.

Attention! The target point time is not rounded by the size of the chart timeframe, so even on the H1 and D1 charts, you can get a value with minutes and even seconds.

int ChartXOnDropped()

int ChartYOnDropped()

These two functions return the X and Y screen coordinates of a point in pixels. The origin of the coordinates is located in the upper left corner of the main chart window. We talked about the direction of the axes in the [Screen specifications](/en/book/common/environment/env_screen) section.

The Y coordinate is always counted from the upper left corner of the main chart, even if the drop point belongs to a subwindow. To translate this value into a coordinate y relative to a subwindow, use the property [CHART_WINDOW_YDISTANCE](/en/book/applications/charts/charts_scale_price) (see example).

Let's output the values of all mentioned functions to the log in the script ChartDrop.mq5.

```
void OnStart()
{
   const int w = PRTF(ChartWindowOnDropped());
   PRTF(ChartTimeOnDropped());
   PRTF(ChartPriceOnDropped());
   PRTF(ChartXOnDropped());
   PRTF(ChartYOnDropped());
   
   // for the subwindow, recalculate the y coordinate to the local one
   if(w > 0)
   {
      const int y = (int)PRTF(ChartGetInteger(0, CHART_WINDOW_YDISTANCE, w));
      PRTF(ChartYOnDropped() - y);
   }
}

```

For example, if we drop this script into the first subwindow where the WPR indicator is running, we can get the following results.

```
ChartWindowOnDropped()=1 / ok
ChartTimeOnDropped()=2021.11.30 03:52:30 / ok
ChartPriceOnDropped()=-50.0 / ok
ChartXOnDropped()=217 / ok
ChartYOnDropped()=312 / ok
ChartGetInteger(0,CHART_WINDOW_YDISTANCE,w)=282 / ok
ChartYOnDropped()-y=30 / ok

```

Despite the fact that the script is dropped on the EURUSD, H1 chart, we got a timestamp with minutes and seconds.

Note that the "price" value is -50 because the range of WPR values is [0,-100].

In addition, the vertical coordinate of point 312 (relative to the entire chart window) was converted to the local coordinate of the subwindow: since the vertical distance from the beginning of the main chart to the subwindow was 282, the value y inside the subwindow turned out to be 30.
